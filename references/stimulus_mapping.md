# Stimulus Mapping

Task: `Trust Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence Type | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `high_trust` | `partner_cue`, `decision_panel`, `decision_invest`, `decision_keep`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2138559331` | Trust-game investor decision and reciprocal return outcome (paradigm-level) | `psychopy_builtin` | Partner profile uses higher return ratio (`0.6`). |
| `medium_trust` | `partner_cue`, `decision_panel`, `decision_invest`, `decision_keep`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2138559331` | Trust-game investor decision and reciprocal return outcome (paradigm-level) | `psychopy_builtin` | Partner profile uses medium return ratio (`0.4`). |
| `low_trust` | `partner_cue`, `decision_panel`, `decision_invest`, `decision_keep`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2138559331` | Trust-game investor decision and reciprocal return outcome (paradigm-level) | `psychopy_builtin` | Partner profile uses lower return ratio (`0.2`). |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `fixation` | `W2098425678` | Shared instructions, transitions, and cumulative payoff display | `psychopy_builtin` | Chinese participant-facing envelope across human/qa/sim configs. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered with PsychoPy text primitives configured in YAML.
- `generated_reference_asset`: task-specific generated assets from literature-described rules.
- `licensed_external_asset`: external licensed media with citation linkage.
