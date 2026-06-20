from __future__ import annotations

from functools import partial
from psyflow import StimUnit, next_trial_id, resolve_deadline, set_trial_context

from .utils import parse_trust_condition


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
    parsed = parse_trust_condition(condition)
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_index = int(parsed["trial_index"]) if parsed["trial_index"] > 0 else 1
    trial_id = next_trial_id()
    trust_key, keep_key = list(settings.key_list)

    trial_data = {
        "trial_id": trial_id,
        "trial_index": trial_index,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "partner_label": parsed["partner_label"],
        "return_ratio": float(parsed["return_ratio"]),
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    partner_cue = make_unit(unit_label="partner_cue").add_stim(
        stim_bank.get_and_format("partner_cue", partner_label=parsed["partner_label"])
    )
    set_trial_context(
        partner_cue,
        trial_id=trial_id,
        phase="partner_cue",
        deadline_s=resolve_deadline(settings.partner_cue_duration),
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
    partner_cue.show(
        duration=settings.partner_cue_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_partner_cue_onset"),
    ).to_dict(trial_data)

    pre_decision_fixation = make_unit(unit_label="pre_decision_fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        pre_decision_fixation,
        trial_id=trial_id,
        phase="pre_decision_fixation",
        deadline_s=resolve_deadline(settings.pre_decision_fixation_duration),
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
    pre_decision_fixation.show(
        duration=settings.pre_decision_fixation_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_pre_decision_fixation_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="decision").add_stim(
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
        deadline_s=resolve_deadline(settings.decision_duration),
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

    choice_label = "invest" if trusted else "keep" if kept else "timeout"

    outcome = controller.resolve_outcome(
        condition=parsed["condition"],
        block_idx=block_idx_val,
        trial_index=trial_index,
        trusted=trusted,
        timed_out=timed_out,
    )

    decision_confirmation_stim_id = (
        "decision_timeout" if timed_out else "decision_invest" if trusted else "decision_keep"
    )
    decision_confirmation = make_unit(unit_label="decision_confirmation").add_stim(
        stim_bank.get_and_format(decision_confirmation_stim_id, choice_label=choice_label)
    )
    set_trial_context(
        decision_confirmation,
        trial_id=trial_id,
        phase="decision_confirmation",
        deadline_s=resolve_deadline(settings.decision_confirmation_duration),
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
        stim_id=decision_confirmation_stim_id,
    )
    decision_confirmation.show(
        duration=settings.decision_confirmation_duration,
        onset_trigger=settings.triggers.get("decision_confirmation_onset"),
    ).to_dict(trial_data)

    outcome_feedback = make_unit(unit_label="outcome_feedback").add_stim(
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
        outcome_feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=resolve_deadline(settings.outcome_feedback_duration),
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
    outcome_feedback.show(
        duration=settings.outcome_feedback_duration,
        onset_trigger=settings.triggers.get("outcome_feedback_onset"),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=resolve_deadline(settings.iti_duration),
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
