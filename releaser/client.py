import json
import os
import re
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
    def _handle_api_response(resp):
        if resp.status_code == 401:
            raise UnauthorizedError(resp)
        elif resp.status_code == 404:
            raise NotFoundError(resp)

    def _get(self, url):
        full_url = f'{API_ROOT}{url}'
        resp = requests.get(full_url, auth=self._get_auth())

        self._handle_api_response(resp)

        return resp

    def _post(self, url, data):
        full_url = f'{API_ROOT}{url}'
        resp = requests.post(full_url, auth=self._get_auth(), data=data)

        self._handle_api_response(resp)

        return resp

    def get_default_branch(self, owner, repo):
        url = f'repos/{owner}/{repo}'
        return self._get(url).json()['default_branch']

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

    def get_commits_since_release(self, owner, repo, head, release=None):
        base = release or self.get_latest_release(owner, repo)['tag_name']
        return self.compare_commits(owner, repo, base, head)

    def create_release(self, owner, repo, release_type, draft=False, prerelease=True, dry_run=False):
        # TODO: this should be an optional arg
        target_branch = self.get_default_branch(owner, repo)

        # TODO: use Enum for release type
        commits = self.get_commits_since_release(owner, repo, target_branch).json()['commits']
        merge_messages = get_merge_messages(commits)

        body = build_release_body(merge_messages)

        # TODO: handle case where there are no existing releases and treat the base as v0.0.0
        latest_release_tag = self.get_latest_release(owner, repo)['tag_name']
        next_tag = increment_version(latest_release_tag, release_type)


        url = f'repos/{owner}/{repo}/releases'
        payload = json.dumps({
            'tag_name': next_tag, 
            'target_commitish': target_branch,
            'name': next_tag, 
            'draft': draft, 
            'prerelease': prerelease, 
            'body': body,
        })

        if dry_run:
            status_code = 201
            resp = {'status_code': status_code}
        else:
            resp = self._post(url, payload)
            status_code = resp.status_code

        return {
            'ok': status_code == 201,
            'resp': resp,
            'tag_name': next_tag,
            'body': body,
        }


def get_merge_messages(commits):
    return [
        massage_merge_message(c['commit']['message'])
        for c in commits
        if c['commit']['message'].startswith('Merge pull request')
    ]


def massage_merge_message(message):
    # Merge messages seem to start with a "Merge pull request #x from owner/branch\n\n",
    # so let's grab everything after that.
    if message is None:
        return ''
    return re.sub(r'(Merge pull request.*\n\n)', '', message)


def build_release_body(messages):
    return '\n'.join(f'- {msg}' for msg in messages)
