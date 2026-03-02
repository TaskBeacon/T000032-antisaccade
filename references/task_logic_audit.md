# Task Logic Audit: Antisaccade Task

## 1. Paradigm Intent

- Task: `antisaccade`.
- Construct: inhibitory control and rule-dependent response remapping.
- Manipulated trial factor: response rule (`prosaccade` vs `antisaccade`) with randomly sampled target side (`left`/`right`).
- Primary dependent measures:
  - saccade response accuracy
  - response latency on correct trials
  - timeout/omission rate.
- Key citations:
  - `W2163144416` (Geier et al., 2009, Cerebral Cortex)
  - `W2104663113` (Everling & Munoz, 2000, Journal of Neuroscience)
  - `W1875187353` (Everling et al., 1999, Journal of Neuroscience)

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `3` blocks x `48` trials.
- QA/sim profiles: `1` block x `16` trials.
- For each trial:
  - condition token provides rule (`prosaccade` or `antisaccade`)
  - target side is sampled (`left` or `right`) by controller.

### Trial State Machine

1. `fixation`
- Stimulus: `fixation`.
- Trigger: `fixation_onset`.
- Keys: none.

2. `rule_cue`
- Stimuli: `rule_pro` or `rule_anti` plus anchors.
- Triggers: `rule_pro_onset` or `rule_anti_onset`.
- Keys: none.

3. `gap`
- Stimuli: `left_anchor`, `right_anchor`.
- Trigger: `gap_onset`.
- Keys: none.

4. `saccade_response`
- Stimuli: anchors + `left_target` or `right_target`.
- Trigger: `target_onset_left` or `target_onset_right`.
- Valid keys: `left_key`, `right_key`.
- Response triggers: `response_left` / `response_right`.
- Timeout trigger: `response_timeout`.

5. `iti`
- Stimulus: `fixation`.
- Trigger: `iti_onset`.
- Keys: none.

## 3. Condition Semantics

- `prosaccade`:
  - expected response is same direction as target side.
- `antisaccade`:
  - expected response is opposite direction from target side.

Correct key mapping is computed per trial from `(rule, target_side, left_key, right_key)`.

## 4. Response and Scoring Rules

- Key mapping (default):
  - `f -> left`
  - `j -> right`
- Correctness:
  - `hit = (response_key == correct_key)`.
- Timeout:
  - no key before deadline, `timed_out=true`, `saccade_response_hit=false`.
- Controller updates per trial:
  - correctness counters
  - timeout counters
  - correct-trial RT aggregates.
- QA-required columns include:
  - `condition`, `block_id`, `trial_index`, `rule`, `target_side`, `correct_key`, `saccade_response_response`, `saccade_response_rt`, `saccade_response_hit`.

## 5. Stimulus Layout Plan

- Spatial layout:
  - `fixation` center at `(0, 0)`.
  - anchors at `(-340, 0)` and `(340, 0)`.
  - target appears at one anchor location (`left_target` or `right_target`).
  - rule cue text shown at top center `(0, 210)`.
- Visual coding:
  - pro rule in green (`rule_pro`), anti rule in red (`rule_anti`).
  - target uses filled white circle for strong peripheral salience.
- Localization policy:
  - all participant-facing instruction/rule/summary text is config-defined.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `rule_pro_onset` | 21 | prosaccade rule cue onset |
| `rule_anti_onset` | 22 | antisaccade rule cue onset |
| `gap_onset` | 30 | gap onset |
| `target_onset_left` | 40 | left target onset |
| `target_onset_right` | 41 | right target onset |
| `response_left` | 50 | left response key |
| `response_right` | 51 | right response key |
| `response_timeout` | 60 | no response before deadline |
| `iti_onset` | 70 | inter-trial interval onset |

## 7. Architecture Decisions (Auditability)

- `src/run_trial.py` is task-native and removes MID-template phases.
- Response phase is explicitly named `saccade_response` to align with responder expectations and QA column contracts.
- Correct key is computed each trial by controller logic and stored in trial context for simulated responders.
- Target-side onset triggers are emitted directly from sampled side (`left` vs `right`) for event-level traceability.
- Behavioral counters remain in controller; `main.py` summarizes from logged trial rows for reproducibility.

## 8. Inference Log

- Duration ranges (fixation, cue, gap, ITI) are implementation inferences constrained by antisaccade workflow literature rather than one fixed universal protocol.
- Human profile uses `3 x 48` trial structure for balanced sampling; QA/sim downsample counts for runtime practicality.
- Keyboard left/right response proxies are used in place of eye-tracker-derived saccades as an implementation inference for portability.
- Rule cues are implemented as colored text (`rule_pro`/`rule_anti`) instead of symbolic shapes; this is an inference preserving explicit rule communication.
