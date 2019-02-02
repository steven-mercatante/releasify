import argparse

from dotenv import load_dotenv
load_dotenv()

from client import create_release


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('owner', help='The owner of the repo')
    parser.add_argument('repo', help='The name of the repo')
    parser.add_argument('release_type', help='The type of release')
    args = parser.parse_args()
    resp = create_release(args.owner, args.repo, args.release_type)
    print(resp.status_code)
