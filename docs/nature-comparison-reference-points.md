# nature-skills 借鉴点总结

> 基于对 `nature-skills-main` 参考项目的完整代码审查，对比 Materials-Science-Skills 当前状态，提炼可借鉴的设计模式、架构思路和工程实践。

---

## 一、架构模式

### 1.1 Static/Dynamic Router 模式已对齐，但 manifest 规范性有差距

nature-skills 的每个 Router-style skill 都严格遵守同一套五步协议：

1. Load manifest + always_load
2. Detect axes
3. Load matching fragments (只加载命中的)
4. Build using loaded material (按优先级顺序)
5. Reach for references only when needed

**借鉴点**：materials-skills 已采用此模式（如 `materials-research`、`materials-writing`），但部分 skill 的 manifest 规范性不足。nature-skills 的 manifest 中 `always_load` 明确区分了 "shared core"（`../_shared/core/`）和 "skill-local core"（`static/core/`），且每个 skill 都在 manifest 注释中标注了该分类。

**参考文件**：
- `nature-polishing/manifest.yaml` L7-L16 — 明确区分 `# Shared layer` 和 `# Skill-local core`
- `nature-figure/manifest.yaml` L11-L13 — 注释 `# Skill-local core (figure does not use the prose-oriented _shared layer)`

### 1.2 "Why this split" 自解释尾段

nature-skills 每个 Router-style SKILL.md 末尾都有一段 "Why this split" 说明，解释为什么采用静态/动态分离架构，并声明 "This structure mirrors `nature-xxx`, `nature-yyy`" 形成跨 skill 的结构一致性声明。

**借鉴点**：materials-skills 的 SKILL.md 缺少这个自解释段落。对于新贡献者或 AI agent 理解架构意图很有价值。

**参考文件**：
- `nature-figure/SKILL.md` L55-L60
- `nature-polishing/SKILL.md` L70-L73
- `nature-reader/SKILL.md` L64-L69

---

## 二、写作/论证工作流

### 2.1 Proposal-first 状态机 (nature-proposal-writer)

nature-proposal-writer 是 nature-skills 中最复杂的 skill，实现了完整的 proposal-first 写作状态机：

- **三模式分派**：compose / revise / hybrid，按输入类型自动路由
- **五份 foundation 文件**：`00_scope.md` → `01_research_canon.md` → `02_evidence_table.md` → `03_argument_map.md` → `04_section_contracts.md` → `05_style_guide.md`
- **项目结构**：`state.json` 追踪 mode/round/scores/technical_debts
- **四层 QA Pipeline**：Gate 2 (content expert) → Gate 1 (language) → Gate 3 (auto-validation) → Gate 4 (score threshold)

**借鉴点**：materials-skills 的 `materials-writing` 已有 content-first-qa-pipeline.md，但缺少 foundation 文件体系、state.json 状态追踪、以及显式的模式分派（compose/revise/hybrid）。nature-proposal-writer 的「证据先于文字、论证先于章节、契约先于段落」原则可以直接借鉴。

**参考文件**：
- `nature-proposal-writer/SKILL.md` — 完整架构
- `nature-proposal-writer/templates/` — 8 个模板文件
- `nature-proposal-writer/references/evaluation-rubric.md` — 8 维 × 4 锚点评分
- `nature-proposal-writer/references/stopping-rules.md` — 停止条件

### 2.2 停止规则 (Stopping Rules)

nature-proposal-writer 有显式的停止规则，而非无限迭代：

```
max 3 revision rounds reached
two consecutive score improvements < 0.5
evidence needed for a key claim is missing
specialist conflict cannot be honestly resolved
The user's target for the current deliverable is reached
```

**借鉴点**：materials-skills 的 content-first-qa-pipeline.md 提到了 "不超过 3 轮"，但没有系统化的停止条件。建议在每个带迭代的 skill 中引入停止规则。

**参考文件**：`nature-proposal-writer/references/stopping-rules.md`

### 2.3 评分量规 (Evaluation Rubric)

