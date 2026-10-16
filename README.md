# Keyword to Content Brief

[本轮真实 Sol 6.1 场景、首稿与审阅 / agent behavior evidence](cases/agent-behavior-2026-10-16/README.md) — 合成输入，不代表真实调研或业务效果。

**Purpose: plan evidence-led keyword clusters and reviewable content briefs in Codex.** Start with a seed, URL, strategy or permitted exports. The agent researches where authorized tools are available, qualifies evidence, designs pillar/spoke architecture and links, and reviews the plan, interactive map, individual briefs and planning scorecard. Python renderers stay offline; keyword discovery is an agent task, and no built-in search-volume, live SERP or Search Console connector is claimed.

## Start in one minute

Keep the full repository and provide the nested SKILL.md entrypoint explicitly. Copying only its child folder omits root scripts/docs/cases and attribution resources; installation/discovery depends on the host.

[Current example plan](cases/inventory-context-repair/final-marine-existing/cluster-plan.md) · [Current brief scaffold — needs editorial completion](cases/inventory-context-repair/final-marine-existing/cluster-briefs/page-001.md) · [Earlier completed editorial report — historical example](examples/intake-case/final-report.md) · [Current behavior review](cases/inventory-context-repair/REVIEW.md)

All linked examples use synthetic inputs. Earlier completed reports illustrate editorial handoff, not current CLI decisions or real demand.

