"""Tests for agent config path resolution."""

import json
import os

from agent import config as agent_config


def test_config_dirs_programdata_first(monkeypatch, tmp_path):
    program_data = tmp_path / "ProgramData"
    local_app = tmp_path / "LocalAppData"
    monkeypatch.setenv("ProgramData", str(program_data))
    monkeypatch.setenv("LOCALAPPDATA", str(local_app))

    dirs = agent_config.get_agent_config_dirs()
    assert dirs[0] == str(program_data / "BiblioQ" / "agent")
    assert dirs[1] == str(local_app / "BiblioQ" / "agent")


def test_load_config_prefers_programdata(monkeypatch, tmp_path):
    program_data = tmp_path / "ProgramData"
    local_app = tmp_path / "LocalAppData"
    monkeypatch.setenv("ProgramData", str(program_data))
    monkeypatch.setenv("LOCALAPPDATA", str(local_app))

    user_dir = local_app / "BiblioQ" / "agent"
    user_dir.mkdir(parents=True)
    user_cfg = user_dir / "config.json"
    user_cfg.write_text(
        json.dumps({"supabase_url": "https://a.supabase.co", "agent_api_key": "key-a"}),
        encoding="utf-8",
    )

    machine_dir = program_data / "BiblioQ" / "agent"
    machine_dir.mkdir(parents=True)
    machine_cfg = machine_dir / "config.json"
    machine_cfg.write_text(
        json.dumps({"supabase_url": "https://b.supabase.co", "agent_api_key": "key-b"}),
        encoding="utf-8",
    )

    loaded = agent_config.load_config()
    assert loaded["supabase_url"] == "https://b.supabase.co"
    assert loaded["agent_api_key"] == "key-b"


def test_save_config_writes_programdata_and_mirror(monkeypatch, tmp_path):
    program_data = tmp_path / "ProgramData"
    local_app = tmp_path / "LocalAppData"
    monkeypatch.setenv("ProgramData", str(program_data))
    monkeypatch.setenv("LOCALAPPDATA", str(local_app))

    path = agent_config.save_config(
        {"supabase_url": "https://x.supabase.co", "agent_api_key": "secret"},
        mirror_user=True,
    )
    assert os.path.isfile(path)
    assert os.path.isfile(os.path.join(local_app, "BiblioQ", "agent", "config.json"))
