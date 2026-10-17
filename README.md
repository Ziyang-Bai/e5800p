# e5800p

基于CASIO fx-5800p型计算器的增强型固件。

提供 TABLE 绘图、ASM/Hex 编辑器，以及 **e.basic** 的内存、汇编和绘图命令。随附的 **5800p-kits** 工具链使用 Python 描述和生成固件补丁。

## 从原厂 Flash 构建

准备 Python 3.10+、本项目源码和匹配版本的原厂 **512 KiB Flash**。以下命令在项目根目录的 **PowerShell** 中执行。

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

接着按 [加载与备份](docs/e5800p.md#加载与备份) 将镜像装入独立的模拟器型号副本。

## 升级已有修改版

先保存并关闭模拟器，备份完整型号目录。输入当前持久化 Flash 和匹配的原厂文件：

```powershell
$Current = Read-Host '当前 Flash 文件路径'
$Original = Read-Host '匹配的原厂 Flash 文件路径'
python tools/casio_tool.py build "$Current" --clean "$Original" -o build/e5800p.bin --map build/e5800p.map.json
```

升级保留当前镜像的原生用户数据区，并从原厂参考和 Python 源码重建固件区。型号中的 SRAM/PRAM 等文件随整个目录备份；保存和部署方法见 [固件使用指南](docs/e5800p.md)。

## 文档

| 任务 | 文档 |
| --- | --- |
| 使用 TABLE、ASM/Hex 和 GOTO | [固件使用指南](docs/e5800p.md) |
| 用 Python 或 nXu8 汇编编写功能 | [5800p-kits 工具链](docs/5800p-kits.md) |
| 在计算器上写 BASIC | [输入与示例](docs/BASIC_enhancements.md) · [e.basic 语言参考](docs/e.basic.md) |
| 调用小字体、研究 Flash 映射 | [字体接口](docs/ROM_small_font.md) · [地址映射](docs/flash_upper_mapping.md) |
| 构建模拟器、验证固件 | [模拟器](docs/emulator.md) · [验证方法与记录](docs/verification.md) |

当前固件源码入口是 [`firmware/e5800p/project.py`](firmware/e5800p/project.py)。修改方法和模块分工见 [维护固件](docs/5800p-kits.md#改动如何记录)。

## 许可与分发

项目自有代码按 [GPL-3.0-only](LICENSE) 许可证许可。模拟器补丁基于 [CasioEmuMsvc](https://github.com/telecomadm1145/CasioEmuMsvc)，上游版权归原作者。

仓库分发工具、自定义代码和资源。CASIO 原厂 Flash、ROM、完整修改固件及手册由使用者自行取得并保留本地。源码补丁方案减少完整固件的再分发；具体版权与逆向工程规则取决于相关许可和所在地法律。
