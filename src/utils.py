from __future__ import annotations

import math
from typing import Any, Callable

from psychopy import logging

RULE_PRO = "prosaccade"
RULE_ANTI = "antisaccade"
SIDE_LEFT = "left"
SIDE_RIGHT = "right"

DEFAULT_CONDITIONS = (RULE_PRO, RULE_ANTI)


def _make_seeded_random(seed: int) -> Callable[[], float]:
    value = seed & 0xFFFFFFFF

    def rng() -> float:
        nonlocal value
        value = (value + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((value ^ (value >> 15)) * (1 | value)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    return rng


def _to_float(value: Any, fallback: float) -> float:
    try:
        parsed = float(value)
    except Exception:
        return float(fallback)
    if math.isnan(parsed) or math.isinf(parsed):
        return float(fallback)
    return parsed


def parse_rule(condition: str) -> str:
    token = str(condition).strip().lower()
    if token in DEFAULT_CONDITIONS:
        return token
    raise ValueError(f"Unsupported antisaccade condition: {condition!r}")


def _trial_rng(*, block_seed: int | None, trial_id: int, condition: str) -> Callable[[], float]:
    base = int(block_seed) if block_seed is not None else 0
    rule = parse_rule(condition)
    cond_offset = 11 if rule == RULE_PRO else 12
    mixed_seed = (base * 1000003 + int(trial_id) * 97 + cond_offset) & 0xFFFFFFFF
    return _make_seeded_random(mixed_seed)


def sample_target_side(rng: Callable[[], float]) -> str:
    return SIDE_LEFT if rng() < 0.5 else SIDE_RIGHT


def expected_key(rule: str, target_side: str, left_key: str, right_key: str) -> str:
    if rule == RULE_PRO:
        return left_key if target_side == SIDE_LEFT else right_key
    return right_key if target_side == SIDE_LEFT else left_key


def build_antisaccade_trial_spec(
    *,
    condition: str,
    trial_id: int,
    block_seed: int | None = None,
    settings: Any,
) -> dict[str, Any]:
    rule = parse_rule(condition)
    rng = _trial_rng(block_seed=block_seed, trial_id=trial_id, condition=rule)
    target_side = sample_target_side(rng)

    left_key = str(getattr(settings, "left_key", "f")).strip().lower()
    right_key = str(getattr(settings, "right_key", "j")).strip().lower()
    correct_key = expected_key(rule, target_side, left_key, right_key)

    if bool(getattr(settings, "enable_logging", True)):
        logging.data(
            f"[Antisaccade] condition={rule} trial_id={trial_id} "
            f"target_side={target_side} correct_key={correct_key}"
        )

    return {
        "condition": rule,
        "condition_id": rule,
        "rule": rule,
        "target_side": target_side,
        "correct_key": correct_key,
        "left_key": left_key,
        "right_key": right_key,
    }


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    token = str(value if value is not None else "").strip().lower()
    return token in {"1", "true", "yes", "y"}


def _as_float(value: Any) -> float | None:
    try:
        parsed = float(value)
    except Exception:
        return None
    return parsed if math.isfinite(parsed) else None


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "accuracy": 0.0,
            "mean_rt_ms": 0.0,
            "timeout_count": 0,
            "total_trials": 0,
        }

    correct = 0
    timeout_count = 0
    rt_sum = 0.0
    rt_count = 0
    for row in rows:
        if _as_bool(row.get("saccade_response_hit", False)):
            correct += 1
            rt = _as_float(row.get("saccade_response_rt", None))
            if rt is not None:
                rt_sum += rt
                rt_count += 1
        if _as_bool(row.get("timed_out", False)):
            timeout_count += 1

    accuracy = correct / len(rows)
    mean_rt_ms = (rt_sum / rt_count) * 1000.0 if rt_count > 0 else 0.0
    return {
        "accuracy": accuracy,
        "mean_rt_ms": mean_rt_ms,
        "timeout_count": timeout_count,
        "total_trials": len(rows),
    }


def summarizeBlock(
    reducedRows: list[dict[str, Any]],
    blockId: str,
) -> dict[str, Any]:
    rows = [row for row in reducedRows if str(row.get("block_id", "")) == blockId]
    return _summarize(rows)


def summarizeOverall(reducedRows: list[dict[str, Any]]) -> dict[str, Any]:
    return _summarize(list(reducedRows))
