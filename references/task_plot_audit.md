# Task Plot Audit

- generated_at: 2026-03-18T23:07:51
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\T000032-antisaccade

## 1. Inputs and provenance

- E:\xhmhc\TaskBeacon\T000032-antisaccade\README.md
- E:\xhmhc\TaskBeacon\T000032-antisaccade\config\config.yaml
- E:\xhmhc\TaskBeacon\T000032-antisaccade\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | `fixation` | Show center fixation and left/right peripheral anchors. |
- | `rule_cue` | Present condition cue (`朝圆点` or `背离圆点`). |
- | `gap` | Remove cue and keep neutral anchors before target onset. |
- | `saccade_response` | Present one lateral target and capture left/right response under deadline. |
- | `iti` | Show neutral fixation scene until next trial. |

## 3. Evidence extracted from config/source

- prosaccade: phase=fixation, deadline_expr=fixation_duration, response_expr=n/a, stim_expr='fixation'
- prosaccade: phase=rule cue, deadline_expr=cue_duration, response_expr=n/a, stim_expr=f'{rule_stim_id}+left_anchor+right_anchor'
- prosaccade: phase=gap, deadline_expr=gap_duration, response_expr=n/a, stim_expr='left_anchor+right_anchor'
- prosaccade: phase=saccade response, deadline_expr=response_deadline, response_expr=n/a, stim_expr=f'left_anchor+right_anchor+{target_stim_id}'
- prosaccade: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'
- antisaccade: phase=fixation, deadline_expr=fixation_duration, response_expr=n/a, stim_expr='fixation'
- antisaccade: phase=rule cue, deadline_expr=cue_duration, response_expr=n/a, stim_expr=f'{rule_stim_id}+left_anchor+right_anchor'
- antisaccade: phase=gap, deadline_expr=gap_duration, response_expr=n/a, stim_expr='left_anchor+right_anchor'
- antisaccade: phase=saccade response, deadline_expr=response_deadline, response_expr=n/a, stim_expr=f'left_anchor+right_anchor+{target_stim_id}'
- antisaccade: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 2
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.050, right=0.055, blank=0.158
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0504, 'right_ratio': 0.055, 'blank_ratio': 0.1584}

## 7. Output files and checksums

- E:\xhmhc\TaskBeacon\T000032-antisaccade\references\task_plot_spec.yaml: sha256=947f6701ccdd5d0ecdfcd609f8d7b3f1b7659130263e1f675c1764d3b057b524
- E:\xhmhc\TaskBeacon\T000032-antisaccade\references\task_plot_spec.json: sha256=514d0ee4388fb339a902ef5738d77337f6df34bf05fd3bde07a851fcf9fe85b3
- E:\xhmhc\TaskBeacon\T000032-antisaccade\references\task_plot_source_excerpt.md: sha256=c6c82bc58c7561093552c4928734c5986d8aa8a20ee99c2e7da65a56f458da60
- E:\xhmhc\TaskBeacon\T000032-antisaccade\task_flow.png: sha256=06ce63c0caa1e722313d5fd70ce36aa3e30c224bfcd6720e3cddba3a5b6c7947

## 8. Inferred/uncertain items

- unparsed if-tests defaulted to condition-agnostic applicability: responded; response_key == left_key; response_key == right_key
