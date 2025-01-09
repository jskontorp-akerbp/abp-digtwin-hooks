# ABP Digital Twin Hooks

A collection of **pre-commit hooks** designed to automate tasks related to **Cognite Data Fusion (CDF)** deployment and integration within the **digital twin ecosystem**.

## Features

- **CDF Deployment Dry Run**: Ensures deployment changes are validated before they are committed. This hook will help with local validation of deployment workflows, catching potential issues early.

## Prerequisites

Before using the pre-commit hooks, ensure the following requirements are met:

### 1. **Python Environment**
- Install **Python `>=3.11`** in your system.

### 2. **Pre-Commit Setup**
- Install the `pre-commit` tool globally or in your project's virtual environment:  

```bash
pip install pre-commit
```

### 3. **CDF Authentication**
- Initialize CDF authentication:
```bash
cdf auth init --no-verify
```
and choose the option using client credentials.

### 4. **CDF Modules Initialization**
- Run the following command to initialize CDF modules:  

```bash
cdf modules init
```

- Select the option: `Start with an empty module (1)`.
- **Important**: If already present, the `modules/` directory must be empty before running this command. Note: if you already have initiated the modules, this can be skipped.

### 5. **Configuration File (`./config.dev.yaml`)**
Add or use a previously configured `config.dev.yaml` file in the root directory. It must meet the following criteria:
1. **Module Name**: Use `CogniteDataFusion` (not `custom/`) as the module name.
2. **Project Name**: Set the correct project name, `abp-dev` for instance.
3. **Variable Setup**:
 - From the `config.yaml` file in [dig-cdf-templates](https://akerbp.visualstudio.com/DataOps/_git/dig-cdf-templates?path=/pipeline-templates/cdf-templ/config/config.yaml&version=GBdev&line=20&lineEnd=60&lineStartColumn=7&lineEndColumn=35&lineStyle=plain&_a=contents), add the variables from under:
    ```
   custom_modules:
        custom:
            ...
    ```
    and place them under:
    ```
    variables:
        modules:
        CogniteDataFusion:
            ...
    ```
    in `./config.dev.yaml`

 - Add all `<name>:<variable>` pairs from `custom-variables.yaml` found in [dig-cdf-yggdrasil-twin](https://akerbp.visualstudio.com/DataOps/_git/dig-cdf-yggdrasil-twin?path=%2FCogniteDataFusion%2Fcustom-variables.yaml&version=GBdev&_a=contents). **Note**: These variables can have placeholder values when running a deployement dry run.

---


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

### 4. Troubleshooting
If running fails, review the toolkit logs for `UnresolvedVariableWarning`. If such warnings are present, make sure to add any missing variables (*case sensitive* with `placeholder` values) as descirbed in step 5.3 in prerequisites.

## Adding New Hooks
1. Add a new Python script under the hooks directory.
1. Update the .pre-commit-hooks.yaml file with the new hook configuration.
1. Test the new hook by running it locally and verifying its functionality.
