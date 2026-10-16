# Sol 6.1 agent behavior runs — 2026-10-16

These are real fresh Sol 6.1 agent executions through the existing agent runtime, using only synthetic fixtures. They are not static link checks or paid-provider calls. Each case preserves its user request, tool permissions, tested SKILL SHA256, first answer, same-agent review, final answer and command records. The supervising AI reviewed the actual artifacts; no human approval or marketing effectiveness is claimed.

| Case | Actual result | Deliverable |
|---|---|---|
| Sufficient supplied material | Actual offline renderer first rejected an unmapped SERP-status field. The agent preserved that input/error, mapped evidence as unknown and then mapped existing-page coverage explicitly. Two later runs exited 0. One existing review destination, zero new pages, no invented live SERP/demand. | [Completed editorial handoff](sufficient/final.md), [machine plan](sufficient/renderer-mapped/cluster-plan.json), [first response](sufficient/raw-response.md), [review](sufficient/self-review.md) |
| Insufficient material | Industry-general reference brief; candidate ideas are provisional, all page decisions deferred, metrics unknown. No business script was authorized or claimed. | [Final brief](insufficient/final.md) |
| Conflicting evidence / business tools disabled | Objective/coverage conflicts retained, incompatible markets/dates do not justify overlap, one conditional existing-page review and no new pages. Manual output, no renderer claim. | [Final handoff](conflict-no-tools/final.md) |

## Review and boundaries

No material skill-behavior failure was found in these three outputs. The rejected initial input and subsequent mapping are retained as execution evidence, not hidden as a pass. Generated scaffolds remain scaffolds; the separate final Markdown contains the agent's editorial work. Qualified real search evidence, source authenticity, browser interaction, human approval and SEO outcomes were not verified.

Use the input and tool permissions in each case.json to repeat a task in a fresh Sol 6.1 agent; require a new output folder and retain the original. The fixtures contain no intended answer/rubric. Expected behavior assessment above was written after execution. Script commands and actual exit codes are in each commands.json; semantic harness records are labeled as such.

Public exports redact machine-local path prefixes only. EXPORT.json records original/export hashes; exact originals remain local. Tokens {REPO}, {CASE}, {PYTHON}, {TASK}, {TEMP} are path aliases, not executable relative paths. No source or finding was redacted. Final entrypoint navigation may link this run after generation; tested_skill_sha256 identifies the exact instructions loaded during the run.

## Actual local regression rerun

Keyword: **122 run, 121 passed, 1 environment error, exit 1**. Windows denied fixture symlink creation (WinError 1314); symlink-refusal behavior was not verified here. No administrator/Developer Mode change was attempted. See [commands, preserved failures and results](local-tests/README.md). These are separate from the model scenarios.

## Separate package checks

[Thirteen entrypoint/frontmatter and copied-layout checks](ENTRY-CHECKS.json) record actual static checks. Full-repository relative links resolve; child-only copies intentionally expose missing root resources and are not documented as complete installations. This is not automatic host installation or another agent test. The first harness accidentally selected a preserved legacy SKILL too; selection was corrected without editing any historical file. PyYAML was installed only in the temporary task runtime to run the unchanged official quick validator.
