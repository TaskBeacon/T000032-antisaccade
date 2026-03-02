from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context

from .utils import RULE_ANTI, RULE_PRO, SIDE_LEFT, SIDE_RIGHT


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _as_duration(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_duration"):
        return float(controller.sample_duration(value, default_value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _trial_id(controller) -> int:
    if hasattr(controller, "next_trial_id"):
        return int(controller.next_trial_id())
    return 1


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one antisaccade/prosaccade trial."""
    trial_id = _trial_id(controller)
    rule = str(controller.parse_rule(condition)).strip().lower()
    target_side = str(controller.sample_target_side()).strip().lower()

    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0
    block_trial_index = int(getattr(controller, "trial_count_block", 0)) + 1

    left_key = str(getattr(settings, "left_key", "f")).strip().lower()
    right_key = str(getattr(settings, "right_key", "j")).strip().lower()
    response_keys = [left_key, right_key]
    correct_key = str(controller.expected_key(rule, target_side, left_key, right_key)).strip().lower()

    fixation_duration = _as_duration(controller, settings.fixation_duration, 1.0)
    cue_duration = _as_duration(controller, settings.cue_duration, 0.5)
    gap_duration = _as_duration(controller, settings.gap_duration, 0.2)
    response_deadline = float(getattr(settings, "response_deadline", 1.0))
    iti_duration = _as_duration(controller, settings.iti_duration, 0.6)

    target_stim_id = "left_target" if target_side == SIDE_LEFT else "right_target"
    target_onset_trigger = "target_onset_left" if target_side == SIDE_LEFT else "target_onset_right"
    rule_stim_id = "rule_pro" if rule == RULE_PRO else "rule_anti"
    rule_onset_trigger = "rule_pro_onset" if rule == RULE_PRO else "rule_anti_onset"

    trial_data = {
        "condition": rule,
        "block_id": block_label,
        "block_idx": block_index,
        "trial_id": trial_id,
        "trial_index": block_trial_index,
        "rule": rule,
        "target_side": target_side,
        "correct_key": correct_key,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=_deadline_s(fixation_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=rule,
        task_factors={"stage": "fixation", "rule": rule, "target_side": target_side, "block_idx": block_index},
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    rule_cue = make_unit(unit_label="rule_cue")
    rule_cue.add_stim(stim_bank.get(rule_stim_id))
    rule_cue.add_stim(stim_bank.get("left_anchor"))
    rule_cue.add_stim(stim_bank.get("right_anchor"))
    set_trial_context(
        rule_cue,
        trial_id=trial_id,
        phase="rule_cue",
        deadline_s=_deadline_s(cue_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=rule,
        task_factors={"stage": "rule_cue", "rule": rule, "target_side": target_side, "block_idx": block_index},
        stim_id=f"{rule_stim_id}+left_anchor+right_anchor",
    )
    rule_cue.show(
        duration=cue_duration,
        onset_trigger=settings.triggers.get(rule_onset_trigger),
    ).to_dict(trial_data)

    gap = make_unit(unit_label="gap")
    gap.add_stim(stim_bank.get("left_anchor"))
    gap.add_stim(stim_bank.get("right_anchor"))
    set_trial_context(
        gap,
        trial_id=trial_id,
        phase="gap",
        deadline_s=_deadline_s(gap_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=rule,
        task_factors={"stage": "gap", "rule": rule, "target_side": target_side, "block_idx": block_index},
        stim_id="left_anchor+right_anchor",
    )
    gap.show(
        duration=gap_duration,
        onset_trigger=settings.triggers.get("gap_onset"),
    ).to_dict(trial_data)

    saccade = make_unit(unit_label="saccade_response")
    saccade.add_stim(stim_bank.get("left_anchor"))
    saccade.add_stim(stim_bank.get("right_anchor"))
    saccade.add_stim(stim_bank.get(target_stim_id))
    set_trial_context(
        saccade,
        trial_id=trial_id,
        phase="saccade_response",
        deadline_s=_deadline_s(response_deadline),
        valid_keys=response_keys,
        block_id=block_label,
        condition_id=rule,
        task_factors={
            "stage": "saccade_response",
            "rule": rule,
            "target_side": target_side,
            "correct_key": correct_key,
            "left_key": left_key,
            "right_key": right_key,
            "block_idx": block_index,
        },
        stim_id=f"left_anchor+right_anchor+{target_stim_id}",
    )
    saccade.capture_response(
        keys=response_keys,
        duration=response_deadline,
        onset_trigger=settings.triggers.get(target_onset_trigger),
        response_trigger=None,
        timeout_trigger=settings.triggers.get("response_timeout"),
    )
    saccade.to_dict(trial_data)

    response_key = str(saccade.get_state("response", "")).strip().lower()
    responded = response_key in response_keys
    hit = bool(responded and response_key == correct_key)
    rt = saccade.get_state("rt", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None

    if responded:
        if response_key == left_key:
            trigger_runtime.send(settings.triggers.get("response_left"))
        elif response_key == right_key:
            trigger_runtime.send(settings.triggers.get("response_right"))

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=_deadline_s(iti_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=rule,
        task_factors={"stage": "iti", "rule": rule, "target_side": target_side, "block_idx": block_index},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    trial_data.update(
        {
            "timed_out": not responded,
            "saccade_response_response": response_key if responded else "",
            "saccade_response_rt": rt_s,
            "saccade_response_hit": bool(hit),
            "responded": bool(responded),
        }
    )

    controller.record_trial(
        hit=bool(hit),
        rt_s=rt_s,
        responded=bool(responded),
        rule=rule,
        target_side=SIDE_LEFT if target_side == SIDE_LEFT else SIDE_RIGHT,
    )
    return trial_data
