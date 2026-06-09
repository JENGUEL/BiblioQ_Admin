"""Supabase project URL normalization."""


def normalize_supabase_url(raw: str) -> str:
    """
    Normalize a Supabase project URL for REST/edge calls.
    Raises ValueError on empty or invalid input.
    """
    url = (raw or "").strip()
    if not url:
        raise ValueError("Supabase URL is required.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url.lstrip("/")

    url = url.rstrip("/")
    if url.endswith("/rest/v1"):
        url = url[: -len("/rest/v1")].rstrip("/")

    if "supabase.co" not in url:
        raise ValueError("URL must be a Supabase project URL (*.supabase.co).")

    return url