| What you have / route | Smallest useful next step | Expected result and limit |
|---|---|---|
| Only a URL or seed; Codex/AI conversation | Read [the skill](skills/keyword-to-content-brief/SKILL.md), supply the URL/seed, audience, objective and any known page inventory. Ask it to reuse permitted context and identify missing evidence. | Agent research depends on actual authorized tools. Without them, use supplied content and label candidate ideas provisional; a URL is not a keyword/SERP export. |
| Existing keywords, pages or search evidence; Codex/AI | Supply the permitted files and source/date/market/language/device details. Ask for inventory-first page decisions and reviewable briefs. | The agent maps the documented input, reviews sources and finishes editorial work. General web results do not establish an ordered Google organic top ten. |
| Python offline; structured evidence already available | Follow [the JSON template/questionnaire](skills/keyword-to-content-brief/QUESTIONNAIRE.md) and [offline helper commands](#run-the-existing-offline-helper). Use a fresh output directory. | Evidence decisions and unfinished brief scaffolds; no automatic search, crawling or finished article. The [cluster renderer](docs/CODEX-CLUSTER-PORT.md) has a separate schema. |

Example request: “Use the skill on this URL and my supplied page inventory. Plan for the stated audience and objective, keep missing SERP evidence unknown, and return page decisions plus briefs for review. Do not publish.”

Keep the repository structure available. Other AI hosts require their own tool/path checks; this README does not certify cross-host compatibility.

Report usefulness depends on the quality, completeness and scope of the supplied data. Missing evidence must remain explicit; outputs are proposals for human review, not proof that a page needs changing or that a live defect exists. Maintained for personal use and continuously updated as the workflow develops.

**Everyday/client use:** If a client supplies a permitted keyword export, page inventory and compatible search-result evidence, this workflow can help prepare a planning report and writer brief. Map inputs to the documented schema, check provenance and missing fields, and review conclusions before client delivery. Drafts still require review; everyday use does not make this a fully validated production service or settle the pending license for new contributions.

**An evidence-to-editorial-handoff adaptation of [AgriciDaniel/claude-seo's seo-cluster](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-cluster/SKILL.md), v2.4.2, pinned at 4b99de2f7de7e7d5247042e5fb5b4ea9368ef734.** Upstream is MIT, Copyright (c) 2026 agricidaniel; metadata also credits Lutfiya Miller. [Exact source/license](upstream/claude-seo/) · [Attribution](ATTRIBUTION.md) · [Concrete changes](ADAPTATION.md) · [中文](README.zh-CN.md)

New original contributions are **owner-license-pending**, not yet an MIT grant. Personal use is the project purpose, not a restriction on upstream MIT rights.

Current behavior: [inventory/context repair cases and independent review](cases/inventory-context-repair/REVIEW.md). Earlier paired examples below preserve the prior version and should not be replayed as current derived plans.

## Codex full planning module and retained offline helper

Read [the Codex skill](skills/keyword-to-content-brief/SKILL.md) → [routing and evidence gates](skills/keyword-to-content-brief/references/codex-cluster-routing.md) → [capability guide and commands](docs/CODEX-CLUSTER-PORT.md). The selected seo-cluster planning workflow is ported as Codex agent instructions plus a separate offline output module. It covers expansion/strategy mapping, qualified overlap, intent, hub/spoke design, templates, link matrix, interactive map, brief handoff, planning scorecard and map regeneration. Article production and publishing are not implemented.

The two paths are deliberately distinct:
- Full planning: an agent maps researched/supplied material into the new module contract and reviews its architecture outputs. Business intake still applies; a complete output bundle does not mean the evidence or editorial work is complete.
- Existing supplied-evidence helper: plan_keywords.py and its original input contract remain available for pair evidence, conservative grouping, page decisions and unfinished brief scaffolds. The old CLI is not silently replaced or described as a full live SEO agent.

Generic web discovery is not ordered Google top-ten organic evidence. Only a qualified export/authorized adapter can establish the required engine/query/market/language/device/date/order. Unsupported overlap and volume stay unknown; GSC impressions are not market volume. Expansion counts, word budgets and link density are adjustable planning heuristics, not Google requirements. Optional Ads, GSC, DataForSEO, writer/blog and Google/PDF integrations require actual runtime discovery and authorization; none is bundled.

### Executed paired example
Same five fictional keywords, different business objectives: [awareness brief](cases/codex-cluster-port/final2-awareness/cluster-briefs/page-001.md) teaches onboarding responsibilities; [conversion brief](cases/codex-cluster-port/final2-conversion/cluster-briefs/page-001.md) screens workflow fit and defines a completed walkthrough-request event. [Actual plan/map/scorecard bundle](cases/codex-cluster-port/final2-awareness/) · [Independent review and limits](cases/codex-cluster-port/REVIEW.md). No real search volume or business effects are invented.


## Existing websites and recruitment portfolios

Supply existing-page inventory/mappings before treating candidates as new pages. The planner distinguishes retain, review_existing, defer and new_proposal; missing inventory is not an empty site. Existing URL review work is consolidated and coverage needs a cited supplied assessment. A new proposal requires complete inventory plus a documented gap and business rationale; it is still not permission to publish or proof of search demand.

For recruitment portfolios set business_context.content_purpose to recruitment_portfolio. A commercial reader job can be a career overview or evidence case, rather than automatically a comparison article. The brief preserves supplied next_action and keeps conversion measurement distinct. See [inventory contract and usage](docs/INVENTORY-CONTEXT.md).

## Existing evidence-analysis path

Turn supplied keywords, organic-result snapshots and an existing-page inventory into a small, reviewable content queue: which queries share a page, which existing page to review or retain, whether a verified gap supports an update, which new page fits capacity and which decisions need more evidence. Then use the skill to turn the machine plan into a writer-ready brief. It is useful for:
- A small SaaS team's monthly content handoff when only one new page can be commissioned.
- Reviewing possible duplicate content before adding another guide.
- Separating editorial assumptions, supplied search evidence and claims still needing verification.

The new work is the conservative offline evidence contract, complete-link grouping, inventory-first update/new/defer decisions, capacity handling, claim-gated briefs, and preserved review trail. The upstream overlap heuristic is credited, not claimed as new.

## Business questions first (v0.3)
The agent reuses your brief, asks a small batch of missing questions, then branches by objective, lifecycle, keyword role and existing coverage. Industry, audience/market/language, concrete problem, brand/competitive positioning (evidence versus assumptions), primary objective, conversion event when relevant, resources and constraints affect the report. Brand lifecycle, product lifecycle and website age are distinct.

If you cannot provide a concrete problem, an **industry-general report still has reference value**. It organizes supplied evidence, possible funnel uses, coverage and validation questions without pretending to know your company's priorities. Unknown industry yields a generic framework. A tailored report requires sufficient essential context; complete context alone does not prove search demand or authorize changes. [Adaptive intake EN/中文](docs/business-intake.md) · [New executed cases](examples/intake-case/README.md).

Existing-page mapping now means review_existing, not automatic update; supported coverage can mean retain. Same-target work is consolidated without claiming a keyword cluster. Missing priority evidence produces no fabricated ranking. The original v0.2 case outputs are historical, unchanged.

## Inputs → outputs

Input: structured business_context answers with supplied/assumed/unknown status and sources; keyword IDs, intent with reasons, business priority, source IDs, optional top-10 organic URL snapshots (date/market/language/device), existing pages and new-page capacity. No search volume is invented or required. See [input contract](docs/input-contract.md).

Helper output: pair evidence matrix; alias-preserving groups; page decisions with reasons/provenance; **brief scaffolds**. Agent/editor output: full reader-job/outline/evidence/claims/link briefs, actual review, retained first pass and corrected final pass. The Python helper alone does not write a finished brief.

## Two ways to use it

1. **With an AI:** provide [the skill](skills/keyword-to-content-brief/SKILL.md), your existing brief and evidence. The AI reads first, asks up to three missing questions at a time, accepts your answers (including unknown), maps them to the input, then analyzes, writes and reviews the report.
2. **With the CLI:** copy [INPUT.template.json](skills/keyword-to-content-brief/INPUT.template.json), edit JSON in a text editor (no Python changes), and run the command in the [fillable bilingual questionnaire](skills/keyword-to-content-brief/QUESTIONNAIRE.md). The noninteractive helper automatically chooses tailored / industry_general / generic_framework and outputs next questions and unfinished scaffolds; an AI/editor completes the report.

The questionnaire includes exact field mapping and links to the [canonical intake](docs/business-intake.md). It is **not automatically imported**. Explicit unknown answers use JSON null and suppress repeat questions; omitted fields can generate next questions. The template is runnable but deliberately fictional, with one placeholder keyword and no search-result evidence; replace those before real use. Always write to a fresh/empty output directory. [Template checks](docs/usage-template-checks-20261016.md).

For the AI flow, reuse relevant authorized context actually accessible in the current chat, supplied brief or host memory first. Briefly state the known business/audience/objective and critical source/date/confidence; distinguish inference, stale data, conflicts and other-client material. Latest user instructions win. If sufficient, proceed with authorized read-only analysis; ask only gaps/conflicts/time-sensitive essentials. No global or cross-chat access is assumed; without memory use the brief. Memory cannot replace SERP/crawl/Search Console evidence or grant permissions. Do not store user/client memory in this repository or templates. CLI still reads JSON only. [Bilingual instructions and fictional example](skills/keyword-to-content-brief/QUESTIONNAIRE.md#reuse-accessible-context-first--先复用可访问的上下文).

## Run the existing offline helper

Python 3.10+, standard library only; no paid account, network or install required.

```sh
python scripts/plan_keywords.py examples/intake-case/input.json --out /tmp/keyword-plan-new
python -m unittest discover -s tests -v
```

Use a new or empty output directory. Existing evidence is never overwritten by the helper. To complete the editorial work, ask an agent to read [the skill](skills/keyword-to-content-brief/SKILL.md), the contract and your input, run the helper, write a full first brief, review it and preserve final corrections. Copying only SKILL.md is insufficient: keep this repository's relative scripts/docs/source links intact. No live-service access is required by this workflow.

## Historical v0.2 fictional case (preserved baseline)

[Request](examples/studio-case/REQUEST.md) · [raw input](examples/studio-case/input.json) · [executed case and run log](examples/studio-case/agent-run/) · [first output](examples/studio-case/agent-run/first-output.md) · [review](examples/studio-case/agent-run/review.md) · [final output](examples/studio-case/agent-run/final-output.md)

MossNote Studio is fictional. An agent ran the skill from ten supplied rows (nine unique queries), generated the page plan and wrote complete new-page and existing-guide briefs. The fabricated URL sets exercise overlap, an exact-normalized duplicate, a market mismatch, missing evidence, mixed/navigational intent and limited capacity. They are not actual Google results. No real competitor, product-performance or demand claims are supported.

## Tests and honest limits

The original baseline had 49 offline tests: evidence/decision tests, adaptive intake/report gates and 4 retained v0.1 validator checks. They cover threshold boundaries, context mismatches, duplicate conflicts, non-transitive grouping, inventory conflicts, capacity, unsafe URL credentials, query preservation and overwrite prevention. [Evaluation scope](evals/rubric.md).

Neither helper collects keywords or audits a live site. The full Codex route can research candidates with available authorized tools; it does not prove search demand, rank pages, predict traffic, independently verify every product claim or publish anything. Intent/inventory mappings need human judgment; one complete snapshot is still weak evidence. Market/date/device/language mismatches remain unknown. Final briefs remain needs_human_review. For real use supply current, permitted exports, actual page content and verified product facts.

[Legacy v0.1](legacy/v0.1/) is retained unchanged for comparison; its prefilled three-keyword example and old attribution statements are historical, not the current workflow. Existing root examples/input.json and scripts/validate_plan.py remain legacy compatibility fixtures. [Pre-publication checklist](REVIEW_BEFORE_PUBLIC.md).

To reproduce the preserved v0.2 execution, use repository commit `75b34eb9da534d967170b2a92d5f08e0b37c93b8` and its original helper. The current v0.3 helper intentionally gates old inputs and will not reproduce v0.2 decisions. No old execution output was replaced.
