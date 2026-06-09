"""In-memory admin session."""


class Session:
    _user = None

    @classmethod
    def login(cls, user: dict):
        cls._user = user

    @classmethod
    def logout(cls):
        cls._user = None

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls._user is not None

    @classmethod
    def user(cls) -> dict | None:
        return cls._user

    @classmethod
    def username(cls) -> str:
        return (cls._user or {}).get("username", "")
