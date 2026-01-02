import requests
from typing import List, Dict, Protocol, Tuple, Generator
from .utils import logger
from .config import AppConfig

class RepoProvider(Protocol):
    def get_repos(self) -> Generator[Dict[str, str], None, None]:
        '''Yields dictionaries with 'name' and 'clone_url'.'''
        pass


class GitHubProvider:
    def __init__(self, config: AppConfig):
        self.config = config
        self.headers = {'Authorization': f'token {config.api_token}'}


    def get_repos(self) -> Generator[Dict[str, str], None, None]:
        if not self.config.api_token or not self.config.org_name:
            logger.error('API_TOKEN and ORG_NAME are required for GitHub provider.')
            return

        page = 1
        while True:
            # Try fetching as an organization first
            url = f'https://api.github.com/orgs/{self.config.org_name}/repos?type=all&per_page=100&page={page}'
            response = requests.get(url, headers=self.headers)
            
            # If 404, might be a user, not an org
            if response.status_code == 404 and page == 1:
                logger.info(f'Organization \'{self.config.org_name}\' not found, trying as user...')
                url = f'https://api.github.com/users/{self.config.org_name}/repos?type=all&per_page=100&page={page}'
                response = requests.get(url, headers=self.headers)

            if response.status_code != 200:
                logger.error(f'Failed to fetch repos from GitHub: {response.status_code} {response.text}')
                break

            data = response.json()
            if not data:
                break

            for repo in data:
                clone_url = repo['clone_url'].replace('https://', f'https://{self.config.api_token}@')
                yield {'name': repo['name'], 'clone_url': clone_url}
            
            page += 1


class BitbucketProvider:
    def __init__(self, config: AppConfig):
        self.config = config
        self.auth = self._get_auth()


    def _get_auth(self):
        if ':' in self.config.api_token:
            user, pwd = self.config.api_token.split(':', 1)
            return (user, pwd)
        else:
            logger.warning('Bitbucket API_TOKEN should be format \'username:app_password\' for best results.')
            return (self.config.org_name, self.config.api_token)


    def get_repos(self) -> Generator[Dict[str, str], None, None]:
        if not self.config.api_token or not self.config.org_name:
            logger.error('API_TOKEN and ORG_NAME (Workspace) are required for Bitbucket provider.')
            return

        url = f'https://api.bitbucket.org/2.0/repositories/{self.config.org_name}'
        
        while url:
            response = requests.get(url, auth=self.auth)
            if response.status_code != 200:
                logger.error(f'Failed to fetch repos from Bitbucket: {response.status_code} {response.text}')
                break

            data = response.json()
            for repo in data.get('values', []):
                clone_link = next((l['href'] for l in repo['links']['clone'] if l['name'] == 'https'), None)
                if clone_link:
                    final_url = self._inject_auth(clone_link)
                    yield {'name': repo['name'], 'clone_url': final_url}

            url = data.get('next')


    def _inject_auth(self, clone_link: str) -> str:
        if '@' in clone_link:
            prefix, rest = clone_link.split('@', 1)
            return f'https://{self.auth[0]}:{self.auth[1]}@{rest}'
        else:
            repo_path = clone_link.replace('https://', '')
            return f'https://{self.auth[0]}:{self.auth[1]}@{repo_path}'


def get_provider(config: AppConfig) -> RepoProvider:
    if config.git_provider == 'github':
        return GitHubProvider(config)
    elif config.git_provider == 'bitbucket':
        return BitbucketProvider(config)
    else:
        raise ValueError(f'Unknown provider: {config.git_provider}')
