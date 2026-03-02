# Task Logic Audit: Trust Game

## 1. Paradigm Intent

- Task: `trust_game` (investor-role trust game).
- Research construct: willingness to trust a partner under uncertainty about reciprocal return.
- Manipulated factor in this implementation: partner return tendency (`high_trust`, `medium_trust`, `low_trust`).
- Trial choice:
  - `invest` (send full endowment to partner)
  - `keep` (keep full endowment)
- Key references used for paradigm-level grounding:
  - `W2138559331`
  - `W2098425678`
  - `W3038067977`

## 2. Block and Trial Workflow

### Block Structure

- Total blocks: `3`
- Trials per block: `24`
- Total trials: `72`
- Block scheduling: `Controller.prepare_block(...)` builds a shuffled schedule over partner profiles.

### Trial State Machine (Implemented)

1. `partner_cue`
   - Participant sees current partner type (`本轮对手：{partner_label}`).
   - Trigger: condition-specific cue onset (`high_trust_partner_cue_onset`, `medium_trust_partner_cue_onset`, `low_trust_partner_cue_onset`).
   - Duration: `timing.partner_cue_duration` (fallback-compatible with legacy `cue_duration`).
   - Response: none.
2. `pre_decision_fixation`
   - Participant sees fixation (`+`) before decision.
   - Trigger: no dedicated marker in current map.
   - Duration: `timing.pre_decision_fixation_duration` (fallback-compatible with legacy `anticipation_duration`).
   - Response: none.
3. `decision`
   - Participant chooses invest (`f`) or keep (`j`) on the decision panel.
   - Trigger: condition-specific decision onset and response/timeout markers.
   - Duration: `timing.decision_duration`.
   - Timeout policy: timeout is treated as keep (no investment).
4. `decision_confirmation`
   - Participant sees immediate choice confirmation (`投资` / `保留` / timeout).
   - Trigger: `decision_confirmation_onset` (fallback-compatible with legacy `decision_feedback_onset`).
   - Duration: `timing.decision_confirmation_duration` (fallback-compatible with legacy `decision_feedback_duration`).
   - Response: none.
5. `outcome_feedback`
   - Participant sees invested amount, multiplied amount, returned amount, and cumulative earnings.
   - Trigger: `outcome_feedback_onset`.
   - Duration: `timing.outcome_feedback_duration` (fallback-compatible with legacy `feedback_duration`).
   - Response: none.
6. `iti`
   - Participant sees fixation before next trial.
   - Trigger: `iti_onset`.
   - Duration: `timing.iti_duration`.
   - Response: none.

## 3. Condition Semantics

- `high_trust`
  - Partner profile label: high-return partner.
  - Return ratio: `0.6` of multiplied investment (plus optional bounded noise).
- `medium_trust`
  - Partner profile label: medium-return partner.
  - Return ratio: `0.4`.
- `low_trust`
  - Partner profile label: low-return partner.
  - Return ratio: `0.2`.

## 4. Response, Timeout, and Scoring Rules

- Endowment per trial: `10` points.
- Transfer multiplier: `3.0`.
- Choice mapping:
  - `f` -> invest full endowment
  - `j` -> keep full endowment
- Timeout handling:
  - timeout => treated as keep (invested amount = 0).
- Outcome computation (`Controller.resolve_outcome`):
  - `invested = endowment` if invest else `0`
  - `multiplied_amount = invested * transfer_multiplier`
  - `returned = round(multiplied_amount * return_ratio + noise)`
  - `earned = endowment - invested + returned`
- Cumulative metric:
  - `total_earned` accumulates across trials and is shown in block/end summaries.

## 5. Stimulus Layout Plan

- All participant-facing text screens (`instruction_text`, `partner_cue`, `decision_panel`, `outcome_feedback`, `block_break`, `good_bye`) are center-aligned text stimuli with `wrapWidth=980` and `font=SimHei`.
- Decision screen presents two explicit options (left invest, right keep) in stable positions to preserve key-option consistency.
- `fixation` is centrally presented and reused for pre-decision and ITI phases.

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | Task start marker |
| `exp_end` | 2 | Task end marker |
| `block_onset` | 10 | Block start |
| `block_end` | 11 | Block end |
| `high_trust_partner_cue_onset` | 20 | High-trust partner cue onset |
| `medium_trust_partner_cue_onset` | 21 | Medium-trust partner cue onset |
| `low_trust_partner_cue_onset` | 22 | Low-trust partner cue onset |
| `high_trust_decision_onset` | 30 | High-trust decision onset |
| `medium_trust_decision_onset` | 31 | Medium-trust decision onset |
| `low_trust_decision_onset` | 32 | Low-trust decision onset |
| `decision_response` | 50 | Decision response captured |
| `decision_timeout` | 51 | Decision timeout |
| `decision_confirmation_onset` | 52 | Decision-confirmation onset |
| `outcome_feedback_onset` | 53 | Outcome feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Inference Log

- Selected references define trust-game structure but do not prescribe a single fixed runtime timing set; current phase durations are inferred implementation parameters.
- Deterministic partner return ratios (`0.6/0.4/0.2`) with optional bounded noise are implementation-level operationalization for reproducible behavioral sampling.
- Legacy MID-style output labels (`target_response`, `decision_feedback_*`) were removed from active runtime units in favor of trust-game-specific stage labeling.
