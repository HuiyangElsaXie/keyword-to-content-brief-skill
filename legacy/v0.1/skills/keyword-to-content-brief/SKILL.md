---
name: keyword-to-content-brief
description: Turn keyword evidence and existing-page context into a capacity-aware page map and content brief.
---
# Inputs
Business goal, target audience, keyword list, intent evidence, existing pages, available capacity and data provenance. Search volume and SERP evidence may be absent. Mark them unknown; never fabricate them.

# Decisions
1. Separate observed search evidence from editorial hypotheses and synthetic fixtures.
2. Group by reader task, not lexical similarity alone. Check live SERP overlap only when real approved data is available; otherwise label grouping as provisional.
3. Review existing pages before proposing new ones. Assign update, new, merge-review, or defer with a reason.
4. Prioritize business relevance, evidence confidence and available capacity. Do not call a subjective priority a revenue forecast.
5. Produce a brief for the highest-priority approved page: reader question, promise, outline, required evidence, internal links and acceptance checks.
6. Flag likely overlap for human review; a shared keyword alone does not prove cannibalization.
7. Return the page map, decision rationale, one brief, missing evidence, and validation plan. Never publish pages or promise rankings.

# Outputs
A page-decision table, one evidence-bounded brief, explicit assumptions, and next validation steps. Reject contradictory assignments and capacity overruns with scripts/validate_plan.py.
