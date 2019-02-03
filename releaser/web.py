import base64
import json

import falcon

from .client import (
    Client, 
    ClientError, 
    NotFoundError, 
    UnauthorizedError,
)


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
    @staticmethod
    def _convert_status_code(status_code):
        try:
            return getattr(falcon, f'HTTP_{status_code}')
        except (AttributeError):
            return falcon.HTTP_500

    def on_post(self, req, resp):
        payload = json.load(req.bounded_stream)

        # TODO: owner, repo, release_type should be required
        owner = payload['owner']
        repo = payload['repo']
        release_type = payload['release_type']

        client = Client(req.context['user'], req.context['password'])

        result = client.create_release(owner, repo, release_type)
        
        resp.status = self._convert_status_code(result['resp'].status_code)

        resp.media = {
            'body': result['body'],
            'tag_name': result['tag_name'],
        }


def handle_error(exception, req, resp, params):
    """Map custom exceptions to Falcon exceptions"""
    if isinstance(exception, UnauthorizedError):
        raise falcon.HTTPUnauthorized()
    elif isinstance(exception, NotFoundError):
        raise falcon.HTTPNotFound()


api = falcon.API(middleware=[AuthMiddleware()])

api.add_error_handler(ClientError, handle_error)

api.add_route('/releases', ReleaseResource())
