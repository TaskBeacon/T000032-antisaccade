# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['prosaccade', 'antisaccade']` | `W2163144416` | `high` | Core contrast is prosaccade versus antisaccade rule sets. |
| `task.total_blocks` | `3` | `W1989816441` | `inferred` | Multi-block layout supports stable within-subject performance estimation in baseline profile. |
| `task.trial_per_block` | `48` | `W1989816441` | `inferred` | Fixed block length provides balanced per-condition sampling. |
| `task.left_key` | `f` | `W2163144416` | `inferred` | Keyboard surrogate for leftward response direction. |
| `task.right_key` | `j` | `W2163144416` | `inferred` | Keyboard surrogate for rightward response direction. |
| `timing.fixation_duration` | `[0.8, 1.2]` | `W2104663113` | `inferred` | Short jittered fixation period before rule cue and target preparation. |
| `timing.cue_duration` | `[0.4, 0.6]` | `W2104663113` | `inferred` | Brief preparatory rule-cue epoch before gap/target stages. |
| `timing.gap_duration` | `[0.15, 0.25]` | `W1875187353` | `inferred` | Gap interval separates instruction cue and response target onset. |
| `timing.response_deadline` | `1.0` | `W2163144416` | `inferred` | Bounded response window for consistent timeout handling. |
| `timing.iti_duration` | `0.6` | `W1989816441` | `inferred` | Fixed ITI for block pacing and event separation. |
| `triggers.map.fixation_onset` | `20` | `W2163144416` | `inferred` | Marks fixation state onset. |
| `triggers.map.rule_pro_onset` | `21` | `W2163144416` | `inferred` | Marks prosaccade cue onset. |
| `triggers.map.rule_anti_onset` | `22` | `W2163144416` | `inferred` | Marks antisaccade cue onset. |
| `triggers.map.gap_onset` | `30` | `W2104663113` | `inferred` | Marks cue-target gap onset. |
| `triggers.map.target_onset_left` | `40` | `W2163144416` | `inferred` | Marks left target onset in response phase. |
| `triggers.map.target_onset_right` | `41` | `W2163144416` | `inferred` | Marks right target onset in response phase. |
| `triggers.map.response_left` | `50` | `W2163144416` | `inferred` | Marks captured left response key. |
| `triggers.map.response_right` | `51` | `W2163144416` | `inferred` | Marks captured right response key. |
| `triggers.map.response_timeout` | `60` | `W2163144416` | `inferred` | Marks no response before deadline. |
| `triggers.map.iti_onset` | `70` | `W1989816441` | `inferred` | Marks inter-trial interval onset. |
