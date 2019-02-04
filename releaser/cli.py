import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from releaser.client import Client


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('owner', help='The owner of the repo')
    parser.add_argument('repo', help='The name of the repo')
    parser.add_argument('release_type', help='The type of release')
    args = parser.parse_args()

    # TODO: let user & password be passed in via optional CLI args
    client = Client(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))
    result = client.create_release(args.owner, args.repo, args.release_type)

    if result['ok']:
        print(f'Created release {result["tag_name"]}')
    else:
        # TODO: show error code & message?
        pass
