# fx-5800P 外部 Flash 地址映射与高 512 KiB 验证条件

当前 e5800p、匹配 ROM 和模拟器使用低 512 KiB 窗口：

```text
CPU 8:0000–F:FFFF → Flash 物理偏移 0x00000–0x7FFFF
Flash 物理偏移 = CPU 线性地址 − 0x80000
```

例如 `8:0000 → 0x00000`、`F:FFFF → 0x7FFFF`；`8:4000` 是 SA1 起点。e5800p 构建和部署的完整镜像为 512 KiB，操作见 [加载与备份](e5800p.md#加载与备份)。

MX29LV800CB 容量为 1 MiB，高半区物理地址 `0x80000–0xFFFFF` 对应 SA11–SA18。实体机访问该区需要驱动 A18 等总线信号；该版 fx-5800P 的选通路径尚未板测确认。

## 在独立模拟器副本中实验

按 [加载与备份](e5800p.md#加载与备份) 使用 512 KiB 镜像创建并启动型号副本。

### 观察地址

在独立模拟器源码和型号副本上添加只读日志，构建方法见 [模拟器说明](emulator.md#构建模拟器)。日志记录以下字段：

1. `MMU::ReadCode` 的 `HW_FX_5800P` 分支：输入 `offset` 与实际偏移 `offset & 0x7ffff`。核对 `8:0000` 和 `F:FFFE` 的 16 位代码读取分别使用物理偏移 `0x00000` 和 `0x7FFFE`。
2. `MMU::ReadData`：DSR=`0x10`、偏移 `0x0001` 对应的未映射访问分支。`10:xxxx` 实验限定为读取和日志观察。

日志用于核对软件分支；实体 A18 电平和芯片应答见 [板级测量](#高半区访问的实施前提)。

## 地址证据

### CPU 的代码地址与数据地址

代码地址使用 4 位 CSR。OKI nX-U8/100 Core Instruction Manual §1.2.2.3、§1.3.1（PDF 页 18、24）规定 `CSR:PC` 为 20 位地址，范围 `0:0000–F:FFFF`；`PC` 溢出在当前段内回绕，CSR 保持原值。代码段 `8–F` 合计 8 × 64 KiB。

数据地址使用独立的 8 位 DSR。同手册 §1.2.2.10、§1.3.5（PDF 页 23、29）定义数据段寄存器，例如 `10:0000` 表示数据地址 `0x100000`。代码地址由 CSR:PC 决定，数据地址对应的设备与物理偏移由总线映射决定。§1.3.6（PDF 页 32）说明内存模型由目标器件定义；ML610901B 的外部总线、银行控制和板级连接须按器件资料和实测核对。

### 芯片容量与命令

Macronix MX29LV800CB 规格/引脚（PDF 页 2、6）及扇区表（PDF 页 12，SA0–SA18）给出 x8 容量 1,048,576 字节。高半区 `0x80000–0xFFFFF` 属于 SA11–SA18，每个扇区 64 KiB。

x8 模式的最低字节地址位经 `Q15/A-1`，因此软件 20 位字节地址的 bit19（`0x80000`）对应芯片 A18；SA11 从 A18=1 开始。x16 模式则按 word 地址解释。

命令表 3（PDF 页 23）涵盖读取、复位、ID、编程、扇区/整片擦除、CFI、暂停和恢复。AMD 解锁序列启动相应芯片操作，高半区选择仍需系统总线或外部逻辑驱动高地址引脚。

### ROM 的擦除与编程入口

匹配 Mask ROM 的大小和 SHA-256 见 [ROM 小字体参考](ROM_small_font.md)。下列入口用于现有低半区擦写：

| 入口或数据 | ROM 行为 |
| --- | --- |
| 扇区表 `0x096A`，擦除入口 `0x4EF4` | `0x4F04` 比较扇区号与 `0x0B`，`>=11` 返回；`0x4F10/14` 读取 `0x096A+4*n` 的偏移/段；`0x4F48` 对段号 OR `8`，再发送 `30` 扇区擦除命令。支持 SA0–SA10。 |
| 编程命令 `0x4E86–0x4EBE` | 发送 `AA@8:0AAA`、`55@8:0555`、`A0@8:0AAA`，目标写入前将目标段 OR `8`，在段 `8–F` 发出命令。 |

扇区表数据可能被反汇编为 MOV 等指令，应结合原始字节和查表代码解释。

## 模拟器所实现的范围

以下链接固定于 CasioEmuMsvc 上游提交 `2d26202d56e437654296af85c94a9036bb34ad58`：

| 源码 | 实现范围 |
| --- | --- |
| [`Chipset.cpp` 装载检查](https://github.com/telecomadm1145/CasioEmuMsvc/blob/2d26202d56e437654296af85c94a9036bb34ad58/CasioEmuMsvc/src/Chipset/Chipset.cpp#L785-L800) | FX-5800P 镜像须恰好为 `0x80000` 字节。 |
| [`5800Flash.cpp`](https://github.com/telecomadm1145/CasioEmuMsvc/blob/2d26202d56e437654296af85c94a9036bb34ad58/CasioEmuMsvc/src/Peripheral/5800Flash.cpp#L26-L88) | 注册 CPU 地址 `0x80000` 起、长度 `0x80000` 的区域，读写偏移为 `offset & 0x7ffff`。 |
| [`MMU.cpp` 的 ReadCode/ReadData/WriteData](https://github.com/telecomadm1145/CasioEmuMsvc/blob/2d26202d56e437654296af85c94a9036bb34ad58/CasioEmuMsvc/src/Chipset/MMU.cpp#L65-L225) | 代码段 `>=8` 时读取 `flash_data[offset & 0x7ffff]`；数据地址取 DSR 后查段表。 |
| [`Chipset.cpp` 的 FX-5800P 段表](https://github.com/telecomadm1145/CasioEmuMsvc/blob/2d26202d56e437654296af85c94a9036bb34ad58/CasioEmuMsvc/src/Chipset/Chipset.cpp#L155-L171) | 建立 `0,1,4,8..15` 段。 |

该版本对数据地址 `0x100000` 专门返回 `FF`，对 `10:0001` 等地址按未映射访问处理。

### 低半区擦除补丁

仓库的 [emulator_flash_erase.patch](../patches/emulator/emulator_flash_erase.patch) 补齐低 512 KiB 的 11 个扇区并修正整扇区长度。测试完整扇区行为前，按 [构建模拟器](emulator.md#构建模拟器) 应用五个补丁并构建。实体擦写时序、边界和耐久性仍需硬件实验。

## 高半区访问的实施前提

高半区研究需要该版 fx-5800P PCB/ML610901B 的官方外部总线资料或板级原理图；也可在已完整备份且具备恢复条件的实体机上取得只读测量。先确认地址映射，再设计编程和擦除。

1. 标明 MX29LV800CB 的 `BYTE#`、`A18`、`CE#` 分别连接哪个 MCU 引脚或门电路。
2. 核对访问 `8:0000–F:FFFF` 时 A18 的电平，查找可由软件控制的页选通路。
3. 用逻辑分析仪／示波器同步记录 A18、CE#、WE# 与 CPU 对已知段、候选 SFR/DSR 地址的访问。
4. 用高低半区各自的已知差异数据核对地址独立性，并确认应答来自目标 Flash。单独的 `FF` 读值应结合片选和总线响应解释。
