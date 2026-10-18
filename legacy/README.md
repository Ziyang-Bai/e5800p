# 旧版 e5800p 源码

迁移到 PL/e 前的实现，可独立构建。当前版本见 [主项目](../README.md)，入口为 `firmware/e5800p/project.py`。

## 内容

- `firmware/e5800p/`：92 个汇编区间及 `patchset.py`。
- `tools/`：旧 Python 生成器、汇编器、CLI 和模拟器验证脚本。
- `assets/ziyang_bai.pbm`：旧版关机点阵。
- `tests/`：旧汇编器、补丁构建与 CLI 测试。
- `requirements.txt`、`LICENSE`：归档依赖与许可。

## 独立构建

准备 Python 3.10+ 和匹配的原厂 512 KiB Flash。在仓库根目录打开 PowerShell：

```powershell
Set-Location legacy
python -m pip install -r requirements.txt
$base = (Resolve-Path -LiteralPath (Read-Host '原厂 Flash 文件路径')).Path
$out = Read-Host '本地输出目录'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$out = (Resolve-Path -LiteralPath $out).Path
python tools/casio_tool.py build $base -o (Join-Path $out 'e5800p.bin') --map (Join-Path $out 'e5800p.map.json')
```

构建使用归档中的 `firmware/e5800p/patchset.py`，输出镜像与区间清单，保留原生用户数据银行。部署到[完整型号副本](../docs/e5800p.md#加载与备份)中运行。

### 原厂版本匹配

版本指纹为 `image[:0x4000] + image[0x40000:]` 的 SHA-256：

```text
7a3fb0a93857de3fcd17fc146329409b027d755760e49093a3230a767f004567
```

## 旧生成流程

修改生成器或 PBM 后，先生成 patchset，再构建镜像。在同一 PowerShell 窗口中沿用 `$base`、`$out`，为 patchset 选择一个新目录：

```powershell
$patchset = Read-Host '新 patchset 目录'
python tools/casio_tool.py generate $base -o $patchset
python tools/casio_tool.py build $base --patchset $patchset -o (Join-Path $out 'regenerated.bin')
```

## 归档测试

在 `legacy/` 目录运行：

```powershell
$env:PYTHONPATH = (Resolve-Path tools).Path
python -m unittest discover -s tests -v
```

测试使用合成数据；`basic_smoke*.py` 另需兼容模拟器和型号副本。当前语言见 [e.basic 参考](../docs/e.basic.md)，加载方法见[固件指南](../docs/e5800p.md)。
