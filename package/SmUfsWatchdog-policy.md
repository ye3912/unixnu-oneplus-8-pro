# SM8250 original watchdog owner policy

The real board class is SmUfsPlatformWatchdog : IOWatchdog. H3V native boot
published this service and ran364 software timer callbacks, but the first
watchdogd reached the original IOServiceOpen failure BRK. No client/heartbeat
had succeeded. The actual MACF error was not captured in that run.

Following GFander/UniXNU-kebab88da12ad589eb80f116180822a52cfbdac76d115
docs/SANDBOX-WATCHDOG-20261031.md, the board owns an explicit policy derivative.
The original21H461 readonly Sandbox condition AppleARMWatchdogTimer is mapped
to the actual same-length board class. This is not unmodified Apple policy or
Apple-authenticated policy. Original MACF execution, root/entitlement/exclusive
client checks, heartbeat/deadline/critical handling and AMFI remain in use.

After the normal kernel/prelink build, run scripts/adapt-sm8250-watchdog-policy.py
with --kernel, --plan, --kernelcache, --prelink and a distinct --output path.
Package that derived kernel. The CLI build kernel remains an immutable parent.
Keep the derived .json and .policy.json receipts beside the output. Never alter
the original kernelcache or reuse an older adapted candidate as a fresh parent.

The converter pins the exact original cache, read-only segment, unique context,
normal embedded Mach-O header rebasing and original Sandbox/Watchdog code hashes.
It changes only the21-byte class condition; all other parent kernel bytes match.
Bad input/identity, policy/code changes and repeated application are rejected.

The board patch records the real service-open MACF result and a read-only
IOResources negative control under the same credential/type, without opening
the control or changing the target return. An identity test limits observation
to this actual service. The service note records first-policy PID and first
original newUserClient result separately from aggregate accepted clients.
Original backend behavior is unchanged. This remains software watchdog only.

Host production observer/modelled APIs and deliberate broken observers passed;
final current37-function object/link/ABI checks passed. Native target policy,
negative control, original client and continuing heartbeat are pending H3W.
No full desktop or independent hardware watchdog qualification is claimed.
