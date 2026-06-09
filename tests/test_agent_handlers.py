"""Tests for BiblioQ Admin."""

import bcrypt

from agent.commands.handlers import dispatch


def test_revoke_license_handler(tmp_path, monkeypatch):
    import agent.commands.handlers as h

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setattr(h, "BIBLIOQ_DATA", str(data_dir))
    monkeypatch.setattr(h, "REVOKED_FILE", str(data_dir / "license_revoked.json"))

    ok, msg = dispatch("revoke_license", {"message": "Test revoke"})
    assert ok
    assert "written" in msg.lower()
    assert (data_dir / "license_revoked.json").is_file()


def test_clear_revoke_handler(tmp_path, monkeypatch):
    import agent.commands.handlers as h

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    revoked = data_dir / "license_revoked.json"
    revoked.write_text('{"revoked": true}', encoding="utf-8")
    monkeypatch.setattr(h, "BIBLIOQ_DATA", str(data_dir))
    monkeypatch.setattr(h, "REVOKED_FILE", str(revoked))

    ok, msg = dispatch("clear_revoke", {})
    assert ok
    assert not revoked.is_file()


def test_bcrypt_roundtrip():
    hashed = bcrypt.hashpw(b"secret123", bcrypt.gensalt(rounds=4)).decode()
    assert bcrypt.checkpw(b"secret123", hashed.encode())
