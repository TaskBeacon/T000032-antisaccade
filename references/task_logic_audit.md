# Task Logic Audit: Antisaccade Task

## 1. Paradigm Intent

- Task: `antisaccade`
- Primary construct: inhibitory oculomotor control under prosaccade versus antisaccade rules.
- Manipulated factors: trial rule (`prosaccade`, `antisaccade`) and lateral target side (`left`, `right`).
- Dependent measures: response direction accuracy, correct-trial RT, and timeout rate.
- Key citations:
  - `W2163144416` (Geier et al., 2009, Cerebral Cortex)
  - `W1989816441` (Padmanabhan et al., 2011, Dev Cogn Neurosci)
  - `W2104663113` (Everling and Munoz, 2000, J Neurosci)
  - `W1875187353` (Everling et al., 1999, J Neurosci)

## 2. Block/Trial Workflow

### Block Structure

- Human profile: 3 blocks x 48 trials (`total_trials=144`).
- QA/sim profiles: 1 block x 16 trials.
- Randomization/counterbalancing: `BlockUnit.generate_conditions()` provides block condition stream; each trial samples target side at runtime.

### Trial State Machine

1. `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: `fixation`, `left_anchor`, `right_anchor`
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after sampled `fixation_duration`.
   - Next state: `rule_cue`

2. `rule_cue`
   - Onset trigger: `rule_pro_onset` or `rule_anti_onset`
   - Stimuli shown: fixation and anchors plus rule cue (`rule_pro` or `rule_anti`)
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after sampled `cue_duration`.
   - Next state: `gap`

3. `gap`
   - Onset trigger: `gap_onset`
   - Stimuli shown: `fixation`, `left_anchor`, `right_anchor`
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after sampled `gap_duration`.
   - Next state: `saccade_response`

4. `saccade_response`
   - Onset trigger: `target_onset_left` or `target_onset_right`
   - Stimuli shown: anchors plus lateralized target (`left_target` or `right_target`)
   - Valid keys: `[left_key, right_key]` (default `f/j`)
   - Timeout behavior: if no response before `response_deadline`, emit `response_timeout`.
   - Next state: `iti`

5. `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `fixation`, `left_anchor`, `right_anchor`
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after `iti_duration`.
   - Next state: next trial

## 3. Condition Semantics

- Condition ID: `prosaccade`
  - Participant-facing meaning: orient toward target side.
  - Concrete stimulus realization: green top cue (`LOOK TOWARD`) precedes lateral target onset.
  - Implemented stimuli: `rule_pro`, `left_target`/`right_target`, plus shared fixation/anchors.
  - Outcome rule: correct key equals target side key.

- Condition ID: `antisaccade`
  - Participant-facing meaning: inhibit reflexive orienting and choose opposite side.
  - Concrete stimulus realization: red top cue (`LOOK AWAY`) precedes lateral target onset.
  - Implemented stimuli: `rule_anti`, `left_target`/`right_target`, plus shared fixation/anchors.
  - Outcome rule: correct key is opposite the target side key.

## 4. Response and Scoring Rules

- Response mapping: `left_key=f`, `right_key=j` by default.
- Missing-response policy: timeout if no valid key within `response_deadline`; emit `response_timeout` and mark `timed_out=true`.
- Correctness logic:
  - prosaccade: left target -> `f`, right target -> `j`
  - antisaccade: left target -> `j`, right target -> `f`
- Reward/penalty updates: no monetary reward schedule; controller tracks behavioral performance counters only.
- Running metrics: `correct_total`, `correct_block`, `timeouts_total`, `timeouts_block`, plus per-trial RT and error type.

## 5. Stimulus Layout Plan

- Screen: instruction and summaries
  - Stimulus IDs shown together: `instruction_text`, `block_break`, `good_bye`
  - Layout anchors (`pos`): centered text blocks with explicit `wrapWidth`.
  - Size/spacing: instruction/summary text heights 26-28 px, wrap width 980 px.
  - Readability checks: no overlap with trial stimuli; all text is single-layer per screen.

- Screen: trial display
  - Stimulus IDs shown together: fixation cross, two peripheral anchors, rule cue, and one lateral target.
  - Layout anchors (`pos`):
    - fixation: `(0, 0)`
    - cue text: `(0, 210)`
    - anchors/targets: `(-340, 0)` and `(340, 0)`
  - Size/spacing: anchor radius 34 px, target radius 26 px.
  - Visual hierarchy: rule cue is color-coded (green/red); target appears peripherally to drive response mapping.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation phase onset |
| `rule_pro_onset` | 21 | prosaccade cue onset |
| `rule_anti_onset` | 22 | antisaccade cue onset |
| `gap_onset` | 30 | gap interval onset |
| `target_onset_left` | 40 | left target onset |
| `target_onset_right` | 41 | right target onset |
| `response_left` | 50 | left-key response captured |
| `response_right` | 51 | right-key response captured |
| `response_timeout` | 60 | response window elapsed without key |
| `iti_onset` | 70 | inter-trial interval onset |

## 7. Inference Log

- Decision: implement keyboard left/right responses as a surrogate for gaze-direction output.
- Why inference was required: cited antisaccade protocols describe eye-movement behavior; this baseline behavior build uses keypress responses for portable runtime and QA/sim compatibility.
- Citation-supported rationale: condition logic still preserves core prosaccade versus antisaccade directional rule manipulation.

- Decision: use jittered fixation/cue/gap durations in baseline profile.
- Why inference was required: cited papers vary by hardware and cohort, and no single canonical timing set is universal.
- Citation-supported rationale: short cue-gap-target sequencing is preserved, while exact values are explicitly marked as configurable in `config/*.yaml`.

