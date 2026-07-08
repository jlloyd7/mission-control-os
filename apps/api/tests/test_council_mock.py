from app.providers.base import ModelMessage, ModelRequest
from app.providers.mock_provider import MockProvider
from app.schemas.council import CouncilProposal


async def _complete(agent_key: str):
    req = ModelRequest(
        model="mock-model",
        system_prompt="system",
        messages=[ModelMessage(role="user", content="idea")],
        metadata={"agent_key": agent_key},
    )
    return await MockProvider().complete(req)


async def test_mock_returns_valid_proposal_per_seat():
    for key in ["george", "cipher_fable", "arty_codex"]:
        resp = await _complete(key)
        proposal = CouncilProposal.model_validate(resp.content_json)
        assert proposal.agent_key == key
        assert proposal.best_features
        assert 0 <= proposal.confidence <= 1


async def test_mock_unknown_agent_falls_back_to_valid_proposal():
    resp = await _complete("not_a_real_seat")
    # Falls back to a default proposal that still validates against the schema.
    proposal = CouncilProposal.model_validate(resp.content_json)
    assert proposal.agent_key == "george"


async def test_mock_reports_usage():
    resp = await _complete("george")
    assert resp.usage.input_tokens > 0
    assert resp.usage.output_tokens > 0
