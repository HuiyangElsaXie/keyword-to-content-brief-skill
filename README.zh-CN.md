# 关键词到内容简报

**工具定位：在 Codex 中完成有证据边界的关键词簇规划与内容简报。** 可从种子词、URL、策略文件或获准使用的导出数据开始。Agent 在实际工具与权限允许时研究候选词、核对证据、规划支柱页／子主题页及内链，再审阅计划、交互地图、逐页 brief 与规划评分卡。Python 模块保持离线；不内置搜索量、实时 SERP 或 Search Console 连接器。

## 一分钟开始

保留完整仓库并明确提供嵌套 SKILL.md 入口；仅复制技能子目录会遗漏根目录脚本、文档、案例及来源资源。自动发现／安装规则取决于宿主。

[现行规则输出计划](cases/inventory-context-repair/final-marine-existing/cluster-plan.md) · [现行 brief 骨架，待编辑完善](cases/inventory-context-repair/final-marine-existing/cluster-briefs/page-001.md) · [早期完整编辑报告，历史示例](examples/intake-case/final-report.md) · [现行行为复核](cases/inventory-context-repair/REVIEW.md)

链接示例均使用合成输入。历史完整报告用于理解编辑交接，不代表当前 CLI 决策或真实需求。

| 手头资料／使用方式 | 最短下一步 | 交付与边界 |
|---|---|---|
| 只有网址或种子词；Codex／AI 对话 | 先读 [skill](skills/keyword-to-content-brief/SKILL.md)，提供网址／词、受众、目标和已知页面清单，只补问关键缺口。 | Agent 研究取决于实际可用且获准的工具；没有工具就分析已给资料并标明暂定假设。网址不是关键词或 SERP 导出。 |
| 已有关键词、页面或搜索证据；Codex／AI | 提供获准文件及来源、日期、市场、语言、设备，请先核对已有页面，再交付待审 brief。 | AI 映射输入并完成编辑判断；普通搜索结果不等于有序 Google 自然结果前十。 |
| Python 离线；已有结构化证据 | 按 [JSON 问卷与模板](skills/keyword-to-content-brief/QUESTIONNAIRE.md)及下方离线命令运行，使用新输出目录。 | 输出证据决策和未完成 brief 骨架，不自动搜索、抓站或写文章；[cluster renderer](docs/CODEX-CLUSTER-PORT.md)使用另一套 schema。 |

示例请求：“基于这个网址和我提供的页面清单，为指定受众与目标做页面决策和待审 brief；缺 SERP 证据就保持未知，不发布。”保留仓库结构；其他 AI 宿主需自行核对工具与路径，不承诺未经测试的跨宿主兼容。

报告是否有用，取决于输入数据的质量、完整性和覆盖范围。缺失证据必须明确保留；输出是供人工判断的建议，不等于页面必须修改或线上故障已经证实。本项目个人自用，会随工作流实践持续更新。

**日常／客户项目用法：** 客户已提供获准使用的关键词导出、页面清单及兼容的搜索结果证据时，可用它辅助整理内容规划报告与写作 brief。 使用前先映射为约定的数据格式，核对来源与缺失字段，向客户交付前仍需人工审阅。实际使用仍须审阅；这不表示它已成为经过完整验证的生产服务，或替新增内容选定了许可。

**基于 [AgriciDaniel/claude-seo 的 seo-cluster](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-cluster/SKILL.md) 实质改编**：v2.4.2，固定提交 4b99de2f7de7e7d5247042e5fb5b4ea9368ef734。上游 MIT，Copyright (c) 2026 agricidaniel；源文件还署名 Lutfiya Miller。[原始快照与完整许可](upstream/claude-seo/) · [署名说明](ATTRIBUTION.md) · [逐项改编对照](ADAPTATION.md) · [English](README.md)

新增原创部分的许可仍待所有者选择，不能宣称整个仓库已经 MIT 开源。个人自用是项目用途，不是限制上游 MIT 商业使用权的新条款。

当前行为请看[已有页面/业务目标修复案例及独立检查](cases/inventory-context-repair/REVIEW.md)。下方早期成对示例保留历史版本证据，旧生成计划不代表当前决策门。

## 新 Codex 完整规划入口与保留的离线路径

先读 [Codex skill](skills/keyword-to-content-brief/SKILL.md)、[路由与证据门](skills/keyword-to-content-brief/references/codex-cluster-routing.md)及[能力边界／命令](docs/CODEX-CLUSTER-PORT.md)。所选 seo-cluster 规划流程已转为 Codex agent 指令与独立的离线输出模块，涵盖扩词／策略映射、合格 SERP 重叠、意图、支柱与子页架构、模板、内链矩阵、交互地图、逐页 brief、规划评分卡和地图重建。不实现自动文章生产或发布。

