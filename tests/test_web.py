import base64
import json
from unittest.mock import MagicMock

from falcon import testing
import pytest

from releasify.client import Client
from releasify.web import (
    MissingRequiredArgError, 
    create_api, 
    get_required_arg,
)


@pytest.fixture()
def http_client():
    return testing.TestClient(create_api())


def _get_headers():
    token = base64.b64encode(b'foo:bar').decode('utf-8')
    return {'Authorization': f'Basic {token}', 'Content-Type': 'application/json'}


def test_get_required_arg():
    args = {'foo': 'bar'}
    assert get_required_arg(args, 'foo') == 'bar'


def test_get_required_arg_raises():
    args = {'foo': 'bar'}
    
    with pytest.raises(MissingRequiredArgError):
        get_required_arg(args, 'baz')


def test_api_success(http_client):
    # client = Client('user', 'password')
    # client.get_default_branch = MagicMock(return_value='master')
    # client.get_latest_release_tag = MagicMock(return_value='v1.0.0')
    # client.get_commits_since_release = MagicMock(return_value=[])

    payload = {
        'owner': 'foo',
        'repo': 'bar',
        'release_type': 'major',
        'dry_run': True
    }

    resp = http_client.simulate_post('/releases', headers=_get_headers(), json=payload)

    print(resp.status_code)
    print(resp.json)
    
    assert resp.status_code == 201
    assert resp.json['tag_name'] == 'v2.0.0'


@pytest.mark.parametrize('payload,expected', [
    ({'_owner': 'foo', 'repo': 'bar', 'release_type': 'major'}, 'owner'),
    ({'owner': 'foo', '_repo': 'bar', 'release_type': 'major'}, 'repo'),
    ({'owner': 'foo', 'repo': 'bar', '_release_type': 'major'}, 'release_type'),
])
def test_missing_required_args_raises(payload, expected, http_client):
    expected_err_msg = f"You're missing the required `{expected}` argument"

    resp = http_client.simulate_post('/releases', headers=_get_headers(), json=payload)

    assert resp.status_code == 500
    assert resp.json['description'] == expected_err_msg


def test_missing_credentials_raises():
    raise NotImplementedError()
