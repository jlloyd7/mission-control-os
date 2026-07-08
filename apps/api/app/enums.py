"""String enums for statuses, risk, and autonomy.

Stored as plain strings in the DB (portable across SQLite/Postgres) and validated
at the schema layer.
"""

from __future__ import annotations

from enum import Enum


class IdeaStatus(str, Enum):
    raw = "raw"
    council_ready = "council_ready"
    council_running = "council_running"
    council_complete = "council_complete"
    best_parts_extracted = "best_parts_extracted"
    blueprint_ready = "blueprint_ready"
    promoted_to_mission = "promoted_to_mission"
    archived = "archived"


class MissionStatus(str, Enum):
    draft = "draft"
    queued = "queued"
    running = "running"
    blocked = "blocked"
    waiting_approval = "waiting_approval"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class RunStatus(str, Enum):
    queued = "queued"
    running = "running"
    paused = "paused"
    waiting_approval = "waiting_approval"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class StepType(str, Enum):
    user_input = "user_input"
    agent_thought_summary = "agent_thought_summary"
    agent_proposal = "agent_proposal"
    tool_call = "tool_call"
    tool_result = "tool_result"
    best_parts_extraction = "best_parts_extraction"
    blueprint_generation = "blueprint_generation"
    approval_request = "approval_request"
    approval_decision = "approval_decision"
    artifact_created = "artifact_created"
    error = "error"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    expired = "expired"
    cancelled = "cancelled"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AutonomyLevel(str, Enum):
    recommend_only = "recommend_only"
    draft_only = "draft_only"
    execute_readonly = "execute_readonly"
    execute_low_risk = "execute_low_risk"
    approval_required = "approval_required"
    disabled = "disabled"


class AgentKey(str, Enum):
    george = "george"
    cipher_fable = "cipher_fable"
    arty_codex = "arty_codex"
