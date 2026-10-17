# 验证方法与记录

修改工具或固件后，先运行单元测试，再用独立型号副本验证计算器行为。下方 [验证记录](#验证记录) 按各次构建保存证据范围。

## 工具链测试

在已安装工具链的项目根目录运行：

```powershell
python -m unittest discover -s tests -v
```

测试使用合成数据。当前 [GitHub Actions](../.github/workflows/check.yml) 覆盖 Ubuntu/Windows、Python 3.10/3.13，并检查命令行、wheel 安装和固件编译。

## 模拟器验证

使用包含 ROM、`config.bin`、Flash、RAM/SRAM 的完整隔离副本，并独占其 MCP 服务。先通过原生 OFF 保存需要保留的编辑，备份整个型号。

验收会复位并改写原生程序、变量和 Flash **S1～S6**，涉及公式、程序库和快照扇区。runner 在结束时恢复所改 Flash；故障退出时使用完整备份恢复。

### 运行普通验收

在项目根目录的 PowerShell 中设置路径。型号已按 [加载与备份](e5800p.md#加载与备份) 部署待验镜像，模拟器使用配套擦除与 PRAM 补丁，MCP 端口为 3001。

```powershell
$Exe = Read-Host '兼容的 CasioEmuMsvc.exe 路径'
$Model = Read-Host '待验的完整型号副本目录'
$Out = Read-Host '本次验证输出目录'
New-Item -ItemType Directory -Force $Out | Out-Null
```

1. 启动已关闭的副本；若该副本已运行，核对 MCP 进程和型号后进入下一步。

   ```powershell
   python tools/casio_tool.py model start --exe "$Exe" --model "$Model"
   ```

2. 运行验收：

   ```powershell
   python tools/casio_tool.py verify --case all --model "$Model" --out "$Out/basic-validation"
   ```

3. 检查命令退出状态和 `$Out/basic-validation` 中的记录。成功返回 0，失败返回非零并保留对应证据。

单独检查一类功能时，将 `all` 替换为下表的 case：

| 范围 | case |
| --- | --- |
| 原生与输入 | `native`、`tokens`、`control` |
| 表达式与编码 | `expressions`、`codec` |
| 内存与调用 | `memory`、`call` |
| 图形与 Flash | `graphics`、`flash` |
| 汇编与回归 | `asm`、`regression` |

`verify` 调用 `tools/basic_smoke.py`，保留退出码并核对实际进程、型号和 ROM SHA。将本次结果目录、镜像、map 和 SHA-256 一起留在本地；结果包含返回值、内存、寄存器及图像证据。

### 验证原生持久化

1. 按 [OFF 保存流程](e5800p.md#原生-program-的模拟器持久化) 等待关机与 Flash 落盘。
2. 正常关闭窗口，再冷启动同一完整副本。
3. 重开并运行 PROGRAM，核对程序记录与结果。

模拟器 snapshot 保存 CPU/RAM 探针现场，NOR Flash 保留最近擦写的内容；外设时序在恢复后可能需要复位才能重新响应键盘。重复实验使用完整副本或明确恢复磁盘镜像。普通验收会复位到已保存的原生状态。

### 旧 Hex journal 断电验收

沿用上方路径变量，在完整隔离副本上运行：

```powershell
python tools/casio_tool.py verify --suite power --model "$Model" --out "$Out/basic-power-validation" --exe "$Exe"
```

该 runner 会暂停、关闭并重启型号，验证旧 journal 的显式提交和恢复；运行期间独占该副本。普通 `--case all` 验证常规场景，BASIC 原始编程的故障恢复由作者另行安排。结果以本次 runner 的退出状态与证据为准。

### 实机验证

实体机的 NOR 时序、掉电恢复、耐久度和 TICKS 频率分别记录。刷机前保留完整 Flash/ROM 备份，确认匹配版本与硬件恢复方法。

固件保留原生 Built-in Prog/YAMAYO 库、版本设置及保护/释放功能。直接覆盖原生数据银行会破坏相应内容，程序作者管理备份和目标空间。

## 验证记录

以下记录来自对应开发批次。镜像完整哈希随原生用户数据变化；使用自己的输入构建后，保存同次验证结果。

### 2026-10-16 源码构建

Windows x64 / Python 3.13 上完成：

- 从仅含 Git 暂存源码的干净目录运行 48 项单元测试：47 项通过，1 项因 Windows 符号链接权限跳过。
- 原厂 Flash 经 90 个汇编区间重建，与当时 Python 生成器输出逐字节一致；原生用户数据与升级保留区均已比对。
- 模拟器普通验收通过 237 个场景，覆盖原生 BASIC、指令/表达式、ASM、Hex 翻页/GOTO/写入、内存、CALL、图形、Flash 与签名。落盘比对后正常退出，退出码 0。

### 旧汇编源码迁移

迁移到 `patchset.py` 与具名汇编后，干净源码运行 72 项测试：70 项通过，2 项因符号链接权限跳过。92 个区间重建及保留用户数据的升级构建均与迁移前逐字节一致。

原厂输入的完整 SHA-256：

```text
72cb81533dc15fdc1e340f4967225769ef16a38c0ff3f84dedcc52c0493cf06c
```

该批次验证源码导出、独立构建和升级；237 个模拟器场景来自上一批次。

### 2026-10-17 Python DSL 调用

66 次实际 CPU 调用覆盖整数边界、乘除/移位、条件/循环、短路副作用、嵌套调用、奇地址 word 访存和 ROM 破坏寄存器后的恢复。

原生 BASIC 执行 `CALL(540672)` 得到 42；LCD 正文清空，状态行保留。这些结果来自模拟器。

### 当前固件的 Python DSL 迁移

- 单元测试 112 项：111 项通过，1 项因 Windows 符号链接权限跳过。92 个代码/数据区由 Python DSL 构建，仓库外独立安装的 wheel 和升级构建生成相同镜像。
- `legacy/` 的独立构建及旧生成流程得到迁移前镜像；归档测试 72 项，70 项通过，2 项因符号链接权限跳过。
- 14 次实际 CPU/BASIC 调用覆盖原生 DSL 的进位、寄存器段访存、有符号步进、EA 自增、条件/循环、break/continue、除法、嵌套调用和普通函数寄存器保存；BASIC 两类入口分别返回 42、49。
- 11 类模拟器 case 分批通过 238 个场景，覆盖原生 BASIC、token、控制流、ASM、表达式、编解码、内存、CALL、图形、Flash、Hex 和签名，含新增 SRAM BLIT 回归。实际检查了 Hex 与关机 LCD；运行中 Flash、退出落盘的两个镜像均与构建产物一致，退出码 0。

该输入构建的完整 SHA-256：

```text
81606a11bc9fc06ec7e6dc74b971309114aa4897da675abead39744160406fac
```

相较迁移前镜像，修改为 BLIT 的两字节寄存器段前缀及一个校验字节：`0F 9A` 改为 `AF 90`，使图案读取使用 R10 指定的段。旧镜像的 SRAM 图案读取错误已在模拟器中复现。

### 持久化与恢复记录

此前修复副本验证过：编辑保存 `1→A`（源码 `31 0E 41 0D`）、原生 OFF、关闭窗口、冷启动、进入 EDIT；程序记录和源码保持一致。

旧 Hex journal 的七阶段冷启动恢复属于此前二进制记录，当前 DSL 批次运行普通 case。历史恢复批次曾在模拟器退出阶段报告 `0xc0000005`；退出前的落盘比对和后续重启恢复断言通过，退出异常原因待定位。恢复结果与进程退出稳定性分别记录。

### 历史空间测量

下表为此前二进制的同口径测量。当前代码大小以本次构建 map 为准。

| 模块 | 原始基线字节数 | 更早版本字节数 | 此前二进制字节数 |
| --- | ---: | ---: | ---: |
| 原 S4 可移动扩展及共享实现 | 24,306 | 21,895 | 21,777 |
| 新增 BASIC 主体 | 0 | 19,536 | 18,331 |
| BASIC 原生接入钩子 | 0 | 108 | 108 |

此前可移动扩展比原始基线少 2,529 字节，旧扩展与 BASIC 合计比更早版本少 1,323 字节。固定 S0 的选择器、扫描器、GRAPH、journal 共 3,308 字节，另有 18 字节原生钩子。

当前完整 Flash 仍为 512 KiB，使用 S0 空隙与 F 尾部，保留原生程序库银行。模拟器性能测量见 [运行时记录](emulator.md#历史测量)。
