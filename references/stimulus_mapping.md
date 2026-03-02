# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `prosaccade` | rule_cue | `rule_pro`, `left_anchor`, `right_anchor` | Green rule cue instructs orienting toward the target location. | W2104663113 | Pro-saccade preparatory set is distinct from anti-saccade set. | psychopy_builtin | `config/*.yaml -> stimuli.rule_pro/left_anchor/right_anchor` | Rule wording is config-defined. |
| `antisaccade` | rule_cue | `rule_anti`, `left_anchor`, `right_anchor` | Red rule cue instructs orienting opposite to target location. | W2104663113 | Anti-saccade condition requires rule-dependent response inversion. | psychopy_builtin | `config/*.yaml -> stimuli.rule_anti/left_anchor/right_anchor` | Rule wording is config-defined. |
| `all_conditions` | fixation | `fixation` | Central fixation cross before each trial and during ITI. | W1989816441 | Fixation baseline is needed before rule and target events. | psychopy_builtin | `config/*.yaml -> stimuli.fixation` | Used in both `fixation` and `iti` phases. |
| `all_conditions` | gap | `left_anchor`, `right_anchor` | Brief gap phase keeps spatial anchors visible before target onset. | W1875187353 | Gap interval supports preparation/execution separation in saccade paradigms. | psychopy_builtin | `config/*.yaml -> stimuli.left_anchor/right_anchor` | Trigger: `gap_onset`. |
| `all_conditions` | saccade_response | `left_anchor`, `right_anchor`, `left_target` or `right_target` | Peripheral target appears on one side; participant responds left/right per current rule. | W1875187353 | Target side and rule jointly determine the expected saccade response. | psychopy_builtin | `config/*.yaml -> stimuli.left_target/right_target/anchors` | Response phase label is `saccade_response` for QA/sim interoperability. |
| `all_conditions` | envelope | `instruction_text`, `block_break`, `good_bye` | Instruction and summary screens report accuracy, RT, and timeout metrics. | W2163144416 | Behavioral outcomes are summarized across pro/anti inhibitory control performance. | psychopy_builtin | `config/*.yaml -> stimuli.instruction_text/block_break/good_bye` | Participant-facing text remains in config. |
