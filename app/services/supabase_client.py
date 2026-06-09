"""Supabase REST / RPC client for admin operations."""

from __future__ import annotations

import requests

from app.config import load_config
from app.utils.crypto import decrypt_config_value
from app.utils.logger import logger
from app.utils.supabase_url import normalize_supabase_url


class SupabaseClient:
    def __init__(self, base_url: str | None = None, service_key: str | None = None):
        cfg = load_config()
        raw_url = base_url if base_url is not None else (cfg.get("supabase_url") or "")
        if raw_url:
            try:
                self.base_url = normalize_supabase_url(raw_url)
            except ValueError:
                self.base_url = raw_url.strip().rstrip("/")
        else:
            self.base_url = ""

        if service_key is not None:
            self.service_key = service_key
        else:
            self.service_key = decrypt_config_value(cfg.get("supabase_service_key") or "")

        self.anon_key = decrypt_config_value(cfg.get("supabase_anon_key") or "")
        self.admin_token = decrypt_config_value(cfg.get("admin_api_token") or "")
        edge = cfg.get("edge_functions_base") or self.base_url
        self.functions_base = edge.rstrip("/") + "/functions/v1"

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.service_key)

    def _headers(self, service: bool = True) -> dict:
        key = self.service_key if service else self.anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def rpc(self, name: str, payload: dict) -> dict:
        url = f"{self.base_url}/rest/v1/rpc/{name}"
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        if resp.status_code >= 400:
            logger.error("RPC %s failed: %s", name, resp.text[:200])
            resp.raise_for_status()
        if not resp.text:
            return {}
        return resp.json()

    def select(self, table: str, params: dict | None = None) -> list:
        url = f"{self.base_url}/rest/v1/{table}"
        resp = requests.get(url, headers=self._headers(), params=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def insert(self, table: str, row: dict) -> dict:
        url = f"{self.base_url}/rest/v1/{table}"
        resp = requests.post(url, headers=self._headers(), json=row, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) and data else data

    def update(self, table: str, match: dict, row: dict) -> None:
        url = f"{self.base_url}/rest/v1/{table}"
        resp = requests.patch(
            url, headers=self._headers(), params=match, json=row, timeout=30
        )
        resp.raise_for_status()

    def delete(self, table: str, match: dict) -> None:
        url = f"{self.base_url}/rest/v1/{table}"
        resp = requests.delete(url, headers=self._headers(), params=match, timeout=30)
        resp.raise_for_status()

    def call_edge(self, function: str, body: dict, admin: bool = True) -> dict:
        url = f"{self.functions_base}/{function}"
        headers = {"Content-Type": "application/json"}
        if admin and self.admin_token:
            headers["x-admin-token"] = self.admin_token
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code >= 400:
            logger.error("Edge %s failed: %s", function, resp.text[:200])
            resp.raise_for_status()
        return resp.json() if resp.text else {}

    def test_connection(self) -> tuple[bool, str]:
        if not self.configured:
            return False, "Supabase URL and service key are required in Settings."
        try:
            self.select("installations", {"select": "machine_id", "limit": "1"})
            return True, "Connected to Supabase."
        except Exception as ex:
            return False, str(ex)[:120]
