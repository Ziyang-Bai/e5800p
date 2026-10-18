# 5800p-kits 工具链

版本 0.1.0，需要 Python 3.10+。先按 [README](../README.md#从原厂-flash-构建) 安装工具链并生成 `build/e5800p.bin`。命令在项目根目录的 PowerShell 中执行。

- [PL/e](#ple)：函数、内存、ROM 调用和原生寄存器。
- [应用包](#应用包)：构建 `.bin`、备份 S4、安装与恢复。
- [汇编与镜像工具](#python-工具链)：汇编、反汇编、写入镜像。
- [调试](#调试)：断点、单步与内存读回。
- [维护固件](#改动如何记录) · [测试](#测试)：模块分工、布局与测试命令。

## PL/e

PL/e 使用 Python 语法，将 `@fw.function` 函数编译为 nXu8 机器码。模块导入、资源读取和固件声明由电脑上的 Python 执行；编译错误带源码路径和行号。

### 编译并调用示例

[`examples/python_demo.py`](../examples/python_demo.py) 中的 `main` 调用 `clear_screen` 清除 LCD 正文，再通过 `add_two(40)` 返回 42。

示例写入 `8:4000–5FFF` 中放置函数的区域。备份该区后，在型号副本中试运行。

1. 编译并生成汇编清单：

   ```powershell
   python -m kits examples/python_demo.py build/e5800p.bin --listing build/python-demo.asm
   ```

2. 按 [加载与备份](e5800p.md#加载与备份) 部署生成的 `build/python-demo.bin`。
3. 在该副本的 BASIC 中运行：

   ```text
   CALL(540672)→A
   ```

`540672` 是入口 `8:4000` 的十进制地址。调用清除正文、保留状态行，变量 A 得到 42。修改后重新编译、部署。

也可在 Python 脚本中调用 `fw.build(original=..., output=...)`，或用 `fw.link()` 取得函数地址与代码块。原厂 Flash 可作为构建输入；BASIC 的 CALL 由 e5800p 提供，其他镜像可通过自己的入口或调试器调用。

### 函数、内存与类型

| 声明 | 行为 |
| --- | --- |
| `Firmware(name, regions=[(start, stop), ...])` | 指定代码可放置的 CPU 半开区间；区域用途由作者分配 |
| `@fw.function` | 自动安排地址；函数调用按最终地址链接 |
| `@fw.function(address=...)` | 固定公开入口，增加代码后仍按最终布局计算调用目标 |
| `class LCD(Memory)` | 将相关缓冲区命名分组 |
| `Buffer(address, size, dtype=u8)` | `address` 为完整数据地址，`size` 为元素个数；缓冲位于同一 64 KiB 数据段 |

默认参数和局部变量为 `u16`，算术按 16 位回绕，比较使用无符号值。`u8` 参数、返回类型及显式转换截为 8 位；`u16` 缓冲元素采用小端双字节。只执行操作的函数标为 `-> None`。

常量下标越界会报编译错误；动态下标直接访问目标内存，范围由作者保证。局部变量须在所有到达读取处的路径上先赋值。

### 控制流与运算

支持赋值、增量赋值、`if/else`、`while`、`for ... in range(...)`、`break`、`continue` 和 `return`。`range` 在进入循环时求值，步长为正或负的编译期常量，边界按无符号值解释。

运算包括 `+ - * & | ^ << >>`、比较和短路 `and/or/not`。`and/or` 返回选中的操作数；移位次数达到 16 时结果为零。`//` 和 `%` 的除数为 1–65535 的编译期常量。全局整数、`len(Buffer)` 和显式整数转换可参与表达式。

文件操作、容器和异常处理可用于构建层 Python；`@fw.function` 函数体使用上述语法。

### 调用约定与 ROM

普通函数最多四个整数参数，依次放在 ER0/ER2/ER4/ER6，结果在 ER0。函数保存 R4–R15 和 SP；PSW、EA 可改变。临时值、局部变量和嵌套调用使用栈，须为原生系统留出空间。

示例中的 `refresh = ROM(0x043BE, result=None)` 声明 ROM 刷新入口，函数内调用 `refresh()`。`ROM` 的参数寄存器支持 R0–R7、ER0/ER2/ER4/ER6，最多四个且各自占用独立字节；`result` 指定返回寄存器。

调用器保存使用中的 R4–R15。目标 ROM 对内存、字体、显示状态和指针的要求仍按其 ABI（调用约定）处理。

### 原生寄存器

原生挂钩和固定寄存器例程使用 `native=True`。它直接描述 CPU 操作，入口参数来自寄存器和原生栈，函数定义采用空形参列表。

将下面的完整项目保存为 `build/native_demo.py`。它使用 `8:4000–401F`；先备份该处内容。

```python
from kits import Firmware, cpu

fw = Firmware('native-demo', regions=((0x84000, 0x84020),))

@fw.function(native=True, address=0x84000)
def answer():
    cpu.r0 = 42
    cpu.r1 = 0
    cpu.ret()
```

编译：

```powershell
python -m kits build/native_demo.py build/e5800p.bin --listing build/native-demo.asm
```

输出为 `build/native-demo.bin`，入口机器码为 `2A 00 00 01 1F FE`。部署后使用 `CALL(540672)→A` 得到 42。

寄存器与访存：

- `cpu.r0`～`r15`、`er0/2/…/14`、`xr0/4/8/12`、`qr0/8` 对应物理寄存器；`sp`、`ea`、`lr`、`pc`、`psw` 等按指令支持的组合使用。
- 赋值生成 MOV，增量与位赋值生成对应操作。`compare` 更新标志，`add_carry/sub_carry` 使用进位；`multiply/divide` 保持原指令的结果与副作用。有符号立即数写实际值，如 `-1`。ER 的 ADD 立即数范围为 −64…63，SP 为 −128…127；较大的加法先将常量装入 ER，再使用寄存器相加。
- `cpu.mem8/16/32/64[...]` 指定宽度。立即段、寄存器段和复用 DSR 分别写作 `cpu.mem8[4, cpu.er2]`、`cpu.mem8[cpu.r10, cpu.er8]`、`cpu.mem8[cpu.dsr, cpu.er2]`；单下标按原生段状态访存。
- 位移写 `cpu.er14 + 4`；保留零位移编码用 `cpu.offset(cpu.er14, 0)`。EA 自增用 `cpu.post(cpu.ea)`，有效地址计算用 `cpu.ea = cpu.address(...)`。
- 多字节访存遵循 CPU 的地址对齐规则。读取紧凑记录中的奇地址 u16 时，分别用 `mem8` 读取低、高字节；写回同样逐字节完成。

控制流与数据：

- `cpu.label('loop')` 定义符号；`call/jump/branch` 分别调用、跳转和短跳转。整数目标为完整 CPU 地址，字符串目标为符号。
- `if cpu.eq: cpu.branch('done')` 生成条件短跳转。支持 `eq/ne/lt/ge/gt/le` 和有符号 `lts/ges/gts/les`；一般 `if/else`、`while`、`break/continue` 也可使用标志，循环体负责更新标志。
- 用 `push/pop` 保存和恢复寄存器，以 `cpu.ret()`、`return` 或 `cpu.pop(cpu.pc)` 返回；编译器按代码中的压栈、出栈和返回指令生成机器码。
- 常量表用 `fw.data(name, bytes, address=..., labels={名称:偏移})`，内嵌数据用 `cpu.data`。

普通函数通过 `ROM(address, args=..., result=...)` 声明原生入口后调用；直接把原生函数作为普通函数调用会报编译错误。

## 应用包

应用使用 PL/e，`app build` 输出包含机器码与装载信息的 `.bin` 文件。

### 构建并安装 HELLO

S4 是 CPU `9:0000–9:FFFF` 的 64 KiB，初始化后用于应用。原生 Built-in/YAMAYO 库与应用共用这一区域；保存完整备份后再初始化。

1. 构建 HELLO：

   ```powershell
   python tools/casio_tool.py app build examples/app_hello.py -o build/hello.bin --stack-bytes 512 --listing build/hello.asm
   ```

2. 备份原库并建立空应用目录。备份路径使用一个新文件名：

   ```powershell
   python tools/casio_tool.py app init build/e5800p.bin -o build/apps-empty.bin --backup-s4 build/s4-original.bin
   ```

3. 安装并查看目录：

   ```powershell
   python tools/casio_tool.py app install build/apps-empty.bin build/hello.bin -o build/apps-hello.bin
   python tools/casio_tool.py app list build/apps-hello.bin
   ```

4. 关闭型号副本，再[部署并启动](e5800p.md#加载与备份) `build/apps-hello.bin`。后续安装以副本最新保存的 Flash 为输入。
5. 在配套模拟器的计算页面按 **F10 → 6:Add-in → HELLO**。HELLO 显示文字，EXIT 返回启动器，屏幕显示 `RETURN 42`，EXE 回列表。

第二个示例 [`examples/app_return.py`](../examples/app_return.py) 链接到 `9:1000`，返回 7。HELLO 位于 `9:0100`；两个示例可装入同一镜像。

### 生成实机烧写镜像

在项目根目录准备以下文件：

- `chip-backup.bin`：用烧录器读取的原机 1 MiB 全片备份。
- `stock.bin`：与本机匹配的原厂 512 KiB 固件。

应用使用上一节编译的 `build/hello.bin`。

1. 从芯片备份取出低半区，构建 e5800p：

   ```powershell
   New-Item -ItemType Directory -Force build | Out-Null
   python tools/casio_tool.py read chip-backup.bin --offset 0 --size 0x80000 -o build/current-low.bin | Out-Null
   python tools/casio_tool.py build build/current-low.bin --clean stock.bin -o build/e5800p.bin
   ```

2. 第一次使用 Add-in，先备份 S4 中的原程序库，再建立应用目录：

   ```powershell
   python tools/casio_tool.py app init build/e5800p.bin -o build/apps-empty.bin --backup-s4 build/s4-original.bin
   ```

   保留 `build/s4-original.bin`，供恢复原库。已有同名备份时换一个新文件名。

   已有 Add-in 目录时跳过这一步，第 3 步的输入改用 `build/e5800p.bin`。

3. 安装 HELLO：

   ```powershell
   python tools/casio_tool.py app install build/apps-empty.bin build/hello.bin -o build/flash-low.bin
   python tools/casio_tool.py app list build/flash-low.bin
   python tools/casio_tool.py inspect build/flash-low.bin --native-checksum
   ```

   `app list` 应列出 HELLO，校验结果应为 `"valid": true`。安装自己的应用时，把 `build/hello.bin` 换成对应的应用文件；更新同名应用时，在安装命令末尾加 `--replace`。

4. 把修改后的低半区放回芯片备份，生成烧录文件：

   ```powershell
   python tools/casio_tool.py patch chip-backup.bin build/flash-low.bin --offset 0 -o build/flash-to-program.bin
   python tools/casio_tool.py inspect build/flash-to-program.bin
   ```

   检查结果应为 `"size": 1048576`。高半区 `0x80000–0xFFFFF` 沿用原机备份，地址关系见 [Flash 映射](flash_upper_mapping.md)。

| 文件 | 大小 | 用途 |
| --- | ---: | --- |
| `build/flash-low.bin` | 512 KiB | 加载到配套模拟器 |
| `build/flash-to-program.bin` | 1 MiB | 交给烧录器，按 raw BIN 格式写入 MX29LV800CB |

保留 `chip-backup.bin`。烧写后整片读回，与 `build/flash-to-program.bin` 比较，确认内容一致。

实机烧写和读回需硬件验证。

### 替换、删除与恢复

对同名应用使用 `--replace`；CLI 会检查它与其他应用及目录的地址范围。改变链接地址后，从 Python 源码重新构建：

```powershell
python tools/casio_tool.py app install build/apps-hello.bin build/hello.bin -o build/apps-replaced.bin --replace
python tools/casio_tool.py app remove build/apps-replaced.bin HELLO -o build/apps-removed.bin
python tools/casio_tool.py app restore build/apps-removed.bin build/s4-original.bin -o build/library-restored.bin
```

`restore` 用备份覆盖整个 S4，恢复原生库。每条命令生成独立输出；参数或格式错误时保留已有文件。`list` 的 `modified` 表示代码 CRC 与包记录有差异，可在设备上选择 `APP MODIFIED → 1:RUN` 运行。

### 应用入口

用 `Firmware(name, regions=...)` 声明名称和固定链接区间。`app build` 默认入口为 `main`，可用 `--entry` 指定其他函数。名称长 1–12 个字符，采用 ASCII `20–5F`。

| 入口寄存器 | 内容 |
| --- | --- |
| ER0 / ER2 | 段 0 栈工作区偏移 / 0 |
| ER4 / ER6 | 声明的工作区字节数 / 0 |
| ER0（返回） | 应用返回值 |

`--work-bytes` 默认 0；零长度时入口 ER0、ER2、ER4 均为 0。非零工作区按偶数字节分配并清零，生存期到应用 RET。`--stack-bytes` 由作者声明，包含应用的最深调用和临时压栈；启动器按声明及原生调用余量检查近 RAM。

启动器恢复寄存器、SP、PSW、EA、数学工作区和字体。应用写入 A/B/X/Ans 的值保留；应用须平衡栈并正常返回。

### E5AP 包与 E5AD 目录

`.bin` 使用小端整数，由 44 字节 E5AP 头和连续 payload 组成。payload 按实际链接范围展开，块间填 `FF`：

| 偏移 | 字段 |
| --- | --- |
| 0 | `E5AP` |
| 4 / 6 | format:u16 = 1 / header_size:u16 = 44 |
| 8 / 12 / 16 | load_address:u32 / entry_offset:u32 / payload_size:u32 |
| 20 / 22 | work_bytes:u16 / stack_bytes:u16 |
| 24 / 25 | name_len:u8 / reserved[3] = 0 |
| 28 | name[12]，余位填 0 |
| 40 | CRC32，覆盖头 0–39 与 payload |

payload 位于 CPU `[0x90100, 0x9FFF0)`，入口为 payload 内的偶数地址。

S4 开头 256 字节填 `FF`。尾部 `9:FFF0` 保存 16 字节 E5AD 固定头：magic[4]、format:u16=1、count:u16、directory_size:u32、CRC32:u32。其前紧邻 `count` 个 44 字节应用头，按装载地址排序。`directory_size = 16 + count * 44`；目录 CRC32 覆盖固定头前 12 字节，再接全部记录。每个 payload 的末端须在当前目录起点以内。

目录随应用数量增长。删除会回收旧 payload 和多余目录字节；安装其他应用时保留已有应用的手改代码。`init`、`install`、`remove`、`restore` 的镜像改动集中在 S4。

## Python 工具链

`tools/casio_tool.py` 处理源码、镜像和模拟器。地址参数接受十进制、`0x` 十六进制或十六进制 `段:偏移`。

### 汇编并写入镜像

[`examples/return42.asm`](../examples/return42.asm) 用 `PUSH LR → CALL add_two → POP PC` 返回 42，入口为 `9:2000`（`0x92000`，598016）。S4 用于原生程序库或 Add-in；备份并确认覆盖范围后，在型号副本中试验。

使用已构建的 `build/e5800p.bin`，依次执行：

1. 汇编并生成符号表：

   ```powershell
   python tools/casio_tool.py asm examples/return42.asm --origin 0x92000 -o build/return42.bin --listing build/return42.list.json --symbols build/return42.symbols.json
   ```

2. 反汇编生成的机器码：

   ```powershell
   python tools/casio_tool.py disasm build/return42.bin --offset 0 --origin 0x92000 -o build/return42.disasm.json
   ```

3. 写入镜像并更新校验和：

   ```powershell
   python tools/casio_tool.py patch build/e5800p.bin build/return42.bin --cpu-address 9:2000 --image-base 8:0000 -o build/demo.bin --native-checksum --map build/demo.patch.json
   ```

4. 检查镜像并读回目标前 16 字节：

   ```powershell
   python tools/casio_tool.py inspect build/demo.bin --native-checksum --map build/demo.patch.json
   python tools/casio_tool.py read build/demo.bin --offset 0x12000 --size 16 -o build/readback.bin
   ```

5. 按 [加载与备份](e5800p.md#加载与备份) 部署 `build/demo.bin`，在 BASIC 中运行 `CALL(598016)→A`；A 应为 42。

先用 `build` 重建固件，再用 `patch` 写入手工补丁。`patch` 按物理偏移或 `CPU地址−image-base` 替换字节；`--native-checksum` 用于 512 KiB 镜像。单独修正校验：

```powershell
$Image = Read-Host '待修正的完整 Flash 文件'
$Output = Read-Host '修正后另存的文件路径'
python tools/casio_tool.py checksum "$Image" -o "$Output"
```

### 电脑端汇编语法

汇编器使用 `tools/instruction_table.py` 的指令目录。设备内联 ASM 使用 [e.basic 参考](e.basic.md#当前支持的指令形式)中的目录和规则。

| 项目 | 电脑端写法 |
| --- | --- |
| 符号与数值 | 前后向标签，符号大小写等价；十进制、`0x`、`H` 后缀，整数 `+/-` 表达式；`;` 起行注释 |
| 常量与定位 | `.equ NAME,值` 或 `NAME EQU 值`；`.org 地址` 向前补零，地址在布局时可求值 |
| 数据 | DB 支持 ASCII 字符串和双引号转义，DW 输出小端 word |
| 调用与跳转 | CALL/JMP 的纯数字 `<0x10000` 表示当前段偏移；符号和 CALL_SYS 为绝对地址；跨段可写 `CALL 0x9:0x2000` |
| 数据段 | 完整 8 位立即段、寄存器段、复用 DSR，如 `L R0,0xFF:[ER2]`、`L R0,R3:0x8000`、`L R0,DSR:4[ER2]` |

支持 BAL、BP/FP 位移、EA 访存和寄存器跳转等原生形式。数值 `MOV ERn,#立即数` 在 −64～63 或 `0xFFC0～0xFFFF` 时使用两字节原生指令，其他 uint16 值使用四字节宏；符号立即数固定四字节，保持前向布局稳定。符号数量和行长取决于主机内存，编码宽度、对齐和分支距离仍按 CPU 要求。

Python 可导入 `nxu8_asm.assemble/disassemble` 与 `casio_emulator.MCPClient`。`assemble(source, origin)` 返回机器码 bytes、绝对符号 dict 和 listing list；`disassemble(data, origin)` 返回 listing。记录含 `address`、十六进制 `bytes`、`text`，汇编记录另含源码 `line`。反汇编对表外、歧义或截断编码输出 DW/DB，以保留可重新汇编的原字节。

## 调试

先启动已部署返回 42 示例的型号副本。MCP 调试服务的默认地址为 `http://127.0.0.1:3001/mcp`，`debug tools` 列出工具和参数。修改操作和通用调用使用 `--model` 核对本地进程及型号。

### 连接并读取寄存器与内存

```powershell
$Model = Read-Host '正在运行的型号副本目录'
python tools/casio_tool.py debug --model "$Model" tools
python tools/casio_tool.py debug --model "$Model" status
```

确认型号后，暂停并读取入口字节：

```powershell
python tools/casio_tool.py debug --model "$Model" pause
python tools/casio_tool.py debug --model "$Model" registers
python tools/casio_tool.py debug --model "$Model" read 9:2000 16 -o build/live.bin
```

### 命中入口并单步

1. 设置断点并恢复执行：

   ```powershell
   python tools/casio_tool.py debug --model "$Model" breakpoint --address 9:2000
   python tools/casio_tool.py debug --model "$Model" resume
   ```

2. 在计算器 BASIC 中执行 `CALL(598016)`，等待入口断点命中。
3. 单步并读取寄存器：

   ```powershell
   python tools/casio_tool.py debug --model "$Model" step
   python tools/casio_tool.py debug --model "$Model" registers
   ```

4. 清除断点，恢复正常执行：

   ```powershell
   python tools/casio_tool.py debug --model "$Model" breakpoint --clear
   python tools/casio_tool.py debug --model "$Model" resume
   ```

写内存的命令格式为 `debug --model MODEL write ADDRESS DATA.bin`；目标应是自己管理的缓冲区，硬件 Flash 写入仍遵循 NOR 编程流程。通用调用格式为 `debug --model MODEL call TOOL --args JSON`，例如暂停后调用 `write_register`，参数为 `{"name":"r0","value":42}`。

`debug --url` 选择其他本地 MCP 端点。`model start --url` 指定启动检查所期待的端点，模拟器端口另行配置；启动会检查端口占用并返回新 PID，随后用 `debug status` 核对实际服务。

## 改动如何记录

[`firmware/e5800p/project.py`](../firmware/e5800p/project.py) 创建 Firmware 并加载各功能模块。

| 功能 | 模块 |
| --- | --- |
| e.basic 输入、执行、编译、内存和绘图 | `basic.py`、`basic_asm.py`、`memory.py`、`graphics.py` |
| GRAPH、原生公式与数值分析 | `graph_view.py`、`graph_gate.py`、`graph_input.py`、`graph_math.py`、`mcs.py` |
| Add-in 目录、启动器与原生库切换 | `apps.py`、`app_hooks.py` |
| 菜单、ASM/Hex 与指令目录 | `ui.py`、`editing.py`、`instructions.py` |
| 批量改写、journal、关机签名与原生接入 | `batch.py`、`storage.py`、`logo.py`、`hooks.py` |
| 固定入口、区间大小与原始指纹 | `layout.py` |

原生代码使用 PL/e 的寄存器操作，常量表用 Python 数据声明。修改长度时同步调整布局、原始区间指纹和地址引用，然后重新构建：

```powershell
$Original = Read-Host '匹配的原厂 Flash 文件路径'
python -m kits firmware/e5800p/project.py "$Original" -o build/e5800p.bin --map build/e5800p.map.json --listing build/e5800p.asm
```

构建会执行项目模块中的 Python 代码。`build --project` 可指定其他项目；旧生成器和 `generate/--patchset` 流程见 [legacy](../legacy/README.md)。

### 原生挂钩与数据替换

`fw.hook(address, function, expected=原字节, call=True)` 用四字节远调用连接函数；`call=False` 使用远跳转。`fw.patch(address, data, expected=原字节)` 描述等长替换。

构建检查原字节、对齐、段边界、区间重叠和尺寸。挂钩须按调用点要求保存寄存器，处理被替换的指令及返回位置。

输出与输入、源码、点阵或其他输出指向同一文件时报错。指定的输出文件可覆盖已有文件。固件构建会创建输出父目录，其他命令使用已有目录。

### 原厂版本与升级

| 指纹 | 值与用途 |
| --- | --- |
| `ORIGINAL_IMAGE_SHA256` | `c3bd74079d60fd070a8fe0351d000b34f15a23e5bc78153b0c159e639ac712d4`，辨认参考原厂文件 |
| `ORIGINAL_FIRMWARE_SHA256` | `7a3fb0a93857de3fcd17fc146329409b027d755760e49093a3230a767f004567`，用于构建时匹配版本 |

版本指纹计算 `image[:0x4000] + image[0x40000:]` 的 SHA-256，允许原生用户数据区 `[0x4000,0x40000)` 含不同内容。参考原厂的 S0 `[0,0x4000)` 为 FF。

升级以当前保存的镜像为 BASE，通过 `--clean` 指定匹配的原厂参考。用户数据银行及 footer 中校验和以外的字节取自 BASE，其余固件区从参考和项目重建，会覆盖 BASE 固件区中的手工改动。输出哈希随用户数据变化。

### 布局、map 与校验

固件在低 512 KiB 内分配代码。芯片容量和高半区访问条件见 [地址映射](flash_upper_mapping.md)。

`layout.py` 定义固定区间，`tools/flash_layout.py` 提供工具和验证入口常量：

| 区域 | 当前用途 |
| --- | --- |
| S0 | `8:0200–2FFF` 放置已登记的固件函数；选择器 `8:0200`、CALL 桥 `8:0400`、扫描器 `8:0800` 保持固定入口。 |
| journal | `8:3000–3FFF` 保存 Hex 提交与恢复数据。 |
| F 尾部 | `F:3E68–FFDF` 按完整例程排列 e.basic、GRAPH、ASM/Hex、Add-in 及其数据；原生 FUNCTION 表保留至 `F:3E67`。 |
| S4 | `9:0000–FFFF` 由原生程序库或显式初始化后的 Add-in 使用；应用从 `9:0100` 起装载，目录位于银行尾部。 |
| 原生 footer | `F:FFE0–FFFD` 保存启动签名、型号与版本；`F:FFFE` 为校验 word。 |

map 的 `regions` 按 CPU 地址排序，每项含 `name,cpu_start,physical_start,size,reserved_stop,kind`；kind 为 code/data，另记录原生校验字段。公开入口地址固定，私有函数地址和大小见 `layout.py` 及构建 map。

原生校验是物理 `[0x40000,0x7FFFE)` 的无符号字节和模 65536，结果按小端写入 `0x7FFFE`。原生 Flash 诊断在 SUM 通过后会擦除 S0 及其中的扩展；保留扩展的验证流程在擦除调用前返回。

## 测试

在已安装工具链的项目根目录运行单元测试：

```powershell
python -m unittest discover -s tests -v
```

模拟器测试需要[配套模拟器](emulator.md)、已[加载固件](e5800p.md#加载与备份)的完整型号副本，以及匹配的原厂 512 KiB Flash。先执行 OFF 保存并备份整个型号，再启动副本，独占 MCP 端口 3001。测试会复位并改写程序、变量及 Flash S1～S6；失败时用备份恢复。

```powershell
$Model = Read-Host '正在运行的型号副本目录'
$Original = Read-Host '匹配的原厂 512 KiB Flash 路径'
$Out = Read-Host '尚未创建的输出目录（型号目录之外）'
python tools/casio_tool.py verify --case all --model "$Model" --original "$Original" --out "$Out"
```

Windows 下另测 Hex journal 中断恢复，会关闭并重启正在运行的副本：

```powershell
$Exe = Read-Host '当前模拟器的 CasioEmuMsvc.exe 路径'
python tools/casio_tool.py verify --suite power --model "$Model" --exe "$Exe" --out "$Out/power"
```

选项见 `python tools/casio_tool.py verify --help`，可选 case 见 `python tools/basic_smoke.py --help`。CI 配置见 [check.yml](../.github/workflows/check.yml)。
