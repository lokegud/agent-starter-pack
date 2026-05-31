"""Tests for inference backend detection and instantiation."""
import pytest
import os
from unittest.mock import patch
from forgix.core.model import (
    auto_detect_backend,
    OllamaBackend,
    LlamaCppBackend,
    OpenAICompatBackend,
    InferenceBackend,
)


def test_auto_detect_returns_inference_backend():
    config = {"backend": "ollama", "model_tag": "gemma4:2b"}
    backend = auto_detect_backend(config)
    assert isinstance(backend, InferenceBackend)


def test_auto_detect_ollama_default():
    config = {"backend": "ollama", "model_tag": "gemma4:2b"}
    backend = auto_detect_backend(config)
    assert isinstance(backend, OllamaBackend)


def test_auto_detect_custom_endpoint():
    config = {
        "backend": "custom",
        "custom_endpoint": "http://localhost:8000",
        "model_tag": "gemma4:2b",
    }
    backend = auto_detect_backend(config)
    assert isinstance(backend, OpenAICompatBackend)


def test_auto_detect_termux_uses_llamacpp():
    config = {"backend": "auto", "model_tag": "gemma4:2b"}
    fake_prefix = "/data/data/com.termux/files/usr"
    with patch.dict(os.environ, {"PREFIX": fake_prefix}):
        backend = auto_detect_backend(config)
    assert isinstance(backend, LlamaCppBackend)


def test_ollama_backend_has_correct_url():
    config = {"backend": "ollama", "model_tag": "gemma4:2b", "ollama_host": "http://localhost:11434"}
    backend = auto_detect_backend(config)
    assert "11434" in backend.base_url or "localhost" in backend.base_url


def test_model_name_propagated():
    config = {"backend": "ollama", "model_tag": "gemma4:e2b"}
    backend = auto_detect_backend(config)
    assert "gemma" in backend.model_name.lower() or "e2b" in backend.model_name.lower()


def test_backends_have_required_methods():
    config = {"backend": "ollama", "model_tag": "gemma4:2b"}
    backend = auto_detect_backend(config)
    assert hasattr(backend, "chat")
    assert hasattr(backend, "is_available")
    assert callable(backend.chat)
    assert callable(backend.is_available)
