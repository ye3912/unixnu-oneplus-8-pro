# ArmCpu

ARM generic interrupt controller and timer.

starts the CPU, GIC and timer on sheng and on the QEMU virt machine.

Build and interface details: [documentation](https://unixnu.com/reference/components). Component sources and dependencies: [catalog](https://unixnu.com/reference/components).

`armcpu-redist-ipi=1` selects SGI 0 delivery through each target's GICv3
redistributor. This mode requires `armcpu-self-ipi=1` and an active GIC, and
cannot be combined with `armcpu-spi-ipi=1`. Enable it only on a board whose
redistributor set-pending path has been verified.
