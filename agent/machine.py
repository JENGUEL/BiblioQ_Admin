"""Machine identity helpers (matches BiblioQ license_service)."""

import hashlib
import platform
import socket
import uuid


def get_machine_id() -> str:
    raw = f"{platform.node()}-{uuid.getnode()}-BiblioQ"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def get_hostname() -> str:
    return platform.node() or socket.gethostname()


def get_os_version() -> str:
    return f"{platform.system()} {platform.release()} {platform.version()}"
