# 分支管理声明

为确保代码库变更的可追溯性和协作质量，特制定以下分支管理规则。**所有与本仓库交互的 Agent（包括但不限于 Mimo、Codex、DeepSeek 等）必须遵守。**

---

## 1. 禁止直接修改 `main`

`main` 分支是受保护的主线，任何 Agent **不得**直接在其上修改文件。所有变更必须通过特性分支进行。

## 2. 专属分支

每个 Agent 在开始修改前，必须先切换到自己的专属分支：

| Agent | 分支 |
|---|---|
| Mimo | `mimo` |
| Codex | `codex` |
| DeepSeek | `deepseek` |

> 如需新增 Agent，应在 `BRANCH-POLICY.md` 中补充对应分支，并创建该分支。

## 3. 工作流程

```
① 确定要修改的内容
② 切换到对应分支：git checkout <agent-branch>
③ 修改并提交
④ 推送到远程：git push origin <agent-branch>
⑤ 提出 Pull Request / Merge Request → main
⑥ 经人工批准后方可合并入 main
```

## 4. 合并审批

任何分支在合并到 `main` 之前，**必须**获得项目负责人的明确批准。未经批准的合并将被回滚。

## 5. 分支同步

各 Agent 分支应定期从 `main` 同步（rebase 或 merge），以保持与主线一致，减少合并冲突。

---

*本文件自发布之日起生效。*
