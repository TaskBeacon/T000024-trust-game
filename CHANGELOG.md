# CHANGELOG

## [v0.2.3-dev] - 2026-03-02

### Changed
- Standardized `main.py` into the single-flow task runtime pattern used by current task-build outputs (shared `run(options)` path with QA/sim runtime context handling).
- Repaired `src/run_trial.py` phase and timing usage to trust-game naming only:
  - removed residual MID-style stage naming,
  - aligned durations to `partner_cue_duration`, `pre_decision_fixation_duration`, `decision_confirmation_duration`, `outcome_feedback_duration`.
- Kept decision response data under `decision` unit labels to preserve QA artifact compatibility (`decision_response`).
- Replaced code-side localized decision labels with neutral semantic tokens (`invest`, `keep`, `timeout`) so participant-facing language stays config-driven.
- Updated references artifacts to pass the current contract schema:
  - added required `## Mapping Table` sections and required table columns in mapping docs,
  - aligned `task_logic_audit.md` headings to required `## 1`..`## 8` structure,
  - aligned `references.md` column schema.

### Validation
- `python -m py_compile main.py src/run_trial.py`
- `python -m psyflow.validate e:/Taskbeacon/T000024-trust-game`
- `psyflow-qa e:/Taskbeacon/T000024-trust-game --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`

## [v0.2.2-dev] - 2026-02-19

### Changed
- Removed legacy MID-style runtime unit labels from trial data output:
  - `cue/anticipation/target/decision_feedback/feedback` -> `partner_cue/pre_decision_fixation/decision/decision_confirmation/outcome_feedback`.
- Updated trust-game timing keys in all configs:
  - `partner_cue_duration`, `pre_decision_fixation_duration`, `decision_confirmation_duration`, `outcome_feedback_duration`.
- Renamed trust-game cue/confirmation trigger keys in all configs:
  - `*_partner_cue_onset`, `decision_confirmation_onset`.
- Updated sampler responder to act on trust decision phases (`decision` / `trust_decision`) instead of legacy `target`.
- Updated QA acceptance criteria column from `target_response` to `decision_response`.
- Rewrote `references/task_logic_audit.md` and `references/stimulus_mapping.md` to literature-first trust-game descriptions and concrete mapping.
- Synced `README.md`, `references/parameter_mapping.md`, and `taskbeacon.yaml` with the repaired naming scheme.

## [v0.2.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.


All notable development changes for `T000024-trust-game` are documented here.

## [v0.2.0-dev] - 2026-02-18
### Added
- Trust-game specific controller for partner-profile scheduling and return/earnings computation.
- Trust-game specific sampler responder (`responders/task_sampler.py`) using EV/logit choice policy.

### Changed
- Replaced placeholder MID-style pipeline with true Trust Game logic:
  - participant invests or keeps endowment,
  - invested amount is multiplied,
  - partner returns condition-dependent amount,
  - trial and cumulative earnings tracked in controller.
- Rebuilt `src/run_trial.py` to a trust-game sequence:
  - cue -> anticipation -> decision(target) -> decision feedback -> outcome feedback -> iti.
- Rebuilt `src/utils.py` as a trust-game scheduler/outcome engine (no adaptive target-duration logic).
- Updated `main.py` block summaries to trust metrics (`trust_rate`, `block_earned`, `total_earned`).
- Rewrote all config profiles to human-readable sectioned YAML and split usage:
  - `config.yaml` (human),
  - `config_qa.yaml` (QA/dev short profile),
  - `config_scripted_sim.yaml` (scripted sim short profile),
  - `config_sampler_sim.yaml` (sampler sim short profile).
- Rewrote README to standardized auditable structure (`## 1`..`## 4`) with flow/config/method details.

### Fixed
- Removed placeholder target hit/miss and adaptive-duration behavior that did not belong to Trust Game.

### Validation
- `python -m psyflow.validate e:/Taskbeacon/T000024-trust-game`
- `python main.py qa --config config/config_qa.yaml`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
