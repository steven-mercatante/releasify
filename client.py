import os
import requests


API_ROOT = 'https://api.github.com/'
REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
REPO_NAME = os.getenv('GITHUB_REPO_NAME')


def _get(url):
    full_url = f'{API_ROOT}{url}'
    # print('full_url:', full_url)
    return requests.get(
        full_url,
        auth=(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))
    ).json()


def get_releases():
    url = f'repos/{REPO_OWNER}/{REPO_NAME}/releases'
    return _get(url)


def get_latest_release():
    # TODO: possible to call API and only fetch one result?
    return get_releases()[0]


def compare_commits(base, head):
    url = f'repos/{REPO_OWNER}/{REPO_NAME}/compare/{base}...{head}'
    return _get(url)


def get_commits_since_release(release=None):
    base = release or get_latest_release()['tag_name']
    return compare_commits(base, 'develop')


def get_merges(commits):
    return [c for c in commits if c['commit']['message'].startswith('Merge pull request')]