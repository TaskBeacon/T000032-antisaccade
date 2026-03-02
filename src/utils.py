from __future__ import annotations

import random
from typing import Any

from psychopy import logging

RULE_PRO = "prosaccade"
RULE_ANTI = "antisaccade"
SIDE_LEFT = "left"
SIDE_RIGHT = "right"


class Controller:
    """Trial sampler and performance tracker for antisaccade/prosaccade task."""

    def __init__(
        self,
        fixation_duration: list[float] | tuple[float, ...] | float = (0.8, 1.2),
        cue_duration: list[float] | tuple[float, ...] | float = (0.4, 0.6),
        gap_duration: list[float] | tuple[float, ...] | float = (0.15, 0.25),
        response_deadline: float = 1.0,
        iti_duration: float = 0.6,
        random_seed: int | None = None,
        enable_logging: bool = True,
    ):
        self.fixation_duration = fixation_duration
        self.cue_duration = cue_duration
        self.gap_duration = gap_duration
        self.response_deadline = max(0.1, float(response_deadline))
        self.iti_duration = max(0.0, float(iti_duration))
        self.enable_logging = bool(enable_logging)
        self.rng = random.Random(random_seed)

        self.block_idx = -1
        self.trial_count_total = 0
        self.trial_count_block = 0
        self.correct_total = 0
        self.correct_block = 0
        self.timeout_total = 0
        self.timeout_block = 0
        self.correct_rt_sum_total = 0.0
        self.correct_rt_sum_block = 0.0
        self.correct_rt_n_total = 0
        self.correct_rt_n_block = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        cfg = dict(config or {})
        return cls(
            fixation_duration=cfg.get("fixation_duration", (0.8, 1.2)),
            cue_duration=cfg.get("cue_duration", (0.4, 0.6)),
            gap_duration=cfg.get("gap_duration", (0.15, 0.25)),
            response_deadline=cfg.get("response_deadline", 1.0),
            iti_duration=cfg.get("iti_duration", 0.6),
            random_seed=cfg.get("random_seed", None),
            enable_logging=bool(cfg.get("enable_logging", True)),
        )

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0
        self.correct_block = 0
        self.timeout_block = 0
        self.correct_rt_sum_block = 0.0
        self.correct_rt_n_block = 0

    def next_trial_id(self) -> int:
        return int(self.trial_count_total) + 1

    def sample_duration(self, value: Any, default: float) -> float:
        if isinstance(value, (int, float)):
            return max(0.0, float(value))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            try:
                low = float(value[0])
                high = float(value[1])
            except Exception:
                return max(0.0, float(default))
            if high < low:
                low, high = high, low
            return max(0.0, float(self.rng.uniform(low, high)))
        return max(0.0, float(default))

    def parse_rule(self, condition: str) -> str:
        token = str(condition).strip().lower()
        if token in {RULE_PRO, RULE_ANTI}:
            return token
        raise ValueError(f"Unsupported antisaccade condition: {condition!r}")

    def sample_target_side(self) -> str:
        return SIDE_LEFT if self.rng.random() < 0.5 else SIDE_RIGHT

    @staticmethod
    def expected_key(rule: str, target_side: str, left_key: str, right_key: str) -> str:
        if rule == RULE_PRO:
            return left_key if target_side == SIDE_LEFT else right_key
        return right_key if target_side == SIDE_LEFT else left_key

    @staticmethod
    def side_label(side: str) -> str:
        return SIDE_LEFT if side == SIDE_LEFT else SIDE_RIGHT

    def record_trial(self, *, hit: bool, rt_s: float | None, responded: bool, rule: str, target_side: str) -> None:
        self.trial_count_total += 1
        self.trial_count_block += 1
        if bool(hit):
            self.correct_total += 1
            self.correct_block += 1
            if rt_s is not None:
                rt = max(0.0, float(rt_s))
                self.correct_rt_sum_total += rt
                self.correct_rt_sum_block += rt
                self.correct_rt_n_total += 1
                self.correct_rt_n_block += 1
        if not responded:
            self.timeout_total += 1
            self.timeout_block += 1

        if self.enable_logging:
            logging.data(
                f"[Antisaccade] block={self.block_idx} trial_block={self.trial_count_block} "
                f"trial_total={self.trial_count_total} rule={rule} side={target_side} "
                f"hit={bool(hit)} responded={responded} rt={rt_s}"
            )
