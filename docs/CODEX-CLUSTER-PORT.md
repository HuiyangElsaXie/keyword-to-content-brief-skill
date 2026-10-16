# Codex seo-cluster planning port

## Scope and attribution

This ports the selected **seo-cluster planning module**, not the entire claude-seo plugin, into Codex-readable instructions plus a local Python output module. Read [SKILL.md](../skills/keyword-to-content-brief/SKILL.md), [routing](../skills/keyword-to-content-brief/references/codex-cluster-routing.md), [business intake](business-intake.md) and [questionnaire](../skills/keyword-to-content-brief/QUESTIONNAIRE.md). Preserve the repository structure. A natural-language request such as “plan a cluster from this seed” is an agent task, not an installed `/seo` slash command.

Adapted from [AgriciDaniel/claude-seo seo-cluster v2.4.2](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-cluster/SKILL.md), commit `4b99de2f7de7e7d5247042e5fb5b4ea9368ef734`; original metadata credits Lutfiya Miller. Upstream MIT license and source are retained under [upstream/claude-seo](../upstream/claude-seo/). See [attribution](../ATTRIBUTION.md) and [adaptation record](../ADAPTATION.md). New original contributions remain owner-license-pending; this is not a blanket MIT grant for the repository.

## What is implemented, and by whom

- **Codex agent workflow:** authorized context reuse and adaptive intake; seed/URL research or strategy mapping; candidate expansion and intent review; evidence qualification; inventory/capacity review; architecture rationale; editorial brief completion; actual first/review/final trail.
- **New offline module, `scripts/cluster_workflow.py`:** validates explicitly mapped JSON, compares supplied compatible top-ten snapshots, builds conservative groups and deterministic provisional architecture, emits plan JSON/Markdown, self-contained interactive HTML, per-page brief scaffolds and planning scorecard JSON/Markdown. It supports saved-plan map regeneration, briefs-only execution and scorecard regeneration.
- **Existing offline module, `scripts/plan_keywords.py`:** unchanged separate entry point and schema for canonical intake gates, supplied-evidence pair decisions, inventory/coverage decisions, new-page capacity and brief scaffolds. See [input contract](input-contract.md).
- **Not implemented here:** network research inside either Python module, automatic arbitrary strategy/URL/questionnaire import, paid API adapters, account connections, live crawling, market-volume collection, article writing/resume/backfill, publishing, real production scorecards or Google/PDF reports.

“Full planning” means the agent plus renderer workflow. The renderer alone is not a full business analyst or writer. It does not check the actual page body, enforce business-context sufficiency, budget a production calendar, or know whether a supplied source is genuine. An arbitrary nonempty context object does not establish tailored status.

## Runtime routing

Discover the actual host tools for read/search/browser/shell. Use only tools genuinely available and authorized; do not invent callable tools or copy Claude wrappers, plugin root variables or home paths. If no search is available, use supplied material and label expansion as editorial hypotheses. If no shell is available, draft the same deliverables manually and disclose that the executable module was not run. Do not claim execution based on reading source.

Optional GSC, Ads, DataForSEO, external writer/blog, SEO quality/schema and Google/PDF integrations are **external and unverified until discovered**. They are not dependencies. Each requires its own permissions, tool-specific schema, permitted data use and budget where relevant. A provider mentioned in upstream text is not automatically installed. Do not install software, connect accounts or make paid calls merely to follow this guide. Article production is outside this port; `execute --mode briefs` only generates brief files.

## Evidence rules

A generic web search is discovery, not necessarily an ordered Google top-ten organic snapshot. For comparable overlap, supply an authorized export or actual adapter output preserving exact query, Google engine, market, language, device, capture date and ordered ten unique organic HTTP(S) URLs. Exclude ads, PAA and other modules. Analyst verification of engine, order, freshness, authenticity and source rights is still required. The parser validates shape, not truth. Non-Google or partial results must remain exploratory/incomplete/unknown, not complete.

The new module compares complete snapshots only when market, language, device and date match. Missing/mismatched evidence yields null overlap. Seven or more shared URLs is a credited same-page review heuristic; complete-link checks prevent transitive chain merges, and compatible intent is also required. Four to six suggests topic relationship; two to three suggests an editorial cross-link candidate. No observed evidence means no verified cluster. The provisional intent folders and hub/spoke links require relevance review.

Unknown volume is null, never zero by default. A supplied volume needs source/date/market and a source description explaining the metric definition and period. Do not put GSC impressions in volume: they describe observed first-party visibility, not market search volume. The renderer does not rank by volume; it prefers non-navigational/non-mixed candidates for the pillar, choosing the exact seed page where eligible, otherwise strongest measured connections then stable ID. Explain and review that structural default rather than calling it business priority.

## Inventory/context extension

