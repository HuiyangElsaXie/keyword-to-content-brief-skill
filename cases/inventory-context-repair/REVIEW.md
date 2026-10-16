# Independent inventory/context repair review

2026-10-16 UTC. Independent AI review, not human sign-off. All fixtures and URLs in this case directory are fictional. No private site data was copied here. No network calls, remote writes, site publication, or deletion were performed.

## Result

21 independent inventory/context tests pass. The full repository suite passes: 122 tests. See repair-tests-final-check1.log and full-suite-final.log. Seven final fixture runs used the real CLI and all returned zero; see final-cli-runs.json. Plan, brief and scorecard JSON/Markdown were inspected, including their substantive next actions and templates.

- Two candidate queries explicitly mapped to one sufficiently covered destination become one retained review item, not two proposed articles.
- Distinct existing destinations remain separate review items with no automatic links, no production pillar/spoke assignment, no word budgets, no generic metadata replacement, and null graph reachability.
- Marine-industry reuse is protected just like portfolio reuse. An unmapped topic without sufficient absence evidence is deferred.
- Missing and partial inventories cannot establish an absent page, even when a gap statement is supplied. Missing inventory remains explicitly unknown.
- A complete inventory with a cited gap and business rationale preserves a new-page proposal. An explicitly empty, complete new-site inventory also supports such a proposal. These are proposals, never execution approval.
- Normalized URL aliases collapse. Conflicting sufficient/partial mappings remain review_existing. Duplicate inventory rows do not duplicate destinations.
- Lexical title/term matching is a review hint only. Semantic overlap, content coverage, cannibalization resolution and measured gaps are not established by exact-key duplicate counts.
- Recruitment portfolios get evidence/recruiter templates. Supplied next actions are propagated, editorial next actions take precedence, and conversion definitions remain separate.
- Missing SERPs, volume, publication/implementation and actual coverage remain null. Unknown mapping and gap source IDs are rejected. Supplied citations are not independent verification.
- The legacy mapping CLI route is exercised through an actual subprocess and saved-plan reconstruction.

## Preserved evidence and iterations

baseline-* outputs and baseline-cli-runs.json were captured before the implementation. baseline-script.sha256 identifies that script. The baseline emitted two comparison pages and two automatic links for the same existing portfolio destination. Original test_cluster_port_truth.py is preserved as a text backup.

first-repair-tests.log is an early implementation test run, not an original baseline: its initial strict defer expectation was corrected to allow a conservative lexical review hint. repaired-* outputs are an intermediate snapshot. repair-tests-graph-first.log and first-repair-distinct-existing-destinations preserve the subsequently exposed automatic-link and generic-metadata failures. final-* artifacts are the final actual CLI runs after those corrections. No historical outputs were overwritten.

## Compatibility and limitations

The old saved-plan loader reconstructs against current code. A historical saved plan may therefore fail equality checks after this behavior repair. Preserve it and regenerate from the original input plus explicit mapping into a new directory. Do not silently rewrite historical evidence.

This is an offline deterministic evidence-gate regression check. It does not establish real search demand, validate source authenticity, prove semantic coverage, or approve execution. The tests do not claim live-browser rendering QA.
