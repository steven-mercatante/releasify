from unittest.mock import MagicMock

import pytest

from releasify.client import (
    Client,
    InvalidReleaseTypeError,
    NoCommitsError,
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


def test_create_release_exits_if_no_commits_since_last_release():
    client = Client('user', 'password')
    client.get_default_branch = MagicMock(return_value='master')
    client.get_latest_release_tag = MagicMock(return_value='v1.0.0')
    client.get_commits_since_release = MagicMock(return_value=[])
    
    with pytest.raises(NoCommitsError):
        client.create_release('owner', 'repo', 'major', dry_run=True)


def test_create_release_with_force_release_flag_doesnt_raise():
    client = Client('user', 'password')
    client.get_default_branch = MagicMock(return_value='master')
    client.get_latest_release_tag = MagicMock(return_value='v1.0.0')
    client.get_commits_since_release = MagicMock(return_value=[])
    
    resp = client.create_release('owner', 'repo', 'major', dry_run=True, force_release=True)

    assert resp['ok'] is True


def test_passing_invalid_release_type_raises():
    client = Client('user', 'password')
    
    with pytest.raises(InvalidReleaseTypeError):
        resp = client.create_release('owner', 'repo', 'bad_release_type', dry_run=True)
