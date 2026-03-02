# Stimulus Mapping

Task: `Antisaccade Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `prosaccade` | `fixation`, `left_anchor`, `right_anchor`, `rule_pro`, `left_target`, `right_target` | `W2163144416` | Prosaccade trials require orienting toward a lateral target after rule preparation. | `psychopy_builtin` | Correct key is same-side key as target location. |
| `antisaccade` | `fixation`, `left_anchor`, `right_anchor`, `rule_anti`, `left_target`, `right_target` | `W2163144416` | Antisaccade trials require inhibitory remapping to the side opposite the lateral target. | `psychopy_builtin` | Correct key is opposite-side key from target location. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye` | `W1989816441` | Shared instruction and summary screens provide stable task envelope across blocks and modes. | `psychopy_builtin` | No external media assets are required. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.

