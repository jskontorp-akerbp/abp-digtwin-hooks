# ABP Digital Twin Hooks

A collection of **pre-commit hooks** designed to automate tasks related to **Cognite Data Fusion (CDF)** deployment and integration within the **digital twin ecosystem**.

## Features

- **CDF Deployment Dry Run**: Ensures deployment changes are validated before they are committed. This hook will help with local validation of deployment workflows, catching potential issues early.

## Prerequisites

- Python `>=3.11`
- `pre-commit` installed globally or within your project

## Installation

To use the hooks in your project, follow these steps:

### 1. Add the Hooks Repo to Your `.pre-commit-config.yaml`

Include the following configuration in your main project's `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/jskontorp-akerbp/abp-digtwin-hooks
    rev: main  # Replace with the desired branch or tag
    hooks:
    -   id: cdf-deployment-dry-run
```

### 2. Install the pre-commit hooks
Run the following command in your project directory:
```bash
pre-commit autoupdate # To get latest version
pre-commit install
```

### 3. Test the Hook
To test the `cdf-deployment-dry-run` hook locally, run:

```bash
pre-commit run --all-files
```

## Adding New Hooks
1. Add a new Python script under the hooks directory.
1. Update the .pre-commit-hooks.yaml file with the new hook configuration.
1. Test the new hook by running it locally and verifying its functionality.
