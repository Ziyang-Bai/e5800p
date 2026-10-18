# CasioEmuMsvc 配套模拟器

已有兼容运行时时，按 [加载与备份](e5800p.md#加载与备份) 启动型号；需要自行构建时，使用下面固定版本和补丁。

仓库中的五个补丁对应上游提交 `2d26202d56e437654296af85c94a9036bb34ad58`。

## 构建模拟器

在 Windows / MinGW-w64 下构建。在项目根目录打开 PowerShell，将 Git、CMake、Ninja、MinGW-w64 和 Python 加入 PATH。字体生成器会准备 `fonttools` 依赖。

### 取得源码并应用补丁

1. 输入源码和构建路径，源码目录须为新目录：

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

运行时需保留同目录的 MCP 插件、`locales`、`roms.db` 和运行库；构建会复制 MCP 插件。接着按 [加载与备份](e5800p.md#加载与备份) 启动型号。

## 补丁作用

| 补丁 | 作用 |
| --- | --- |
| [flash_erase](../patches/emulator/emulator_flash_erase.patch) | 修正低 512 KiB 全部 11 个物理扇区的擦除范围：16/8/8/32 KiB 启动区及后续 64 KiB 扇区。Hex 提交和 BASIC 显式擦除依赖此补丁。 |
| [pram_load](../patches/emulator/emulator_pram_load.patch) | 在外部 SRAM 分配之后执行 `LoadRAMImage()`，使 `pram.dmp` 在启动时载入。 |
| [mingw](../patches/emulator/emulator_mingw.patch) | 按平台选择 Objective-C 源文件和 MCP 编译参数，将 Windows 资源脚本转为 UTF-8。 |
| [debugger](../patches/emulator/emulator_debugger.patch) | 断点按 PC 存储、匹配和删除，支持 Flash 和静态 ROM 列表以外的地址；单步执行 CPU 指令。 |
| [performance](../patches/emulator/emulator_performance.patch) | 调整等待、刷新与纹理复用，见下节。 |

高 512 KiB 的硬件可达性见 [Flash 映射](flash_upper_mapping.md)。

模拟器 Code 窗口的静态反汇编以 ROM 为源。查看 Flash 新代码时，使用工具链的 `debug read` 和 `disasm`，见 [调试](5800p-kits.md#调试)。

## ImGui 运行时性能优化

- 主线程通过 `SDL_WaitEventTimeout` 等待输入或下一帧。桌面前台刷新间隔至少 17 ms，低性能模式 24 ms，Android 40 ms；失去焦点后为 100 ms，录屏时保持正常间隔。
- 复用整机合成纹理，在尺寸、格式或渲染设备变化时重建。隐藏或最小化的主窗口、调试窗口、镜像窗口跳过绘制和提交。
- 屏幕外设继续处理截图、录屏和镜像请求；主窗口最小化后，可见镜像仍能更新和接收按键。
- 模拟 CPU 独立调度，暂停后恢复时不补跑暂停期间的周期。

