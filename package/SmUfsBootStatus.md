# Board boot-status contract (H3X)

21H461 original watchdogd SHA256 ded4c688e1c2add74acf3e7f9eea5fe2c2c569180ce81492221877944d913a01.
H3W user transcript: target0/control1, original client result0/clients3;
first BRK pid52 pc100934160, exact16-word match at original0x10000b160,
slide0x929000. Caller0x100009ef4 follows IOServiceGetMatchingService returning0
for IOService + IOPropertyMatch{IOPMUPrimary:NSNumber(1)}. Final critical PID127
has no separately captured PC. No heartbeat sequence observed (beats0).

H3X implements this discovery and numeric IOPMUBootStage storage as an explicitly
software-only, volatile board service. This is not a PM8150 PON device, a physical
PMU identity, persistent boot-stage storage, RTC, regulator, power, or reset backend.
Hardware accesses are absent. Published backend/capability properties state this.
Unknown/mixed properties, nonnumbers, values outside0..255, unprivileged tasks,
and writes before readiness fail. Storage failure propagates. No foreground app
name property is implemented; it is refused rather than silently accepted.

Original IOKit MACF property checks run before the root-only service setter.
Original watchdog client/selector/heartbeat/deadline code and H3W owner policy are
retained. No new sandbox grant or no-pmu boot argument. Startup publishes exactly
one primary boot-status interface before original launchd. Actual native writes
and watchdog heartbeat progression require the next native result.

GF fixed88da12ad589eb80f116180822a52cfbdac76d115 docs/GF-WATCHDOG-CLOCK-20261030.md
documents the same matching contract on another OS. Its actual PON hardware
verification is not claimed for this board; no GF addresses or code are copied.
New service code is MIT licensed; no new external dependency.