nature-proposal-writer 的评分体系非常精细：
- 8 个维度，每维度 0-10 分
- 每维度 4 个锚点（3/5/7/9 分），每个锚点有具体描述
- 每个维度有 "Common fix" 或 "Red flags"
- 分层阈值：< 6.0 不可交付 / 6.0-7.0 内部草稿 / 7.0-8.0 可给导师看 / > 8.0 正式打磨
- 阶段阈值：foundation_score > 7.5 / section_score > 6.5 / proposal_score > 7.0 / > 8.0

**借鉴点**：materials-skills 的 content-first-qa-pipeline.md 有阈值但缺锚点描述。可借鉴 nature-proposal-writer 的锚点方式，为每个维度提供 3-4 个具体锚点，让评分有据可依。

**参考文件**：`nature-proposal-writer/references/evaluation-rubric.md`

---

## 三、文献管线

### 3.1 文献管线作为完整产品 (nature-literature-pipeline)

nature-literature-pipeline 不是简单的"查文献"skill，而是一个完整的自动化产品：

- **五阶段 Pipeline**：Search → Coarse Filter → Fine Read → Deliver → Archive
- **六维评分系统**：Topic Match ×35 + Methodological Value ×20 + Journal Quality ×15 + Network Relevance ×10 + Applied Value ×10 + Archival Value ×10
- **评分规则**：每维度有上限，总分必须重新计算，Topic Match < 10 自动淘汰
- **内置安全机制**：分数验证、三重去重（DOI/arXiv ID/OpenAlex ID）、优雅降级（Semantic Scholar 挂了自动切换）、只读归档
- **Cron 驱动**：支持本地 cron 定时任务、推送消息格式化、多平台投递（飞书/Telegram）
- **双层架构**：Engine 层（评分/分类/笔记模板/缺口分析）+ Application 层（cron/推送/归档）

**借鉴点**：用户已在 `codex/nature-comparison-upgrade` 分支上创建了 `materials-literature-pipeline`，结构与 nature-literature-pipeline 对齐。但 nature 版本的评分系统更精细（六维加权 + 门控规则），materials 版本可以进一步增强评分维度的描述和验证逻辑。

**参考文件**：
- `nature-literature-pipeline/SKILL.md` — 完整流水线架构
- `nature-literature-pipeline/references/scoring-system.md` — 六维评分系统
- `nature-literature-pipeline/templates/literature-push-template.md` — 推送格式模板

### 3.2 得分校准 (Score Calibration)

nature-literature-pipeline 有明确的校准指南：
- 2-3 轮后检查分数分布
- 如果 top papers 持续 90+，量规太松
- 如果没有 paper 突破 60，关键词太窄或领域稀疏
- 根据用户反馈调整权重

**借鉴点**：materials-literature-pipeline 的 `static/core/scoring.md` 可以加入类似的校准指南。

---

## 四、实验记录

### 4.1 结构化实验日志系统 (nature-experiment-log)

nature-experiment-log 是一个完整的实验记录系统，而非简单的模板：

- **实验 ID 规则**：`{体系代码}-{设备代码}-YYMMDD-{序号}`
- **样品批次 ID 规则**：`{体系代码}-{候选编号}-B{序号}`
- **设备代码表**：M=马弗炉, T=管式炉, E=电化学, G=手套箱, F=可控气氛炉, B=通用
- **Obsidian 集成**：YAML frontmatter + Dataview 查询仪表盘
- **双路径输入**：CLI 直接提交 + 飞书群扫描
- **目录结构**：`raw/` 原始层 + `wiki/` 标准层
- **异常检测**：自动追加异常记录

**借鉴点**：materials-skills 目前没有独立的实验记录 skill。materials-doe 有 experiment-record 模板，但缺少 ID 体系、Obsidian 集成、异常追踪等。对于你的研究方向（改性乳化沥青），可以参考 nature-experiment-log 的设计，建立自己的实验 ID 体系和日志模板。

