# Mimir Syncer

Mimir Syncer is a Python-based tool designed to synchronize repositories from GitHub or Bitbucket to a local directory, specifically for indexing with OpenGrok.

## Features
- **Provider Support**: GitHub and Bitbucket (Cloud).
- **Branch Prioritization**: Configurable priority list for branches (e.g., `master, test, main`).
- **Auto-Sync**: Runs in a loop with a configurable interval.
- **OpenGrok Integration**: Automatically triggers a reindex on OpenGrok (if configured) after sync.

## Configuration
Configuration is handled via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GIT_PROVIDER` | `github` or `bitbucket` | `github` |
| `API_TOKEN` | Auth token (GitHub PAT or Bitbucket App Password) | Required |
| `ORG_NAME` | Organization or User name | Required |
| `REPOS_DIR` | Directory to clone repos into | `/opengrok/src` |
| `SYNC_INTERVAL` | Seconds between sync cycles | `3600` |
| `SYNC_BRANCH_PRIORITY` | Comma-separated list of branches to prioritize | Empty (defaults to HEAD) |
| `DRY_RUN` | If `true`, only logs commands | `false` |

## Usage
### Docker Compose
```yaml
  mimir-syncer:
    build: ./syncer
    environment:
      - GIT_PROVIDER=github
      - API_TOKEN=${API_TOKEN}
      - ORG_NAME=myorg
      - SYNC_BRANCH_PRIORITY=master,test
    volumes:
      - ./opengrok/src:/opengrok/src
```

## Development
Run locally:
```bash
export API_TOKEN=...
export ORG_NAME=...
python3 -m src.mimir_syncer.main
```
