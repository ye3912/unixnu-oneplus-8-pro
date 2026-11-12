# UniXNU-sm8250-common

Shared SM8250 (kona) support for UniXNU. Qualcomm Snapdragon 865 / 865+.

## Scope

| File | Contents |
| --- | --- |
| `soc.toml` | Profile: name, hardware data source, selected components |
| `dts/sm8250.dtsi` | CPU topology, PSCI, GICv3, architected timer rate, UFS host and PHY |
| `configs/sm8250.config` | SoC-wide kernel options (none yet) |
| `patches/xnu/series` | SoC patch series (empty) |
| `kits/` | Shared platform operations (none yet) |

## Sources

Every register range, interrupt number and timer rate in `dts/sm8250.dtsi` is taken
from the OnePlus 8 series ColorOS 16 kernel tree
(`arch/arm64/boot/dts/vendor/qcom/kona.dtsi`). Change a value only against that
source or a register read from the device.

## Selecting it from a device

```toml
[board]
soc = "SM8250"
soc_source = "sm8250"

[device_tree]
source = "device:dts/<device>.dts"
include_dirs = ["soc:dts"]
```

The board DTS includes `sm8250.dtsi` and supplies memory, enabled peripherals and
reservations. Boards enable the UFS nodes with `&ufs { status = "okay"; };`.

## State

Board-level bring-up only. No GPU (Adreno 650 is unsupported), no SMMU, no clock or
power controller nodes yet.

## License

BSD-2-Clause-Patent. See `LICENSE`.
