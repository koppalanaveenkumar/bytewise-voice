def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["backend"] == "fake"
    assert {m["key"] for m in body["models"]} == {"kokoro", "chatterbox"}


def test_models(client):
    models = client.get("/api/models").json()
    cloning = {m["key"]: m["supports_cloning"] for m in models}
    assert cloning == {"kokoro": False, "chatterbox": True}


def test_voices_are_kokoro_presets(client):
    voices = client.get("/api/voices").json()
    assert voices
    assert all(v["model"] == "kokoro" and v["id"].startswith("kokoro:") for v in voices)


def test_docs_page(client):
    assert client.get("/docs").status_code == 200


def test_rejects_other_hosts(make_client):
    client = make_client(base_url="http://evil.example")
    assert client.get("/api/health").status_code == 400


def test_token_required_when_configured(make_client):
    client = make_client(token="secret123")
    assert client.get("/api/health").status_code == 401
    ok = client.get("/api/health", headers={"X-ByteWise-Token": "secret123"})
    assert ok.status_code == 200
