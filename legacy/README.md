# 旧版 e5800p 源码

这里保存迁移到 Python DSL 前的完整实现，可独立构建。当前固件入口为仓库根目录的 `firmware/e5800p/project.py`，开发当前版本请从[主项目](../README.md)开始。

## 内容

- `firmware/e5800p/`：92 个汇编区间及 `patchset.py`。
- `tools/`：旧 Python 生成器、汇编器、CLI 和模拟器验证脚本。
- `assets/ziyang_bai.pbm`：旧版关机点阵。
- `tests/`：旧汇编器、补丁构建与 CLI 测试。
- `requirements.txt`、`LICENSE`：归档依赖与许可。

归档源文件保持迁移前的内容；原厂镜像、完整型号和构建产物在本地另行保存。

## 独立构建

准备 Python 3.10+ 和自行取得的匹配原厂 **512 KiB Flash**。在仓库根目录打开 PowerShell，运行以下命令，并按提示输入实际路径。

```powershell
Set-Location legacy
python -m pip install -r requirements.txt
$base = (Resolve-Path -LiteralPath (Read-Host '原厂 Flash 文件路径')).Path
$out = Read-Host '本地输出目录'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$out = (Resolve-Path -LiteralPath $out).Path
python tools/casio_tool.py build $base -o (Join-Path $out 'e5800p.bin') --map (Join-Path $out 'e5800p.map.json')
```

构建默认使用本归档的 `firmware/e5800p/patchset.py`，输出镜像与区间清单，保留输入中的原生用户数据银行。命令只生成本地文件；部署时另用隔离的完整型号副本。

### 原厂版本匹配

构建用 `image[:0x4000] + image[0x40000:]` 的 SHA-256 识别原厂版本，排除原生用户数据银行。匹配的指纹为：

```text
7a3fb0a93857de3fcd17fc146329409b027d755760e49093a3230a767f004567
```

## 旧生成流程

修改旧 Python 生成器或 PBM 后，先导出新的 patchset，再用它构建。在上面的同一 PowerShell 会话中运行，沿用 `$base`、`$out`；为 patchset 选择一个**待创建的新目录**：

```powershell
$patchset = Read-Host '新 patchset 目录'
python tools/casio_tool.py generate $base -o $patchset
python tools/casio_tool.py build $base --patchset $patchset -o (Join-Path $out 'regenerated.bin')
```

`regenerated.bin` 同样保留输入的原生用户数据银行。

## 归档测试

在 `legacy/` 目录运行：

```powershell
$env:PYTHONPATH = (Resolve-Path tools).Path
python -m unittest discover -s tests -v
```

这些测试使用合成数据；`basic_smoke*.py` 另需兼容模拟器和隔离型号副本。当前语言行为见 [e.basic 参考](../docs/e.basic.md)，当前固件的加载与操作见[固件指南](../docs/e5800p.md)。
