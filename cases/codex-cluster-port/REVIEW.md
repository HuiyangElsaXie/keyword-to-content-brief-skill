# Independent review: Codex cluster port

Status: **needs_human_review**. Synthetic procedure demonstration, not SEO outcome evidence. No external APIs, actual Google results, article writing, publication or live links were verified.

## Result

Latest reviewed deliverables: `final2-awareness/` and `final2-conversion/`. Prior `first-*` and `final-*` folders are preserved historical evidence.

Canonical intake check: both controlled cases qualify as tailored to their fictional supplied context, with no missing commissioning essentials and explicitly assumed positioning. This is not evidence of a real business or market. `awareness.intake-gate-check.json` and `conversion.intake-gate-check.json` record the actual old-helper gates: two candidate new pages within the stated capacity; navigation remains `/login` review and mixed intent remains deferred.

33 independent Python tests pass in `new-port-final2-tests.txt`. Node parses and runs the map script against a minimal DOM, and checks cards, graph nodes, detail selection, search, role filtering and keyboard selection (`map-dom-final2-results.json`). This is not browser or visual QA: existing Chromium could not start because its socket creation was denied; see `browser-blocker.txt`. No screenshot was generated or claimed.

The independent agent followed the new SKILL/routing, explicitly mapped the old nested intake to the new schema, wrote context-specific editorial direction, then ran the real CLI for both cases. The outputs are usable planning handoffs with substantial agent additions, not a proof that the deterministic helper can research or write completed articles.

## Expected versus actual matrix

| Check | Expected | Actual |
|---|---|---|
| Same input queries | Hold keyword/query evidence constant across contexts | Five identical queries and snapshot sets in both cases |
| K1/K2 | One checklist candidate from 8 shared synthetic URLs | page-001 retains K1 and K2 |
| K4 | Separate commercial job | page-002 comparison scaffold with agent-authored direction |
| K6 navigation | Destination review, not article commission | page-003 review_only, null word target; original `/login` inventory mapping retained in source intake but not imported by new helper |
| K7 mixed/no snapshot | Resolve intent before production | page-004 review_only, null word target and provisional evidence |
| Awareness substance | Explain sequence and ownership | Owner/due-date/status checklist, handoff stages, educational adaptation next step |
| Conversion substance | Assess fit and define exact event | Requirement/evidence/question table, unsupported capability blockers, conditional walkthrough CTA, unique completed request event; click explicitly not completion |
| Unknown volume | No invented zero or estimate | Every candidate/page volume is null |
| Counts | Separate plan/scaffold/review/article | 4 architecture nodes; 2 actionable planning scaffolds; 2 review-only nodes; 4 generated scaffold files, of which 2 contain agent editorial direction; written/published/implemented metrics null |
| Full writer | No fabricated articles | No writer invoked; zero articles created by this run; scorecard's wider unobserved article inventory remains null |
| Artifacts | JSON, Markdown, local HTML, briefs, scorecard | Each case has 9 files: plan JSON/MD, map HTML, four scaffold/brief handoffs, scorecard JSON/MD |
| Replay | Saved input authoritative | map, execute --mode briefs, and scorecard commands exit successfully against final saved plan |
| Context evidence | Preserve qualification and source | Positioning remains an assumption; context source S1/date/locator carried in business_context_provenance |
| Missing context | No false tailored claim | Generic-framework warning; agent applies canonical report gates outside helper |
| Safety | No network or destructive overwrite | Escaping, JavaScript URL rejection, traversal, tampered-plan and nonempty-output tests pass |

## First-pass findings and real revisions

1. Initial code review identified navigation/mixed nodes receiving article word budgets, navigational grouping/pillar risks, synthetic evidence labelled only `supplied_top10`, and generic text being described as briefs. The author changed these to review-only/null word targets, non-navigation pillar preference, synthetic labels, and explicit scaffolds. The first successful paired outputs remain unchanged under `first-awareness/` and `first-conversion/`; code was being revised during their generation, so they are not asserted to reproduce every earlier code-review finding.
2. Initial mapped input omitted a new required `collection_method`; the actual CLI rejected it. Original inputs and errors are preserved as `*.schema-first-input.json` and `first-*-command.txt`. Corrected inputs explicitly declare the simulated Google-top-ten shape, while fictional=true and synthetic sources make clear these are not captured Google observations.
3. First independent new-port test run: 27 tests, two failures for accepting future capture/metric dates. See `new-port-first-tests.txt`. Author added date validation.
4. First date fix used local date and rejected current UTC fixtures near a timezone boundary. Actual failures remain in `final-*-command.txt`. Author changed validation to UTC; rerun outputs are in `final-*-retry-command.txt` and `final-*/`.
5. Plain first scaffolds had generic structures. Agent-enriched inputs add sourced fictional reader jobs, specific H2/H3 directions, useful checklists/fit tables, evidence gaps, permitted next actions and acceptance checks. They remain human-review handoffs, not approved final copy.

6. Parent review identified buried authored outlines and misplaced link headings, plus unreviewed automatic links to navigation/mixed nodes. Author corrected the renderer and link graph. `final2-*` regenerations preserve older folders; the independent agent read both actual checklist briefs and confirmed supplied structures are prominent, link headings immediately precede their links, and provenance is an appendix. Final test expansion covers all-review graph semantics.

## Editorial judgment and remaining limits

- Awareness versus conversion differs in the actual work assigned to the writer, decision criteria and next action, not just headings or the objective label. The awareness checklist teaches responsibility; conversion asks the reader to qualify fit and unanswered requirements. Neither claims time savings, superiority or improved conversion.
- The new helper is not the old inventory/capacity commissioning gate. The controlled agent run uses the old intake as its source of inventory, qualification and a three-brief cap. It does not authorize replacing `/login` with the helper's generated placeholder path or building a page for mixed intent. Review-only map nodes and proposed links are architecture records, not publishable instructions.
- Final2 suppresses automatic links to both review-only nodes. Two proposed reciprocal links connect only the checklist and comparison planning pages. Review nodes remain visible and listed as review_pending_unlinked; they are excluded from orphan/reachability success checks. An all-review test reports null reachability rather than false success. Human review should still keep only a justified reader journey; no link was implemented and no crawl verified a destination.
- Existing-page content is not audited. S2 contains URLs only, so no competitor gap can be claimed. Pillar selection uses the supplied seed rather than unknown volume.
- Synthetic tests check the input contract and guardrails, not authenticity of self-reported sources. A maliciously mislabelled real-world export still requires analyst verification.
- Actual Google capture, DataForSEO/GSC/Ads, external article writers and PDF integrations remain optional and not live-verified. The available execution fallback is brief scaffolds plus agent editorial direction and a planning scorecard.
- Browser rendering/click behavior requires a future permitted browser check; only static security and Node minimal-DOM functionality were validated here.

## Reproduce

From repository root:

    python -m unittest discover -s tests -p test_cluster_port_truth.py -v
    python scripts/cluster_workflow.py plan --input cases/codex-cluster-port/awareness.agent-enriched-input.json --out NEW_AWARENESS_DIRECTORY
    python scripts/cluster_workflow.py plan --input cases/codex-cluster-port/conversion.agent-enriched-input.json --out NEW_CONVERSION_DIRECTORY
    node cases/codex-cluster-port/check_map_dom.cjs

Use a fresh directory on each CLI run. Existing evidence is intentionally not overwritten.
