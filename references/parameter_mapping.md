# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `task_name` | `task.task_name` | `trust_game` | `W2138559331` | Investor-role trust game paradigm identity. | `direct` | Core paradigm anchor. |
| `conditions` | `task.conditions` | `high_trust, medium_trust, low_trust` | `W2138559331` | Partner-dependent reciprocity drives trust decisions. | `adapted` | Three partner-return profiles for condition contrast. |
| `endowment` | `task.endowment` | `10` | `W2138559331` | Fixed investor endowment in one-shot trust-game style trials. | `adapted` | Constant per trial for clear payoff accounting. |
| `transfer_multiplier` | `task.transfer_multiplier` | `3.0` | `W2138559331` | Invested amount is multiplied before partner return. | `adapted` | Deterministic multiplier in implementation. |
| `response_keys` | `task.key_list` | `f=invest, j=keep` | `W2138559331` | Binary investor choice (trust vs keep). | `adapted` | Desktop key mapping for PsychoPy runtime. |
| `total_blocks_human` | `task.total_blocks` | `3` | `W2138559331` | Repeated interaction blocks for stable behavior estimates. | `inferred` | Practical session-length configuration. |
| `trials_per_block_human` | `task.trial_per_block` | `24` | `W2138559331` | Repeated trust decisions by partner profile. | `inferred` | Balanced schedule across conditions. |
| `total_trials_human` | `task.total_trials` | `72` | `W2138559331` | Sufficient sample for condition-wise trust rate. | `inferred` | Derived from block and trial settings. |
| `partner_cue_duration` | `timing.partner_cue_duration` | `0.6` | `W2138559331` | Partner identity shown before trust decision. | `adapted` | Dedicated cue phase for trigger segmentation. |
| `pre_decision_fixation_duration` | `timing.pre_decision_fixation_duration` | `0.6` | `W2138559331` | Short fixation between cue and decision phase. | `inferred` | Added for temporal separation and auditability. |
| `decision_duration` | `timing.decision_duration` | `2.0` | `W2138559331` | Time-limited trust decision response window. | `adapted` | Enables timeout event handling. |
| `decision_confirmation_duration` | `timing.decision_confirmation_duration` | `0.5` | `W2138559331` | Brief post-choice confirmation stage. | `inferred` | UI stage for decision acknowledgement. |
| `outcome_feedback_duration` | `timing.outcome_feedback_duration` | `1.0` | `W2138559331` | Outcome information shown after investor choice. | `adapted` | Includes returned and cumulative earnings. |
| `iti_duration` | `timing.iti_duration` | `0.8` | `W2138559331` | Inter-trial interval pacing. | `inferred` | Fixed ITI for reproducibility. |
| `timeout_policy` | `src/run_trial.py` | `timeout -> keep (no investment)` | `W2138559331` | Non-invest choice preserves endowment. | `inferred` | Deterministic non-response behavior. |
| `return_noise_ratio` | `controller.return_noise_ratio` | `0.05` (human), `0.0` (qa/sim) | `W2138559331` | Partner return behavior varies around profile tendency. | `adapted` | Disabled in qa/sim for deterministic tests. |
| `exp_onset` | `triggers.map.exp_onset` | `1` | `inferred` | Experiment start marker. | `inferred` | Framework boundary code. |
| `exp_end` | `triggers.map.exp_end` | `2` | `inferred` | Experiment end marker. | `inferred` | Framework boundary code. |
| `block_onset` | `triggers.map.block_onset` | `10` | `inferred` | Block start marker. | `inferred` | Framework block code. |
| `block_end` | `triggers.map.block_end` | `11` | `inferred` | Block end marker. | `inferred` | Framework block code. |
| `partner_cue_onsets` | `triggers.map.{condition}_partner_cue_onset` | `high=20, medium=21, low=22` | `inferred` | Condition-resolved cue event coding. | `inferred` | Enables condition-specific epoch extraction. |
| `decision_onsets` | `triggers.map.{condition}_decision_onset` | `high=30, medium=31, low=32` | `inferred` | Condition-resolved trust decision coding. | `inferred` | Paired with response/timeout markers. |
| `decision_response` | `triggers.map.decision_response` | `50` | `inferred` | Trust decision response marker. | `inferred` | Captured on accepted keypress. |
| `decision_timeout` | `triggers.map.decision_timeout` | `51` | `inferred` | Trust decision timeout marker. | `inferred` | Captured on response deadline expiry. |
| `decision_confirmation_onset` | `triggers.map.decision_confirmation_onset` | `52` | `inferred` | Confirmation stage onset marker. | `inferred` | Post-decision stage coding. |
| `outcome_feedback_onset` | `triggers.map.outcome_feedback_onset` | `53` | `inferred` | Outcome feedback onset marker. | `inferred` | Outcome-stage segmentation. |
| `iti_onset` | `triggers.map.iti_onset` | `60` | `inferred` | ITI stage onset marker. | `inferred` | Trial boundary anchor. |