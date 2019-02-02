import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_ROOT = 'https://api.github.com/'
REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
REPO_NAME = os.getenv('GITHUB_REPO_NAME')


def _get(url):
    full_url = f'{API_ROOT}{url}'
    # print('full_url:', full_url)
    return requests.get(
        full_url,
        auth=(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD'))
    ).json()


def get_releases():
    url = f'repos/{REPO_OWNER}/{REPO_NAME}/releases'
    return _get(url)


def main():
    releases = get_releases()
    tags = [r['tag_name'] for r in releases]
    print(tags)


if __name__ == '__main__':
    main()
