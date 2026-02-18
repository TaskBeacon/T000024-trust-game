from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _parse_condition(condition: Any) -> dict[str, Any]:
    if isinstance(condition, tuple) and len(condition) >= 5:
        name, partner_label, return_ratio, condition_id, trial_index, *_ = condition
        return {
            "condition": str(name),
            "partner_label": str(partner_label),
            "return_ratio": float(return_ratio),
            "condition_id": str(condition_id),
            "trial_index": int(trial_index),
        }

    if isinstance(condition, dict):
        return {
            "condition": str(condition.get("condition", "neutral")),
            "partner_label": str(condition.get("partner_label", "Partner")),
            "return_ratio": float(condition.get("return_ratio", 0.33)),
            "condition_id": str(condition.get("condition_id", "unknown")),
            "trial_index": int(condition.get("trial_index", 0)),
        }

    return {
        "condition": str(condition),
        "partner_label": str(condition),
        "return_ratio": 0.33,
        "condition_id": str(condition),
        "trial_index": 0,
    }


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
    """Run one Trust Game trial."""
    parsed = _parse_condition(condition)
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_id = int(parsed["trial_index"]) if parsed["trial_index"] > 0 else 1
    trust_key, keep_key = list(settings.key_list)

    trial_data = {
        "trial_id": trial_id,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "partner_label": parsed["partner_label"],
        "return_ratio": float(parsed["return_ratio"]),
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: partner_cue
    cue = make_unit(unit_label="cue").add_stim(
        stim_bank.get_and_format("partner_cue", partner_label=parsed["partner_label"])
    )
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="partner_cue",
        deadline_s=_deadline_s(settings.cue_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "partner_cue",
            "condition": parsed["condition"],
            "partner_label": parsed["partner_label"],
            "block_idx": block_idx_val,
        },
        stim_id="partner_cue",
    )
    cue.show(
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_cue_onset"),
    ).to_dict(trial_data)

    # phase: pre_decision_fixation
    anticipation = make_unit(unit_label="anticipation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        anticipation,
        trial_id=trial_id,
        phase="pre_decision_fixation",
        deadline_s=_deadline_s(settings.anticipation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "pre_decision_fixation",
            "condition": parsed["condition"],
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    anticipation.show(duration=settings.anticipation_duration).to_dict(trial_data)

    # phase: trust_decision
    decision = make_unit(unit_label="target").add_stim(
        stim_bank.get_and_format(
            "decision_panel",
            partner_label=parsed["partner_label"],
            endowment=int(controller.endowment),
        )
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="trust_decision",
        deadline_s=_deadline_s(settings.decision_duration),
        valid_keys=[trust_key, keep_key],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "trust_decision",
            "condition": parsed["condition"],
            "partner_label": parsed["partner_label"],
            "return_ratio": float(parsed["return_ratio"]),
            "endowment": int(controller.endowment),
            "transfer_multiplier": float(controller.transfer_multiplier),
            "trust_key": trust_key,
            "keep_key": keep_key,
            "block_idx": block_idx_val,
        },
        stim_id="decision_panel",
    )
    decision.capture_response(
        keys=[trust_key, keep_key],
        duration=settings.decision_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_decision_onset"),
        response_trigger=settings.triggers.get("decision_response"),
        timeout_trigger=settings.triggers.get("decision_timeout"),
    )
    decision.to_dict(trial_data)

    response = decision.get_state("response")
    trusted = bool(response == trust_key)
    kept = bool(response == keep_key)
    timed_out = not (trusted or kept)
    if timed_out:
        trusted = False

    choice_label = "投资" if trusted else "保留" if kept else "超时"

    outcome = controller.resolve_outcome(
        condition=parsed["condition"],
        block_idx=block_idx_val,
        trial_index=trial_id,
        trusted=trusted,
        timed_out=timed_out,
    )

    decision_feedback_name = "decision_invest" if trusted else "decision_keep" if kept else "decision_timeout"
    # phase: decision_confirmation
    decision_feedback = make_unit(unit_label="decision_feedback").add_stim(
        stim_bank.get_and_format(decision_feedback_name, choice_label=choice_label)
    )
    set_trial_context(
        decision_feedback,
        trial_id=trial_id,
        phase="decision_confirmation",
        deadline_s=_deadline_s(settings.decision_feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "decision_confirmation",
            "choice_label": choice_label,
            "trusted": trusted,
            "timed_out": timed_out,
            "block_idx": block_idx_val,
        },
        stim_id=decision_feedback_name,
    )
    decision_feedback.show(
        duration=settings.decision_feedback_duration,
        onset_trigger=settings.triggers.get("decision_feedback_onset"),
    ).to_dict(trial_data)

    # phase: outcome_feedback
    feedback = make_unit(unit_label="feedback").add_stim(
        stim_bank.get_and_format(
            "outcome_feedback",
            partner_label=outcome["partner_label"],
            invested=int(outcome["invested"]),
            multiplied_amount=int(outcome["multiplied_amount"]),
            returned=int(outcome["returned"]),
            earned=int(outcome["earned"]),
            total_earned=int(outcome["total_earned"]),
        )
    )
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=_deadline_s(settings.feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "outcome_feedback",
            "trusted": trusted,
            "invested": int(outcome["invested"]),
            "returned": int(outcome["returned"]),
            "earned": int(outcome["earned"]),
            "total_earned": int(outcome["total_earned"]),
            "block_idx": block_idx_val,
        },
        stim_id="outcome_feedback",
    )
    feedback.show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get("outcome_feedback_onset"),
    ).to_dict(trial_data)

    # phase: inter_trial_interval
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=_deadline_s(settings.iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(duration=settings.iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    trial_data["choice_label"] = choice_label
    trial_data["trusted"] = trusted
    trial_data["kept"] = kept
    trial_data["timed_out"] = timed_out
    trial_data["endowment"] = int(outcome["endowment"])
    trial_data["invested"] = int(outcome["invested"])
    trial_data["multiplied_amount"] = int(outcome["multiplied_amount"])
    trial_data["returned"] = int(outcome["returned"])
    trial_data["earned"] = int(outcome["earned"])
    trial_data["total_earned"] = int(outcome["total_earned"])
    trial_data["feedback_delta"] = int(outcome["earned"])

    return trial_data
