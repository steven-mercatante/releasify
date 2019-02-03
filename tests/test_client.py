import pytest

from releaser.client import (
    build_release_body,
    get_merge_messages,
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


def test_get_merge_messages_with_commits():
    commits = [
        {'commit': {'message': 'foo'}},
        {'commit': {'message': 'Merge pull request #1 from owner/branch\n\npizza hut'}},
        {'commit': {'message': 'Merge pull request #1 from owner/branch\n\ndominoes'}},
        {'commit': {'message': 'my stomach hurts'}},
    ]
    expected = ['pizza hut', 'dominoes']
    assert get_merge_messages(commits) == expected


def test_get_merge_messages_with_empty_commits():
    commits = []
    expected = []
    assert get_merge_messages(commits) == expected


@pytest.mark.parametrize('input,expected', [
    ('Merge pull request #42 from owner/branch\n\nhello world', 'hello world'),
    ('foo', 'foo'),
    ('', ''),
    (None, ''),
])
def test_massage_merge_message(input, expected):
    assert massage_merge_message(input) == expected