See [structured existing-page input and mapping adapter](INVENTORY-CONTEXT.md). Inventory is unknown when omitted; older inputs remain readable but candidates without inventory/gap evidence now defer instead of implying new work. Supplied destination assessments and same-URL work consolidation do not establish SERP equivalence. Only new_proposal nodes can participate in automatic proposal architecture; existing reviews need no new paths, word budgets or links. Recruitment context and supplied next_action are carried explicitly. Historical case outputs record the earlier implementation and are preserved; use the new inventory-context repair cases for current behavior.

## New input contract: cluster-input-1.0

The new schema is separate from the old `INPUT.template.json`. No automatic conversion is performed. The AI maps the questionnaire explicitly and preserves evidence status/source/date/confidence in the editorial report and source descriptions. Do not convert an assumed or unknown business answer into an unqualified supplied fact.

Required top-level fields:
- `schema_version`: `cluster-input-1.0`.
- `project`, `seed`: nonempty strings.
- `fictional`: boolean; synthetic sources require true.
- `sources`: nonempty list of unique `{id, kind, description}`; kind is supplied or synthetic. Records are provenance assertions, not authentication.
- `candidates`: nonempty list, unique IDs and normalized keywords. Each has `id`, `keyword`, `intent`, `intent_reason`, `source_id`; optional `serp` and `volume` default to null. Intent: informational, commercial, transactional, navigational or mixed. Reconcile aliases before calling the new module; unlike the old helper it rejects normalized duplicates instead of preserving alias rows.

Optional fields:
- `business_context`: object of nonempty string values, such as audience, primary_objective, brand_position and conversion_definition. These are self-reported/unverified context labels, **not** the old structured status/value/source_ids objects. Omit unknown values or label their uncertainty plainly. This helper does not choose tailored/industry_general/generic_framework; the agent must apply the canonical intake gates in its report. It also does not implement the old inventory/capacity schema. Use the old helper when those machine gates are needed, and explain the reconciliation in the final report.
- `business_context_provenance`: optional map keyed by existing business_context field names. Each value is `{source_id, date, status, evidence_locator}`: source_id must exist; date is a nonfuture ISO date; status is confirmed, self_reported, assumption or unknown; evidence_locator is nonempty text identifying the supplied location. This preserves traceability, not independent verification. Do not invent dates to populate the map; if a date is unavailable, omit that entry and explain the gap in the report. With provenance the output business_context_status is provenance_supplied_not_independently_verified; without it, string context is self_reported_unverified, or unknown when absent.
- `settings`: candidate_target_min (30), candidate_target_max (50), pillar_words ([2500,4000]), spoke_words ([1200,1800]), sibling_link_limit (3), cross_link_limit (1). Counts are nonnegative integers; candidate minimum must be positive and no greater than maximum; word ranges are two positive ordered integers. Unknown setting names are rejected. These defaults are adjustable planning heuristics, not Google rules. A small candidate list produces a warning, not fabricated padding.

A complete `serp` object has `status: "complete"`, `query` matching the candidate keyword, `engine: "google"`, `collection_method: "google_organic_top10"`, `market`, `language`, `device`, ISO `date`, known `source_id` and `organic_urls` containing exactly ten ordered, normalized-distinct HTTP(S) URLs. The collection_method is a supplied evidence assertion, not proof of actual collection. Other statuses are exploratory, incomplete and unknown; those are not overlap-eligible. Optional `volume` is `{value, source_id, date, market}`, where value is finite and nonnegative. Explain metric definition/period in the cited source description; absence is null.

A candidate may also supply `editorial`: string fields title, meta_description, differentiation, reader_job and next_action; nonempty list-of-nonempty-string fields outline, key_points, acceptance_criteria, evidence_needed and evidence_source_ids. Referenced source IDs must exist. These carry agent-authored direction into the generated scaffold; their presence does not independently validate the writing. Navigational and mixed-intent pages remain review_only proposals with no article word target.

### Minimal fictional input

Save this as a new working file such as `/tmp/my-cluster-input.json`. It intentionally has no live evidence or volume; one candidate only demonstrates execution and triggers the expansion-target warning. It is not a real keyword-research result. Because it supplies no confirmed industry or complete intake, the agent report is generic_framework; the renderer only labels its string context self_reported_unverified. Its volume and overlap remain null. With no inventory or sourced gap, it defers production rather than proposing a new page.

