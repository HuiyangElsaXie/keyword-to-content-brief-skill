# Example generations

- `studio-case/`: current v0.2 case, supplied raw keyword evidence with no prefilled page decisions. `helper-run/` is the rebuilding agent's deterministic smoke run; `agent-run/` is a separate actual agent execution with full editorial work and review. Both use synthetic data, not observed search results.
- Root `input.json`, `output.md`, `comparison.md`: historical v0.1 examples retained without edits. These used prefilled decisions and are not proof of v0.2 behavior.
- `../legacy/v0.1/`: complete pre-rebuild file snapshot, including the historical attribution and proposal documents.
