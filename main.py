from dotenv import load_dotenv
load_dotenv()

from client import (
    get_latest_release,
    get_commits_since_release,
    get_merges,
    create_release
)


def main():
    # latest_release = get_latest_release()['tag_name']
    # commits_since_latest_release = get_commits_since_release(latest_release)['commits']
    # merges = get_merges(commits_since_latest_release)
    # print(merges)
    # for m in merges:
    #     print(m['commit']['message'])

    create_release('patch')

if __name__ == '__main__':
    main()
