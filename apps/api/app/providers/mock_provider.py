"""Deterministic mock provider — lets the whole flow run with no API keys."""

from __future__ import annotations

from typing import Any

from .base import ModelProvider, ModelRequest, ModelResponse, ModelUsage


def _score(uv, sv, orig, feas, rev, risk, effort) -> dict[str, int]:
    return {
        "user_value": uv,
        "strategic_value": sv,
        "originality": orig,
        "feasibility": feas,
        "revenue_potential": rev,
        "risk": risk,
        "build_effort": effort,
    }


# Deterministic CouncilProposal-shaped output per seat.
MOCK_PROPOSALS: dict[str, dict[str, Any]] = {
    "george": {
        "agent_key": "george",
        "title": "Control Plane Strategy",
        "summary": (
            "Build a creation-to-execution control plane. Start with Ideas Forge, "
            "Council Room, Best Parts Extractor, Blueprints, and Mission Control. Use a "
            "monorepo, an API control plane, Postgres state, and provider adapters."
        ),
        "assumptions": [
            "Single-tenant, single-operator to start.",
            "Mock model mode is the default for the open-source build.",
        ],
        "proposal": (
            "Stage the build as a vertical slice: idea capture -> triad council -> "
            "best-parts synthesis -> blueprint -> promoted mission with a run timeline. "
            "Keep model routing behind provider adapters so seats are logical, not "
            "hardcoded."
        ),
        "best_features": [
            {
                "part_type": "architecture",
                "title": "Provider-adapter control plane",
                "summary": "FastAPI control plane with mock/OpenAI/Anthropic adapters behind one interface.",
                "why_it_matters": "Lets seats be swapped by config and keeps the frontend model-agnostic.",
                "score": _score(9, 9, 6, 8, 6, 3, 5),
                "recommended_decision": "keep",
            },
            {
                "part_type": "feature",
                "title": "Best-parts synthesis with lineage",
                "summary": "Extract, score, and merge the strongest fragments while tracking their source agent.",
                "why_it_matters": "Turns three opinions into one build-ready blueprint you can trust.",
                "score": _score(9, 8, 8, 7, 6, 3, 6),
                "recommended_decision": "keep",
            },
            {
                "part_type": "launch",
                "title": "Dogfood the platform on itself",
                "summary": "Ship MCOS by running its own build through the council.",
                "why_it_matters": "Proves the loop and produces the first demo.",
                "score": _score(8, 8, 7, 7, 5, 3, 4),
                "recommended_decision": "keep",
            },
        ],
        "weak_points": ["Synthesis quality depends on prompt/model quality once real models are on."],
        "risks": ["Scope creep beyond the vertical slice.", "State model drift between SQLite and Postgres."],
        "dependencies": ["Provider adapters", "Postgres/SQLite schema", "Seed data"],
        "build_steps": [
            "Scaffold monorepo + backend",
            "Model the domain",
            "Wire council mock",
            "Best parts + blueprint",
            "Promote to mission + timeline",
        ],
        "human_approval_needed": ["Enabling any real external tool", "Turning on real model providers"],
        "confidence": 0.89,
    },
    "cipher_fable": {
        "agent_key": "cipher_fable",
        "title": "Risk and Governance Challenge",
        "summary": (
            "The core risks are tool misuse, excessive agency, memory poisoning, prompt "
            "injection, and unapproved external actions. Default to mock/read-only tools, "
            "BBOM cards, approval gates, audit logs, and risk scoring."
        ),
        "assumptions": [
            "Any tool that writes/sends/deploys is dangerous by default.",
            "Retrieved/idea content is untrusted input.",
        ],
        "proposal": (
            "Ship safe-by-default: read-only tools on, write/deploy/send tools disabled or "
            "approval-gated, every side effect audited, and a visible approval center. "
            "Keep system prompts server-side and never let idea content override policy."
        ),
        "best_features": [
            {
                "part_type": "security",
                "title": "Approval gates before side effects",
                "summary": "High-risk/write/deploy/send tools require an explicit human approval record.",
                "why_it_matters": "Bounds agent blast radius and creates an auditable decision trail.",
                "score": _score(8, 9, 5, 8, 4, 2, 4),
                "recommended_decision": "keep",
            },
            {
                "part_type": "security",
                "title": "Behavioral Bill of Materials per agent",
                "summary": "Each seat publishes can_do / cannot_do_without_approval and an autonomy level.",
                "why_it_matters": "Makes agent authority explicit and reviewable, not implicit.",
                "score": _score(7, 9, 7, 8, 3, 2, 3),
                "recommended_decision": "keep",
            },
            {
                "part_type": "risk",
                "title": "Prompt-injection surfacing",
                "summary": "Flag suspicious instructions from untrusted content in the run timeline.",
                "why_it_matters": "Turns a silent attack surface into a visible, reviewable event.",
                "score": _score(7, 8, 6, 6, 3, 4, 6),
                "recommended_decision": "needs_human_approval",
            },
        ],
        "weak_points": ["Approval fatigue if gates are too broad.", "Audit logs need retention/rotation later."],
        "risks": [
            "Memory poisoning via unreviewed writes",
            "Prompt injection from idea/tool content",
            "Over-permissive tool allowlists",
        ],
        "dependencies": ["Tool registry with permissions", "Audit log", "Approvals table"],
        "build_steps": [
            "Seed tools with safe defaults",
            "Add approval records for risky tools",
            "Write audit entries on every state change",
        ],
        "human_approval_needed": [
            "Enabling deploy_app or send_email",
            "Any memory write containing sensitive data",
        ],
        "confidence": 0.86,
    },
    "arty_codex": {
        "agent_key": "arty_codex",
        "title": "Command Center Prototype",
        "summary": (
            "Make the product feel like a command center. Use a dark app shell, agent seat "
            "cards, idea cards, best-parts fragments, mission timelines, and a clear "
            "Create from Best Parts flow."
        ),
        "assumptions": [
            "Operators want density with clarity, not sci-fi clutter.",
            "A high-res, crisp UI is a first-class requirement.",
        ],
        "proposal": (
            "Dark command-center shell with a left nav, an environment badge, and card "
            "panels. The idea detail page is the heart: seat cards on the right, best "
            "parts and blueprint on the left, with obvious primary actions."
        ),
        "best_features": [
            {
                "part_type": "ux",
                "title": "Three-seat Council Room cards",
                "summary": "George/Cipher/Arty cards with status lights, summary, counts, and confidence.",
                "why_it_matters": "Makes multi-agent collaboration legible at a glance.",
                "score": _score(9, 7, 7, 8, 4, 2, 4),
                "recommended_decision": "keep",
            },
            {
                "part_type": "ux",
                "title": "Best Parts grouped by decision",
                "summary": "Fragments bucketed into Keep / Modify / Needs Approval / Needs Evidence / Reject.",
                "why_it_matters": "Turns synthesis into a scannable, decision-first surface.",
                "score": _score(8, 7, 7, 8, 3, 2, 4),
                "recommended_decision": "keep",
            },
            {
                "part_type": "open_source",
                "title": "Polished, HiDPI-first theme",
                "summary": "Design tokens, crisp typography, vector icons, real dark theme, 1x/2x tested.",
                "why_it_matters": "Makes the open-source project feel premium and demo-ready from day one.",
                "score": _score(8, 6, 6, 7, 3, 2, 5),
                "recommended_decision": "keep",
            },
        ],
        "weak_points": ["Timeline density can overwhelm; needs progressive disclosure."],
        "risks": ["Over-styling hurting usability", "Inconsistent tokens across pages"],
        "dependencies": ["Design tokens", "Component library", "API client"],
        "build_steps": [
            "App shell + nav",
            "Idea detail with council/best-parts/blueprint panels",
            "Mission timeline",
        ],
        "human_approval_needed": [],
        "confidence": 0.88,
    },
}


class MockProvider(ModelProvider):
    name = "mock"

    async def complete(self, request: ModelRequest) -> ModelResponse:
        agent_key = str(request.metadata.get("agent_key", "george"))
        proposal = MOCK_PROPOSALS.get(agent_key, MOCK_PROPOSALS["george"])
        summary = proposal["summary"]
        # Deterministic, cheap usage placeholders for observability.
        in_tokens = len(request.system_prompt.split()) + sum(
            len(m.content.split()) for m in request.messages
        )
        out_tokens = len(summary.split()) * 3
        return ModelResponse(
            content_text=summary,
            content_json=proposal,
            usage=ModelUsage(
                input_tokens=in_tokens,
                output_tokens=out_tokens,
                estimated_cost_usd=0.0,
            ),
            raw={"provider": "mock", "agent_key": agent_key},
        )
