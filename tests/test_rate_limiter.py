"""
Pruebas unitarias del rate limiter.
"""

import pytest
import time

from utils.rate_limiter import RateLimiter


def test_first_request_is_allowed():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("client-1") is True


def test_allows_requests_up_to_limit():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is True


def test_rejects_request_after_limit():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is False


def test_different_clients_have_independent_limits():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is False

    assert limiter.is_allowed("client-2") is True
    assert limiter.is_allowed("client-2") is True
    assert limiter.is_allowed("client-2") is False


def test_request_is_allowed_after_window_expires():
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=1,
    )

    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is False

    time.sleep(1.1)

    assert limiter.is_allowed("client-1") is True


def test_reset_clears_all_limits():
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=60,
    )

    assert limiter.is_allowed("client-1") is True
    assert limiter.is_allowed("client-1") is False

    limiter.reset()

    assert limiter.is_allowed("client-1") is True


def test_rejects_invalid_max_requests():
    with pytest.raises(
        ValueError,
        match="max_requests",
    ):
        RateLimiter(
            max_requests=0,
            window_seconds=60,
        )


def test_rejects_invalid_window_seconds():
    with pytest.raises(
        ValueError,
        match="window_seconds",
    ):
        RateLimiter(
            max_requests=10,
            window_seconds=0,
        )


def test_global_rate_limiter_uses_configuration():
    from config import (
        RATE_LIMIT_REQUESTS,
        RATE_LIMIT_WINDOW_SECONDS,
    )
    from utils.rate_limiter import rate_limiter

    assert rate_limiter.max_requests == RATE_LIMIT_REQUESTS
    assert rate_limiter.window_seconds == RATE_LIMIT_WINDOW_SECONDS


def test_get_retry_after_without_requests():
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=60,
    )

    assert limiter.get_retry_after("unknown-client") == 0
