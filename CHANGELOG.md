# CHANGELOG

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
