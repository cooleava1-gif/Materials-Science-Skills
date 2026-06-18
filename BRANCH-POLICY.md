# 分支管理声明

为确保代码库变更的可追溯性和协作质量，特制定以下分支管理规则。**所有与本仓库交互的 Agent 必须遵守。**

---

## 1. 权威分支

`main` 是唯一权威分支（source-of-truth）。任何维护工作都应从最新的 `origin/main` 开始。

- 每次开始任务前执行：
  ```
  git fetch origin
  git checkout main
  git pull --ff-only origin main
  ```
- `git status --short --branch` 必须处于干净状态；若存在未提交改动，先检查并保留无关的用户或 Agent 工作。

## 2. 受保护分支

`main` 是受保护分支，**任何 → `main` 的合并必须获得项目负责人（人类）的明确批准**。未经批准的合并将被回滚。

## 3. Agent 分支规则

- `gemini` 与 `mimo` 仅作为审计/对比分支使用，除非维护者明确提升某项变更，否则不得视为权威来源。
- `deepseek`、`codex` 等实验分支已退役，**禁止重新创建**。
- 不要直接在 `main` 上累积本地改动后强制推送；所有变更通过特性分支发起，并经人工审批后合并。

## 4. 跨分支审查

DeepSeek (Reasonix) 可以审查和批准 `mimo` 等审计分支上的变更，但不允许直接修改这些分支。审查通过后，由对应 Agent 自行合并或经人工批准后代为合并。

## 5. 分支同步

各审计/特性分支应定期从 `main` 同步（rebase 或 merge），以保持与主线一致，减少合并冲突。

## 6. 相关文档

完整操作规则另见：

- `AGENTS.md`：Agent 交接与约定
- `docs/architecture/maintenance-handoff.md`：维护者接手指南与验证矩阵

---

*本文件自发布之日起生效。*
