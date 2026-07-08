def test_full_idea_to_mission_flow(client):
    idea = client.post(
        "/ideas",
        json={"title": "Flow Test", "seed_prompt": "Build a governed workflow.", "tags": ["t"]},
    ).json()
    iid = idea["id"]
    assert idea["status"] == "raw"

    run = client.post(f"/ideas/{iid}/run-council").json()
    assert run["status"] == "completed"
    assert len(run["contributions"]) == 3
    assert {c["agent_key"] for c in run["contributions"]} == {
        "george",
        "cipher_fable",
        "arty_codex",
    }

    parts = client.post(f"/ideas/{iid}/extract-best-parts").json()
    assert len(parts) > 0
    assert all(p["weighted_score"] is not None for p in parts)

    bp = client.post(f"/ideas/{iid}/generate-blueprint").json()
    assert len(bp["feature_list"]) > 0
    assert bp["readiness_score"] is not None
    assert len(bp["lineage"]) > 0

    mission = client.post(f"/ideas/{iid}/promote-to-mission").json()
    mid = mission["id"]
    assert mission["source_idea_id"] == iid

    detail = client.get(f"/missions/{mid}").json()
    assert len(detail["runs"]) >= 1

    run_id = detail["runs"][0]["id"]
    run_detail = client.get(f"/runs/{run_id}").json()
    assert len(run_detail["steps"]) >= 1

    final = client.get(f"/ideas/{iid}").json()
    assert final["status"] == "promoted_to_mission"
    assert final["idea_score"] is not None
    assert final["readiness_score"] is not None

    # Idempotency: re-promoting the same idea must not create a duplicate mission.
    assert client.post(f"/ideas/{iid}/promote-to-mission").status_code == 409


def test_extract_before_council_conflicts(client):
    idea = client.post(
        "/ideas", json={"title": "No Council", "seed_prompt": "x"}
    ).json()
    r = client.post(f"/ideas/{idea['id']}/extract-best-parts")
    assert r.status_code == 409


def test_missing_idea_404(client):
    assert client.get("/ideas/does-not-exist").status_code == 404