**参考文件**：
- `nature-experiment-log/SKILL.md` — 完整设计
- `nature-experiment-log/templates/experiment-index.md` — Dataview 查询仪表盘
- `nature-experiment-log/templates/anomaly-log.md` — 异常记录
- `nature-experiment-log/templates/equipment-tracking.md` — 设备追踪

---

## 五、共享层设计

### 5.1 术语账本 (Terminology Ledger)

nature-skills 的 `_shared/core/terminology-ledger.md` 是一个精心设计的共享模块：

- **首次接触即建立**：收到稿件后先提取所有领域术语建立账本，再编辑正文
- **向用户展示**：以紧凑表格形式展示规范术语、首次使用定义、已见变体、决策
- **锁定并强制执行**：一旦设定，全程使用规范形式；术语一致性优先于词汇多样性
- **不发明术语**：不替作者命名方法/模块/概念

**借鉴点**：materials-skills 已有 `_shared/core/terminology-ledger.md`，但 nature 版本更强调 "首次接触即建立" 和 "向用户展示" 的工作流步骤。可以强化 materials 版本中的工作流描述。

**参考文件**：`nature-skills/skills/_shared/core/terminology-ledger.md`

### 5.2 论文类型分类法 (Paper-Type Taxonomy)

nature-skills 的 `_shared/core/paper-type-taxonomy.md` 定义了 5 种规范类型：

| Type | Definition | Reader's central question |
|------|-----------|--------------------------|
| research | Reports a phenomenon/mechanism/finding | What was found and what does it mean? |
| methods | Proposes a new method/protocol/measurement | Does it work? Is it better? Is it reproducible? |
| hypothesis | Establishes or rules out a causal explanation | Is the proposed mechanism the right one? |
| algorithmic | Proposes a procedure/model/system/device | Does it perform? Where does it fail? |
| review | Synthesizes the state of a field | What is known, where is the disagreement, what is open? |

每个 skill 的 `static/fragments/paper_type/<type>.md` 在此基础上添加 skill-specific 的 action layer。

**借鉴点**：materials-skills 没有统一的论文类型分类法。nature 的 taxonomy 设计精妙之处在于：它是共享词汇表，action 是 skill-specific 的。materials-polishing 和 materials-writing 可以共享同一个分类法，各自添加 domain-specific 的诊断或构建规则。

**参考文件**：`nature-skills/skills/_shared/core/paper-type-taxonomy.md`

### 5.3 读者工作流 (Reader Workflow)

nature-skills 的 `_shared/core/reader-workflow.md` 定义了读者的 5 个问题序列：

1. Relevance — Is this for me?
2. Novelty — What is new here?
3. Trust — Do I believe it?
4. Reuse — Can I use it?
5. Meaning — What does it mean, and where are the boundaries?

**借鉴点**：materials-skills 缺少这种读者视角的共享认知。这个模型可以指导 materials-writing 和 materials-polishing 的写作和润色策略。

---

## 六、工程实践

### 6.1 测试文化

nature-skills 在多个 skill 中有正式的测试：

- `nature-paper-to-patent/tests/test_validation.py` — pytest 单元测试
- `nature-academic-search/mcp-server/tests/` — 多源测试（test_sources.py, test_mcp_tools.py, test_elsevier_live.py）
- `nature-downloader/tests/python/test_config_wizard.py` — 配置向导测试
- `nature-downloader/tests/unit/` — JavaScript 单元测试

**借鉴点**：materials-skills 的测试覆盖较弱。nature-skills 的测试策略是「每个有独立脚本的 skill 都应该有测试」，且测试文件与源码同目录或邻近目录。

**参考文件**：
- `nature-paper-to-patent/tests/test_validation.py`
- `nature-academic-search/mcp-server/tests/`

### 6.2 验证脚本模式

nature-paper-to-patent 有一组完整的验证和构建脚本：

```bash
python scripts/validate_patent_draft.py draft.json    # 结构化验证
python scripts/build_patent_package.py draft.json ...  # 构建输出包
```

验证脚本遵循严格模式：
- ERROR vs WARNING 分级
- 明确的错误码（MISSING_KEY, NO_CLAIMS, CLAIM_SEQUENCE, EMPTY_CLAIM 等）
- 正则表达式验证（SOURCE_ID, PLACEHOLDER, VAGUE_RESULT）
- 质量阈值配置

