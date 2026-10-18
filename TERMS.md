# 项目术语

e.basic：CASIO BASIC 扩展规范，定义 PEEK/POKE 等内存操作、机器码调用、内联汇编、图形与底层函数的语法和行为。

e5800p：fx-5800P 修改固件，实现 e.basic、GRAPH、ASM/Hex 编辑器等功能。

PL/e：基于 Python 的固件编程 DSL，由 5800p-kits 编译为 nXu8 机器码。

5800p-kits：随 e5800p 提供的 Python 工具链，用于编译 PL/e、构建和调试程序与固件补丁。
