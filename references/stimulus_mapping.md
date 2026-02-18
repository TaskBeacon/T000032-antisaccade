# Stimulus Mapping

Task: `Antisaccade Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `prosaccade` | `prosaccade_cue`, `prosaccade_target` | `W2171760615` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for PROSACCADE; target token for condition-specific response context. |
| `antisaccade` | `antisaccade_cue`, `antisaccade_target` | `W2171760615` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for ANTISACCADE; target token for condition-specific response context. |
| `catch` | `catch_cue`, `catch_target` | `W2171760615` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for CATCH; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
