# Fillable business questionnaire / 可填写业务问卷

This is a worksheet for the [canonical adaptive intake](../../docs/business-intake.md), not a second intake specification. Field types and gates are defined in the [input contract](../../docs/input-contract.md). Read those documents when interpreting answers. / 本文件是规范提问流程的填写入口，字段及报告门以链接文档为准。

## Choose a flow / 选择使用方式

### 1. AI conversation → answers → report / AI 对话 → 回答 → 报告
Give the AI [SKILL.md](SKILL.md), your existing brief, keyword/page evidence and this worksheet, keeping the repository structure available. The AI first reads the brief, summarizes known answers with sources, and asks at most three missing essentials at a time according to the canonical intake. You answer in ordinary language; unknown is acceptable. The AI maps answers to [INPUT.template.json](INPUT.template.json), runs the helper if appropriate, explains the resulting mode and completes the report/briefs with review. Do not require the user to fill every line or repeat an explicitly unknown answer.

把 skill、已有 brief、关键词及页面材料交给 AI。AI 先读已有信息，每轮最多询问三个缺失关键问题；你用自然语言回答，不知道可以明确说不知道。AI 将答案映射到 JSON，运行辅助脚本，解释报告层级，再完成报告、简报及审阅。按需填写下方项目，不必一次填写全部。

### 2. Edit JSON → CLI → review / 编辑 JSON → 命令行 → 审阅
Copy the JSON template to your own input file; edit JSON values, not Python source. Run from the repository root:

```sh
cp skills/keyword-to-content-brief/INPUT.template.json /tmp/my-keyword-input.json
# Edit /tmp/my-keyword-input.json in a text editor, then:
python scripts/plan_keywords.py /tmp/my-keyword-input.json --out /tmp/my-keyword-plan-new
```

Choose a fresh/empty output directory every run. The CLI is noninteractive: it never stops to interview you. It automatically selects `tailored`, `industry_general` or `generic_framework` using the canonical gates. Read `plan.json` → `business_context.report_mode`, `commissioning_status`, `missing_for_commission`, `next_questions`; `plan.md` also shows the mode and next questions. Answer later by editing a new copy of the input and rerunning to a fresh output directory. `brief-scaffolds.md` is unfinished; an AI/editor still writes and reviews the final report. `tailored` does not bypass keyword/page evidence gates.

复制模板并用文本编辑器修改 JSON，不改 Python。CLI 不进行互动提问，会自动判断报告层级并输出缺失项及下一轮问题。查看上述文件和字段，补充答案后输出到新的空目录；骨架仍须由 AI／编辑完成并审阅，不能直接当成交付终稿。

**No automatic questionnaire import:** neither CLI nor a Markdown parser reads these answers. You or the AI must map each answer to JSON explicitly. / **问卷不会被自动导入**；需要你或 AI 明确转成 JSON。

## Reuse accessible context first / 先复用可访问的上下文

For the AI flow, first reuse relevant, authorized information actually accessible in the current conversation, supplied documents or the host's memory. Do not assume global ChatGPT history, another conversation or another client's context is accessible or applicable. A host without memory uses the supplied brief. Check that the material belongs to this project/client, distinguish facts from inference, and flag stale or conflicting information. The latest user instruction takes precedence.

Briefly tell the user what business, audience and objective you are using, with source/date/confidence for critical context when available. Label an unavailable date or uncertain confidence honestly. If context is sufficient, proceed with authorized read-only analysis without mandatory reconfirmation; ask only about missing answers, conflicts or time-sensitive essentials. Do not ask the entire questionnaire again.

AI 先复用当前对话、已提供材料及宿主确实可访问且获准使用的相关记忆；不能假定能读取所有 ChatGPT 历史或跨对话信息。没有记忆功能就用 brief。先核对是否属于本项目／客户，区分事实和推断，检查过时与冲突，并以用户最新指示为准。简短说明“已有资料显示……本次据此……”，关键上下文注明来源、日期及把握程度；不知道日期就明确标注。信息足够可直接进行获准的只读分析，不强制重复确认，只问缺口、冲突或时效性关键项。

