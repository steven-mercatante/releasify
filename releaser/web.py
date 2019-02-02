from dotenv import load_dotenv
load_dotenv()

import json

import falcon

from .client import create_release


# TODO: add basic auth
class ReleaseResource:
    def on_post(self, req, resp):
        payload = json.load(req.bounded_stream)

        # TODO: owner, repo, release_type should be required
        owner = payload['owner']
        repo = payload['repo']
        release_type = payload['release_type']

        result = create_release(owner, repo, release_type)
        resp.media = result.status_code


api = falcon.API()
api.add_route('/releases', ReleaseResource())
