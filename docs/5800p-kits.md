# 5800p-kits 工具链

先编译仓库中的 [Python 示例](#python-固件-dsl)，再修改函数并查看生成的机器码。

本指南对应当前仓库的 `5800p-kits 0.1.0`。需要 Python 3.10+，并已按 [README](../README.md#从原厂-flash-构建) 安装工具链、生成 `build/e5800p.bin`。命令在项目根目录的 PowerShell 执行。

- [Python 固件 DSL](#python-固件-dsl)：函数、内存、ROM 调用和原生寄存器。
- [汇编与镜像工具](#python-工具链)：汇编、反汇编、写入镜像。
- [调试](#调试)：断点、单步与内存读回。
- [维护固件](#改动如何记录)：模块分工、布局和构建规则。

## Python 固件 DSL

DSL（领域专用语言）用 Python 描述计算器程序。电脑上的 Python 负责导入模块、读取资源和声明固件；`@fw.function` 的函数体编译为 nXu8 机器码，在计算器上执行。源码保存为 `.py` 文件，编译错误指向原文件和行号。

### 编译并调用示例

[`examples/python_demo.py`](../examples/python_demo.py) 是完整示例：`main` 调用 `clear_screen` 清除 LCD 正文，再通过 `add_two(40)` 返回 42。

示例将 `8:4000–5FFF` 交给代码使用，会覆盖实际放置函数的位置。先备份该区域，在独立型号副本中试运行。

1. 编译示例，同时输出便于检查的汇编：

   ```powershell
   python -m kits examples/python_demo.py build/e5800p.bin --listing build/python-demo.asm
   ```

2. 按 [加载与备份](e5800p.md#加载与备份) 部署生成的 `build/python-demo.bin`。
3. 在该副本的 BASIC 中运行：

   ```text
   CALL(540672)→A
   ```

`540672` 是入口 `8:4000` 的十进制地址。调用清除正文像素、保留状态行，变量 A 得到 **42**。编辑示例后重新编译和部署，即可使用新代码。

普通 Python 脚本也可用 `fw.build(original=..., output=...)` 构建，或用 `fw.link()` 取得函数地址与代码块。原厂 Flash 可直接作为 DSL 构建输入；通过 BASIC 调用需要 e5800p 提供的 CALL，其他镜像使用自己的调用入口或调试器。

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

文件操作、容器和异常处理由构建层 Python 执行。装饰函数体使用上述受支持语法，超出范围时编译器按源位置报错。

### 调用约定与 ROM

普通函数最多四个整数参数，依次放在 **ER0/ER2/ER4/ER6**，结果在 **ER0**。函数保存 R4–R15 和 SP；PSW、EA 可改变。临时值、局部变量和嵌套调用使用栈，程序须为自身和原生系统留下足够空间。

示例中的 `refresh = ROM(0x043BE, result=None)` 声明 ROM 刷新入口，函数内调用 `refresh()`。`ROM` 的参数寄存器支持 R0–R7、ER0/ER2/ER4/ER6，最多四个且各自占用独立字节；`result` 指定返回寄存器。

调用器保存使用中的 R4–R15。目标 ROM 对内存、字体、显示状态和指针的要求仍按其 ABI（调用约定）处理。

### 原生寄存器 DSL

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

**寄存器与访存：**

- `cpu.r0`～`r15`、`er0/2/…/14`、`xr0/4/8/12`、`qr0/8` 对应物理寄存器；`sp`、`ea`、`lr`、`pc`、`psw` 等按指令支持的组合使用。
- 赋值生成 MOV，增量与位赋值生成对应操作。`compare` 更新标志，`add_carry/sub_carry` 使用进位；`multiply/divide` 保持原指令的结果与副作用。有符号立即数写实际值，如 `-1`。
- `cpu.mem8/16/32/64[...]` 指定宽度。立即段、寄存器段和复用 DSR 分别写作 `cpu.mem8[4, cpu.er2]`、`cpu.mem8[cpu.r10, cpu.er8]`、`cpu.mem8[cpu.dsr, cpu.er2]`；单下标按原生段状态访存。
- 位移写 `cpu.er14 + 4`；保留零位移编码用 `cpu.offset(cpu.er14, 0)`。EA 自增用 `cpu.post(cpu.ea)`，有效地址计算用 `cpu.ea = cpu.address(...)`。

**控制流与数据：**

- `cpu.label('loop')` 定义符号；`call/jump/branch` 分别调用、跳转和短跳转。整数目标为完整 CPU 地址，字符串目标为符号。
- `if cpu.eq: cpu.branch('done')` 生成条件短跳转。支持 `eq/ne/lt/ge/gt/le` 和有符号 `lts/ges/gts/les`；一般 `if/else`、`while`、`break/continue` 也可使用标志，循环体负责更新标志。
- 显式 `push/pop` 保存现场，以 `cpu.ret()`、`return` 或 `cpu.pop(cpu.pc)` 返回；编译器保留显式栈和返回行为。
- 常量表用 `fw.data(name, bytes, address=..., labels={名称:偏移})`，内嵌数据用 `cpu.data`。

普通函数通过 `ROM(address, args=..., result=...)` 声明原生入口后调用；直接把原生函数作为普通函数调用会报编译错误。

## Python 工具链

`tools/casio_tool.py` 处理源码、镜像和模拟器。地址参数接受十进制、`0x` 十六进制或十六进制 `段:偏移`。

### 汇编并写入镜像

[`examples/return42.asm`](../examples/return42.asm) 用 `PUSH LR → CALL add_two → POP PC` 返回 42。示例入口为 **9:2000（0x92000，598016）**，该银行由原生 Built-in Prog/YAMAYO 程序库使用。先备份并确认目标范围可供覆盖，在独立型号副本中试验。

以下命令使用已经构建的 `build/e5800p.bin`，依次执行：

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

先 build 后 patch：build 重建固件区；patch 按物理偏移或 `CPU地址−image-base` 替换字节。`--native-checksum` 用于完整 512 KiB 镜像。已有镜像单独修正校验时可运行：

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

先启动已部署返回 42 示例的型号副本。MCP 是模拟器提供的调试服务，默认地址为 `http://127.0.0.1:3001/mcp`。修改操作和通用调用使用 `--model` 核对本地进程及型号。

### 连接并读取现场

```powershell
$Model = Read-Host '正在运行的型号副本目录'
python tools/casio_tool.py debug --model "$Model" tools
python tools/casio_tool.py debug --model "$Model" status
```

核对服务器确实加载该副本后，暂停并保存入口字节：

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

`tools` 返回当前服务器的工具名、参数和必填项；调试能力以该 schema（接口定义）为准。CLI 错误返回非零状态。还可使用 `keys`、`reset`、`pause/resume/step`。

写内存的命令格式为 `debug --model MODEL write ADDRESS DATA.bin`；目标应是自己管理的缓冲区，硬件 Flash 写入仍遵循 NOR 编程流程。通用调用格式为 `debug --model MODEL call TOOL --args JSON`，例如暂停后调用 `write_register`，参数为 `{"name":"r0","value":42}`。

`debug --url` 选择其他本地 MCP 端点。`model start --url` 指定启动检查所期待的端点，模拟器端口另行配置；启动会检查端口占用并返回新 PID，随后用 `debug status` 核对实际服务。

## 改动如何记录

当前固件由 [`firmware/e5800p/project.py`](../firmware/e5800p/project.py) 声明一个 Firmware，再按功能加载模块。

| 功能 | 模块 |
| --- | --- |
| e.basic 输入、执行、编译、内存和绘图 | `basic.py`、`basic_asm.py`、`memory.py`、`graphics.py` |
| TABLE、菜单、ASM/Hex 与指令目录 | `graph.py`、`ui.py`、`editing.py`、`instructions.py` |
| 批量改写、journal、关机签名与原生接入 | `batch.py`、`storage.py`、`logo.py`、`hooks.py` |
| 固定入口、区间大小与原始指纹 | `layout.py` |

原生代码使用寄存器 DSL，常量表使用 Python 数据声明，共 81 个代码区和 11 个数据区。修改长度时同步调整布局、原始区间指纹和地址引用。重新构建并查看汇编清单：

```powershell
$Original = Read-Host '匹配的原厂 Flash 文件路径'
python -m kits firmware/e5800p/project.py "$Original" -o build/e5800p.bin --map build/e5800p.map.json --listing build/e5800p.asm
```

构建会执行项目声明和资源读取，使用可信的 Python 源码。指定其他项目时，CLI 的 `build --project` 接受该文件路径。旧 `generate/--patchset` 流程及生成器见 [legacy](../legacy/README.md)。

### 原生挂钩与数据替换

`fw.hook(address, function, expected=原字节, call=True)` 用四字节远调用连接函数；`call=False` 使用远跳转。`fw.patch(address, data, expected=原字节)` 描述等长替换。

构建先核对原字节，再检查对齐、段边界、重叠和固定区间尺寸。挂钩的寄存器、原指令续接及现场要求由具体调用点决定。输出与输入、源码、点阵或其他输出路径冲突时会报错；显式输出可以替换旧产物。构建自动创建输出父目录，其他命令使用已存在的目录。

### 原厂版本与升级

| 指纹 | 值与用途 |
| --- | --- |
| `ORIGINAL_IMAGE_SHA256` | `c3bd74079d60fd070a8fe0351d000b34f15a23e5bc78153b0c159e639ac712d4`，辨认参考原厂文件 |
| `ORIGINAL_FIRMWARE_SHA256` | `7a3fb0a93857de3fcd17fc146329409b027d755760e49093a3230a767f004567`，用于构建时匹配版本 |

版本指纹计算 `image[:0x4000] + image[0x40000:]` 的 SHA-256，允许原生用户数据区 `[0x4000,0x40000)` 含不同内容。参考原厂的 S0 `[0,0x4000)` 为 FF。

升级使用当前持久化镜像作为 BASE，并通过 `--clean` 指定匹配原厂参考。原生用户数据银行及 footer 中校验和以外的字节取自 BASE；其余固件区从参考与项目重建，因此 BASE 固件区里的其他改动会被替换。完整输出哈希随用户数据变化，记录时同时保存镜像、map 和验证结果。

### 布局、map 与校验

Flash 器件标称 1 MiB，当前已证实的 CPU/ROM 和模拟器映射及擦写范围是低 512 KiB；固件在此范围分配。高半区的板级条件见 [地址映射](flash_upper_mapping.md)。

`layout.py` 定义固定区间，`tools/flash_layout.py` 提供工具和验证入口常量：

| 区域 | 当前用途 |
| --- | --- |
| S0 | 选择器 `8:0200`、BASIC CALL 桥 `8:0400`、扫描器 `8:0800`、journal `8:3000–3FFF` |
| 指令目录 | 记录 `8:113C–17FF`，名称 `F:9100–93FF`，ISA 菜单从 `F:7E68` 起 |
| BASIC | 接入、Flash、汇编、内存和图形使用 `F:3E68–7E67`、`F:9530–D12F`；原生 FUNCTION 表保留至 `F:3E67` |
| 编辑器 | 地址输入从 `8:25C6` 起，Hex、程序控制、Disas 和批量写入占已登记的 F 尾部/S0 区间 |
| 原生 footer | `F:FFE0–FFFD` 保存启动签名、型号与版本；`F:FFFE` 为校验 word |

map 的 `regions` 按 CPU 地址排序，每项含 `name,cpu_start,physical_start,size,reserved_stop,kind`；kind 为 code/data，另记录原生校验字段。当前迁移保持 92 个原区间的大小与入口，历史生成器的精简预算保存在 legacy。

原生校验是物理 `[0x40000,0x7FFFE)` 的无符号字节和模 65536，结果按小端写入 `0x7FFFE`。**原生 Flash 诊断在 SUM 通过后会擦除 S0，破坏其中的扩展。** 保留扩展的受控验证在擦除调用前返回。

### 项目文件

| 路径 | 内容 |
| --- | --- |
| `tools/`、`firmware/e5800p/` | 工具链与当前 Python 固件 |
| `examples/`、`tests/` | 示例与合成数据单元测试 |
| `docs/`、`TERMS.md` | 使用、参考和[项目术语](../TERMS.md) |
| `legacy/`、`patches/emulator/` | 旧版独立归档与模拟器补丁 |
| `.local/`、`build/` | Git 忽略的本地输入、模型、证据与构建产物 |

完成修改后，按 [验证方法](verification.md) 检查工具链和实际型号。
