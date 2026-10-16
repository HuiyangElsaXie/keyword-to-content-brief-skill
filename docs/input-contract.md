# Input contract v0.2

Python 3.10+; standard library only. JSON object:
- `project`, `audience`, `goal`: nonempty strings.
- `fictional`: boolean; all included case data is fictional.
- `monthly_new_page_capacity`: nonnegative integer (not boolean).
- `sources`: list of objects with unique `id`, `kind`, `description`. `kind` is `synthetic` or `supplied`; source IDs support traceability, not authentication.
- `existing_pages`: list of `{path, title, keyword_ids}`. Paths are local site paths starting `/`, unique; keyword IDs indicate inventory mappings supplied by the analyst, not automated page audits.
- `keywords`: nonempty list of `{id, keyword, intent, intent_reason, business_priority, source_id, serp}`. Intent is informational/commercial/transactional/navigational/mixed. Priority is 1–5, 1 highest; it is editorial priority, not search volume. `serp` may be absent/null or `{source_id,date,market,language,device,organic_urls}`. Date uses ISO YYYY-MM-DD. Exactly 10 unique normalized URLs are required for a comparable snapshot. Any smaller sample remains visible but cannot support automatic page creation/merge.

Comparable snapshots must match date, market, language and device. The helper deliberately does not infer an acceptable age. Reviewer decides freshness for real projects, including checking that recorded dates are genuine and not future-dated. The helper validates calendar syntax only; it is not a timestamp-authenticity check. URLs must use http(s); host is lowercased, fragment and known tracking parameters removed, trailing slash normalized. Semantic query parameters and path case are preserved. No URL is fetched. URLs in synthetic fixtures use reserved `.example` hosts.

Keyword normalization: Unicode NFKC, casefold, and whitespace collapse only; no stemming or article stripping. Duplicate wording must have identical intent/priority/SERP evidence; otherwise fail for analyst reconciliation. All aliases are retained in output.

Output files: `plan.json`, `plan.md`, `brief-scaffolds.md`. The last file explicitly requires agent/editor completion. Plan records each pair, each unique keyword group, deferred reasons, targets, alias IDs and incoming evidence. Page path suggestions are derived from primary keyword, then made unique against inventory. They need editorial/URL review. Output folder must be new/empty: the tool refuses to overwrite evidence.

The script does not accept search-volume inputs. Keep metrics in a separate cited source if using them for an editorial review; never invent them. Missing metrics do not prevent planning by a declared business priority.

## v0.3 intake and reporting gate (current)
The original v0.2 executed artifacts remain unchanged. Old inputs still parse but now produce a limited generic-framework report instead of an implicitly prioritized queue. `business_priority` may be omitted/null (unknown), or 1–5. Existing `project`, `audience`, `goal` are labels, not a substitute for structured business answers.

`business_context` is an optional object. Fields: industry, audience, geography, language, business_problem, primary_objective, objective_tradeoffs, brand_position, competitive_position, lifecycle, brand_lifecycle, product_lifecycle, website_stage, conversion_definition, resources, constraints. Each answer is `{status: supplied|assumed|unknown, value: string|null, source_ids: [source ID]}`. Supplied answers require at least one known source ID; assumed answers must remain marked as assumptions. Unknown answers use null/empty value. Sources establish traceability, not truth. Synthetic sources remain fictional. `primary_objective` is awareness/consideration/conversion/retention/other. Geography/language use the exact market/language tokens of intended SERP context (e.g., US/en). Other fields are free text; “none” is a valid explicit constraint answer.

Missing/unknown answers do not hard-fail. Invalid types/status/source IDs do. Report modes: tailored (essential business context ready), industry_general (industry supplied but essential context incomplete), generic_framework (industry not supplied). Separate `commissioning_status` is limited/context_ready: industry, audience, geography, language, problem, objective, lifecycle, resources and constraints must be supplied; positioning must at least be explicitly assumed; conversion requires a supplied conversion_definition. Optional tradeoffs/site stage never block a limited report. No industry facts are inferred from the industry label.

Each keyword can supply `brand_scope`: brand/nonbrand/competitor/unknown; `funnel_stage`: awareness/consideration/conversion/retention/navigation/unknown; `priority_evidence`: `{source_id, objective, rationale}`. A known priority, brand role, funnel stage and objective-matching rationale are required for prioritized commissioning. These are analyst statements, not empirical demand. Conflicting duplicate context also fails reconciliation.

Inventory can include `coverage_review: {result: gap|covered|unknown, source_id, detail}`. A mapping alone yields review_existing; covered yields retain; gap plus business/priority gates can yield an update proposal. Gap details must describe actual supplied content evidence for real work; a source ID does not independently verify the assertion. Updates are not executed. Mixed or conflicting intent can still defer despite a page review.

`work_items` consolidate identical targets across separate groups without declaring a keyword cluster. Scaffolds use one section per target. `business_priority` is null when a gate prevents using it; `supplied_priority` preserves the user's original value. Work-item order and group IDs do not establish a priority ranking. `guidance` is explicitly editorial heuristics, not industry research. Reports expose answers, assumptions, missing fields and up to three next unanswered questions. Resources are free text: the helper cannot parse total editorial capacity, so an editor must estimate review/update effort before scheduling.

中文：新契约允许缺失业务答案并输出通用参考；只有格式不一致、错误来源等无效输入才报错。行业已知但问题/目标未知时报告为 industry_general，仍有参考价值；行业未知为 generic_framework。用户自述不等于核验事实。现有页映射只能触发 review_existing；有覆盖证据则 retain；有缺口证据、业务上下文和目标关联优先级才可提出 update。结构化答案和实际例子见 [intake-case](../examples/intake-case/)。

Brand/product lifecycle can differ: use brand_lifecycle and product_lifecycle separately when needed; lifecycle is the shared planning context, never inferred from website_stage. 品牌与产品阶段不同则分别填写 brand_lifecycle 和 product_lifecycle，不能用网站年龄推断。
