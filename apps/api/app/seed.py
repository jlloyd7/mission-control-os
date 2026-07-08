"""Idempotent dev seed: org, user, agents (+BBOM), tools, and a sample idea.

Run:  python -m app.seed   (safe to re-run)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from .config import get_settings
from .db import SessionLocal, init_db

PROMPTS = Path(__file__).parent / "prompts"
settings = get_settings()


def _prompt(name: str) -> str:
    path = PROMPTS / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


# --- Behavioral Bill of Materials per agent -------------------------------

BBOM: dict[str, dict[str, Any]] = {
    "george": {
        "agent_key": "george",
        "can_do": [
            "Create mission plans",
            "Synthesize blueprints",
            "Assign tasks to council seats",
            "Generate architecture recommendations",
            "Recommend approval gates",
        ],
        "cannot_do_without_approval": [
            "Send external messages",
            "Modify production data",
            "Deploy builds",
            "Spend money",
            "Delete files",
        ],
        "default_autonomy": "recommend_only",
        "risk_level": "medium",
    },
    "cipher_fable": {
        "agent_key": "cipher_fable",
        "can_do": [
            "Review risks",
            "Challenge assumptions",
            "Inspect tool permissions",
            "Generate defensive threat models",
            "Review build plans",
            "Recommend rollback plans",
        ],
        "cannot_do": [
            "Execute external actions",
            "Change permissions directly",
            "Override human approval",
            "Perform offensive exploitation",
        ],
        "default_autonomy": "recommend_only",
        "risk_level": "medium",
    },
    "arty_codex": {
        "agent_key": "arty_codex",
        "can_do": [
            "Generate UI concepts",
            "Scaffold code",
            "Create prototype plans",
            "Suggest components",
            "Draft build artifacts",
        ],
        "cannot_do_without_approval": [
            "Merge code",
            "Deploy",
            "Access secrets",
            "Modify live customer data",
            "Run arbitrary shell commands",
        ],
        "default_autonomy": "draft_only",
        "risk_level": "medium",
    },
    "opus_4_8": {
        "agent_key": "opus_4_8",
        "can_do": [
            "Deep implementation review",
            "Turn plans into buildable engineering steps",
            "Catch correctness and integration issues",
            "Propose test strategy",
        ],
        "cannot_do_without_approval": [
            "Merge code",
            "Deploy",
            "Access secrets",
            "Run arbitrary shell commands",
        ],
        "default_autonomy": "recommend_only",
        "risk_level": "medium",
    },
    "sonnet_5": {
        "agent_key": "sonnet_5",
        "can_do": [
            "Fast drafting of UI, components, and copy",
            "Produce simple shippable first versions",
            "Prototype quickly within the shared schema",
        ],
        "cannot_do_without_approval": [
            "Merge code",
            "Deploy",
            "Access secrets",
            "Modify live customer data",
        ],
        "default_autonomy": "draft_only",
        "risk_level": "medium",
    },
}

AGENTS = [
    {
        "key": "george",
        "name": "George Prime",
        "persona": "Mission Commander",
        "provider": settings.george_provider,
        "model_name": settings.george_model,
        "autonomy_level": "recommend_only",
        "risk_level": "medium",
        "prompt_file": "george.md",
    },
    {
        "key": "cipher_fable",
        "name": "Cipher Fable",
        "persona": "Sentinel",
        "provider": settings.cipher_provider,
        "model_name": settings.cipher_model,
        "autonomy_level": "recommend_only",
        "risk_level": "medium",
        "prompt_file": "cipher_fable.md",
    },
    {
        "key": "arty_codex",
        "name": "Arty Codex",
        "persona": "Maker",
        "provider": settings.arty_provider,
        "model_name": settings.arty_model,
        "autonomy_level": "draft_only",
        "risk_level": "medium",
        "prompt_file": "arty.md",
    },
    {
        "key": "opus_4_8",
        "name": "Opus 4.8",
        "persona": "Engineer / Deep Reviewer",
        "provider": settings.opus_provider,
        "model_name": settings.opus_model,
        "autonomy_level": "recommend_only",
        "risk_level": "medium",
        "prompt_file": "opus.md",
    },
    {
        "key": "sonnet_5",
        "name": "Sonnet 5",
        "persona": "Fast Maker",
        "provider": settings.sonnet_provider,
        "model_name": settings.sonnet_model,
        "autonomy_level": "draft_only",
        "risk_level": "medium",
        "prompt_file": "sonnet.md",
    },
]

# key, name, description, can_read, can_write, can_delete, requires_approval, risk, enabled
TOOLS = [
    ("knowledge_search", "Knowledge Search", "Read-only search over indexed knowledge.",
     True, False, False, False, "low", True),
    ("file_reader", "File Reader", "Read the contents of a local workspace file.",
     True, False, False, False, "medium", True),
    ("blueprint_writer", "Blueprint Writer", "Write a blueprint artifact to internal storage.",
     True, True, False, False, "low", True),
    ("code_scaffold", "Code Scaffold", "Generate local code artifacts (no execution).",
     True, True, False, True, "medium", True),
    ("deploy_app", "Deploy App", "Deploy a build to an external environment.",
     True, True, True, True, "critical", False),
    ("send_email", "Send Email", "Send an email to an external recipient.",
     True, True, False, True, "high", False),
]

SAMPLE_IDEA = {
    "title": "Agentic Mission-Control Platform",
    "seed_prompt": (
        "Build an agentic OS mission-control platform with an Ideas Forge and "
        "Council Room where George, Fable/Cipher, and Arty turn ideas into "
        "governed missions."
    ),
    "description": "The dogfood idea: MCOS building itself.",
    "tags": ["agentic", "open-source", "mission-control"],
    "status": "raw",
}


def _get_or_create(db: Session, model, defaults: dict, **filters):
    obj = db.scalar(select(model).filter_by(**filters))
    created = False
    if obj is None:
        obj = model(**{**filters, **defaults})
        db.add(obj)
        db.flush()
        created = True
    return obj, created


def seed() -> None:
    init_db()
    db = SessionLocal()
    created_counts = {"organizations": 0, "users": 0, "agents": 0, "agent_versions": 0,
                      "tools": 0, "approvals": 0, "ideas": 0}
    try:
        org, c = _get_or_create(
            db, models.Organization,
            {"name": settings.dev_org_name},
            slug="mission-control-dev",
        )
        created_counts["organizations"] += int(c)

        user, c = _get_or_create(
            db, models.User,
            {"organization_id": org.id, "display_name": "George Dev", "role": "owner"},
            email=settings.dev_user_email,
        )
        created_counts["users"] += int(c)

        for spec in AGENTS:
            agent, c = _get_or_create(
                db, models.Agent,
                {
                    "name": spec["name"],
                    "persona": spec["persona"],
                    "provider": spec["provider"],
                    "model_name": spec["model_name"],
                    "autonomy_level": spec["autonomy_level"],
                    "risk_level": spec["risk_level"],
                    "is_enabled": True,
                    "metadata_": {"bbom_summary": BBOM[spec["key"]]},
                },
                organization_id=org.id, key=spec["key"],
            )
            created_counts["agents"] += int(c)

            version = db.scalar(
                select(models.AgentVersion).filter_by(agent_id=agent.id, version=1)
            )
            if version is None:
                db.add(models.AgentVersion(
                    agent_id=agent.id,
                    version=1,
                    system_prompt=_prompt(spec["prompt_file"]),
                    bbom=BBOM[spec["key"]],
                    created_by_user_id=user.id,
                ))
                db.flush()
                created_counts["agent_versions"] += 1

        for (key, name, desc, r, w, d, appr, risk, enabled) in TOOLS:
            _, c = _get_or_create(
                db, models.Tool,
                {
                    "name": name, "description": desc,
                    "can_read": r, "can_write": w, "can_delete": d,
                    "requires_approval": appr, "risk_level": risk, "is_enabled": enabled,
                },
                organization_id=org.id, key=key,
            )
            created_counts["tools"] += int(c)

        # Sample pending approvals for the disabled, dangerous tools.
        sample_approvals = [
            ("Deploy MCOS demo to staging",
             "An agent requested deploy_app to push the demo build externally.",
             "deploy_app", "critical", "george"),
            ("Email weekly mission digest",
             "An agent requested send_email to send a digest to the team.",
             "send_email", "high", "arty_codex"),
        ]
        for title, desc, tool_key, risk, agent_key in sample_approvals:
            exists = db.scalar(
                select(models.Approval).filter_by(organization_id=org.id, title=title)
            )
            if exists is None:
                tool = db.scalar(
                    select(models.Tool).filter_by(organization_id=org.id, key=tool_key)
                )
                db.add(models.Approval(
                    organization_id=org.id,
                    tool_id=tool.id if tool else None,
                    requested_by_agent_key=agent_key,
                    title=title,
                    description=desc,
                    action_payload={"tool": tool_key},
                    risk_level=risk,
                    status="pending",
                ))
                created_counts["approvals"] += 1

        _, c = _get_or_create(
            db, models.Idea,
            {
                "organization_id": org.id,
                "created_by_user_id": user.id,
                "seed_prompt": SAMPLE_IDEA["seed_prompt"],
                "description": SAMPLE_IDEA["description"],
                "tags": SAMPLE_IDEA["tags"],
                "status": SAMPLE_IDEA["status"],
            },
            title=SAMPLE_IDEA["title"],
        )
        created_counts["ideas"] += int(c)

        db.commit()
        print("Seed complete. Newly created:", created_counts)
        print(f"  org={org.name!r} user={settings.dev_user_email!r}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