两条路径不能混称：
- 完整规划：Agent 将研究／用户材料明确映射为新模块输入并审阅输出；仍沿用业务提问规范，生成了全部文件不代表证据或编辑工作已完整。
- 原有离线分析：plan_keywords.py 与原输入契约继续提供成对证据、保守分组、页面决策和未完成的 brief 骨架，原 CLI 没有被替换。

普通网页搜索不等于 Google 前十条自然结果。合格导出或实际可用且获准的适配器须保留引擎、精确查询、市场、语言、设备、日期及结果顺序。未知重叠／搜索量仍为未知，GSC 展现量不等于市场搜索量。扩词数量、字数与内链密度只是可调整的规划启发式，不是 Google 规则。Ads、GSC、DataForSEO、writer／blog 和 Google／PDF 都是待运行时发现并授权的可选外部能力，不是本仓库已内置的集成。

### 已实际执行的成对示例
同样五个虚构关键词，不同业务目标：[知名度 brief](cases/codex-cluster-port/final2-awareness/cluster-briefs/page-001.md)帮助入门读者理解 onboarding 责任与交接；[转化 brief](cases/codex-cluster-port/final2-conversion/cluster-briefs/page-001.md)筛选工作流适配度，并明确定义完成 walkthrough-request 的事件。[实际计划/地图/scorecard](cases/codex-cluster-port/final2-awareness/) · [独立复核与限制](cases/codex-cluster-port/REVIEW.md)。没有编造真实搜索量或业务成绩。


## 已有网站与求职作品集

先提供现有页面清单或映射，再判断候选词是否需要新页面。工具区分保留、审阅现有页、暂缓和新页提案；没有清单不等于空白网站。同一 URL 的审阅任务会合并，覆盖充分与否需要有来源的评估。只有完整清单及明确内容缺口、业务理由才能支持新页提案，仍不代表可以发布或已证明搜索需求。

求职作品集可设置 business_context.content_purpose 为 recruitment_portfolio。商业评估意图可以对应职业概览或案例证据，不再一律套比较文章模板。brief 会传递已提供的 next_action，并与转化衡量定义分别展示。详见[输入与使用说明](docs/INVENTORY-CONTEXT.md)。

## 原有证据分析路径

把现成关键词、搜索结果证据和已有页面清单，转成编辑可以审核的页面安排与写作简报：哪些词共用一页，哪些应更新旧页，哪些值得安排新页，哪些需要补证据。

适用场景：
- 小型 SaaS 团队每月只能新增一页内容，需要明确取舍与写作交接。
- 已有多篇指南，想在新增文章前检查重复覆盖与页面冲突。
- 希望把业务判断、所提供的搜索证据和待验证产品说法分开管理。

本次新增的是离线证据契约、保守分组、优先匹配旧页面、容量约束、写作事实边界与完整审阅记录；上游搜索结果重叠方法不冒充原创。

## 输入与交付

输入包括关键词及 ID、意图与理由、业务优先级、来源 ID、可选的前十条自然搜索结果 URL（带日期/市场/语言/设备）、已有页面和新增页面容量。不要求付费工具，也不编造搜索量。

脚本输出成对重叠证据、保留重复词原始 ID 的分组、更新/新增/暂缓决策与理由，以及明确标为未完成的简报骨架。Agent/编辑再完成读者任务、标题与描述、H2/H3 大纲、证据需求、禁用说法、相关内链与验收条件。脚本骨架不是完整写作简报。[输入契约](docs/input-contract.md)。

## 两种使用方式

可交给 AI 阅读 [skill](skills/keyword-to-content-brief/SKILL.md)，也可直接编辑 [INPUT.template.json](skills/keyword-to-content-brief/INPUT.template.json)，按[问卷命令](skills/keyword-to-content-brief/QUESTIONNAIRE.md)运行 CLI。分工如下：

1. **你**提供业务决策、受众、已知页面清单和获准关键词／搜索导出；未知可以明确回答未知。
2. **AI**复用背景，每轮最多问三个关键缺口，并映射所选输入契约；直接 CLI 路径由**你**编辑 JSON，不互动提问。
3. **AI／离线模块**核对证据，按路径生成计划、骨架或 cluster 产物；研究取决于实际授权工具，缺 SERP／搜索量保持未知。
4. **AI**审阅意图、已有覆盖、容量与主张，完善编辑 brief，记录修正并保留首稿。
5. **你**收到计划与简报后判断内容取舍再采用；完整模块另含地图、内链和评分卡，原 helper 单独只产待编辑完善的骨架。不执行文章生产或发布。

问卷包含精确字段映射，沿用[规范业务提问](docs/business-intake.md)，**不会自动导入脚本**。明确不知道用 unknown 状态加真正的 JSON null，不重复追问；省略的必要字段才可能成为下一轮问题。模板可直接运行，但只有明确标为虚构的占位关键词，没有真实搜索证据；实际使用前需替换。每次输出到新的空目录。[模板执行检查](docs/usage-template-checks-20261016.md)。

