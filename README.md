# UniXNU — OnePlus 8 Pro / IN2020

当前保存的是 **iPadOS 17.7.11（21H461）、Metal 已在设备运行的 R1 源码基线**。用户已确认设置正常进入；在启用 GPU 拷帧后，反馈“撕裂没有了，卡顿明显改善”。镜像 SHA256：`493568fd555fda131014d45d023346cc4e867cec10d04ef78842c688266a4965`。

这是一份开发源码快照。正在另外重建的上游 GPU R2 尚未实测，未混入此版本；这里也不包含启动镜像、固件、Apple 系统文件或 Data。

## 已确认的范围与限制

- 桌面、触摸、上滑解锁、亮度、八核启动以及 3 GiB OwnerData 持久化已有设备进展；本快照保留对应实现。
- GPU 注册、持久 Data 上 addon 安装、用户态 Metal 加载、提交和 fence 完成有日志证据。R1 保留 `sheng-fb-gpu=1 sheng-early-retire=1`。
- 仍有 `verify_swap failed`、backboardd watchdog 和慢帧；未宣称稳定 60 FPS，也未证明真实面板 vblank/page flip。
- 三段式档位识别已接线，系统静音图标仍未通过验收，已暂停；音频、Wi-Fi、蓝牙等未完成。
- 本次上传验证源码内容、版本和排除范围，没有重新在干净机器构建或启动手机。

## 目录

| 路径 | 内容 |
| --- | --- |
| `board.toml`、`configs/`、`dts/`、`package/`、`drivers/`、`patches/`、`scripts/` | IN2020 板级实现及有序 XNU 补丁 |
| `porting.toml` | 各子系统的历史开发及验收记录，可能引用未上传的本地日志 |
| `support/UniXNU/` | 当前核心及组件的文本源码快照，含实际本地修改；非 Git submodule |
| `support/UniXNU-sm8250-common/` | SM8250 公共配置与设备树源码 |
| `support/a650-reference/` | 内核实际采用的 A650 与配套 kit 文本源码 |
| `support/gop-r20/` | 构建时选择的 GOP presenter 引用源码 |
| `support/uefi/` | 固定 Mu-Silicium 基版本上的本地补丁及编辑文件 |
| `evidence/` | R1 启动参数、设备结论及 R72 addon 哈希/签名索引 |
| `source-pins.json`、`source-manifest.json` | 原始版本、范围说明及逐文件 SHA256 |

快照的原始核心版本及子模块版本见 `source-pins.json`。上游协议和目录名保持原样；各组件保留其 LICENSE/NOTICE。根目录 `LICENSE` 适用于板级仓库，组件按各自许可证分发。

## 构建边界

完整说明见 [源码快照与外部输入](docs/SOURCE-SNAPSHOT.md)。外部输入须由使用者自行准备，路径与摘要见 `proprietary-files.txt`、`docs/omitted-inputs.json` 及构建脚本；**不要生成随意的替代文件绕过哈希或 ABI 校验**。

特别是 OwnerKey/OwnerPolicy、精确 21H461 kernelcache、存储 ABI 参考输入、A650 固件、原版签名 trust 数据和 Data seed 未提交。现有部分脚本还带历史机器路径；本仓库是可追溯的工作源码快照，并非已经验证“一条命令在新机器复现”的发行包。

`evidence/r1-boot-config.toml` 才是已验收镜像的实际启动配置。`board.toml` 中较早的默认参数不等于最终镜像参数。禁止照搬旧 scaffold 中的分区刷写步骤；本仓库不自动操作硬件。

上游：[UniXNU](https://github.com/UniXNU/UniXNU)、[设备仓库说明](https://unixnu.com/porting/device-repository)、[GPU/Metal 路线](https://unixnu.com/porting/gpu)。
