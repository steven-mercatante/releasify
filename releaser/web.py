from dotenv import load_dotenv
load_dotenv()

import json
from base64 import b64decode

import falcon

from .client import create_release


class AuthMiddleware(object):
    def process_request(self, req, resp):
        auth = req.get_header('Authorization')
        if auth is None:
            raise falcon.HTTPUnauthorized('Please provide a username and password')

        if not auth.startswith('Basic '):
            raise falcon.HTTPUnauthorized('Basic auth required')

        encoded_creds = auth.lstrip('Basic ')
        user, password = b64decode(encoded_creds).decode().split(':')


# TODO: add basic auth
class ReleaseResource(object):
    def on_post(self, req, resp):
        payload = json.load(req.bounded_stream)

        # TODO: owner, repo, release_type should be required
        owner = payload['owner']
        repo = payload['repo']
        release_type = payload['release_type']

        result = create_release(owner, repo, release_type)
        resp.media = result.status_code


api = falcon.API(middleware=[AuthMiddleware()])
api.add_route('/releases', ReleaseResource())
