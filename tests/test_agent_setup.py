"""Tests for agent config setup via admin service."""

import json
import os

from app.services import agent_setup


def test_write_agent_config(monkeypatch, tmp_path):
    program_data = tmp_path / "ProgramData"
    local_app = tmp_path / "LocalAppData"
    monkeypatch.setenv("ProgramData", str(program_data))
    monkeypatch.setenv("LOCALAPPDATA", str(local_app))

    path = agent_setup.write_agent_config(
        "kexuogfefmtndgmjqrdo.supabase.co/rest/v1/",
        "test-agent-key-123",
    )
    assert os.path.isfile(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert data["supabase_url"] == "https://kexuogfefmtndgmjqrdo.supabase.co"
    assert data["agent_api_key"] == "test-agent-key-123"
    assert "supabase_service_key" not in data

    mirror = os.path.join(local_app, "BiblioQ", "agent", "config.json")
    assert os.path.isfile(mirror)