**借鉴点**：materials-skills 有 `run_release_checks.py` 和 `check_skill_architecture.py`，但缺少 skill-level 的结构化验证脚本。nature-paper-to-patent 的 validate → build 模式值得借鉴。

**参考文件**：`nature-paper-to-patent/scripts/validate_patent_draft.py`

### 6.3 安装脚本

nature-skills 有完整的安装/更新脚本 `scripts/update-codex-skills.sh`，支持：
- `--pull` 安装/更新
- `--check` 验证
- `--prune` 清理已删除的旧目录
- diff 验证

**借鉴点**：materials-skills 作为 Codex plugin 已有 plugin.json 配置，但缺少独立的安装/更新/验证脚本。可以考虑提供类似的脚本，让用户能一键安装或更新 skills。

### 6.4 Agent 配置文件

nature-skills 在多个 skill 中有 `agents/openai.yaml` 配置文件：

- `nature-data/agents/openai.yaml`
- `nature-paper-to-patent/agents/openai.yaml`
- `nature-downloader/agents/openai.yaml`

**借鉴点**：materials-skills 也有 `agents/openai.yaml`（如 `materials-citation`、`materials-doe` 等），但 nature-skills 的 agent 配置更简洁。可以对比优化。

---

## 七、内容组织

### 7.1 共享核心的精简原则

nature-skills 的 `_shared/core/` 只有 4 个文件：
- `ethics.md` — AI 边界、引用伦理
- `paper-type-taxonomy.md` — 论文类型分类
- `reader-workflow.md` — 读者问题序列
- `terminology-ledger.md` — 术语账本

而 materials-skills 的 `_shared/core/` 有 12+ 个文件。

**借鉴点**：nature-skills 的共享核心遵循「只放跨 skill 真正共享的内容」原则。materials-skills 的 `_shared/` 可以审视哪些内容可以下沉到具体 skill 的 `static/` 中。

### 7.2 Chinese Mode 作为显式轴

nature-skills 在多个 skill 中把 "用户语言" 作为显式的工作模式轴：

- `nature-polishing` 的 manifest 中有 `language: en / zh-to-en` 轴
- `nature-citation` 有 `static/core/chinese-mode.md`
- `nature-data` 有 `static/core/chinese-mode.md`

**借鉴点**：materials-skills 主要面向中文用户，但缺少显式的 "Chinese mode" 模式切换。可以在需要双语输出的 skill 中引入类似设计。

**参考文件**：
- `nature-polishing/manifest.yaml` L47-L56 — language 轴
- `nature-citation/static/core/chinese-mode.md`

### 7.3 figures4papers / materials4papers 示例体系

nature-figure 有丰富的 `figures4papers/` 示例目录，包含 8 个子目录，每个有 `plot_*.py` + `figures/` 输出：
- figure_CellSpliceNet, figure_Cflows, figure_Dispersion, figure_FPGM, figure_ImmunoStruct, figure_RNAGenScape, figure_VIGIL, figure_brainteaser, figure_ophthal_review

materials-figure 也有 `materials4papers/`，但只有 5 个示例。

**借鉴点**：materials4papers 可以继续扩充材料科学领域的经典图表示例，覆盖更多表征类型（XRD、SEM、FTIR、DSC、TGA、流变等）。

---

## 八、具体可落地的升级建议（按优先级）

### 高优先级（直接复用设计模式）

1. **为 materials-writing 引入 foundation 文件体系**
   - 参考 nature-proposal-writer 的 templates/，创建 `00_scope.md`、`01_research_canon.md`、`02_evidence_table.md`、`03_argument_map.md`、`04_section_contracts.md`
   - 引入 `state.json` 追踪写作状态

2. **为 materials-writing 和 materials-polishing 引入停止规则**
   - 参考 `nature-proposal-writer/references/stopping-rules.md`

3. **完善 materials-literature-pipeline 的评分系统**
   - 参考 nature 的六维加权评分 + 门控规则 + 校准指南

