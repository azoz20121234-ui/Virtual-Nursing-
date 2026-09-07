# Research State Machine

Canonical order:
`FRAME → QUESTION → PICO/PICOT → SEARCH → SCREEN → APPRAISE → EXTRACT → SYNTHESIZE → CONTRADICTION → RED TEAM → SAUDI → GAP → INNOVATION → VALIDATION → DECISION`

Runtime enforcement lives in `runtime/state_machine.py`.

- bounded iterations: 45 transitions by contract
- per-state retries: 2
- explicit RETRY and FAILED states
- circular transitions rejected
- stopping condition: decision reached with sufficient evidence
- human gates: clinical, regulatory, Go/No-Go
- gate rejection blocks the decision path

The state machine is model-agnostic. Claude Code is only an integration adapter.
