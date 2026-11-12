# AGENTS.md

Read the UniXNU documentation before changing this repository.

| Topic | Page |
| --- | --- |
| Device repository layout | https://unixnu.com/porting/device-repository |
| Device tree | https://unixnu.com/porting/device-tree |
| Driver adaptation order | https://unixnu.com/porting/drivers |
| Porting record | https://unixnu.com/porting/records |
| Bring-up stages | https://unixnu.com/porting/bring-up |

## Responsibility

Board policy for the OnePlus 8 Pro: memory size, enabled peripherals, reservations,
partition geometry, firmware selection, payload policy and board services under
`package/`. Shared SM8250 resources belong to `UniXNU-sm8250-common`.

## Rules

- `components.include`, `kernel.archives`, `config_fragments` and `patch_series` are
  arrays: an override replaces the inherited array, so each one lists every entry.
- Hardware values come from the device kernel tree or a register read. Record the
  source in the commit message and in `porting.toml`.
- Firmware, IPSW members and Data seeds stay out of Git; `proprietary-files.txt`
  records them with a hash.
- The payload volume has to fit the 96 MiB boot partition. Raise `[payload] size_mib`
  only after measuring the packaged kernel.
- Two vendor panel XMLs carry a mismatched filename. Identify a panel by its
  `<PanelName>` and `<HorizontalActive>`, never by filename.
