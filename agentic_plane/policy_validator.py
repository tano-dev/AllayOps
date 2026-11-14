"""Constitutional AI Safety Gate (PolicyValidator) for AllayOps."""

from __future__ import annotations

import json
import re
from typing import Any

from shared_interfaces.schemas import ActionProposal, SafetyVerdict

ALLOWED_ACTIONS: frozenset[str] = frozenset(
    {
        "save_all",
        "tick_freeze",
        "tick_unfreeze",
        "say_alert",
        "clear_tnt_bounded",
        "clear_items_bounded",
        "set_view_distance",
        "graceful_restart",
    }
)

PROHIBITED_TOKENS: frozenset[str] = frozenset(
    {
        "rm -rf",
        "del /s",
        "format",
        "drop_table",
        "drop_database",
        "delete_world",
        "kill @e",
        "stop_unclean",
        "/op ",
        "op ",
        "deop ",
        "ban-ip",
        "bypass_validation",
    }
)


def _strip_comments(text: str) -> str:
    no_block = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    no_line = re.sub(r"--[^\r\n]*", " ", no_block)
    return " ".join(no_line.split()).lower()


def _extract_all_strings(obj: Any) -> list[str]:
    found: list[str] = []
    if isinstance(obj, str):
        found.append(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.append(str(k))
            found.extend(_extract_all_strings(v))
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            found.extend(_extract_all_strings(item))
    return found


class PolicyValidator:
    """Deterministic lexical, whitelist, and numeric-bound gate."""

    def validate(self, proposal: ActionProposal) -> SafetyVerdict:
        """Validate an untrusted ActionProposal before execution."""
        serialized = _strip_comments(
            json.dumps(
                {"action_type": proposal.action_type, "parameters": proposal.parameters},
                default=str,
            )
        )
        all_strings = [_strip_comments(s) for s in _extract_all_strings(proposal.parameters)]
        all_strings.append(serialized)

        for text in all_strings:
            for forbidden in PROHIBITED_TOKENS:
                if forbidden in text:
                    return SafetyVerdict(
                        allowed=False,
                        reason=f"Prohibited token detected: '{forbidden}'",
                        violated_rule="CONSTITUTIONAL_LEXICAL_PROHIBITION",
                    )

        if proposal.action_type not in ALLOWED_ACTIONS:
            return SafetyVerdict(
                allowed=False,
                reason=f"Action '{proposal.action_type}' is outside closed whitelist.",
                violated_rule="WHITELIST_VIOLATION",
            )

        # Numeric parameter bounds (explicitly reject bools because isinstance(True, int) is True)
        if proposal.action_type in {"clear_tnt_bounded", "clear_items_bounded"}:
            radius = proposal.parameters.get("radius", 32)
            if isinstance(radius, bool) or not isinstance(radius, int) or not (1 <= radius <= 64):
                return SafetyVerdict(
                    allowed=False,
                    reason="Bounded entity cleanup radius must be an integer in [1, 64].",
                    violated_rule="PARAMETER_BOUNDS_VIOLATION",
                )

        if proposal.action_type == "set_view_distance":
            val = proposal.parameters.get("value", 8)
            if isinstance(val, bool) or not isinstance(val, int) or not (4 <= val <= 16):
                return SafetyVerdict(
                    allowed=False,
                    reason="view-distance must be an integer in [4, 16].",
                    violated_rule="PARAMETER_BOUNDS_VIOLATION",
                )

        return SafetyVerdict(allowed=True, reason="Passed Constitutional Safety Gate.")