AI 先复用当前对话、brief 或宿主确实可访问且获准使用的相关记忆，简短说明已有业务／受众／目标及关键资料的来源、日期和把握程度；区分事实与推断，检查过时、冲突和其他客户资料，以用户最新指示为准。足够时直接进行获准的只读分析，只问缺口、冲突或时效性关键项。不假定拥有全局或跨对话访问；无记忆功能则用 brief。记忆不能替代 SERP／抓取／Search Console 证据或授予行动权限，用户／客户记忆不写进仓库或模板；CLI 仍只读取 JSON。[双语说明与虚构示例](skills/keyword-to-content-brief/QUESTIONNAIRE.md#reuse-accessible-context-first--先复用可访问的上下文)。

## 运行原有离线 helper

Python 3.10+，仅标准库，不联网、不调用付费服务。

```sh
python scripts/plan_keywords.py examples/intake-case/input.json --out /tmp/keyword-plan-new
python -m unittest discover -s tests -v
```

输出目录需为空或不存在，避免覆盖已有证据。请让 Agent 阅读 [skill](skills/keyword-to-content-brief/SKILL.md)、输入契约和原始材料，实际运行脚本，再写首稿、审阅并保存终稿。保留仓库结构，不要只复制 SKILL.md 导致相对路径失效。

## 实际执行过的虚构案例

[请求](examples/studio-case/REQUEST.md) · [输入](examples/intake-case/input.json) · [实际运行记录](examples/studio-case/agent-run/RUN_LOG.md) · [首稿](examples/studio-case/agent-run/first-output.md) · [审阅](examples/studio-case/agent-run/review.md) · [终稿](examples/studio-case/agent-run/final-output.md)

MossNote Studio 是虚构项目。Agent 从十行、九个去重关键词出发，运行页面安排并完成一份新增页面简报与一份旧指南更新简报。数据包含重复词、不同市场、缺失证据、混合/导航意图和单页容量。所有搜索结果 URL 集合均为构造测试数据，不是真实 Google 结果，不代表真实竞品、客户、产品效果或需求。

## 验证与边界

原基线包含 49 项离线测试：包含契约/决策、业务提问与报告门，以及 4 项旧版校验测试。覆盖重叠阈值、上下文不一致、重复冲突、禁止传递式错误合并、页面冲突、容量、URL 凭据、语义查询参数和防覆盖。测试证明逻辑约束，不证明 SEO 排名效果。

两个 Python 模块都不会联网采集关键词或审计网站；完整 Codex 路径可通过实际可用且获准的工具研究候选词，但不承诺流量、自动验证全部产品能力或发布内容。意图和旧页面映射仍是人工判断；完整单次快照也不等于真实需求。不同日期/市场/语言/设备不会强行比较。终稿仍待人工审核。实际项目需要有权使用的当前导出数据、页面正文与可验证产品事实。

[v0.1 完整旧版](legacy/v0.1/) 保留作对照；旧版三关键词预填示例与旧署名说明只适用于历史版本。根目录旧 examples/input.json 与 scripts/validate_plan.py 继续保留兼容。[公开前检查](REVIEW_BEFORE_PUBLIC.md)。


## v0.3：先提问，再决定报告层级
先复用已提供的 brief，第一轮最多问三个缺失关键问题，再按目标、生命周期、关键词角色和已有内容追问。行业、受众/地区/语言、具体业务问题、品牌与竞争位置（证据和假设分开）、首要目标、转化事件、资源及限制会影响建议。品牌阶段、产品阶段与网站年龄分开记录。

**无法提供具体问题时，仍可获得有参考价值的行业通用报告（industry_general）**：整理已提供的关键词、页面承接、可考虑的用途、证据缺口和验证问题，但不冒充公司专属优先级。行业也未知时输出 generic_framework 通用框架。业务上下文足够时才标注 tailored；这仍不代表已证明需求或可以直接执行。

已有页面映射改为 review_existing；覆盖充分可 retain，缺口证据和目标关联优先级齐备才可建议 update。同 URL 只形成一个工作项，不伪造关键词簇。详情：[双语提问流程](docs/business-intake.md)、[新案例实际执行](examples/intake-case/README.md)。该历史基线曾通过 49 项离线测试；不代表新模块测试总数或真实 SEO 效果验证。

原 v0.2 示例输出保留不变。需要复现旧执行时使用仓库固定提交 75b34eb9da534d967170b2a92d5f08e0b37c93b8 的原 helper；当前 v0.3 对旧输入会进入通用框架和证据门，不再复现旧 update 决策。新增代码的作者许可仍待确认，上游署名与 MIT LICENSE 保留。
