# SEO Content Planner

Convert a small keyword brief into page decisions and an actionable writing brief without inventing search volume or ranking evidence.

[中文说明](README.zh-CN.md)

## What this proves

A reviewer can inspect the business decision, the evidence used, and the resulting deliverable without running an AI tool. This is an original, AI-assisted portfolio draft awaiting Huiyang Xie's review.

## Start here

1. Read examples/input.json.
2. Inspect examples/output.md for the worked result.
3. Read skills/keyword-to-content-brief/SKILL.md for the repeatable method.
4. Review evals/rubric.md and examples/comparison.md for limitations and quality checks.

## Run the offline checks

Python 3.10+; standard library only; no account, API, installation or paid call required.

    python -m unittest discover -s tests -v

Tests validate the included fixtures and deterministic checks. They do not establish SEO ranking gains, revenue impact, content effectiveness, or general AI output quality.

## Repository contents

- skills/: input/output contract and decision workflow
- examples/: fictional input, reviewed sample output, comparison
- scripts/: offline validation or analysis
- tests/: reproducible fixture tests
- evals/: human review criteria
- ATTRIBUTION.md: origin and reference boundaries
- REVIEW_BEFORE_PUBLIC.md: private-review checklist

## Status and scope

Private-review draft, v0.1.0. No content publishing, advertising changes, live crawling, customer data, or private OE material. Outputs require human review. No public license has been selected or granted. LICENSE-PROPOSAL.md contains a proposal for owner review, not operative terms.
