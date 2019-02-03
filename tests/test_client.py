import pytest

from releaser.client import build_release_body


def test_build_release_body_with_messages():
    messages = ['foo', 'bar', 'baz']
    expected = "- foo\n- bar\n- baz"
    result = build_release_body(messages)
    assert result == expected


def test_build_release_body_with_empty_messages():
    messages = []
    expected = ''
    result = build_release_body(messages)
    assert result == expected