**Fictional example / 虚构示例:** “Your supplied brief dated 2026-10-01 describes a fictional design-studio tool for small studios, with awareness as the goal. I’ll use that context for this report. These are direct brief statements, not independently verified market facts; I’m less certain that the launch timing is still current, so what is the current launch date?” / “你提供的 2026-10-01 brief 描述了面向小型工作室的虚构工具，目标是提升认知。本次据此分析。这些是 brief 的直接陈述，并非核验过的市场事实；上市时间可能已变化，请问目前的上市日期是什么？” This example contains no real user/client memory.

Memory is not SERP, crawl or Search Console evidence and grants no publishing, payment or other action permission. Do not persist private user/client memory in this repository or its distributable template. Only deliberately supplied, task-relevant input belongs in the user's own working file. CLI still reads JSON only: it does not retrieve memory, read chat history or import the questionnaire.

Source/date/confidence are explanatory provenance in the report or a source's existing `description`, **not new JSON keys**. Map business statements only to the documented `business_context.<field>` objects (`status`, `value`, `source_ids`); register traceable source IDs in `sources`. Direct user statements can be `supplied`; inferred positioning stays `assumed`; unresolved answers stay `unknown`. Do not invent evidence dates or confidence scores. / 来源、日期和把握程度写在说明／报告或既有 source.description 中，不另造 JSON 字段；只用现有字段映射，CLI 不会自动导入记忆。

## Answer format and missing values / 答案格式与缺失值

Every field below maps to `business_context.<field>` as an object with `status`, `value`, `source_ids`:
- Confirmed supplied answer: `{"status":"supplied","value":"your answer","source_ids":["S_BRIEF"]}`. Add `S_BRIEF` to the top-level `sources` list with `kind: "supplied"` and an honest source description. Self-reported answers are traceable statements, not independent verification.
- Explicit assumption: `{"status":"assumed","value":"qualified assumption","source_ids":[]}`. Use known source IDs where available; never promote assumptions to supplied facts.
- Explicitly unknown: `{"status":"unknown","value":null,"source_ids":[]}`. JSON `null` is not the string `"null"` or `"unknown"`. Unknown status cannot hide a text answer.
- Not asked yet: omit the whole field object from `business_context`. Only omitted required fields are eligible for the helper's next questions, up to three. Explicit unknown fields remain in `missing_for_commission` but are not repeatedly asked. Because the template explicitly marks all answers unknown, its initial `next_questions` is empty. Delete the appropriate field object if you want it treated as unanswered rather than explicitly unknown.

已提供答案选 supplied 并登记来源；推测选 assumed 并写清限定；明确不知道选 unknown 且 value 为真正的 null。尚未询问则省略整个字段对象。模板已把全部字段明确标为 unknown，因此初次运行没有待追问问题，但仍会列出业务缺失项。这不表示上下文完整。

For each prompt, fill: Answer / 答案: ____; Status / 状态: ____; Source IDs and source description / 来源 ID 及说明: ____. Blank worksheet lines alone have no machine meaning.

## Exact business field mapping / 业务字段逐项映射

### `industry` → `business_context.industry`
What industry, offer and business model? / 行业、产品或服务及商业模式是什么？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `audience` → `business_context.audience`
Who is the primary audience and their problem/decision? / 主要受众是谁，要解决什么问题或决策？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `geography` → `business_context.geography`
Which target market? Use the SERP market token. / 目标市场是什么？与搜索结果 market 标记一致。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `language` → `business_context.language`
Which content language? Use the SERP language token. / 内容语言是什么？与搜索结果 language 标记一致。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `business_problem` → `business_context.business_problem`
What concrete decision should this report support? / 报告要帮助解决哪个具体问题或决策？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `primary_objective` → `business_context.primary_objective`
Choose awareness, consideration, conversion, retention or other. / 首要目标选择上述英文值之一：认知、评估、转化、留存或其他。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `objective_tradeoffs` → `business_context.objective_tradeoffs`
Which secondary goals must not override the primary goal? / 哪些次要目标不能压过首要目标？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `brand_position` → `business_context.brand_position`
Current promise/differentiators: what is supported versus aspirational? / 当前品牌承诺和差异点，哪些有证据、哪些只是愿景？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `competitive_position` → `business_context.competitive_position`
What alternatives do customers consider, and what supports your position? / 客户会考虑什么替代方案，竞争位置有什么依据？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `lifecycle` → `business_context.lifecycle`
Shared planning stage: prelaunch, launch, growth, mature, repositioning or other? / 本次规划采用什么阶段？上市前、上市、成长、成熟、重新定位或其他。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `brand_lifecycle` → `business_context.brand_lifecycle`
If different, what is the brand stage? / 如有差异，品牌处于什么阶段？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `product_lifecycle` → `business_context.product_lifecycle`
If different, what is this product/offer stage? / 如有差异，此产品或服务处于什么阶段？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `website_stage` → `business_context.website_stage`
Separately, site age and measurement history? / 单独记录网站年龄和测量历史，不能推断品牌阶段。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `conversion_definition` → `business_context.conversion_definition`
For conversion, what completed action, audience and measurement count? / 转化目标下，具体完成事件、对象与衡量方式是什么？点击不等于成交。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `resources` → `business_context.resources`
Available production/review capacity, expertise, assets and measurement? / 制作与审核能力、专业知识、素材和测量资源有哪些？

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

