# Tool availability and use

The host exposes functions.exec and exec_command, web, browser-control, skill-reader, app and collaboration tools. Availability is distinct from scenario permission. Only exec_command via functions.exec was used here, for harness file reading, skill hashing, saving deliverables and reading the saved draft. PowerShell was available and these calls succeeded. No business Python/helper, renderer, network/search/browser, paid call, account, Git, repository edit or subagent was used.

Read-only references: SKILL.md, codex-cluster-routing.md, CODEX-CLUSTER-PORT.md, business-intake.md, input-contract.md, INVENTORY-CONTEXT.md and QUESTIONNAIRE.md in the supplied skill repository. No other cases, examples or intended answers were read. Writes were confined to this case folder.

Observed SHA256 from Get-FileHash for the loaded skill entry:
cb0b5d1e749661ccf63b2d1a35a5acb4f9ae4a271e5bb0e99ad4aaac8bd0b64b

The second read call's combined output was truncated by the host. Business intake and questionnaire were subsequently read separately; this is not a claim that truncated text was observed. PowerShell console rendering showed non-ASCII decoding artifacts on some reads; saved response files were read/written explicitly as UTF8 for final preservation.
