import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from releasify.client import Client


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('owner', help='The owner of the repo')
    parser.add_argument('repo', help='The name of the repo')
    parser.add_argument('type', help='The type of release')
    parser.add_argument('-d', '--dryrun', help='Perform a dry run (doesn\'t create the release)', 
                        action='store_true')
    parser.add_argument('-f', '--force', help='Create a release even if there aren\'t any commits since the last release', 
                        action='store_true')
    parser.add_argument('-ll', '--loglevel', help='Set the logging level. One of: debug, info, warning, error', default='warning')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    # TODO: let user & password be passed in via optional CLI args
    client = Client(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))

    try:
        result = client.create_release(
            args.owner, args.repo, args.type, dry_run=args.dryrun, force_release=args.force
        )

        if result['ok']:
            print(f'Release name: {result["tag_name"]}')
            print(f'Release body: {result["body"]}')
        else:
            # TODO: show error code & message?
            pass
    except (Exception) as e:
        print(e)
