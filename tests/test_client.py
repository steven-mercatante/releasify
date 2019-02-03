import pytest

from releaser.client import (
    build_release_body,
    massage_merge_message,
)


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


@pytest.mark.parametrize('input,expected', [
    ('Merge pull request #42 from owner/branch\n\nhello world', 'hello world'),
    ('foo', 'foo'),
    ('', ''),
    (None, ''),
])
def test_massage_merge_message(input, expected):
    assert massage_merge_message(input) == expected
