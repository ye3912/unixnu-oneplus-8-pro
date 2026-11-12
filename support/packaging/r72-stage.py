"""Replace the signed Metal bundle executable in the R71 image and refresh its trust."""
import difflib
import json
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

work = Path(__file__).resolve().parent
sys.path[:0] = [str(work.parent / f"desktop-r{revision}") for revision in (59, 65)]
from metal_inputs import BUNDLE, CLIENTS, addon_records, cdhashes, contents, owner_trust, sha256
from package import BOARD, base, tree, trust_entry, unpack

archive = work / "native-adreno-metal-ios17-r72.zip"
archive_sha = "1316af90ccd17434d6d5c099b58782ea116500338bb40275a89dc8d62b957971"
assert sha256(archive.read_bytes()) == archive_sha
with zipfile.ZipFile(archive) as artifact:
    assert sorted(artifact.namelist()) == ["adreno-metal-plugin/trust.json", "gpuaddon.bin"]
    signed = addon_records(artifact.read("gpuaddon.bin"))
    signing = json.loads(artifact.read("adreno-metal-plugin/trust.json"))
    plugin_name = BUNDLE + "NativeAdrenoMetal"
    turnip_name = BUNDLE + "libvulkan_freedreno.dylib"
    plugin_hash = bytes.fromhex(signing["cdhash"])
    assert plugin_hash in cdhashes(contents(signed[plugin_name]))
    assert bytes.fromhex(signing["turnip_cdhash"]) in cdhashes(contents(signed[turnip_name]))

parent = base / "builds/2026-11-09/h4c-a650-pager-ownership-r71"
delivery = json.loads((parent / "delivery.json").read_text())
blob = (parent / delivery["image"]).read_bytes()
assert sha256(blob) == delivery["image_sha256"] == "a15de87543cf0fce6f85d658deac326d265c40202e99ee2396a9f068187282bc"
with tempfile.TemporaryDirectory(prefix="r72-parent-") as scratch:
    fat = Path(scratch) / "payload.img"
    fat.write_bytes(unpack(blob)[2])
    trust = subprocess.check_output(["mtype", "-i", fat, trust_entry])
assert sha256(trust) == delivery["fat_files_after"][trust_entry]
count, first, second, third = struct.unpack_from("<4I", trust)
assert (count, first, second - first) == (3, 16, 72)
stock_trust = struct.pack("<3I", 2, 12, 12 + third - second) + trust[second:]

old = (work.parent / "desktop-r66/kernel.macho.gpuaddon").read_bytes()
old_sha = "8805663fba91f7693074448463df3139ee898a48168560a84d42a85fa4edf81a"
assert sha256(old) == old_sha
records = addon_records(old)
owner_hashes = [trust[offset:offset + 20] for offset in (first + 24, first + 48)]
old_plugins = set(owner_hashes) & cdhashes(contents(records[plugin_name]))
old_turnips = set(owner_hashes) & cdhashes(contents(records[turnip_name]))
assert len(old_plugins) == len(old_turnips) == 1 and old_plugins.isdisjoint(old_turnips)
assert owner_trust(stock_trust, sorted(owner_hashes)) == trust
assert plugin_hash not in owner_hashes
assert contents(signed[BUNDLE + "Info.plist"]) == contents(records[BUNDLE + "Info.plist"])
assert contents(records[CLIENTS]) == b"CollectionsPoster\nAegirPoster\nPreferences\niconservicesagent\n"

records[plugin_name] = signed[plugin_name]
body = b"".join(record[0] for record in records.values())
addon = struct.pack("<8sIIQ", b"NGPUADD2", len(records), 0, 24 + len(body)) + body
assert addon_records(addon) == records
next_trust = owner_trust(stock_trust, sorted({plugin_hash} | old_turnips))
addon_sha = sha256(addon)

source = "bsd/kern/bsd_init.c"
before = (tree / ".cache/xnu-work" / source).read_text()
hash_literal = lambda digest: ",".join(f"0x{byte:02x}" for byte in bytes.fromhex(digest))
old_size, new_size = (f"metal ? {len(data)} :" for data in (old, addon))
assert before.count(old_size) == before.count(hash_literal(old_sha)) == 1
after = before.replace(old_size, new_size, 1).replace(hash_literal(old_sha), hash_literal(addon_sha), 1)
patch = "".join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                     f"a/{source}", f"b/{source}"))
patches = BOARD / "patches/xnu"
series = patches / "series"
name = "sm8250-metal-pipeline-addon-r72.patch"
assert series.read_text().endswith("sm8250-a650-pager-ownership-r71.patch\n")
assert not (patches / name).exists()

(work / "kernel.macho.gpuaddon").write_bytes(addon)
(work / "kernel.macho.trustcache").write_bytes(next_trust)
(work / "inputs.json").write_text(json.dumps({
    "artifact_id": 13684985374, "artifact_sha256": archive_sha,
    "addon_sha256": addon_sha, "trust_sha256": sha256(next_trust),
    "plugin_cdhash": plugin_hash.hex(), "turnip_cdhash": next(iter(old_turnips)).hex(),
}, indent=2) + "\n")
(work / name).write_text(patch)
(patches / name).write_text(patch)
with series.open("a") as order:
    order.write(name + "\n")
print("R72 addon", len(addon), addon_sha)
