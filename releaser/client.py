import json
import os
from pprint import pprint

import requests

from .utils import increment_version


API_ROOT = 'https://api.github.com/'


class ClientError(Exception):
    pass


class UnauthorizedError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class Client(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _get_auth(self):
        return self.user, self.password

    @staticmethod
    def _handle_status_code(status_code):
        if status_code == 401:
            raise UnauthorizedError()
        elif status_code == 404:
            raise NotFoundError()

    def _get(self, url):
        full_url = f'{API_ROOT}{url}'
        resp = requests.get(full_url, auth=self._get_auth())

        self._handle_status_code(resp.status_code)

        return resp

    def _post(self, url, data):
        full_url = f'{API_ROOT}{url}'
        resp = requests.post(full_url, auth=self._get_auth(), data=data)

        self._handle_status_code(resp.status_code)

        return resp

    def get_releases(self, owner, repo):
        url = f'repos/{owner}/{repo}/releases'
        return self._get(url)

    def get_latest_release(self, owner, repo):
        # TODO: docstring mention that this isn't the same as the repos/latest call from the API
        # TODO: possible to call API and only fetch one result?
        releases = self.get_releases(owner, repo)
        return releases.json()[0]

    def compare_commits(self, owner, repo, base, head):
        url = f'repos/{owner}/{repo}/compare/{base}...{head}'
        return self._get(url)

    def get_commits_since_release(self, release=None):
        base = release or self.get_latest_release()['tag_name']
        return self.compare_commits(base, 'master')

    def create_release(self, owner, repo, release_type, draft=False, prerelease=True):
        # TODO: use Enum for release type
        # TODO: handle case where there are no existing releases and treat the base as v0.0.0
        latest_release_tag = self.get_latest_release(owner, repo)['tag_name']
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

        return self._post(url, payload)


def get_merges(commits):
    return [c for c in commits if c['commit']['message'].startswith('Merge pull request')]
