# Antisaccade Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Antisaccade Task |
| Version | v0.1.2-dev |
| URL / Repository | https://github.com/TaskBeacon/T000032-antisaccade |
| Short Description | Rule-dependent inhibitory control with prosaccade versus antisaccade responses. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a two-condition antisaccade paradigm:

- `prosaccade`: respond toward the target side.
- `antisaccade`: respond opposite the target side.

Each trial presents a fixation baseline, a rule cue, a short gap, and a lateralized target response window. The build uses keyboard direction keys (`f/j`) as a surrogate behavioral output for gaze direction in a portable PsyFlow runtime.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block setup | Load block condition stream and reset block counters in controller. |
| 2. Trial execution | Run fixation -> rule cue -> gap -> saccade response -> ITI for each trial. |
| 3. Block summary | Show block-level accuracy, correct RT, and timeout count. |
| 4. Final summary | Show session-level totals and save CSV output. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `fixation` | Show center fixation and left/right peripheral anchors. |
| `rule_cue` | Present condition cue (`LOOK TOWARD` or `LOOK AWAY`). |
| `gap` | Remove cue and keep neutral fixation anchors before target onset. |
| `saccade_response` | Present one lateral target and capture left/right response under deadline. |
| `iti` | Show neutral fixation scene until next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Rule parser | Converts condition tokens to `prosaccade` or `antisaccade` runtime rule. |
| Target sampler | Samples target side (`left`/`right`) per trial with equal probability. |
| Correct-key mapper | Prosaccade uses same-side key; antisaccade uses opposite-side key. |
| Performance tracker | Maintains trial/block/session counts for accuracy, RT, and timeouts. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `fixation` | Neutral baseline before instruction cue. |
| `rule_cue` | Rule preparation period. |
| `gap` | Cue-target separation interval. |
| `saccade_response` | Active response capture window. |
| `iti` | Inter-trial reset interval. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `fixation` | Central fixation cross used in fixation/gap/ITI phases. |
| `rule_pro`, `rule_anti` | Color-coded rule cues (`LOOK TOWARD`, `LOOK AWAY`). |
| `left_anchor`, `right_anchor` | Peripheral position anchors shown before target onset. |
| `left_target`, `right_target` | Lateral white target circles for directional response. |
| `instruction_text`, `block_break`, `good_bye` | Entry, transition, and completion text screens. |

### d. Timing

| Stage | Duration |
|---|---|
| fixation | uniform in `fixation_duration` range |
| rule cue | uniform in `cue_duration` range |
| gap | uniform in `gap_duration` range |
| response window | `response_deadline` |
| ITI | `iti_duration` |

## 4. Methods (for academic publication)

Participants completed a rule-based oculomotor inhibition task containing prosaccade and antisaccade trials. Each trial began with fixation, followed by an explicit rule cue and a short cue-target gap, then a lateral target requiring a directional response. Prosaccade trials required same-side responses relative to target location; antisaccade trials required opposite-side responses.

Behavioral outputs were logged at trial level, including condition, target side, response key, correctness, reaction time, and timeout status. The implementation emits phase-aligned triggers for fixation, cue, gap, target onset, response category, and ITI to support synchronized acquisition workflows.

