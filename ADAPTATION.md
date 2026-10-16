# What was actually adapted

Source pin and full license: [ATTRIBUTION.md](ATTRIBUTION.md). This is a narrower working derivative, not only a README reference.

| Upstream source section | Retained concept | Implemented adaptation | Evidence |
|---|---|---|---|
| SKILL Step 1 expansion/deduplication | Clean keyword candidates before planning | Supplied list only; Unicode/whitespace normalization, retained alias IDs, conflicting duplicates rejected; no fabricated 30–50 expansion | plan_keywords.prepare; duplicate tests |
| SKILL Step 2 / methodology scoring | Shared top-10 organic URLs; 7/4/2 thresholds | Same thresholds explicitly attributed; exact context compatibility and 10 unique URLs required; every pair in a merged group must reach 7 | overlap + plan; boundary, incomplete, context and chain tests |
| Methodology URL normalization | Compare result URLs rather than word similarity | Preserve scheme, meaningful queries and path case; remove fragments/known tracking only, no assumed canonicalization | norm_url; query/case tests |
| Methodology skip rules | Reduce unnecessary work | Omitted assumed overlap and long-tail shortcuts; compute every pair of supplied records, unknown remains null | pairs output, unknown-evidence tests |
| SKILL Step 3 intent | Use intent to avoid inappropriate pages | Supplied reason required, mixed intent visible and deferred, navigational queries retained in disposition report | plan decisions + case review |
| SKILL Step 4 architecture/cannibalization | One primary page for related demand | Match inventory before commissioning; conflicting targets defer; deterministic complete-link greedy groups, one-new-page cap and business priority without volume | inventory, cap, path collision tests |
| SKILL Step 5 links | Contextual internal links | Editor proposes only relevant links to known/planned paths; no fabricated minimum links or forced hub/spoke scale | final case briefs |
| SKILL Execution fallback briefs | Briefs for writer handoff | Helper generates clearly labeled scaffolds; actual agent completes reader job, outline, evidence needed, claims gates and review | agent-run first/final output |
| SKILL scorecard | Review output quality | Contract tests + factual/editorial self-review, not an SEO effectiveness score | tests, evals and case review |

## Deliberately omitted
Live SERP acquisition, DataForSEO/MCP paid calls, automatic expansion, volume-based priority, auto-post writing/publication, interactive map template, FLOW prompts, cross-skill installation, redirects and traffic forecasts. No upstream Python scripts or HTML templates were copied. Only the three explicitly listed reference files are vendored unchanged.

## Limitations of the adaptation
The greedy complete-link grouping is deterministic, not a globally optimal cluster solution. Explicit intent and inventory mappings are analyst judgments; the helper cannot audit page contents. A complete snapshot makes a new-page proposal eligible but does not establish business demand. Updates also consume editorial capacity. Snapshots from different dates/markets/languages/devices are never compared automatically. Current-case reproducibility is not cross-model robustness or production validation.


## v0.4: selected module port to Codex

| Pinned upstream component | Treatment and actual implementation |
|---|---|
| Seed expansion and strategy import | Codex agent may use available authorized search to discover candidates or read an explicitly supplied strategy; candidates retain source and inferred/observed status. Helper consumes prepared JSON; it does not perform live search or import arbitrary tables automatically. |
| SERP overlap method | Retain 7/4/2 shared-URL relationship thresholds as upstream heuristics; require complete comparable supplied Google top-ten organic evidence, preserve missing/exploratory status and prohibit invented metrics. |
| Hub/spoke architecture and link matrix | Produce structured plan and proposed links. Business purpose can change brief goal/rationale; counts and word targets remain configurable heuristics, not Google requirements. |
| cluster-map.html | Exact upstream template preserved as a reference. Local self-contained renderer is rewritten for escaped data and safe interaction without external CDN dependencies; do not claim byte-identical visualization. |
| Execution workflow | Implement the original briefs fallback and artifact status/scorecard. Optional full article writer, automatic article updates and publishing are not implemented or authorized by a plan. |
| Claude-specific commands, plugin-root launcher and tools | Replace with Codex skill instructions and actual local helper commands. No stale ~/.claude or CLAUDE_PLUGIN_ROOT command is presented as runnable in the adapted entrypoint. |
| seo-plan/content/schema/google/dataforseo, FLOW and claude-blog | Explicit optional capabilities; runtime detection/permission required. Their prompts, APIs and claimed outcomes are not silently inherited. |
| Original scorecard | Separate planned, briefed and actually written content. Artifact integrity is not live-site linking, traffic or ranking validation. |

New project requirements include business-specific questions and prior-background reuse, requested by Huiyang Xie. This is transparent requirements/implementation credit, not a claim that those ideas were invented here. Existing earlier fixtures and output evidence remain preserved. Upstream exact source is retained as reference content, not instructions to execute without review.

## Existing-site/context repair (2026-10-16)
The real-site validation exposed generic new-page placeholders, automatic links and commercial=comparison defaults despite an existing-site brief. The local planner now receives structured inventory and coverage assessments, consolidates same destinations, gates new-page proposals, adapts recruitment portfolio templates and carries supplied next actions through briefs. These are original adaptation changes; the pinned upstream snapshot remains unchanged. Existing page facts still need supplied evidence and editorial review, not inferred demand. Private personal-site test inputs are not included in this repository.
