# Usage template checks — 2026-10-16

Scope: documentation and template additions only; existing implementation and evidence were not edited. Executed locally with the repository's current helper. Test derivatives are fictional and remain in a fresh temporary directory; these are schema/behavior checks, not real business research or finished client reports.

## Results

```text
PASS: all 16 canonical business fields represented in template and exact questionnaire mapping.
PASS template: mode=generic_framework; commissioning=limited; next_questions=0; new_pages=0.
Command: /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python scripts/plan_keywords.py /workspace/scratch/100764731f7e/marketing-portfolio-drafts-20261016/keyword-to-content-brief/skills/keyword-to-content-brief/INPUT.template.json --out /tmp/keyword-usage-verification-z3su0oqc/template
Output: 1 unique keywords; 0 new page(s); review pending
Directory: /tmp/keyword-usage-verification-z3su0oqc/template
PASS unanswered: mode=generic_framework; commissioning=limited; next_questions=3; new_pages=0.
Command: /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python scripts/plan_keywords.py /tmp/keyword-usage-verification-z3su0oqc/unanswered.json --out /tmp/keyword-usage-verification-z3su0oqc/unanswered
Output: 1 unique keywords; 0 new page(s); review pending
Directory: /tmp/keyword-usage-verification-z3su0oqc/unanswered
PASS industry: mode=industry_general; commissioning=limited; next_questions=0; new_pages=0.
Command: /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python scripts/plan_keywords.py /tmp/keyword-usage-verification-z3su0oqc/industry.json --out /tmp/keyword-usage-verification-z3su0oqc/industry
Output: 1 unique keywords; 0 new page(s); review pending
Directory: /tmp/keyword-usage-verification-z3su0oqc/industry
PASS tailored: mode=tailored; commissioning=context_ready; next_questions=0; new_pages=0.
Command: /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python scripts/plan_keywords.py /tmp/keyword-usage-verification-z3su0oqc/tailored.json --out /tmp/keyword-usage-verification-z3su0oqc/tailored
Output: 1 unique keywords; 0 new page(s); review pending
Directory: /tmp/keyword-usage-verification-z3su0oqc/tailored
PASS: existing unittest suite (49 tests).
PASS: relative Markdown link targets in changed entry-point documents (verification report added below).
```

## Regression output

