import os

import requests
from dotenv import load_dotenv


def main():
    r = requests.get('https://api.github.com/user', auth=(os.getenv('GITHUB_USER'), os.getenv('GITHUB_PASSWORD')))
    print(r.content)

if __name__ == '__main__':
    load_dotenv()
    main()