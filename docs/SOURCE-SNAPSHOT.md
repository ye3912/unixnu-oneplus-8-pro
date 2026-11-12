# R1 源码快照说明

本快照于 2026-11-13 从实际 bring-up 源码目录导出，没有修改原工作树。R2 已动过的 `NativeLegacyDisplay.cpp` 和 `build_display.py` 在导出副本中恢复为 R1 备份，存储绑定审计也恢复为该轮输入记录；没有把 R2 的扫描移除改动冒充为已经实测。

R1 native kernel SHA256 为 `bf0c1eb4b50de9a7f8061d0e227813d0d66daa40b443f1e6347e7c57b5c24c9a`。实际交付 kernel 还经过既有 watchdog policy / panic 打包适配，所以不得混淆 native 与镜像内核的摘要。R1 在持久 Data 上复用 R72 addon，输入与 CDHashes 见 `../evidence/r72-addon-inputs.json`。

## 源码与原始版本

`../source-pins.json` 记录核心、组件、A650、Mu-Silicium 原始提交；`../source-manifest.json` 给出导出文件的实际摘要。本地改动已经体现在导出的核心/组件文件中；这些目录不是子模块，不应对它们运行 `git submodule update` 来覆盖快照。

Mu-Silicium 完整上游树须按记录版本另行获取，再应用 `../support/uefi/local-changes.patch`；overlay 中提供相同编辑文件便于复核。固件二进制不在补丁内。

R72 addon 由历史构建产物复用；目前能核对本地 ZIP、最终 addon 和签名摘要，尚未完整恢复该远端构建的源码/工作流链。仓库同时保存当前本地核心/Metal 组件源码，但不声称其重新编译一定逐字节等同 R72。该限制与正在进行的 R2 配套重建分别记录。

## 本地构建入口

板级内核入口仍是 UniXNU 的 `build kernel -D <设备目录>`，GOP 使用导出快照 `support/gop-r20`；A650 构建脚本通过 `SM8250_A650_REFERENCE` 指向 `support/a650-reference`。根 `feeds.toml` 只把 SoC local 路径改为仓库内的公共源码，未改变硬件值或补丁顺序。

在拥有原始输入与工具链的环境中，入口形式为：

```sh
DEVICE_DIR="$(pwd)"
export SM8250_A650_REFERENCE="$DEVICE_DIR/support/a650-reference"
cd "$DEVICE_DIR/support/UniXNU"
./unixnu build kernel -D "$DEVICE_DIR" --out /absolute/path/to/out \
  --local-module "driver:GopFramebuffer=$DEVICE_DIR/support/gop-r20"
```

这是入口说明，未作为干净环境复现命令实测。部分 ABI 审计、打包步骤仍引用历史绝对路径和先前测得的原版 21H461 输入；先补齐这些输入再构建，不能删掉守卫来让命令返回成功。

## 排除项

- OwnerKey 及其他凭据、`.env`、本地 Git 认证配置。
- 固件、IPSW、DMG、系统 kernelcache、trustcache、boot image 和 Data seed。
- 编译中间产物、缓存、历史 `.bak`、对象、归档、机器生成的二进制测试 fixture。
- R2 的源码修改与尚未验收的上游组件。

`omitted-inputs.json` 列出导出时碰到的非文本/二进制输入路径及大小。这里只是索引，文件内容没有上传。必要的固件来源与摘要仍沿用 `proprietary-files.txt`。

验收结论取自 `../evidence/r1-device-result.json` 和 `../evidence/ownerdata-device-result.json`；其中的本地路径是历史证据定位信息，不代表相应日志已经公开。本次未上传原始串口日志或真实用户 Data。
