from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass(frozen=True)
class PartnerProfile:
    label: str
    return_ratio: float


class Controller:
    """Trust game scheduler and payoff tracker."""

    def __init__(
        self,
        *,
        partner_profiles: dict[str, dict[str, Any]],
        endowment: int = 10,
        transfer_multiplier: float = 3.0,
        return_noise_ratio: float = 0.0,
        seed: int = 24024,
        enable_logging: bool = True,
    ) -> None:
        self.endowment = int(endowment)
        self.transfer_multiplier = float(transfer_multiplier)
        self.return_noise_ratio = max(0.0, float(return_noise_ratio))
        self.seed = int(seed)
        self.enable_logging = bool(enable_logging)

        self._rng = random.Random(self.seed)
        self._profiles = self._build_profiles(partner_profiles)
        self._history: list[dict[str, Any]] = []
        self._total_earned = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        profiles = config.get("partner_profiles", {})
        if not isinstance(profiles, dict) or not profiles:
            raise ValueError("controller.partner_profiles must be a non-empty mapping")
        return cls(
            partner_profiles=profiles,
            endowment=int(config.get("endowment", 10)),
            transfer_multiplier=float(config.get("transfer_multiplier", 3.0)),
            return_noise_ratio=float(config.get("return_noise_ratio", 0.0)),
            seed=int(config.get("seed", 24024)),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def _build_profiles(self, raw: dict[str, dict[str, Any]]) -> dict[str, PartnerProfile]:
        profiles: dict[str, PartnerProfile] = {}
        for key, spec in raw.items():
            ratio = float(spec.get("return_ratio", 0.33))
            ratio = max(0.0, min(1.0, ratio))
            profiles[str(key)] = PartnerProfile(
                label=str(spec.get("label", key)),
                return_ratio=ratio,
            )
        return profiles

    @property
    def total_earned(self) -> int:
        return int(self._total_earned)

    @property
    def histories(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in self._history:
            grouped.setdefault(str(item["condition"]), []).append(item)
        return grouped

    def get_profile(self, condition: str) -> PartnerProfile:
        condition = str(condition)
        if condition not in self._profiles:
            raise KeyError(f"Unknown condition: {condition!r}")
        return self._profiles[condition]

    def prepare_block(self, *, block_idx: int, n_trials: int, conditions: list[str]) -> list[tuple[Any, ...]]:
        if n_trials <= 0:
            return []

        valid_conditions = [str(c) for c in conditions if str(c) in self._profiles]
        if not valid_conditions:
            raise ValueError("No valid trust-game conditions available")

        scheduled = [valid_conditions[i % len(valid_conditions)] for i in range(n_trials)]
        self._rng.shuffle(scheduled)

        planned: list[tuple[Any, ...]] = []
        for trial_index, cond in enumerate(scheduled, start=1):
            profile = self.get_profile(cond)
            condition_id = f"{cond}_r{int(round(profile.return_ratio * 100)):02d}_t{trial_index:03d}"
            planned.append((cond, profile.label, float(profile.return_ratio), condition_id, int(trial_index)))

        if self.enable_logging:
            logging.data(
                "[TrustController] "
                f"block={block_idx} n_trials={n_trials} seed={self.seed} "
                f"conditions={valid_conditions}"
            )
        return planned

    def _sample_return(self, multiplied_amount: int, ratio: float) -> int:
        if multiplied_amount <= 0:
            return 0

        expected = multiplied_amount * ratio
        if self.return_noise_ratio > 0:
            noise_span = multiplied_amount * self.return_noise_ratio
            expected += self._rng.uniform(-noise_span, noise_span)

        returned = int(round(expected))
        return max(0, min(multiplied_amount, returned))

    def resolve_outcome(
        self,
        *,
        condition: str,
        block_idx: int,
        trial_index: int,
        trusted: bool,
        timed_out: bool,
    ) -> dict[str, Any]:
        profile = self.get_profile(condition)

        invested = int(self.endowment if trusted else 0)
        multiplied_amount = int(round(invested * self.transfer_multiplier))
        returned = self._sample_return(multiplied_amount, profile.return_ratio)
        earned = int(self.endowment - invested + returned)

        self._total_earned += earned

        record = {
            "condition": str(condition),
            "partner_label": profile.label,
            "return_ratio": float(profile.return_ratio),
            "block_idx": int(block_idx),
            "trial_index": int(trial_index),
            "trusted": bool(trusted),
            "timed_out": bool(timed_out),
            "endowment": int(self.endowment),
            "invested": int(invested),
            "multiplied_amount": int(multiplied_amount),
            "returned": int(returned),
            "earned": int(earned),
            "total_earned": int(self._total_earned),
        }
        self._history.append(record)

        if self.enable_logging:
            logging.data(
                "[TrustController] "
                f"trial={trial_index} block={block_idx} condition={condition} "
                f"trusted={trusted} timed_out={timed_out} "
                f"invested={invested} returned={returned} earned={earned} total={self._total_earned}"
            )

        return record
