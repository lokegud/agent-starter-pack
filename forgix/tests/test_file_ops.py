"""Tests for sandboxed file operations."""
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch
from forgix.skills.builtin import file_ops
from forgix.skills.builtin.file_ops import _safe_path


@pytest.fixture
def temp_sandbox(tmp_path):
    sandbox = tmp_path / "workspace"
    sandbox.mkdir()
    with patch.object(file_ops, "SANDBOX", sandbox):
        yield sandbox


@pytest.mark.asyncio
async def test_write_and_read_file(temp_sandbox):
    result = await file_ops.write_file("test.txt", "hello world")
    assert "hello world" in result or "Wrote" in result
    content = await file_ops.read_file("test.txt")
    assert "hello world" in content


@pytest.mark.asyncio
async def test_list_dir(temp_sandbox):
    await file_ops.write_file("a.txt", "a")
    await file_ops.write_file("b.txt", "b")
    listing = await file_ops.list_dir()
    assert "a.txt" in listing
    assert "b.txt" in listing


@pytest.mark.asyncio
async def test_path_escape_blocked(temp_sandbox):
    result = await file_ops.read_file("../../etc/passwd")
    assert "[Security" in result or "escape" in result.lower() or "sandbox" in result.lower()


@pytest.mark.asyncio
async def test_path_escape_absolute_blocked(temp_sandbox):
    result = await file_ops.read_file("/etc/passwd")
    assert "[Security" in result or "escape" in result.lower() or "sandbox" in result.lower()


def test_safe_path_raises_on_escape(temp_sandbox):
    with pytest.raises(ValueError, match="[Ss]andbox|[Ee]scape"):
        _safe_path("../../etc/passwd")


def test_safe_path_raises_on_absolute(temp_sandbox):
    with pytest.raises(ValueError):
        _safe_path("/etc/passwd")


def test_safe_path_allows_normal_filename(temp_sandbox):
    path = _safe_path("notes.txt")
    assert str(path).startswith(str(temp_sandbox))


@pytest.mark.asyncio
async def test_append_mode(temp_sandbox):
    await file_ops.write_file("log.txt", "line1\n")
    await file_ops.write_file("log.txt", "line2\n", append=True)
    content = await file_ops.read_file("log.txt")
    assert "line1" in content
    assert "line2" in content


@pytest.mark.asyncio
async def test_read_nonexistent_returns_not_found(temp_sandbox):
    result = await file_ops.read_file("does_not_exist.txt")
    assert "not found" in result.lower() or "error" in result.lower()


@pytest.mark.asyncio
async def test_subdirectory_allowed(temp_sandbox):
    (temp_sandbox / "subdir").mkdir()
    await file_ops.write_file("subdir/note.txt", "nested content")
    content = await file_ops.read_file("subdir/note.txt")
    assert "nested content" in content
