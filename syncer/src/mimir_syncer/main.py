import os
import time
import requests
from typing import NoReturn
from .config import AppConfig
from .utils import logger
from .providers import get_provider
from .git import run_command, checkout_priority_branch


def sync_repos(config: AppConfig):
    logger.info('Starting sync process...')
    
    try:
        provider = get_provider(config)
    except ValueError as e:
        logger.error(str(e))
        return

    repos_synced = 0
    if not os.path.exists(config.repos_dir):
        os.makedirs(config.repos_dir)

    for repo in provider.get_repos():
        repo_name = repo['name']
        repo_url = repo['clone_url']
        target_path = os.path.join(config.repos_dir, repo_name)
        
        try:
            if not os.path.exists(target_path):
                logger.info(f'[{repo_name}] Cloning...')
                if not run_command(['git', 'clone', repo_url, target_path], dry_run=config.dry_run):
                    continue
            
            logger.info(f'[{repo_name}] Updating...')
            if not run_command(['git', 'fetch', '--all'], cwd=target_path, dry_run=config.dry_run):
                 logger.warning(f'[{repo_name}] Fetch failed, trying to proceed with cached refs.')

            if not config.dry_run:
                checkout_priority_branch(target_path, repo_name, config)
            
            repos_synced += 1

        except Exception as e:
            logger.error(f'[{repo_name}] Error syncing repo: {e}')

    logger.info(f'Sync process completed. Synced {repos_synced} repositories.')

    trigger_opengrok_reindex(config)


def trigger_opengrok_reindex(config: AppConfig):
    if config.dry_run:
        logger.info('[DRY RUN] Would trigger OpenGrok reindex.')
        return

    try:
        headers = {}
        if config.opengrok_rest_token:
            headers['Authorization'] = f'Bearer {config.opengrok_rest_token}'
        
        logger.info(f'Triggering OpenGrok reindex at {config.opengrok_reindex_url}...')
        response = requests.get(config.opengrok_reindex_url, timeout=30, headers=headers)
        
        if response.status_code in [200, 202, 204]:
            logger.info(f'OpenGrok reindex triggered successfully. Status: {response.status_code}')
        else:
            logger.warning(f'Failed to trigger reindex: {response.status_code} {response.text}')
    except Exception as e:
        logger.warning(f'Could not trigger OpenGrok reindex: {e}')


def main() -> NoReturn:
    config = AppConfig()
    try:
        config.validate()
    except ValueError as e:
        logger.critical(str(e))
        sys.exit(1)

    logger.info(f'Mimir Syncer started for Org: {config.org_name} using Provider: {config.git_provider}')
    logger.info(f'Sync Interval: {config.sync_interval} seconds')

    while True:
        try:
            sync_repos(config)
        except Exception as e:
            logger.error(f'An unexpected error occurred in main loop: {e}', exc_info=True)
        
        logger.info(f'Sleeping for {config.sync_interval} seconds...')
        time.sleep(config.sync_interval)


if __name__ == '__main__':
    import sys
    main()
