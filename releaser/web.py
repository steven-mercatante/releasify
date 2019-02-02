import base64
import json

import falcon

from .client import Client


class AuthMiddleware(object):
    def process_request(self, req, resp):
        auth = req.get_header('Authorization')
        if auth is None:
            raise falcon.HTTPUnauthorized('Please provide a username and password')

        if not auth.startswith('Basic '):
            raise falcon.HTTPUnauthorized('Basic auth required')

        encoded_creds = auth.replace('Basic ', '')
        user, password = base64.urlsafe_b64decode(encoded_creds).decode().split(':')

        req.context['user'] = user
        req.context['password'] = password


class ReleaseResource(object):
    def on_post(self, req, resp):
        payload = json.load(req.bounded_stream)

        # TODO: owner, repo, release_type should be required
        owner = payload['owner']
        repo = payload['repo']
        release_type = payload['release_type']

        client = Client(req.context['user'], req.context['password'])
        result = client.create_release(owner, repo, release_type)
        resp.media = result.status_code


api = falcon.API(middleware=[AuthMiddleware()])
api.add_route('/releases', ReleaseResource())
