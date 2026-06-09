"""Auth service tests."""

import json

import bcrypt

from app.services.auth_service import (
    AuthService,
    DEFAULT_LOCAL_PASS,
    DEFAULT_PASSWORD_HASH,
)


def test_local_login(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    local_file = cfg_dir / "local_auth.json"
    monkeypatch.setattr("app.services.auth_service.CONFIG_DIR", str(cfg_dir))
    monkeypatch.setattr("app.services.auth_service.LOCAL_AUTH_FILE", str(local_file))

    hashed = bcrypt.hashpw(b"testpass", bcrypt.gensalt(rounds=4)).decode()
    with open(local_file, "w", encoding="utf-8") as f:
        json.dump({"username": "admin", "password_hash": hashed}, f)

    class FakeClient:
        configured = False

    monkeypatch.setattr("app.services.auth_service.SupabaseClient", lambda: FakeClient())

    svc = AuthService()
    bad = svc.login("admin", "wrong")
    assert not bad["success"]
    good = svc.login("admin", "testpass")
    assert good["success"]


def test_changeme_default_hash():
    assert bcrypt.checkpw(DEFAULT_LOCAL_PASS.encode(), DEFAULT_PASSWORD_HASH.encode())


def test_supabase_bad_hash_falls_back_to_local(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    local_file = cfg_dir / "local_auth.json"
    monkeypatch.setattr("app.services.auth_service.CONFIG_DIR", str(cfg_dir))
    monkeypatch.setattr("app.services.auth_service.LOCAL_AUTH_FILE", str(local_file))

    with open(local_file, "w", encoding="utf-8") as f:
        json.dump(
            {"username": "admin", "password_hash": DEFAULT_PASSWORD_HASH},
            f,
        )

    class FakeClient:
        configured = True
        repaired = False

        def select(self, table, params):
            return [
                {
                    "id": "uuid-1",
                    "username": "admin",
                    "password_hash": "wrong-hash-not-bcrypt",
                }
            ]

        def update(self, table, match, row):
            FakeClient.repaired = True
            assert row["password_hash"] == DEFAULT_PASSWORD_HASH

    monkeypatch.setattr("app.services.auth_service.SupabaseClient", lambda: FakeClient())

    result = AuthService().login("admin", DEFAULT_LOCAL_PASS)
    assert result["success"]
    assert FakeClient.repaired
