# Stimulus Mapping

Task: `Trust Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `high_trust` | `partner_cue`, `decision_panel`, `decision_invest/keep/timeout`, `outcome_feedback` | `W2138559331`, `W2163301974` | Trustee-type manipulation with trial-level decision and return feedback in repeated trust interactions. | `psychopy_builtin` | Maps to high-return partner profile (`return_ratio=0.60`) in controller. |
| `medium_trust` | `partner_cue`, `decision_panel`, `decision_invest/keep/timeout`, `outcome_feedback` | `W2138559331`, `W2163301974` | Intermediate trustee reciprocity condition for graded trust calibration. | `psychopy_builtin` | Maps to medium-return partner profile (`return_ratio=0.40`). |
| `low_trust` | `partner_cue`, `decision_panel`, `decision_invest/keep/timeout`, `outcome_feedback` | `W2138559331`, `W2163301974` | Low reciprocity trustee condition producing lower expected return from trust decisions. | `psychopy_builtin` | Maps to low-return partner profile (`return_ratio=0.20`). |
| Shared trial scaffolding | `fixation`, `block_break`, `good_bye` | `inferred` | Standard fixation/summary structure for pacing and participant status feedback across blocks. | `psychopy_builtin` | Operational scaffolding; no condition identity leakage beyond partner label. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
