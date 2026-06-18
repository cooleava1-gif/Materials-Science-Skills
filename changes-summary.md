# 仓库结构精简改动清单

> 生成时间：2026-06-18  
> 目标：`main` 只保留 `plugins/materials-skills/` 作为唯一 Codex 插件包；仓库根目录不再保留重复的 `skills/`、`_shared/`、`mcp-server/` 或第二套插件描述。

## 改动概览

| 类型 | 数量 | 说明 |
|---|---:|---|
| 修改 | 71 | 脚本、文档、测试和插件内说明改为插件布局 |
| 删除 | 1336 | 删除顶层重复目录、旧 MCP 根配置、根级 `.claude-plugin/plugin.json` |
| 重命名 | 1 | 将 MCP `requirements.txt` 保留到插件内 MCP 目录 |

`changes-summary.md` 是本次审查说明文件，未计入上表。

## 保留的唯一插件包

- `plugins/materials-skills/.codex-plugin/plugin.json`
- `plugins/materials-skills/.mcp.json`
- `plugins/materials-skills/skills/`
- `plugins/materials-skills/skills/_shared/`
- `plugins/materials-skills/_shared/`

仓库根目录已不再存在这些重复入口：

- `skills/`
- `_shared/`
- `mcp-server/`
- `.mcp.json`
- `.claude-plugin/`

## 关键修复

- `scripts/skill_manifest.py` 默认发现路径改为 `plugins/materials-skills/skills/`。
- `scripts/run_release_checks.py`、`scripts/check_skill_architecture.py`、`scripts/validate_*`、`scripts/run_*tests.py` 等发布/校验脚本均以插件内路径为准。
- `scripts/install.ps1` 从 `plugins/materials-skills/skills/materials-*` 安装技能，同时复制：
  - `plugins/materials-skills/skills/_shared` 到 `$CODEX_HOME/skills/_shared`
  - `plugins/materials-skills/_shared` 到 `$CODEX_HOME/_shared`
- `plugins/materials-skills/.mcp.json` 从插件根解析，`cwd` 为 `.`，MCP entrypoint 为 `./skills/materials-citation/mcp/academic_search/server.py`。
- 根级 `.claude-plugin/plugin.json` 已删除，避免出现第二个插件包入口。
- `install.md` 与 `RELEASE_NOTES.md` 的手动安装说明已同步插件布局和两个 `_shared` 复制步骤。
- 插件内测试不再依赖 `REPO_ROOT / "skills"`；所有路径从各自技能目录或插件根推导。
- `scripts/generate_narrative.py` 帮助文本已更新为插件内默认输出路径。

## 删除内容

| 路径 | 说明 |
|---|---|
| `skills/` | 顶层技能镜像，已由 `plugins/materials-skills/skills/` 取代 |
| `_shared/` | 顶层共享资源镜像，已由 `plugins/materials-skills/_shared/` 取代 |
| `mcp-server/` | 顶层 MCP 服务端镜像，已由插件内 `materials-citation/mcp/academic_search/` 取代 |
| `.mcp.json` | 指向旧顶层 MCP 路径的根级配置 |
| `.claude-plugin/plugin.json` | 根级第二插件描述，已由插件包内 `.codex-plugin/plugin.json` 取代 |

## 重命名

| 原路径 | 新路径 |
|---|---|
| `mcp-server/materials-academic-search/requirements.txt` | `plugins/materials-skills/skills/materials-citation/mcp/academic_search/requirements.txt` |

## 验证结果

以下命令已通过：

```powershell
python -m py_compile scripts/check_skill_architecture.py scripts/run_release_checks.py scripts/validate_manifest.py scripts/validate_registry.py scripts/validate_handoffs.py scripts/run_behavioral_tests.py scripts/run_pressure_tests.py scripts/generate_narrative.py scripts/skill_manifest.py
python scripts/check_skill_architecture.py --json
python scripts/run_release_checks.py --json
python -m unittest tests.test_release_architecture_dynamic -v
python -m unittest discover -s tests -p "test_*.py" -v
```

根测试结果：`Ran 102 tests ... OK`。

补充插件局部测试也已通过：

```powershell
python -m unittest discover -s plugins/materials-skills/skills/materials-research/tests -p "test_*.py" -v
python -m unittest discover -s plugins/materials-skills/skills/materials-reader/tests -p "test_*.py" -v
python -m unittest discover -s plugins/materials-skills/skills/materials-doe/tests -p "test_*.py" -v
python -m unittest discover -s plugins/materials-skills/skills/materials-figure/tests -p "test_*.py" -v
```

物理目录检查：

```powershell
Get-ChildItem -LiteralPath . -Force | Where-Object { $_.Name -in @('skills','_shared','mcp-server','.claude-plugin') }
```

结果无输出，表示这些顶层重复目录不存在。

## 远端同步状态

- `git fetch origin main` 成功。
- `git pull --ff-only` 返回 `Already up to date.`。
- 当前本地 `main` 相对 `origin/main` 为 ahead 状态，`origin/main` 是当前 `HEAD` 的祖先。
