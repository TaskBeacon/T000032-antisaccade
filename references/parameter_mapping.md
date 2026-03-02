# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['prosaccade','antisaccade']` | W2104663113 | Core paradigm contrast is pro-vs-anti rule switching with common target locations. | high | Condition token maps to rule cue stimulus. |
| task.blocks_trials | `task.total_blocks`, `task.trial_per_block` | Human `3 x 48`; QA/sim `1 x 16` | W2163144416 | Repeated trial sampling is required for stable inhibitory control metrics. | inferred | QA/sim reduced for validation runtime only. |
| task.key_mapping | `task.left_key`, `task.right_key`, `task.key_list` | left=`f`, right=`j`, continue=`space` | W2163144416 | Binary saccade-direction response mapping must be explicit and stable. | inferred | Keys remain config-defined for hardware/localization portability. |
| timing.fixation | `timing.fixation_duration` | Human `[0.8,1.2]`; QA `[0.3,0.4]` | W1989816441 | Fixation epoch precedes preparatory rule cue and target onset. | inferred | Sampled per trial by controller. |
| timing.rule_cue | `timing.cue_duration` | Human `[0.4,0.6]`; QA `[0.2,0.3]` | W2104663113 | Preparatory-set cue duration supports pro/anti rule preparation. | inferred | Rendered as colored rule text stimulus. |
| timing.gap | `timing.gap_duration` | Human `[0.15,0.25]`; QA `[0.08,0.12]` | W1875187353 | Gap between cue and target is commonly used in antisaccade control paradigms. | inferred | Triggered by `gap_onset`. |
| timing.response_deadline | `timing.response_deadline` | Human `1.0s`; QA `0.8s` | W2163144416 | Bounded response window supports hit/error/timeout classification. | inferred | Timeout trigger emitted on no key response. |
| timing.iti | `timing.iti_duration` | Human `0.6s`; QA `0.2s` | W1989816441 | ITI separates sequential oculomotor control events. | inferred | Configured as fixed duration in this implementation. |
| trigger.rule | `triggers.map.rule_pro_onset`, `triggers.map.rule_anti_onset` | `21`, `22` | W2104663113 | Rule-preparation onsets must be separable between pro and anti settings. | inferred | Emitted at cue onset. |
| trigger.target | `triggers.map.target_onset_left`, `triggers.map.target_onset_right` | `40`, `41` | W1875187353 | Target-side onsets are critical for lateralized response analysis. | inferred | Set by sampled target side each trial. |
| trigger.response | `triggers.map.response_left`, `triggers.map.response_right`, `triggers.map.response_timeout` | `50`, `51`, `60` | W2163144416 | Response direction and omission must be separately event-coded. | inferred | Left/right triggers emitted after response mapping. |
| trigger.iti | `triggers.map.iti_onset` | `70` | W1989816441 | Inter-trial boundary code supports event segmentation. | inferred | Emitted for every trial. |
