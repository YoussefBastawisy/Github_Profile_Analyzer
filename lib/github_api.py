import urllib.request
import urllib.error
import json
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')


class GitHubAPIError(Exception):
    pass


def _request(url):
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('User-Agent', 'GitScore-Analyzer/1.0')
    if GITHUB_TOKEN:
        req.add_header('Authorization', f'Bearer {GITHUB_TOKEN}')

    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise GitHubAPIError('User not found. Please check the username.')
        elif e.code == 403:
            raise GitHubAPIError('GitHub API rate limit exceeded. Try again in a minute.')
        else:
            raise GitHubAPIError(f'GitHub API returned error {e.code}.')
    except Exception as e:
        raise GitHubAPIError(f'Could not reach GitHub API: {str(e)}')


def fetch_user(username):
    return _request(f'https://api.github.com/users/{username}')


def fetch_repos(username):
    return _request(
        f'https://api.github.com/users/{username}/repos?per_page=100&sort=updated'
    )
