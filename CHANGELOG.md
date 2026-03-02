# CHANGELOG

## [v0.1.3-dev] - 2026-03-02

### Changed
- Replaced `src/run_trial.py` MID-template code with antisaccade-native execution phases (`fixation -> rule_cue -> gap -> saccade_response -> iti`).
- Wired condition rule parsing, target-side sampling, and trial-level correct-key computation into runtime context and outputs.
- Rebuilt all reference artifacts to the current contract schema (`references.yaml`, `references.md`, `parameter_mapping.md`, `stimulus_mapping.md`, `task_logic_audit.md`).

### Fixed
- Restored QA-required antisaccade output columns (`trial_index`, `rule`, `target_side`, `correct_key`, `saccade_response_*`).
- Added explicit response trigger emission (`response_left`/`response_right`) and timeout handling in `saccade_response` phase.
- Restored contract-required reference headings and columns, including `## 7. Architecture Decisions (Auditability)` and `## 8. Inference Log`.

## [v0.1.2-dev] - 2026-02-19

### Changed
- Replaced MID-derived trial flow with a zero-base antisaccade state machine (`fixation -> rule_cue -> gap -> saccade_response -> iti`).
- Rewrote `src/run_trial.py` for rule-dependent side mapping and lateralized target onset/response triggers.
- Replaced adaptive MID controller in `src/utils.py` with antisaccade rule/side sampler and performance tracker.
- Updated `main.py` summaries to use antisaccade accuracy, RT, and timeout metrics.
- Replaced `responders/task_sampler.py` with antisaccade-aware simulation policy using `correct_key` from runtime factors.
- Rebuilt all task configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`) to match antisaccade stimuli, timing, and trigger map.
- Rebuilt literature artifacts (`references/task_logic_audit.md`, `references/stimulus_mapping.md`, `references/parameter_mapping.md`, `references/references.yaml`, `references/references.md`, `references/selected_papers.json`) with antisaccade-specific evidence.
- Updated `README.md` and `taskbeacon.yaml` metadata to align with repaired implementation and evidence IDs.

### Fixed
- Removed legacy `catch` fallback mapping from `src/utils.py` so only true antisaccade conditions are accepted.

All notable development changes for `T000032-antisaccade` are documented here.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Antisaccade Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`

