# Stimulus Mapping

Task: `Trust Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `high_trust` | `partner_cue`, `decision_panel`, `outcome_feedback`, `fixation` | `W2138559331` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `medium_trust` | `partner_cue`, `decision_panel`, `outcome_feedback`, `fixation` | `W2138559331` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `low_trust` | `partner_cue`, `decision_panel`, `outcome_feedback`, `fixation` | `W2138559331` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `fixation` | `W2138559331` | Shared instruction, transition, and fixation assets support the common task envelope across all conditions. | `psychopy_builtin` | Shared assets are condition-agnostic and used in every run mode. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
