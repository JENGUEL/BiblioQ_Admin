"""Tests for Supabase URL normalization."""

import pytest

from app.utils.supabase_url import normalize_supabase_url


def test_strips_rest_v1_suffix():
    assert (
        normalize_supabase_url("https://kexuogfefmtndgmjqrdo.supabase.co/rest/v1/")
        == "https://kexuogfefmtndgmjqrdo.supabase.co"
    )


def test_adds_https_prefix():
    assert (
        normalize_supabase_url("kexuogfefmtndgmjqrdo.supabase.co")
        == "https://kexuogfefmtndgmjqrdo.supabase.co"
    )


def test_partial_host_with_rest_path():
    assert (
        normalize_supabase_url("mtndgmjqrdo.supabase.co/rest/v1/")
        == "https://mtndgmjqrdo.supabase.co"
    )


def test_empty_raises():
    with pytest.raises(ValueError, match="required"):
        normalize_supabase_url("")
