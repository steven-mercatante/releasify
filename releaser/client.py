# TODO: use Enum for release type
import json
import os
from pprint import pprint

import requests

from .utils import increment_version


class UnauthorizedError(Exception):
    pass


API_ROOT = 'https://api.github.com/'


def _get_auth():
    return os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD')


def _get(url):
    full_url = f'{API_ROOT}{url}'
    resp = requests.get(full_url, auth=_get_auth())

    if resp.status_code == 401:
        raise UnauthorizedError()

    return resp


def _post(url, data):
    full_url = f'{API_ROOT}{url}'
    resp = requests.post(full_url, auth=_get_auth(), data=data)

    if resp.status_code == 401:
        raise UnauthorizedError()

    return resp


def get_releases(owner, repo):
    url = f'repos/{owner}/{repo}/releases'
    return _get(url)


def get_latest_release(owner, repo):
    # TODO: docstring mention that this isn't the same as the repos/latest call from the API
    # TODO: possible to call API and only fetch one result?
    releases = get_releases(owner, repo)
    return releases.json()[0]


def compare_commits(owner, repo, base, head):
    url = f'repos/{owner}/{repo}/compare/{base}...{head}'
    return _get(url)


def get_commits_since_release(release=None):
    base = release or get_latest_release()['tag_name']
    return compare_commits(base, 'master')


def get_merges(commits):
    return [c for c in commits if c['commit']['message'].startswith('Merge pull request')]


def create_release(owner, repo, release_type, draft=False, prerelease=True):
    # TODO: handle case where there are no existing releases and treat the base as v0.0.0
    latest_release_tag = get_latest_release(owner, repo)['tag_name']
    next_tag = increment_version(latest_release_tag, release_type)

    url = f'repos/{owner}/{repo}/releases'
    payload = json.dumps({
        'tag_name': next_tag, 
        'target_commitish': 'master',
        'name': next_tag, 
        'draft': draft, 
        'prerelease': prerelease, 
        'body': 'placeholder',  # TODO: pass this as arg
    })

    return _post(url, payload)
