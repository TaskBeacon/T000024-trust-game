from __future__ import annotations

from dataclasses import dataclass
from math import exp
import random as _py_random
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Trust Game investment decisions."""

    trust_key: str = "f"
    keep_key: str = "j"
    continue_key: str = "space"
    trust_bias: float = 0.0
    inverse_temp: float = 8.0
    lapse_rate: float = 0.03
    rt_mean_s: float = 0.35
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.16

    def __post_init__(self) -> None:
        self.trust_bias = float(self.trust_bias)
        self.inverse_temp = max(1e-6, float(self.inverse_temp))
        self.lapse_rate = max(0.0, min(1.0, float(self.lapse_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _rand(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _p_trust(self, *, return_ratio: float, endowment: float, transfer_multiplier: float) -> float:
        expected_invest = float(endowment) * float(transfer_multiplier) * float(return_ratio)
        expected_keep = float(endowment)
        utility_diff = ((expected_invest - expected_keep) / max(1.0, float(endowment))) + self.trust_bias
        x = self.inverse_temp * utility_diff
        if x >= 0:
            z = exp(-x)
            return 1.0 / (1.0 + z)
        z = exp(x)
        return z / (1.0 + z)

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self.continue_key in valid_keys:
            return Action(
                key=self.continue_key,
                rt_s=max(self.rt_min_s, self.rt_mean_s - 0.10),
                meta={"source": "task_sampler", "policy": "continue"},
            )

        phase = str(obs.phase or "")
        if phase not in {"decision", "trust_decision"}:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase})

        factors = dict(obs.task_factors or {})
        return_ratio = float(factors.get("return_ratio", 0.33))
        endowment = float(factors.get("endowment", 10.0))
        transfer_multiplier = float(factors.get("transfer_multiplier", 3.0))

        p_trust = self._p_trust(
            return_ratio=return_ratio,
            endowment=endowment,
            transfer_multiplier=transfer_multiplier,
        )

        rt = max(self.rt_min_s, self._normal(self.rt_mean_s, self.rt_sd_s))

        if self._rand() < self.lapse_rate:
            key = valid_keys[0] if self._rand() < 0.5 else valid_keys[-1]
            return Action(key=key, rt_s=rt, meta={"source": "task_sampler", "policy": "lapse"})

        trust = bool(self._rand() < p_trust)
        key = self.trust_key if trust else self.keep_key
        if key not in valid_keys:
            key = valid_keys[0]

        return Action(
            key=key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "policy": "ev_logit",
                "p_trust": p_trust,
                "return_ratio": return_ratio,
                "endowment": endowment,
                "transfer_multiplier": transfer_multiplier,
            },
        )
