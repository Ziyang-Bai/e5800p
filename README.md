# e5800p

CASIO fx-5800P 修改固件。

提供 GRAPH 绘图与数值分析、原生 TABLE、ASM/Hex 编辑器及 e.basic 扩展命令。随附的 5800p-kits 将 [PL/e](docs/5800p-kits.md#ple) 源码编译为固件补丁和 `.bin` 应用。

## 从原厂 Flash 构建

准备 Python 3.10+、项目源码和匹配版本的原厂 512 KiB Flash。在项目根目录打开 PowerShell。

1. 安装工具链：

   ```powershell
   python -m pip install -e .
   ```

2. 按提示输入原厂文件路径，生成固件：

   ```powershell
   $Original = Read-Host '原厂 Flash 文件路径'
   python tools/casio_tool.py build "$Original" -o build/e5800p.bin --map build/e5800p.map.json
   ```

3. 检查输出：

   ```powershell
   python tools/casio_tool.py inspect build/e5800p.bin --native-checksum --map build/e5800p.map.json
   ```

输出文件为 `build/e5800p.bin`；检查结果应包含 `"size": 524288` 和 `"valid": true`。`e5800p.map.json` 记录各补丁的位置和大小。

实机烧录文件的生成方法见 [生成实机烧写镜像](docs/5800p-kits.md#生成实机烧写镜像)。

接着按 [加载与备份](docs/e5800p.md#加载与备份) 将镜像装入独立的模拟器型号副本。

## 升级已有修改版

先保存并关闭模拟器，备份完整型号目录。输入该型号最新保存的 Flash 和匹配的原厂文件：

```powershell
$Current = Read-Host '当前 Flash 文件路径'
$Original = Read-Host '匹配的原厂 Flash 文件路径'
python tools/casio_tool.py build "$Current" --clean "$Original" -o build/e5800p.bin --map build/e5800p.map.json
```

升级重建固件区，保留当前镜像的原生用户数据。SRAM/PRAM 随型号目录备份；部署方法见 [固件使用指南](docs/e5800p.md)。

## 文档

| 任务 | 文档 |
| --- | --- |
| 使用 GRAPH、TABLE、ASM/Hex 和 GOTO | [固件使用指南](docs/e5800p.md) |
| 用 PL/e 或 nXu8 汇编编写功能、安装 Add-in | [5800p-kits 工具链](docs/5800p-kits.md) |
| 在计算器上写 BASIC | [输入与示例](docs/BASIC_enhancements.md) · [e.basic 语言参考](docs/e.basic.md) |
| 调用小字体、研究 Flash 映射 | [字体接口](docs/ROM_small_font.md) · [地址映射](docs/flash_upper_mapping.md) |
| 构建模拟器、运行测试 | [模拟器](docs/emulator.md) · [测试](docs/5800p-kits.md#测试) |

固件入口：[`firmware/e5800p/project.py`](firmware/e5800p/project.py)。开发参考：[模块与布局](docs/5800p-kits.md#改动如何记录) · [项目术语](TERMS.md)。

## 许可与分发

采用 [GPL-3.0-only](LICENSE) 许可证授权。
模拟器补丁基于 [CasioEmuMsvc](https://github.com/telecomadm1145/CasioEmuMsvc)。

