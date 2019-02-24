import json
import logging
import os
import re
from types import SimpleNamespace

import requests

from .exceptions import (
    ClientError,
    InvalidReleaseTypeError,
    NotFoundError,
    NoCommitsError,
    UnauthorizedError,
)
from .utils import ReleaseType, increment_version


API_ROOT = 'https://api.github.com/'


class ReleasifyClient(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _get_auth(self):
        return self.user, self.password

    @staticmethod
    def _handle_api_response(resp):
        if resp.status_code == 401:
            raise UnauthorizedError(resp=resp)
        elif resp.status_code == 404:
            raise NotFoundError(resp=resp)

    def _get(self, url):
        full_url = f'{API_ROOT}{url}'
        logging.info('_get %s' % full_url)
        resp = requests.get(full_url, auth=self._get_auth())

        self._handle_api_response(resp)

        return resp

    def _post(self, url, data):
        full_url = f'{API_ROOT}{url}'
        logging.info('_post %s' % full_url)
        resp = requests.post(full_url, auth=self._get_auth(), data=data)

        self._handle_api_response(resp)

        return resp

    def get_default_branch(self, owner, repo):
        url = f'repos/{owner}/{repo}'
        return self._get(url).json()['default_branch']

    def get_releases(self, owner, repo):
        url = f'repos/{owner}/{repo}/releases'
        return self._get(url)

    def get_latest_release_tag(self, owner, repo):
        # TODO: docstring mention that this isn't the same as the repos/latest call from the API
        # TODO: possible to call API and only fetch one result?
        releases = self.get_releases(owner, repo)
        return releases.json()[0]['tag_name']

    def compare_commits(self, owner, repo, base, head):
        url = f'repos/{owner}/{repo}/compare/{base}...{head}'
        return self._get(url)

    def get_commits_since_release(self, owner, repo, head, release=None):
        base = release or self.get_latest_release_tag(owner, repo)
        return self.compare_commits(owner, repo, base, head).json()['commits']

    def create_release(
        self, owner, repo, release_type, draft=False, prerelease=True, dry_run=False, force=False, target_branch=None
    ):
        try:
            ReleaseType(release_type)
        except (ValueError):
            raise InvalidReleaseTypeError(release_type)

        target_branch = target_branch or self.get_default_branch(owner, repo)

        commits = self.get_commits_since_release(owner, repo, target_branch)
        if len(commits) == 0 and not force:
            raise NoCommitsError()

        merge_messages = get_merge_messages(commits)

        body = build_release_body(merge_messages)

        # TODO: handle case where there are no existing releases and treat the base as v0.0.0
        latest_release_tag = self.get_latest_release_tag(owner, repo)
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
            # Use SimpleNamespace so we get attribute access
            resp = SimpleNamespace(**{'status_code': status_code})
        else:
            resp = self._post(url, payload)
            status_code = resp.status_code

        return {
            'ok': status_code == 201,
            'resp': resp,
            'tag_name': next_tag,
            'body': body,
            'dry_run': dry_run,
            'prerelease': prerelease,
            'force': force,
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
