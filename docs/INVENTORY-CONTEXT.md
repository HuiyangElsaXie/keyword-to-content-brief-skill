# Existing-page inventory and business-context gate

This extension analyzes supplied evidence only. It does not fetch pages, understand coverage independently, discover customer data or grant permission to edit a website. An AI/editor supplies and checks page assessments. See the [cluster contract](CODEX-CLUSTER-PORT.md) for the base schema.

## Structured input

Optional top-level `existing_page_inventory`:

```json
{
  "status": "complete",
  "source_id": "S1",
  "evidence_locator": "Supplied fictional inventory, reviewed 2026-10-16",
  "pages": [
    {
      "url": "https://studio.example/work",
      "title": "Selected studio work",
      "terms": ["design project case study", "studio portfolio"],
      "source_id": "S1",
      "evidence_locator": "Fictional page snapshot: portfolio section"
    }
  ]
}
```

Use `complete`, `partial` or `unknown` honestly. Complete means complete for the stated planning scope, not that search engines indexed every page. Omitting inventory means unknown. A complete empty list describes a supplied new-site inventory, not an assumption from a missing file.

A candidate may carry:

```json
{
  "existing_page": {
    "url": "https://studio.example/work",
    "coverage": "sufficient",
    "source_id": "S1",
    "evidence_locator": "Supplied assessment: relevant case and role already covered"
  }
}
```

Coverage is `sufficient`, `partial` or `unknown`. A source/locator records the assessment; the parser cannot prove its truth. Same normalized destinations consolidate review work. Inventory term matches can indicate a candidate destination, not independently prove semantic equivalence or sufficient coverage. Conflicts and near-duplicates need review; zero exact duplicate keywords never proves no content duplication.

A genuinely proposed new candidate may carry `new_page_evidence` with nonempty `gap`, `business_rationale`, `source_id`, and `evidence_locator`. A complete inventory and these cited reasons permit a `new_proposal`, not an approved task. Search relationships remain provisional without compatible real SERPs. A new-site business rationale is legitimate supplied evidence for a planning hypothesis, not demonstrated search demand.

## Existing mapping adapter

For a separately reviewed list containing `candidate_id` and `existing_url`:

```sh
python scripts/cluster_workflow.py plan --input INPUT.json --page-mapping PAGE-MAPPING.json --out NEW-OUTPUT
```

The adapter explicitly imports the mappings as unknown-coverage assessments. It does not upgrade an old prose disposition into proof of adequate coverage or complete inventory. Original files remain unchanged; the saved plan records the effective supplied input. No hidden questionnaire or chat-memory import occurs.

## Recruitment portfolios and next action

Set `business_context.content_purpose` to `recruitment_portfolio` when the primary reader is evaluating professional suitability. The renderer uses portfolio-oriented content types rather than a mandatory comparison article for commercial intent. Other industries retain their own reader jobs; this flag is not a website-name rule.

Candidate `editorial.next_action` should describe the concrete reader/editor action. `business_context.conversion_definition` describes a completed measurable event if one is actually defined. They are related but not interchangeable. An available next action must not disappear into “Unknown” merely because there is no conversion metric. Do not invent a conversion event to fill a field.

## Interpreting output

- `retain`: supplied coverage supports keeping the existing destination.
- `review_existing`: an existing destination is identified but evidence does not establish whether any change is needed.
- `defer`: insufficient inventory/gap evidence or unresolved conflict.
- `new_proposal`: sufficiently documented planning hypothesis, still requiring editorial/human approval and missing-data review.

Existing-page retention/review does not need a new URL, production word target or automatic new architecture links. Planning/proposal counts are not modification counts. Renderer output remains separate from agent/human editorial assessment and from measured marketing results.

## 中文要点

先提供清单和页面评估，再讨论新页。缺清单不等于没有网页；匹配到页面不等于需要更新；同 URL 合并是工作去重，不是证明关键词的搜索意图相同。覆盖评估由使用者或 AI 阅读真实内容后提供，脚本只检查结构与证据门，不能代替内容判断。

已有映射文件可用 `--page-mapping` 显式导入，原始 JSON 不需修改。导入只说明目标页面存在且覆盖未知，不会把旧文字说明自动变成充分证据。求职作品集使用 `recruitment_portfolio`，以职业概览/案例证据为内容方向；下一步行动和可衡量转化事件分别记录。保持/审阅/暂缓/新页提案四种状态都不构成改站或发布授权。

## Version compatibility

Old input JSON remains readable; omitted inventory now conservatively defers production. The earlier standalone plan_keywords.py contract is unchanged. Historical generated plan artifacts remain as evidence, but their derived fields reflect the older policy. Regenerate from the original input with the current module before using map/execute/scorecard; saved-plan integrity checks reject derived fields that do not match the current deterministic reconstruction. Do not rewrite old reports to hide the difference.
