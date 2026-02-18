# Antisaccade Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Antisaccade Task |
| Version | v0.1.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000032-antisaccade |
| Short Description | Inhibitory control and oculomotor response suppression. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name |  |

## 1. Task Overview

This task implements an antisaccade-style inhibitory control paradigm with `prosaccade`, `antisaccade`, and `catch` conditions. Trials include cueing, anticipation, target response capture, and feedback stages.

The implementation supports standardized PsyFlow execution profiles (human, QA, scripted sim, sampler sim) and condition-specific trigger reporting.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Prepare conditions | Condition stream is prepared per block. |
| 2. Execute trials | `run_trial(...)` runs cue, anticipation, target, and feedback phases. |
| 3. Block summary | Block accuracy and score summary is displayed. |
| 4. End summary | Final score is displayed at task completion. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Condition-specific cue is shown. |
| Anticipation | Fixation stage before target response. |
| Target | Target appears and response is captured. |
| Pre-feedback fixation | Short transition fixation stage. |
| Feedback | Hit/miss feedback with score delta is shown. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive target duration | Target duration is adjusted toward configured target accuracy. |
| Condition history | Outcomes are tracked by condition. |
| Score update | Trial hit/miss outcome updates score. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target monitoring stage. |
| `target` | Target response window stage. |

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

| Name | Type | Description |
|---|---|---|
| `prosaccade_cue`, `antisaccade_cue`, `catch_cue` | text | Condition-specific cue prompts. |
| `prosaccade_target`, `antisaccade_target`, `catch_target` | text | Condition targets used for response capture. |
| `*_hit_feedback`, `*_miss_feedback` | text | Condition-specific outcome feedback. |
| `fixation`, `block_break`, `good_bye` | text | Shared fixation and summary screens. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed an inhibitory control task comprising prosaccade, antisaccade, and catch trials. Each trial combined condition cueing, a pre-target interval, a target-response window, and immediate feedback.

Task difficulty was stabilized with adaptive target-duration control based on recent performance. Trial logs include condition labels, response outcomes, timing metrics, and score updates.

Trigger emissions were configured for major trial stages to support synchronized acquisition and QA reproducibility.
