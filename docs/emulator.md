# CasioEmuMsvc 配套模拟器

已有兼容运行时时，按 [加载与备份](e5800p.md#加载与备份) 启动型号；需要自行构建时，使用下面固定版本和补丁。

e5800p 沿用 SDL/ImGui 界面，通过 MCP 调试服务连接 Python 工具链。仓库中的五个补丁对应上游提交 `2d26202d56e437654296af85c94a9036bb34ad58`。

## 构建模拟器

以下命令适用于 **Windows / MinGW-w64**，从项目根目录的同一个 PowerShell 窗口执行。先将 Git、CMake、Ninja、MinGW-w64 和 Python 加入 PATH。字体生成器会准备 `fonttools` 依赖。

源码、构建目录和型号均放在持久路径，便于后续复用。源码目录使用待创建的新目录。

### 取得源码并应用补丁

1. 输入源码和构建路径：

   ```powershell
   $Patches = Join-Path (Get-Location).Path 'patches/emulator'
   $EmuSource = Read-Host '新的模拟器源码目录'
   $EmuBuild = Read-Host '模拟器构建目录'
   ```

2. 克隆上游：

   ```powershell
   git clone --filter=blob:none --no-checkout https://github.com/telecomadm1145/CasioEmuMsvc.git "$EmuSource"
   ```

3. 切换到配套版本：

   ```powershell
   git -C "$EmuSource" checkout --detach 2d26202d56e437654296af85c94a9036bb34ad58
   ```

4. 取得子模块：

   ```powershell
   git -C "$EmuSource" submodule update --init --recursive --depth 1
   ```

5. 应用补丁：

   ```powershell
   git -C "$EmuSource" apply "$Patches/emulator_flash_erase.patch" "$Patches/emulator_pram_load.patch" "$Patches/emulator_mingw.patch" "$Patches/emulator_debugger.patch" "$Patches/emulator_performance.patch"
   ```

### 编译

依次执行配置、构建和运行库复制；每条成功后继续下一条。

```powershell
cmake -S "$EmuSource" -B "$EmuBuild" -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_EXECUTABLE=ON -DBUILD_MCP_PLUGIN=ON -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSENTRY_BACKEND=none -DSENTRY_TRANSPORT=none
```

```powershell
cmake --build "$EmuBuild" --target CasioEmuMsvc CasioEmuMsvcMcpPlugin --parallel 8
```

```powershell
$Runtime = Join-Path $EmuBuild 'CasioEmuMsvc'
$ToolBin = Split-Path (Get-Command g++).Source
foreach ($Dll in 'libgcc_s_seh-1.dll','libstdc++-6.dll','libwinpthread-1.dll') {
    Copy-Item (Join-Path $ToolBin $Dll) $Runtime
}
$Exe = Join-Path $Runtime 'CasioEmuMsvc.exe'
```

`$Exe` 指向构建产物。保留旁边的 MCP 插件、`locales`、`roms.db` 和运行库；MCP 插件由构建目标复制。接着按 [加载与备份](e5800p.md#加载与备份) 准备并启动独立型号。

## 补丁作用

| 补丁 | 作用 |
| --- | --- |
| [flash_erase](../patches/emulator/emulator_flash_erase.patch) | 覆盖低 512 KiB 的全部 11 个物理扇区：16/8/8/32 KiB 启动区及后续 64 KiB 扇区，擦除完整长度。Hex 提交和 BASIC 显式擦除依赖此行为。 |
| [pram_load](../patches/emulator/emulator_pram_load.patch) | 在外部 SRAM 分配之后执行 `LoadRAMImage()`，使 `pram.dmp` 在启动时载入。 |
| [mingw](../patches/emulator/emulator_mingw.patch) | 按平台选择 Objective-C 源文件和 MCP 编译参数，将 Windows 资源脚本转为 UTF-8。 |
| [debugger](../patches/emulator/emulator_debugger.patch) | 按实际 PC 存储、匹配和删除断点，支持 Flash 新代码及静态 ROM 列表以外的地址；单步仍执行真实 CPU 指令。 |
| [performance](../patches/emulator/emulator_performance.patch) | 调整等待、刷新与纹理复用，具体机制和测量见下节。 |

原版擦除实现漏掉部分扇区，部分长度少一字节；补丁补齐当前工具链使用的范围。高 512 KiB 的硬件可达性见 [Flash 映射](flash_upper_mapping.md)。

模拟器 Code 窗口的静态反汇编以 ROM 为源。查看 Flash 新代码时，使用工具链的 `debug read` 和 `disasm`，见 [调试](5800p-kits.md#调试)。

## ImGui 运行时性能优化

性能补丁保留 SDL/ImGui 界面和 Python/MCP 接口：

- 主线程通过 `SDL_WaitEventTimeout` 等待输入或下一帧。桌面前台刷新间隔至少 17 ms，低性能模式 24 ms，Android 40 ms；失去焦点后为 100 ms，录屏时保持正常间隔。
- 复用整机合成纹理，在尺寸、格式或渲染设备变化时重建。隐藏或最小化的主窗口、调试窗口、镜像窗口跳过绘制和提交。
- 屏幕外设继续处理截图、录屏和镜像请求；主窗口最小化后，可见镜像仍能更新和接收按键。
- 模拟 CPU 独立调度。暂停时消费并丢弃当前时间片的周期额度，恢复时保持原时钟频率。

### 历史测量

下表来自此前 Windows x64 二进制，使用 OpenGL、相同 fx-5800P 型号，同时打开计算器与调试窗口。CPU 按整机 6 个逻辑处理器归一化；GPU 取进程最忙引擎，各状态采样 4 次取均值。最小化时模拟 CPU 仍在运行。

| 状态 | 优化前 CPU | 优化后 CPU | 优化前 GPU | 优化后 GPU |
| --- | ---: | ---: | ---: | ---: |
| 前台运行 | 5.93% | 4.82% | 23.25% | 17.75% |
| 前台暂停 | 3.54% | 1.18% | 24.00% | 18.50% |
| 全部最小化 | 5.08% | 3.03% | 5.00% | 0.00% |

结果随机器和窗口大小变化；新构建的性能需单独测量。

同一历史运行记录覆盖键盘输入、TABLE 水平线、Hex 连续翻页/GOTO/修改、OFF 持久化、Flash 断点和单步、最小化期间 CALL 返回 42、独立镜像输入、隐藏窗口截图/录屏和正常退出。其他平台及设备重置恢复仍需实测，原有 `Gui/hex.hpp` 编译警告保留。完整型号、运行时和私有测量记录保存在本地。
