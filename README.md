# Mimir - Automated OpenGrok Sync

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/docker-compose-orange.svg)

**Mimir** is a robust, Docker-based solution for deploying [OpenGrok](https://oracle.github.io/opengrok/) with automated repository synchronization. It bridges the gap between your code hosting platforms (GitHub, Bitbucket) and your search engine, ensuring your entire organization's codebase is always indexed and searchable.

---

## Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## Features

- **Automated Discovery**: Automatically finds all repositories in a GitHub Organization or Bitbucket Workspace.
- **Smart Branch Selection**: prioritizing branches (e.g., `master` > `test` > `main`) to index the most relevant code.
- **Auto-Reindexing**: Triggers OpenGrok indexing immediately after a sync cycle completes.
- **Provider Agnostic**: extensible design supporting GitHub and Bitbucket Cloud out of the box.
- **Containerized**: Fully Dockerized for easy deployment and isolation.

## Architecture

Mimir consists of two primary services orchestrated via Docker Compose:

1.  **OpenGrok**: The standard OpenGrok container serving the web UI and REST API.
2.  **Mimir Syncer**: A custom Python agent that:
    - Queries the Git Provider API.
    - Clones/Updates repositories to a shared volume.
    - Calls the OpenGrok API to request a reindex.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git (for cloning this repository)
- API Credentials (GitHub PAT or Bitbucket App Password)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/celikfatih/mimir.git
    cd mimir
    ```

2.  **Configure Environment**
    Create a `.env` file from the template:
    ```bash
    cp .env.template .env
    ```
    Edit `.env` and provide your credentials.

3.  **Start Services**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access OpenGrok**
    Navigate to `http://localhost:8080/source` in your browser.

## Configuration

Configuration is managed via environment variables in `.env` or `docker-compose.yml`.

| Variable | Description | Default | Required |
|----------|-------------|---------|:--------:|
| `GIT_PROVIDER` | `github` or `bitbucket` | `github` | Yes |
| `API_TOKEN` | Personal Access Token or App Password | - | Yes |
| `ORG_NAME` | Organization or User name to sync | - | Yes |
| `SYNC_BRANCH_PRIORITY` | Comma-separated list of priority branches | `HEAD` | No |
| `SYNC_INTERVAL` | Sync interval in seconds | `3600` | No |
| `OPENGROK_REST_TOKEN` | Token for securing OpenGrok API | - | No |

## Usage

### Managing the Syncer
View logs to see sync progress:
```bash
docker-compose logs -f mimir-syncer
```

### Forcing a Reindex
The syncer triggers this automatically, but you can also hit the endpoint manually if exposed:
```bash
curl http://localhost:8000/reindex
```

## Development

The `syncer` component is a Python package. To develop locally:

1.  Navigate to `syncer/`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Set environment variables.
4.  Run the module: `python3 -m src.mimir_syncer.main`.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [OpenGrok](https://oracle.github.io/opengrok/) by Oracle.
