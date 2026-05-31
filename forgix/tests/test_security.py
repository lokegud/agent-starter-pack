"""Tests for SecurityManager and RateLimiter."""
import pytest
from forgix.core.security import SecurityManager, RateLimiter


def test_assert_localhost_only_blocks_public():
    with pytest.raises(ValueError, match="SECURITY VIOLATION"):
        SecurityManager.assert_localhost_only("0.0.0.0")


def test_assert_localhost_only_blocks_lan_ip():
    with pytest.raises(ValueError):
        SecurityManager.assert_localhost_only("192.168.1.100")


def test_assert_localhost_only_blocks_any_bind():
    with pytest.raises(ValueError):
        SecurityManager.assert_localhost_only("0.0.0.0")


def test_assert_localhost_only_allows_loopback_ipv4():
    SecurityManager.assert_localhost_only("127.0.0.1")


def test_assert_localhost_only_allows_loopback_ipv6():
    SecurityManager.assert_localhost_only("::1")


def test_assert_localhost_only_allows_localhost_hostname():
    SecurityManager.assert_localhost_only("localhost")


def test_is_lan_subnet_rfc1918_class_c():
    assert SecurityManager.is_lan_subnet("192.168.0.1") is True


def test_is_lan_subnet_rfc1918_class_a():
    assert SecurityManager.is_lan_subnet("10.0.0.1") is True


def test_is_lan_subnet_rfc1918_class_b():
    assert SecurityManager.is_lan_subnet("172.16.0.1") is True


def test_is_lan_subnet_public_false():
    assert SecurityManager.is_lan_subnet("8.8.8.8") is False
    assert SecurityManager.is_lan_subnet("1.1.1.1") is False


def test_rate_limiter_allows_within_limit():
    rl = RateLimiter(requests_per_minute=60)
    for _ in range(10):
        assert rl.is_allowed("127.0.0.1") is True


def test_rate_limiter_blocks_when_exhausted():
    rl = RateLimiter(requests_per_minute=3)
    rl.is_allowed("1.2.3.4")
    rl.is_allowed("1.2.3.4")
    rl.is_allowed("1.2.3.4")
    assert rl.is_allowed("1.2.3.4") is False


def test_rate_limiter_separate_ips_independent():
    rl = RateLimiter(requests_per_minute=2)
    rl.is_allowed("1.1.1.1")
    rl.is_allowed("1.1.1.1")
    rl.is_allowed("1.1.1.1")  # exhausted
    assert rl.is_allowed("1.1.1.1") is False
    assert rl.is_allowed("2.2.2.2") is True  # independent bucket


def test_verify_bearer_token_false_without_setup():
    # Without a session token in keyring, should return False (not raise)
    result = SecurityManager.verify_bearer_token("Bearer totally-fake-token")
    assert result is False


def test_verify_bearer_token_false_on_malformed():
    assert SecurityManager.verify_bearer_token(None) is False
    assert SecurityManager.verify_bearer_token("") is False
    assert SecurityManager.verify_bearer_token("NotBearer token") is False
