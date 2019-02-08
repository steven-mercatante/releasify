import base64
import json

from falcon import testing
import pytest

from releasify.web import create_api



@pytest.fixture()
def client():
    return testing.TestClient(create_api())


@pytest.mark.parametrize('payload,expected', [
    ({'_owner': 'foo', 'repo': 'bar', 'release_type': 'major'}, 'owner'),
    ({'owner': 'foo', '_repo': 'bar', 'release_type': 'major'}, 'repo'),
    ({'owner': 'foo', 'repo': 'bar', '_release_type': 'major'}, 'release_type'),
])
def test_missing_required_args_raises(payload, expected, client):
    token = base64.b64encode(b'foo:bar').decode('utf-8')
    headers = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json'}
    expected_err_msg = f"You're missing the required `{expected}` argument"

    resp = client.simulate_post('/releases', headers=headers, json=payload)

    assert resp.status_code == 500
    assert resp.json['description'] == expected_err_msg
