"""Deterministic scoring for fragments, ideas, and blueprint readiness."""

from __future__ import annotations

from collections.abc import Sequence


def weighted_part_score(
    user_value: int,
    strategic_value: int,
    originality: int,
    feasibility: int,
    revenue_potential: int,
    risk: int,
    build_effort: int,
) -> float:
    return round(
        (user_value * 1.5)
        + (strategic_value * 1.3)
        + (originality * 1.0)
        + (feasibility * 1.2)
        + (revenue_potential * 0.8)
        - (risk * 1.2)
        - (build_effort * 0.8),
        2,
    )


_KEEP_DECISIONS = {"keep", "modify"}


def idea_score_from_parts(parts: Sequence) -> float | None:
    """Average weighted score of kept/modified parts."""
    kept = [p for p in parts if p.decision in _KEEP_DECISIONS and p.weighted_score is not None]
    if not kept:
        return None
    return round(sum(p.weighted_score for p in kept) / len(kept), 2)


def risk_score_from_parts(parts: Sequence) -> float | None:
    """Average risk of kept/modified parts (0-10 scale)."""
    kept = [p for p in parts if p.decision in _KEEP_DECISIONS and p.risk is not None]
    if not kept:
        return None
    return round(sum(p.risk for p in kept) / len(kept), 2)


def readiness_score_from_blueprint(bp) -> float:
    """Heuristic 0-100 completeness score for a blueprint."""
    checks = [
        bool(bp.product_brief),
        bool(bp.feature_list),
        bool(bp.user_flow),
        bool(bp.technical_architecture),
        bool(bp.risk_controls),
        bool(bp.tool_requirements),
        bool(bp.sprint_plan),
        bool(bp.lineage),
    ]
    base = sum(checks) / len(checks) * 100
    # Acceptance criteria present on features nudges readiness up.
    has_ac = any(f.get("acceptance_criteria") for f in bp.feature_list if isinstance(f, dict))
    if has_ac:
        base = min(100.0, base + 5)
    return round(base, 1)
