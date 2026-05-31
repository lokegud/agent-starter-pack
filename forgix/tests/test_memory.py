"""Tests for MemoryStore — encrypted SQLite conversations and audit log."""
import pytest
from pathlib import Path
from unittest.mock import patch
from cryptography.fernet import Fernet


@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test.db"
    key = Fernet.generate_key().decode()
    fernet = Fernet(key.encode())
    return db_path, fernet


@pytest.mark.asyncio
async def test_memory_store_init(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        assert store is not None
        assert store.db_path == db_path


@pytest.mark.asyncio
async def test_add_and_retrieve_messages(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        await store.add_message("conv-1", "user", "Hello")
        await store.add_message("conv-1", "assistant", "Hi there!")
        history = await store.get_history("conv-1")
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"
        assert history[1]["role"] == "assistant"
        assert history[1]["content"] == "Hi there!"


@pytest.mark.asyncio
async def test_messages_are_encrypted_on_disk(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        await store.add_message("conv-1", "user", "SECRET_PAYLOAD_XYZ")
        raw = db_path.read_bytes()
        assert b"SECRET_PAYLOAD_XYZ" not in raw


@pytest.mark.asyncio
async def test_audit_log(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        await store.log_audit("test_event", {"info": "value"})
        log = await store.get_audit_log(limit=10)
        assert len(log) >= 1
        assert any(entry.get("event") == "test_event" for entry in log)


@pytest.mark.asyncio
async def test_list_conversations(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        await store.add_message("conv-aaa", "user", "Hello")
        await store.add_message("conv-bbb", "user", "World")
        convs = await store.list_conversations()
        assert "conv-aaa" in convs
        assert "conv-bbb" in convs


@pytest.mark.asyncio
async def test_history_window_limit(temp_db):
    db_path, fernet = temp_db
    from forgix.core.memory import MemoryStore
    with patch("forgix.core.memory._get_fernet", return_value=fernet):
        store = await MemoryStore.initialize(db_path=db_path)
        for i in range(50):
            await store.add_message("conv-win", "user", f"msg {i}")
        history = await store.get_history("conv-win", limit=10)
        assert len(history) == 10
