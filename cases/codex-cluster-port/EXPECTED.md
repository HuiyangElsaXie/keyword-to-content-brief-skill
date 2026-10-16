# Independent paired-context validation: expected behavior

Validator wrote these expectations before executing the new port. All inputs are synthetic. The same keywords are used in both contexts; their observed demand, actual rankings, volumes and commercial outcomes are unknown. Reserved `.example` URLs are fabricated comparison sets, not visits or retrieved Google results.

| Dimension | Expected behavior |
|---|---|
| K1/K2 checklist | Eight common fake URLs: demonstrate a same-page candidate with both input IDs retained, not a measured SEO success |
| K4 software comparison | Distinct commercial reader job; do not merge into checklist |
| K6 MossNote login | Navigation to a known entity; inspect supplied `/login`, no article |
| K7 onboarding automation | Mixed intent and absent SERP; defer automatic commission |
| Awareness context | Explain onboarding sequence, ownership and approval handoffs; neutral next educational action; no forced demo success metric |
| Conversion context | Assess fit for a notes/checklist workflow; explicit decision criteria and limitations; completed walkthrough-request submission is the specified event, never an inferred result |
| Counts | Page plans, generated writing briefs, and written full articles reported separately; zero written articles without actual writer output |
| Artifact scope | Plan JSON and Markdown, local interactive HTML, briefs, scorecard; no publishing or network calls |
| Evidence boundaries | General web and missing snapshots cannot be promoted to actual Google top-10; market/date/device mismatch blocks overlap inference |
| Security | Untrusted strings inert in HTML; no hidden CDN; dangerous URLs and traversal rejected or rendered inert; existing output preserved |

## Source trace

- `awareness.input.json`: validator-authored adaptation of repository `examples/intake-case/input.json`; source S1 identifies fictional business and source S2 fictional URL sets.
- `conversion.input.json`: same keywords and URLs, changed only stated objective, business problem, tradeoffs, defined conversion event, and objective-linked editorial rationale.
- Neither input contains real user data, competitor facts, volume, traffic, or observed outcomes.
- The independent agent will read the newly authored SKILL and follow its documented workflow, record commands and generated outputs, and evaluate substantive reader goals and rationale rather than headings alone.
