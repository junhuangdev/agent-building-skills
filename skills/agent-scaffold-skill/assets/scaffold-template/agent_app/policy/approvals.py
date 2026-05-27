from __future__ import annotations

from dataclasses import dataclass


HIGH_RISK_LEVELS = {"external", "destructive", "permission", "money"}


@dataclass(frozen=True)
class ApprovalDecision:
    allowed: bool
    reason: str


def check_tool_approval(risk: str, approved: bool = False) -> ApprovalDecision:
    if risk in HIGH_RISK_LEVELS and not approved:
        return ApprovalDecision(False, f"Approval required for {risk} action")
    return ApprovalDecision(True, "allowed")