### `constraints` → `business_context.constraints`
Timing, budget, approval, legal, voice and claim restrictions? State none if none. / 时间、预算、审批、合规、语气与宣传限制是什么？确实没有可填 none。

- Answer / 答案: ____
- Status (supplied / assumed / unknown) / 状态: ____
- Source IDs and description / 来源 ID 及说明: ____

## Evidence and run settings / 证据与运行设置

These are separate from the business answers; see the contract for validation and evidence rules. / 以下不属于 business_context，校验要求见输入契约。

- Project name / 项目名: ____ → top-level `project` (nonempty text).
- Audience label / 受众标签: ____ → top-level `audience`; structured answer still belongs in `business_context.audience`.
- Report-purpose label / 报告用途标签: ____ → top-level `goal`; does not replace `business_problem` or `primary_objective`.
- Fictional dataset? / 是否虚构: ____ → `fictional` boolean. Template is `true`; replace every fictional row/source before using `false` for a real project. Never relabel synthetic data as supplied.
- Approved maximum new pages / 新增页数上限: ____ → `monthly_new_page_capacity`, nonnegative integer. Template `0` means deliberately no new pages allowed, not unknown capacity. Review/update effort remains an editorial judgment.
- Evidence sources / 证据来源: ____ → `sources[]`: unique `id`, `kind` (`supplied` or `synthetic`), `description`. Every referenced ID must exist here.
- Keywords / 关键词: ____ → `keywords[]`: `id`, `keyword`, `intent`, `intent_reason`, `source_id`; `business_priority` is null or 1–5. At least one row is required, so the runnable template has one explicitly fictional placeholder. Replace it before real use. Intent accepts informational/commercial/transactional/navigational/mixed; no unknown intent enum exists.
- Keyword role and funnel / 品牌属性与漏斗: ____ → `keywords[].brand_scope` (brand/nonbrand/competitor/unknown), `keywords[].funnel_stage` (awareness/consideration/conversion/retention/navigation/unknown).
- Objective-linked priority evidence / 目标关联优先级依据: ____ → `keywords[].priority_evidence` (`source_id`, `objective`, `rationale`) or null when absent. Objective must match the business objective for commissioning; priority is not measured demand.
- Supplied search results / 已提供搜索结果: ____ → `keywords[].serp` (null if absent; otherwise `source_id`, `date`, `market`, `language`, `device`, `organic_urls`). Do not fabricate top-10 results to unlock decisions.
- Existing pages / 已有页面: ____ → `existing_pages[]` (`path`, `title`, `keyword_ids`). Empty template list means no inventory supplied, not verified absence of pages. Optional `coverage_review` contains `result` (gap/covered/unknown), `source_id`, `detail`; a mapping alone is not a gap.

No separate structured fields for budget, business model, success metrics or competitor lists are introduced: use the relevant canonical free-text answers (`constraints`, `industry`, `conversion_definition`/`resources`, `competitive_position`) with provenance. / 不添加另一套预算、商业模式、衡量指标或竞品字段，使用规范中对应的自由文本字段并注明来源。
