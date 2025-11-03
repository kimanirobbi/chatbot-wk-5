import os
import sys
import pytest

# Ensure the repository root is on sys.path so tests can import local modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from chatbot_utils import build_conversation_prompt


def test_prompt_basic():
    system = "System: be helpful"
    conv = [
        {"role": "user", "content": "Hello"},
        {"role": "ai", "content": "Hi there"},
    ]
    user_input = "Can you help me?"

    prompt = build_conversation_prompt(system, conv, user_input)

    assert "System: be helpful" in prompt
    assert "user: Hello" in prompt
    assert "ai: Hi there" in prompt
    assert "user: Can you help me?" in prompt


def test_prompt_empty_conversation():
    system = "System instruction"
    conv = []
    user_input = "Hi"
    prompt = build_conversation_prompt(system, conv, user_input)
    assert prompt.startswith(system)
    assert "user: Hi" in prompt


def test_prompt_none_conversation():
    system = "Sys"
    prompt = build_conversation_prompt(system, None, "x")
    assert "user: x" in prompt