4. **为 materials-writing 引入评分量规锚点**
   - 参考 nature-proposal-writer 的 8 维 × 4 锚点评分体系

### 中优先级（增强现有能力）

5. **创建独立的 materials-experiment-log skill**
   - 参考 nature-experiment-log 的 ID 体系、Obsidian 集成、异常追踪

6. **补全 SKILL.md 的 "Why this split" 尾段**
   - 在每个 Router-style skill 的 SKILL.md 末尾添加架构说明

7. **引入论文类型分类法**
   - 在 `_shared/core/` 中创建 `paper-type-taxonomy.md`
   - 在 materials-polishing 和 materials-writing 中添加 paper_type 轴

8. **引入读者工作流共享认知**
   - 在 `_shared/core/` 中创建 `reader-workflow.md`

### 低优先级（工程优化）

9. **增加 skill-level 测试**
   - 参考 nature-paper-to-patent/tests/ 的模式

10. **规范化 manifest 注释**
    - 在 always_load 中区分 shared layer 和 skill-local core

11. **提供安装/更新脚本**
    - 参考 nature-skills 的 `scripts/update-codex-skills.sh`

---

## 九、当前分支已完成的改动概览

在 `codex/nature-comparison-upgrade` 分支上，你已经完成了以下改动：

| 文件 | 改动类型 | 说明 |
|------|---------|------|
| `materials-literature-pipeline/` (新增) | 新 skill | 文献管线 skill，结构与 nature-literature-pipeline 对齐 |
| `literature-pipeline-handoff.yaml` (新增) | 新 handoff 契约 | 文献管线与 materials-research 之间的数据契约 |
| `research-state-contract.md` (新增) | 新共享核心 | 跨 skill 研究状态追踪契约 |
| `research-state-template.yaml` (新增) | 新共享模板 | 研究状态的 YAML 模板 |
| `content-first-qa-pipeline.md` (新增) | 新 reference | materials-writing 的内容优先 QA 管线 |
| `materials-research/SKILL.md` | 修改 | 增加 literature-pipeline 路由和 coverage_tier |
| `materials-research/manifest.yaml` | 修改 | 新增 literature_pipeline 到 companion_skills、handoffs 等 |
| `materials-research/references/companion-modules.md` | 修改 | 增加 literature-pipeline 路由说明 |
| `materials-writing/SKILL.md` | 修改 | 增加 content-first-qa-pipeline 引用 |
| `materials-writing/manifest.yaml` | 修改 | 增加 content-first-qa-pipeline 到 on_demand |
| `materials-figure/manifest.yaml` | 修改 | 移除 1 行 |
| `citation-handoff.yaml` | 修改 | 增加 1 行 |
| `doe-handoff.yaml` | 修改 | (查看 diff) |
| `run_release_checks.py` | 修改 | 增加 literature-pipeline 检查 |
| `README.md` | 修改 | 更新 |
| `docs/skills-index.md` | 修改 | 更新 |
| `plugin.json` | 修改 | 更新 |

这些改动主要集中在 **打通文献管线闭环**（literature-pipeline → research-state → materials-research → companion skills），与 nature-skills 的 literature-pipeline + researchwrite 联动模式对齐。

---

## 十、总结

nature-skills 对 materials-skills 最有价值的借鉴不是某个具体文件，而是以下**设计哲学**：

1. **Router 要薄，Fragment 要独立，Reference 要深** — SKILL.md 不超过 80 行，核心逻辑在 static/ 中，深度知识在 references/ 中按需加载
2. **先建立契约，再写内容** — 证据表、论证图、章节契约、术语账本，都应在正文起草前完成
3. **知道何时停止** — 有显式的停止规则，不无限迭代
4. **评分要有锚点** — 不只是给分数，还要给每个分数段的具体描述
5. **管线要能自愈** — 有降级策略、去重逻辑、分数验证，不是脆弱的脚本链
6. **每个 skill 都是可独立交付的产品** — 有完整的输入→处理→输出→验证→交付闭环