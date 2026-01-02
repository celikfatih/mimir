import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class AppConfig:
    '''Application configuration loaded from environment variables.'''
    git_provider: str = field(default_factory=lambda: os.getenv('GIT_PROVIDER', 'github').lower())
    api_token: str = field(default_factory=lambda: os.getenv('API_TOKEN', ''))
    org_name: str = field(default_factory=lambda: os.getenv('ORG_NAME', ''))
    sync_interval: int = field(default_factory=lambda: int(os.getenv('SYNC_INTERVAL', '3600')))
    repos_dir: str = field(default_factory=lambda: os.getenv('REPOS_DIR', '/opengrok/repos'))
    dry_run: bool = field(default_factory=lambda: os.getenv('DRY_RUN', 'false').lower() == 'true')
    sync_branch_priority: List[str] = field(default_factory=lambda: [b.strip() for b in os.getenv('SYNC_BRANCH_PRIORITY', '').split(',') if b.strip()])
    opengrok_reindex_url: str = field(default_factory=lambda: os.getenv('OPENGROK_REINDEX_URL', 'http://opengrok:8000/reindex'))
    opengrok_rest_token: str = field(default_factory=lambda: os.getenv('OPENGROK_REST_TOKEN', ''))


    def validate(self):
        if not self.api_token:
            raise ValueError('API_TOKEN environment variable is required.')
        if not self.org_name:
            raise ValueError('ORG_NAME environment variable is required.')
        if self.git_provider not in ('github', 'bitbucket'):
            raise ValueError(f'Unsupported GIT_PROVIDER: {self.git_provider}')
