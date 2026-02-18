# Trust Game

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Trust Game |
| Version | v0.2.1-dev |
| URL / Repository | https://github.com/TaskBeacon/T000024-trust-game |
| Short Description | Investment vs keep decisions across partners with different return tendencies. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a standard Trust Game from the investor perspective. On each trial, participants decide whether to invest their endowment or keep it. If they invest, the amount is multiplied and partially returned based on partner condition.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Schedule trials | `Controller.prepare_block(...)` builds balanced partner-condition trial sequences. |
| 2. Execute trials | `BlockUnit(...).run_trial(...)` executes partner cue, decision, and feedback stages. |
| 3. Block summary | Investment rate, block earnings, and cumulative earnings are shown. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Partner cue | Partner label is shown (high/medium/low return tendency). |
| Pre-decision fixation | Fixation before decision panel. |
| Trust decision | Participant chooses invest or keep. |
| Decision confirmation | Choice confirmation (invest/keep/timeout). |
| Outcome feedback | Invested amount, multiplied amount, returned amount, and earnings are shown. |
| Inter-trial interval | Fixation interval before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Condition balancing | Balances partner conditions within block schedules. |
| Outcome resolution | Computes investment return and trial earnings from condition-specific rules. |
| Cumulative tracking | Updates cumulative earnings and trial-level outcomes. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `partner_cue` | Partner cue stage. |
| `pre_decision_fixation` | Fixation before choice. |
| `trust_decision` | Invest/keep decision stage. |
| `decision_confirmation` | Decision confirmation stage. |
| `outcome_feedback` | Trial outcome feedback stage. |
| `inter_trial_interval` | ITI stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Description |
|---|---|
| `subject_id` | Participant identifier. |
| `subname` | Participant name token. |
| `age` | Participant age. |
| `gender` | Participant gender. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `partner_cue` | text | Partner identity cue. |
| `decision_panel` | text | Invest/keep decision panel. |
| `decision_*` | text | Choice confirmation screens. |
| `outcome_feedback` | text | Trial and cumulative outcome summary. |
| `fixation` | text | Central fixation marker. |

### d. Timing

| Phase | Duration |
|---|---|
| partner_cue | 0.6 s |
| pre_decision_fixation | 0.6 s |
| trust_decision | 2.0 s |
| decision_confirmation | 0.5 s |
| outcome_feedback | 1.0 s |
| inter_trial_interval | 0.8 s |

## 4. Methods (for academic publication)

Participants completed repeated trust decisions under partner conditions with different expected return behavior. On each trial, participants either invested their full endowment or kept it. Invested funds were multiplied and partially returned according to condition-specific return logic.

The trial structure included cue, decision, confirmation, and outcome stages to separate expectancy, choice, and feedback processes. Recorded outputs include choice, timing, invested amount, returned amount, trial earnings, and cumulative earnings.

The implementation supports aligned `human`, `qa`, and `sim` pipelines with standardized context metadata for auditability.
