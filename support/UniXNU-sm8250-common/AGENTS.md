# AGENTS.md

Read the UniXNU documentation before changing this repository.

| Topic | Page |
| --- | --- |
| SoC repository contents | https://unixnu.com/porting/soc-support |
| Device tree bindings | https://unixnu.com/porting/device-tree |
| Driver adaptation order | https://unixnu.com/porting/drivers |
| Component catalog | https://unixnu.com/reference/components |

## Responsibility

Shared SM8250 resources: `dts/sm8250.dtsi`, `configs/sm8250.config`, the SoC patch
series and reusable platform operations under `kits/`. Board wiring, memory sizes,
enabled peripherals and policy belong to the device repository.

## Rules

- Every register range and interrupt number needs a source: the device kernel tree,
  a register read, or a hardware document. Record it in the commit message.
- `soc.toml` `[components] include` lists canonical catalog IDs only.
- Keep `dts/sm8250.dtsi` limited to nodes a driver consumes. Unused peripherals stay out.