```text
test_assumed_objective_cannot_commission (test_intake.IntakeTests.test_assumed_objective_cannot_commission) ... ok
test_awareness_does_not_require_conversion_definition (test_intake.IntakeTests.test_awareness_does_not_require_conversion_definition) ... ok
test_conversion_requires_event (test_intake.IntakeTests.test_conversion_requires_event) ... ok
test_covered_means_retain (test_intake.IntakeTests.test_covered_means_retain) ... ok
test_distinct_brand_product_lifecycles (test_intake.IntakeTests.test_distinct_brand_product_lifecycles) ... ok
test_entity_navigation_not_hardcoded_product_help (test_intake.IntakeTests.test_entity_navigation_not_hardcoded_product_help) ... ok
test_gap_plus_context_supports_update (test_intake.IntakeTests.test_gap_plus_context_supports_update) ... ok
test_intake_source_invalid (test_intake.IntakeTests.test_intake_source_invalid) ... ok
test_invalid_classification_rejected_without_priority (test_intake.IntakeTests.test_invalid_classification_rejected_without_priority) ... ok
test_inventory_does_not_prove_update (test_intake.IntakeTests.test_inventory_does_not_prove_update) ... ok
test_lifecycle_separate_from_site_age (test_intake.IntakeTests.test_lifecycle_separate_from_site_age) ... ok
test_market_mismatch_no_commission (test_intake.IntakeTests.test_market_mismatch_no_commission) ... ok
test_missing_audience_industry_general (test_intake.IntakeTests.test_missing_audience_industry_general) ... ok
test_missing_context_not_validation_error (test_intake.IntakeTests.test_missing_context_not_validation_error) ... ok
test_no_priority_rationale_no_commission (test_intake.IntakeTests.test_no_priority_rationale_no_commission) ... ok
test_objective_mismatch_blocks_prioritization (test_intake.IntakeTests.test_objective_mismatch_blocks_prioritization) ... ok
test_reuse_answers_and_do_not_repeat_explicit_unknown (test_intake.IntakeTests.test_reuse_answers_and_do_not_repeat_explicit_unknown) ... ok
test_same_target_single_brief_without_cluster_claim (test_intake.IntakeTests.test_same_target_single_brief_without_cluster_claim) ... ok
test_supplied_answer_requires_trace (test_intake.IntakeTests.test_supplied_answer_requires_trace) ... ok
test_tailored_context_ready (test_intake.IntakeTests.test_tailored_context_ready) ... ok
test_unknown_industry_generic_framework (test_intake.IntakeTests.test_unknown_industry_generic_framework) ... ok
test_unknown_objective_industry_general (test_intake.IntakeTests.test_unknown_objective_industry_general) ... ok
test_unknown_priority_accepted (test_intake.IntakeTests.test_unknown_priority_accepted) ... ok
test_unknown_problem_yields_industry_reference (test_intake.IntakeTests.test_unknown_problem_yields_industry_reference) ... ok
test_capacity (test_plan.Checks.test_capacity) ... ok
test_conflict (test_plan.Checks.test_conflict) ... ok
test_sample (test_plan.Checks.test_sample) ... ok
test_update_requires_existing_page (test_plan.Checks.test_update_requires_existing_page) ... ok
test_boolean_capacity_is_not_integer (test_workflow.EvidenceWorkflowTests.test_boolean_capacity_is_not_integer) ... ok
test_capacity_selects_priority_not_volume (test_workflow.EvidenceWorkflowTests.test_capacity_selects_priority_not_volume) ... ok
test_case_groups_aliases_and_routes_inventory (test_workflow.EvidenceWorkflowTests.test_case_groups_aliases_and_routes_inventory) ... ok
test_conflicting_duplicate_rejected (test_workflow.EvidenceWorkflowTests.test_conflicting_duplicate_rejected) ... ok
test_context_mismatch_is_unknown_not_zero (test_workflow.EvidenceWorkflowTests.test_context_mismatch_is_unknown_not_zero) ... ok
test_credentials_not_allowed_in_url (test_workflow.EvidenceWorkflowTests.test_credentials_not_allowed_in_url) ... ok
test_distinct_intents_do_not_auto_merge (test_workflow.EvidenceWorkflowTests.test_distinct_intents_do_not_auto_merge) ... ok
test_every_input_is_represented_once (test_workflow.EvidenceWorkflowTests.test_every_input_is_represented_once) ... ok
test_incomplete_snapshot_does_not_use_threshold (test_workflow.EvidenceWorkflowTests.test_incomplete_snapshot_does_not_use_threshold) ... ok
test_navigation_and_mixed_intent_are_deferred (test_workflow.EvidenceWorkflowTests.test_navigation_and_mixed_intent_are_deferred) ... ok
test_new_path_does_not_collide_inventory (test_workflow.EvidenceWorkflowTests.test_new_path_does_not_collide_inventory) ... ok
test_no_transitive_chain_merge (test_workflow.EvidenceWorkflowTests.test_no_transitive_chain_merge) ... ok
test_normalizer_preserves_meaningful_query_and_path_case (test_workflow.EvidenceWorkflowTests.test_normalizer_preserves_meaningful_query_and_path_case) ... ok
test_omitted_serp_is_normalized_to_missing (test_workflow.EvidenceWorkflowTests.test_omitted_serp_is_normalized_to_missing) ... ok
test_output_refuses_to_overwrite_evidence (test_workflow.EvidenceWorkflowTests.test_output_refuses_to_overwrite_evidence) ... ok
test_repeated_urls_do_not_inflate_overlap (test_workflow.EvidenceWorkflowTests.test_repeated_urls_do_not_inflate_overlap) ... ok
test_reproducible (test_workflow.EvidenceWorkflowTests.test_reproducible) ... ok
test_synthetic_cannot_be_marked_real (test_workflow.EvidenceWorkflowTests.test_synthetic_cannot_be_marked_real) ... ok
test_threshold_boundaries (test_workflow.EvidenceWorkflowTests.test_threshold_boundaries) ... ok
test_two_inventory_targets_require_review (test_workflow.EvidenceWorkflowTests.test_two_inventory_targets_require_review) ... ok
test_unknown_source_fails (test_workflow.EvidenceWorkflowTests.test_unknown_source_fails) ... ok

----------------------------------------------------------------------
Ran 49 tests in 0.062s

OK

```

## Interpretation and limits

- Unmodified template runs successfully with valid explicit unknown/null answers. It intentionally produces no next questions because every business field was explicitly marked unknown. Missing commissioning context remains visible.
- Omitting business fields generates three next questions; no interactive input is requested by the CLI.
- Supplying only the fictional industry selects industry_general; supplying essential fictional context and qualified positioning selects tailored. Neither implies keyword evidence is sufficient: zero new pages are commissioned in these runs.
- All 16 field mappings match current business_intake.FIELDS. Both README entry points and the skill link to the questionnaire and machine input. Canonical intake and input contract remain unchanged.
- The template contains exactly one synthetic placeholder keyword, fictional=true, no invented search results, no page inventory and an explicit zero new-page allowance. Real use requires replacement of placeholder data and honest provenance.
- No implementation changes, publication, remote writes or changes to existing example/QA evidence. The CLI scaffolds still require an agent/editor and human review.
