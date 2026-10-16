# Evaluation scope

## Automated evidence
Run `python -m unittest discover -s tests -v`. Twenty-one v0.2 tests exercise observable logic and failure cases; four original v0.1 tests are retained. Test results do not measure keyword quality, search intent accuracy, ranking, conversion, or content usefulness.

## Agent case evidence
Use examples/studio-case/REQUEST.md and raw input with the skill. Save initial plan and first complete writing output before review. Review merge evidence, context compatibility, aliases, inventory target conflicts, capacity, unsupported facts, link relevance and concrete writing guidance. Keep all actual corrections. Do not invent errors to make the review look more substantial. The checked-in agent-run directory records one real execution on fictional inputs, not a repeated benchmark or independent human evaluation.

Acceptance gates: all input IDs represented; no ungrounded demand or product metrics; no mixed-market merge; no transitive same-page merge; no capacity overrun; known inventory paths respected; full brief goes beyond a substituted keyword template; review status remains needs_human_review.

## What remains untested
Live SERP retrieval, export authenticity, age suitability, large datasets, real inventory matching, external platform installation, cross-model consistency, reader response and SEO outcomes. Pairwise computation is O(n²), designed for small supplied lists. The helper's contract is not a general hostile-input security audit.