```json
{
  "schema_version": "cluster-input-1.0",
  "project": "Fictional studio planning demonstration",
  "seed": "project handoff checklist",
  "fictional": true,
  "sources": [
    {"id": "S_DEMO", "kind": "synthetic", "description": "Fictional demonstration, 2026-10-16; generated candidate, not observed demand."}
  ],
  "business_context": {
    "audience": "Fictional small design studios; unverified demonstration context",
    "primary_objective": "awareness",
    "brand_position": "Assumed: practical education; not a verified competitive claim"
  },
  "candidates": [
    {
      "id": "K001",
      "keyword": "project handoff checklist",
      "intent": "informational",
      "intent_reason": "Analyst hypothesis: the reader wants a reusable checklist; no SERP confirmation.",
      "source_id": "S_DEMO",
      "serp": null,
      "volume": null
    }
  ]
}
```

## Executable commands

Run from the repository root with Python 3.10+; only the standard library is used. No installation, network or paid service is needed. Use a new or empty output directory each time; existing evidence must not be overwritten.

```sh
python scripts/cluster_workflow.py --help
python scripts/cluster_workflow.py plan --input /tmp/my-cluster-input.json --out /tmp/my-cluster-plan-new
python scripts/cluster_workflow.py map --plan /tmp/my-cluster-plan-new/cluster-plan.json --out /tmp/my-cluster-map-new
python scripts/cluster_workflow.py execute --plan /tmp/my-cluster-plan-new/cluster-plan.json --mode briefs --out /tmp/my-cluster-briefs-new
python scripts/cluster_workflow.py scorecard --plan /tmp/my-cluster-plan-new/cluster-plan.json --out /tmp/my-cluster-scorecard-new
```

`plan` writes `cluster-plan.json`, `cluster-plan.md`, `cluster-map.html`, individual `cluster-briefs/page-NNN.md`, `cluster-scorecard.json` and `cluster-scorecard.md`. `map` writes only HTML; `execute` writes individual brief scaffolds plus scorecards; `scorecard` writes only scorecards. The saved plan retains evidence_input and is validated by rebuilding it: editing derived plan fields directly is rejected. Change input and regenerate instead. Keep editorial judgments and completed briefs as separate first/review/final artifacts rather than patching the machine plan invisibly.

The HTML includes local SVG, keyword search, role filter, selectable nodes/cards and page/link details. No CDN, network request or external browser library is required. Open locally and inspect the interactions; file generation alone is not browser QA. It represents proposed architecture, not crawl-verified site structure.

For the original path, use its original input schema:

```sh
python scripts/plan_keywords.py examples/intake-case/input.json --out /tmp/keyword-plan-new
python -m unittest discover -s tests -v
```

## Complete the human-readable deliverable

1. State business context, source/date/confidence, unresolved conflicts and report mode. Reuse accessible authorized context first; ask at most three missing essentials, never the whole worksheet again. Known industry with incomplete essentials still supports a useful industry-general report; unknown industry yields a generic framework.
2. Distinguish observed queries/results, synthetic fixtures, inferred intent and generated candidates. Show overlap evidence and unknowns. Review existing page coverage and total production/review capacity before selecting work; numeric new-page capacity is not approval for updates.
3. Review the renderer's default pillar, paths, templates and links. Navigational entries are destination-review proposals, not an instruction to commission articles. Contextual relevance wins over link counts; word targets are editable budgets.
4. Complete every selected brief with page-specific reader job, title/meta, H2/H3 outline, factual key points, source needs, forbidden claims, relevant link placement and acceptance criteria. The generated generic structure is a scaffold, not a finished editorial handoff.
5. Preserve a first pass, record actual review findings and retain final corrections. Mark final work needs_human_review unless a human actually approved it.

The scorecard measures proposed architecture and generated scaffold counts only: planned links/incoming/outgoing counts, planned orphan/reachability checks, duplicate primary keywords and provisional pages. Article/publication/image/implemented-link/actual-coverage metrics remain null. Standalone scorecard regeneration does not inspect whether brief files exist; generated-brief count remains unknown for that command. It is not an upstream post-publication SEO quality audit or evidence of traffic results.

## Documentation verification

On 2026-10-16, the JSON block above was extracted and parsed, then plan, map, execute --mode briefs and scorecard each ran successfully with exit code 0 against fresh temporary output directories. Command help and local documentation link targets were checked. This verifies the documented local commands and sample; it is not the separate seeded agent case, browser interaction QA, live Google evidence or production validation.

### Final handoff and review-only nodes

Supplied editorial outlines and key points appear as the primary brief structure; generic scaffold text is used only when those fields are absent. Provenance stays visible in an appendix. Navigational and mixed-intent review-only nodes remain visible for a decision but receive no automatic content-architecture links or article word targets. The scorecard separates eligible planning graph checks from pending review nodes; an all-review input does not claim a reachable content architecture.

Map rendering uses local embedded code and escaped data, without remote libraries. Independent tests can validate its JavaScript and interactions in a minimal DOM; a blocked browser launch is explicitly not counted as visual/browser QA. See the actual test record in cases/codex-cluster-port/REVIEW.md.
