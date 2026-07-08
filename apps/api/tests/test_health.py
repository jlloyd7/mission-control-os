def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_version_is_mock(client):
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body["real_models"] is False
    assert body["provider"] == "mock"
