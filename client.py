import json
import os
import requests
from pprint import pprint

from utils import increment_version


API_ROOT = 'https://api.github.com/'
REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
REPO_NAME = os.getenv('GITHUB_REPO_NAME')


def _get_auth():
    return os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD')


def _get(url):
    full_url = f'{API_ROOT}{url}'
    return requests.get(full_url, auth=_get_auth())


def _post(url, data):
    full_url = f'{API_ROOT}{url}'
    # print('full_url:', full_url)
    return requests.post(full_url, auth=_get_auth(), data=data)


def get_releases():
    url = f'repos/{REPO_OWNER}/{REPO_NAME}/releases'
    return _get(url)


def get_latest_release():
    # TODO: docstring mention that this isn't the same as the repos/latest call from the API
    # TODO: possible to call API and only fetch one result?
    return get_releases().json()[0]


def compare_commits(base, head):
    url = f'repos/{REPO_OWNER}/{REPO_NAME}/compare/{base}...{head}'
    return _get(url)


def get_commits_since_release(release=None):
    base = release or get_latest_release()['tag_name']
    return compare_commits(base, 'master')


def get_merges(commits):
    return [c for c in commits if c['commit']['message'].startswith('Merge pull request')]


def create_release(release_type):
    print('create_release()', release_type)
    latest_release_tag = get_latest_release()['tag_name']
    # print('latest_release_tag:', latest_release_tag)
    next_tag = increment_version(latest_release_tag, release_type)
    # print('next_tag:', next_tag)

    url = f'repos/{REPO_OWNER}/{REPO_NAME}/releases'
    # TODO: name should able to be passed as an arg
    # TODO: draft should able to be passed as an arg
    payload = json.dumps({
        'tag_name': next_tag, 
        'target_commitish': 'master',
        'name': next_tag, 
        'draft': False, 
        'prerelease': True, 
        'body': 'placeholder',
    })

    resp = _post(url, payload)
    print('resp:', resp)
