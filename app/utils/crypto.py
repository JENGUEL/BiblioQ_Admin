"""Local config encryption helpers (machine-bound XOR)."""

import base64
import hashlib
import json
import os
import platform


def _machine_key() -> bytes:
    parts = [platform.node(), "BiblioQ_Admin"]
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            )
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            parts.append(guid)
        except Exception:
            pass
    return hashlib.sha256("|".join(parts).encode()).digest()


def encrypt_string(plaintext: str) -> str:
    key = _machine_key()
    data = plaintext.encode("utf-8")
    out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.b64encode(out).decode("ascii")


def decrypt_string(token: str) -> str:
    key = _machine_key()
    data = base64.b64decode(token.encode("ascii"))
    out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return out.decode("utf-8")


def encrypt_config_value(value: str) -> str:
    if not value:
        return ""
    return "__enc__:" + encrypt_string(value)


def decrypt_config_value(value: str) -> str:
    if not value or not str(value).startswith("__enc__:"):
        return value or ""
    return decrypt_string(value[8:])
