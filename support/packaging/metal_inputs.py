"""Stage the signed UniXNU addon beside the existing IN2020 wallpaper files."""
import hashlib
import json
import plistlib
import struct
import uuid
import zipfile
import zlib
from pathlib import Path

WORK = Path(__file__).resolve().parent
ARCHIVE = WORK / 'native-adreno-metal-ios17-r59.zip'
BUNDLE = 'addons/NativeAdrenoMetal.bundle/'
PUBLISH = 'addons/NativeAdrenoMetal.publish'
CLIENTS = 'addons/NativeAdrenoMetal.clients'
SETTINGS_CLIENTS = ('CollectionsPoster', 'Preferences', 'iconservicesagent')
WALLPAPER_SHA = 'a5cecfc733dfcc0ac1ca73877a4a61f074e7f366de31bf0552a14c3ab9259a81'
APPLE_TRUST_SHA = '7416ca4f8377146626bb284e2133c76bee6cb4e3ee0af5d648b186235a7323a7'


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def addon_records(blob):
    magic, count, reserved, total = struct.unpack_from('<8sIIQ', blob)
    assert magic == b'NGPUADD2' and not reserved and total == len(blob) and 0 < count <= 4096
    records, cursor = {}, 24
    for _ in range(count):
        start = cursor
        path_bytes, mode, size, packed = struct.unpack_from('<IIQQ', blob, cursor)
        cursor += 24
        name = blob[cursor:cursor + path_bytes]
        assert 2 <= path_bytes <= 160 and name.endswith(b'\0') and b'\0' not in name[:-1]
        path = name[:-1].decode('ascii')
        assert path not in records and all(piece not in ('', '.', '..') for piece in path.split('/'))
        cursor += (path_bytes + 7) & ~7
        data_at = cursor
        cursor += (packed + 7) & ~7
        assert mode in (0o644, 0o755) and packed and cursor <= total
        records[path] = (blob[start:cursor], blob[data_at:data_at + packed], size)
    assert cursor == total
    return records


def contents(record):
    _, packed, size = record
    data = zlib.decompress(packed)
    assert len(data) == size
    return data


def config_record(path, data):
    name = path.encode('ascii') + b'\0'
    packed = zlib.compress(data, 9)
    header = struct.pack('<IIQQ', len(name), 0o644, len(data), len(packed))
    return header + name + bytes(-len(name) % 8) + packed + bytes(-len(packed) % 8), packed, len(data)


def settings_clients_addon(addon):
    records = addon_records(addon)
    assert contents(records[CLIENTS]) == b'CollectionsPoster\nAegirPoster\nPreferences\n'
    records[CLIENTS] = config_record(CLIENTS, ('\n'.join(SETTINGS_CLIENTS) + '\n').encode('ascii'))
    body = b''.join(record[0] for record in records.values())
    return struct.pack('<8sIIQ', b'NGPUADD2', len(records), 0, 24 + len(body)) + body


def cdhashes(blob):
    # The iOS signing script emits a thin arm64 Mach-O and a 4 KiB CodeDirectory.
    magic, cpu, _, _, commands, command_bytes = struct.unpack_from('<6I', blob)
    assert magic == 0xfeedfacf and cpu == 0x0100000c and 32 + command_bytes <= len(blob)
    cursor = 32
    for _ in range(commands):
        cmd, length = struct.unpack_from('<II', blob, cursor)
        assert length >= 8 and cursor + length <= 32 + command_bytes
        if cmd == 0x1d:  # LC_CODE_SIGNATURE
            offset, size = struct.unpack_from('<II', blob, cursor + 8)
            signature = blob[offset:offset + size]
            assert len(signature) == size
            break
        cursor += length
    else:
        raise ValueError('Mach-O is missing LC_CODE_SIGNATURE')
    magic, total, count = struct.unpack_from('>III', signature)
    assert magic == 0xfade0cc0 and 12 + 8 * count <= total <= size
    hashes = set()
    for index in range(count):
        slot, offset = struct.unpack_from('>II', signature, 12 + 8 * index)
        if slot != 0 and not 0x1000 <= slot < 0x1005:
            continue
        magic, length = struct.unpack_from('>II', signature, offset)
        assert magic == 0xfade0c02 and 40 <= length <= total - offset
        directory = signature[offset:offset + length]
        if directory[37] == 2 and directory[39] == 12:
            hashes.add(hashlib.sha256(directory).digest()[:20])
    return hashes


def metal_addon(wallpaper, compact=None):
    assert sha256(wallpaper) == WALLPAPER_SHA
    original = addon_records(wallpaper)
    assert len(original) == 5 and all(path.startswith('wallpaper/') for path in original)
    if compact:
        for name in ('J120.png', 'J120-Dark.png'):
            path = 'wallpaper/' + name
            data = (compact / name).read_bytes()
            assert data.startswith(b'\x89PNG\r\n\x1a\n') and struct.unpack_from('>II', data, 16) == (2304, 2304)
            original[path] = config_record(path, data)
    with zipfile.ZipFile(ARCHIVE) as artifact:
        assert sorted(artifact.namelist()) == ['adreno-metal-plugin/trust.json', 'gpuaddon.bin']
        plugin = addon_records(artifact.read('gpuaddon.bin'))
        signing = json.loads(artifact.read('adreno-metal-plugin/trust.json'))
    selected = {path: record for path, record in plugin.items() if path.startswith(BUNDLE) or path == PUBLISH}
    info = plistlib.loads(contents(selected[BUNDLE + 'Info.plist']))
    assert info['CFBundleExecutable'] == 'NativeAdrenoMetal'
    assert contents(selected[PUBLISH]) == b'1\n'
    hashes = []
    for name, key in [('NativeAdrenoMetal', 'cdhash'), ('libvulkan_freedreno.dylib', 'turnip_cdhash')]:
        cdhash = bytes.fromhex(signing[key])
        assert cdhash in cdhashes(contents(selected[BUNDLE + name])), name
        hashes.append(cdhash)
    assert hashes[0] != hashes[1]
    # This pinned iOS plugin reads the official --clients marker. There are three slots beside backboardd.
    selected[CLIENTS] = config_record(CLIENTS, b'CollectionsPoster\nAegirPoster\nPreferences\n')
    records = original | selected
    body = b''.join(record[0] for record in records.values())
    return struct.pack('<8sIIQ', b'NGPUADD2', len(records), 0, 24 + len(body)) + body, sorted(hashes), len(records)


def owner_trust(original, hashes):
    assert sha256(original) == APPLE_TRUST_SHA
    count, first, second = struct.unpack_from('<3I', original)
    assert count == 2 and first == 12
    identifier = uuid.uuid5(uuid.NAMESPACE_URL, 'org.blu-sharky.adreno-metal:' + ''.join(h.hex() for h in hashes))
    owner = struct.pack('<I16sI', 2, identifier.bytes, len(hashes))
    owner += b''.join(value + b'\x02\x00\x00\x00' for value in hashes)
    return struct.pack('<4I', 3, 16, 16 + len(owner), 16 + len(owner) + second - first) + owner + original[first:]
