"""Admin authentication (bcrypt + Supabase admin_users or local fallback)."""

from __future__ import annotations

import json
import os

import bcrypt

from app.config import CONFIG_DIR, ensure_config_dir
from app.services.supabase_client import SupabaseClient
from app.utils.logger import logger

LOCAL_AUTH_FILE = os.path.join(CONFIG_DIR, "local_auth.json")
DEFAULT_LOCAL_USER = "admin"
DEFAULT_LOCAL_PASS = "changeme"
# bcrypt hash for "changeme" (rounds=12) — must match SQL seed in 001_initial.sql
DEFAULT_PASSWORD_HASH = (
    "$2b$12$d8af0vh9fdFRAawDlJ23cu35djuZE2VQmOTL1baI.NmrsKhHXpNVu"
)


class AuthService:
    def __init__(self):
        self._client = SupabaseClient()

    def _load_local(self) -> dict:
        ensure_config_dir()
        if os.path.isfile(LOCAL_AUTH_FILE):
            with open(LOCAL_AUTH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        data = {"username": DEFAULT_LOCAL_USER, "password_hash": DEFAULT_PASSWORD_HASH}
        with open(LOCAL_AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data

    def _verify_bcrypt(self, password: str, stored: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), stored.encode())
        except Exception:
            return False

    def _try_local_login(self, username: str, password: str) -> dict | None:
        if (
            username == DEFAULT_LOCAL_USER
            and password == DEFAULT_LOCAL_PASS
            and self._verify_bcrypt(password, DEFAULT_PASSWORD_HASH)
        ):
            ensure_config_dir()
            with open(LOCAL_AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {"username": DEFAULT_LOCAL_USER, "password_hash": DEFAULT_PASSWORD_HASH},
                    f,
                    indent=2,
                )
            return {
                "success": True,
                "message": "Login successful (local).",
                "user": {"id": "local", "username": username},
            }

        local = self._load_local()
        if local.get("username") != username:
            return None
        if not self._verify_bcrypt(password, local.get("password_hash", "")):
            return None
        return {
            "success": True,
            "message": "Login successful (local).",
            "user": {"id": "local", "username": username},
        }

    def _repair_supabase_password(self, username: str, password_hash: str) -> None:
        if not self._client.configured:
            return
        try:
            self._client.update(
                "admin_users",
                {"username": f"eq.{username}"},
                {"password_hash": password_hash},
            )
            logger.info("Repaired Supabase admin_users password hash for %s", username)
        except Exception as ex:
            logger.warning("Could not repair Supabase password hash: %s", ex)

    def login(self, username: str, password: str) -> dict:
        username = username.strip()
        if not username or not password:
            return {"success": False, "message": "Username and password required."}

        supabase_user_found = False

        if self._client.configured:
            try:
                rows = self._client.select(
                    "admin_users",
                    {
                        "select": "id,username,password_hash",
                        "username": f"eq.{username}",
                        "limit": "1",
                    },
                )
                if rows:
                    supabase_user_found = True
                    row = rows[0]
                    if self._verify_bcrypt(password, row["password_hash"]):
                        return {
                            "success": True,
                            "message": "Login successful.",
                            "user": {"id": row["id"], "username": row["username"]},
                        }
            except Exception as ex:
                logger.warning("Supabase auth failed, trying local: %s", ex)

        local_result = self._try_local_login(username, password)
        if local_result:
            if supabase_user_found and password == DEFAULT_LOCAL_PASS:
                self._repair_supabase_password(username, DEFAULT_PASSWORD_HASH)
            return local_result

        if supabase_user_found:
            return {"success": False, "message": "Invalid password."}
        return {"success": False, "message": "Unknown user."}

    def change_password(self, username: str, old_password: str, new_password: str) -> dict:
        check = self.login(username, old_password)
        if not check.get("success"):
            return {"success": False, "message": "Current password is incorrect."}
        if len(new_password) < 8:
            return {"success": False, "message": "New password must be at least 8 characters."}
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(rounds=12)).decode()

        if self._client.configured:
            try:
                self._client.update(
                    "admin_users",
                    {"username": f"eq.{username}"},
                    {"password_hash": hashed},
                )
                return {"success": True, "message": "Password updated in Supabase."}
            except Exception as ex:
                logger.error("Supabase password update failed: %s", ex)

        local = self._load_local()
        local["password_hash"] = hashed
        with open(LOCAL_AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(local, f, indent=2)
        return {"success": True, "message": "Password updated locally."}
