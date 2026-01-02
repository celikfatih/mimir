import subprocess
from typing import List, Optional
from .utils import logger
from .config import AppConfig


def run_command(command: List[str], cwd: Optional[str] = None, dry_run: bool = False) -> bool:
    '''Runs a shell command and returns True if successful.'''
    cmd_str = ' '.join(command)
    if dry_run:
        logger.info(f'[DRY RUN] Would execute: {cmd_str} in {cwd or "current dir"}')
        return True
    
    try:
        subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f'Command failed: {cmd_str}')
        logger.debug(f'Error output: {e.stderr}')
        return False


def get_remote_branches(repo_path: str) -> List[str]:
    '''Returns a list of remote branches for the repo.'''
    try:
        result = subprocess.run(
            ['git', 'branch', '-r'], 
            cwd=repo_path, 
            check=True, 
            capture_output=True, 
            text=True
        )
        branches = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if '->' in line:
                continue
            if line.startswith('origin/'):
                branches.append(line[7:]) # Remove 'origin/' prefix
        return branches
    except subprocess.SubprocessError:
        return []
        

def checkout_priority_branch(repo_path: str, repo_name: str, config: AppConfig):
    '''
    Checks out the first found priority branch or defaults to origin/HEAD.
    '''
    remote_branches = get_remote_branches(repo_path)
    logger.debug(f'[{repo_name}] Available remote branches: {remote_branches}')
    logger.debug(f'[{repo_name}] Priority list: {config.sync_branch_priority}')
    
    target_branch = None
    for priority_branch in config.sync_branch_priority:
        if priority_branch in remote_branches:
            target_branch = priority_branch
            logger.info(f'[{repo_name}] Found priority branch: {target_branch}')
            break
        else:
            logger.debug(f'[{repo_name}] Priority branch \'{priority_branch}\' not found.')
    
    if target_branch:
        # Checkout priority branch and reset to match remote
        run_command(['git', 'checkout', '-B', target_branch, f'origin/{target_branch}'], cwd=repo_path)
        run_command(['git', 'reset', '--hard', f'origin/{target_branch}'], cwd=repo_path)
    else:
        # Fallback to default behavior
        logger.info(f'[{repo_name}] No priority branch found/configured. Using default branch (origin/HEAD).')
        run_command(['git', 'reset', '--hard', 'origin/HEAD'], cwd=repo_path)
