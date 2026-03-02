# Task Logic Audit: Trust Game (T000024)

## 1. Paradigm Intent

- Task: `trust_game`
- Primary construct: interpersonal trust under uncertain reciprocity in the investor role.
- Manipulated factors: partner return tendency (`high_trust`, `medium_trust`, `low_trust`).
- Dependent measures: trust rate, decision response time, invested amount, returned amount, trial earnings, cumulative earnings.
- Key citations: `W2138559331`, `W2098425678`.

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: `3` in human mode; `1` in QA/sim modes.
- Trials per block: `24` in human mode; `9` in QA/sim modes.
- Randomization/counterbalancing: `Controller.prepare_block(...)` balances condition counts then shuffles trial order with seeded RNG.
- Condition generation method:
  - Custom generator in `Controller.prepare_block(...)`.
  - Reason: each trial payload includes partner label, return ratio, and stable `condition_id` required for audit tracing.
  - Data shape passed into `run_trial.py`: `(condition, partner_label, return_ratio, condition_id, trial_index)`.
- Runtime-generated trial values:
  - Generated in `run_trial.py`: trust/keep/timeout state, choice label, and resolved payoff fields from controller.
  - Determinism/reproducibility: controller uses seeded RNG (`controller.seed`), and sim responders are seed-driven via config.

### Trial State Machine

1. `partner_cue`
   - Onset trigger: `{condition}_partner_cue_onset`
   - Stimuli shown: `partner_cue`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `pre_decision_fixation`
2. `pre_decision_fixation`
   - Onset trigger: optional `{condition}_pre_decision_fixation_onset` (not defined in current trigger map)
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `trust_decision`
3. `trust_decision`
   - Onset trigger: `{condition}_decision_onset`
   - Stimuli shown: `decision_panel`
   - Valid keys: invest key and keep key from `task.key_list`
   - Timeout behavior: timeout emits `decision_timeout` and is handled as keep
   - Next state: `decision_confirmation`
4. `decision_confirmation`
   - Onset trigger: `decision_confirmation_onset`
   - Stimuli shown: one of `decision_invest`, `decision_keep`, `decision_timeout`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `outcome_feedback`
5. `outcome_feedback`
   - Onset trigger: `outcome_feedback_onset`
   - Stimuli shown: `outcome_feedback`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `inter_trial_interval`
6. `inter_trial_interval`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: next trial or block end

## 3. Condition Semantics

- Condition ID: `high_trust`
- Participant-facing meaning: partner with high expected reciprocity.
- Concrete stimulus realization (visual/audio): `partner_label` displayed in `partner_cue`; controller uses `return_ratio=0.6`.
- Outcome rules: investing sends full endowment, multiplied by configured multiplier, then larger expected return.

- Condition ID: `medium_trust`
- Participant-facing meaning: partner with medium expected reciprocity.
- Concrete stimulus realization (visual/audio): `partner_label` displayed in `partner_cue`; controller uses `return_ratio=0.4`.
- Outcome rules: same payoff mechanics with medium expected return.

- Condition ID: `low_trust`
- Participant-facing meaning: partner with low expected reciprocity.
- Concrete stimulus realization (visual/audio): `partner_label` displayed in `partner_cue`; controller uses `return_ratio=0.2`.
- Outcome rules: same payoff mechanics with lower expected return.

Also document where participant-facing condition text/stimuli are defined:

- Participant-facing text source (config stimuli / code formatting / generated assets): config-defined text templates in `config/*.yaml`, populated via `stim_bank.get_and_format(...)`.
- Why this source is appropriate for auditability: all participant wording and layout parameters are centralized in config artifacts.
- Localization strategy (how language variants are swapped via config without code edits): language-specific config files can replace stimulus text while keeping `src/run_trial.py` unchanged.

## 4. Response and Scoring Rules

- Response mapping: first key in `task.key_list` = invest; second key = keep.
- Response key source (config field vs code constant): config (`task.key_list`).
- If code-defined, why config-driven mapping is not sufficient: not applicable.
- Missing-response policy: timeout in decision phase is treated as keep (no investment).
- Correctness logic: no objective correct answer; behavior reflects trust preference.
- Reward/penalty updates:
  - invest: `invested=endowment`, `multiplied=endowment*transfer_multiplier`, returned amount depends on condition return ratio.
  - keep/timeout: `invested=0`, participant keeps endowment.
- Running metrics: controller tracks per-trial outcome fields and cumulative `total_earned`.

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: `trust_decision`
- Stimulus IDs shown together: `decision_panel` (single multiline panel with left/right options)
- Layout anchors (`pos`): centered text anchor
- Size/spacing (`height`, width, wrap): `height=38`, `wrapWidth=980`
- Readability/overlap checks: QA validation run confirms full visibility at `1280x720`
- Rationale: single centered panel keeps decision options explicit while minimizing visual clutter

- Screen name: `outcome_feedback`
- Stimulus IDs shown together: `outcome_feedback` (single multiline payoff summary)
- Layout anchors (`pos`): centered text anchor
- Size/spacing (`height`, width, wrap): `height=34`, `wrapWidth=980`
- Readability/overlap checks: QA validation run confirms no clipping at `1280x720`
- Rationale: compact, auditable summary of trial and cumulative outcomes

## 6. Trigger Plan

- Experiment boundaries: `exp_onset=1`, `exp_end=2`
- Block boundaries: `block_onset=10`, `block_end=11`
- Partner cue onsets: `high_trust=20`, `medium_trust=21`, `low_trust=22`
- Trust decision onsets: `high_trust=30`, `medium_trust=31`, `low_trust=32`
- Decision events: `decision_response=50`, `decision_timeout=51`, `decision_confirmation_onset=52`
- Outcome and pacing: `outcome_feedback_onset=53`, `iti_onset=60`

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why): simple mode-aware single flow for transparent execution (`human|qa|sim`).
- `utils.py` used? (yes/no): yes.
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other): sequence generation and payoff bookkeeping for partner-profile trust outcomes.
- Custom controller used? (yes/no): yes.
- If yes, why PsyFlow-native path is insufficient: condition payload must include profile metadata and deterministic outcome computation with optional noise.
- Legacy/backward-compatibility fallback logic required? (yes/no): no.
- If yes, scope and removal plan: not applicable.

## 8. Inference Log

- Decision: model trust choice as all-or-none investment (full invest vs full keep).
- Why inference was required: selected references vary in exact transfer menus and interaction structure.
- Citation-supported rationale: investor trust decision and reciprocal return mechanism are core across trust-game paradigms (`W2138559331`).

- Decision: use three fixed partner-return profiles (`0.6/0.4/0.2`).
- Why inference was required: literature reports heterogeneous reciprocity distributions and manipulations.
- Citation-supported rationale: condition-dependent reciprocity expectations are central to trust-behavior modulation in trust-game tasks.

- Decision: timeout is treated as keep.
- Why inference was required: non-response handling is not uniformly specified in reported paradigms.
- Citation-supported rationale: keep-equivalent timeout preserves deterministic payoff accounting for computerized fixed-window trials.