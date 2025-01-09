# ABP Digital Twin Hooks

A collection of **pre-commit hooks** designed to automate tasks related to **Cognite Data Fusion (CDF)** deployment and integration within the **digital twin ecosystem**.

## Features

- **CDF Deployment Dry Run**: Ensures deployment changes are validated before they are committed. This hook helps with local validation of deployment workflows, catching potential issues early.

## Prerequisites

Before using the pre-commit hooks, ensure the following requirements are met:

### 1. **Python Environment**
- Install **Python `>=3.11`** in your system.

### 2. **Pre-Commit Setup**
- Install the `pre-commit` tool globally or in your project's virtual environment:  
  ```  
  pip install pre-commit  
  ```  

### 3. **CDF Authentication**
- Initialize CDF authentication:  
  ```  
  cdf auth init --no-verify  
  ```  

1. **Reconfigure Variables**: If prompted with `Auth variables are already set. Do you want to reconfigure the auth variables?`, select `Yes`.
2. **Select Login Flow**: Choose the option `client_credentials: Setup a service principal with client credentials`.  
3. **Provide the Following Details**:
   - **CDF Cluster**: Enter your Cognite Data Fusion cluster name.
   - **CDF Project**: Enter your project name.
   - **Client ID**: Enter the service principal's client ID.
   - **Client Secret**: Retain the existing client secret or set a new one.
   - **Tenant ID**: Enter the tenant ID for MS Entra.
4. **Review Default Variables**: Confirm or modify the default environment variables:
   - `CDF_URL` (e.g., `https://<your-cluster-name>.cognitedata.com`)
   - `IDP_SCOPES` (e.g., `https://<your-cluster-name>.cognitedata.com/.default`)
   - `IDP_AUDIENCE` (e.g., `https://<your-cluster-name>.cognitedata.com`)

The tool will generate or update a `.env` file with the configured authentication details.

### 4. **CDF Modules Initialization**
**Note**: If you have already initialized the modules, skip this step.

1. **Run the Initialization Command**:  
   ```  
   cdf modules init  
   ```  

2. **Select the Directory**:  
   When prompted, press `Enter` to select the current directory (`.`).

3. **Choose Module Package**:  
   Select `None: start with an empty module (1)` when asked to choose a package.

4. **Confirm and Create**:  
   - When asked to confirm your selection, choose `No` to avoid changes.
   - Proceed with creation when prompted.

5. **Verify the Output**:  
   The following directories and files will be created:
   - `modules/custom/my_module`
   - `config.dev.yaml`
   - `config.prod.yaml`

Refer to [CDF Toolkit Documentation](https://docs.cognite.com/cdf/deploy/cdf_toolkit/guides/modules/custom) for additional guidance.

### 5. **Configuration File (`./config.dev.yaml`)**
- Add or use an existing `config.dev.yaml` file in the root directory. It must meet the following criteria:
  1. **Module Name**: Use `CogniteDataFusion` (not `custom/`) as the module name.
  2. **Project Name**: Set the correct project name, such as `abp-dev`.
  3. **Variable Setup**:
     - From the `config.yaml` file in [dig-cdf-templates](https://akerbp.visualstudio.com/DataOps/_git/dig-cdf-templates?path=/pipeline-templates/cdf-templ/config/config.yaml&version=GBdev&line=20&lineEnd=60&lineStartColumn=7&lineEndColumn=35&lineStyle=plain&_a=contents), copy variables under:
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
       in `./config.dev.yaml`.

     - Add all `<name>:<variable>` pairs from `custom-variables.yaml` in [dig-cdf-yggdrasil-twin](https://akerbp.visualstudio.com/DataOps/_git/dig-cdf-yggdrasil-twin?path=%2FCogniteDataFusion%2Fcustom-variables.yaml&version=GBdev&_a=contents). **Note**: These variables can have placeholder values during deployment dry runs.

---

## Installation

To use the hooks in your project, follow these steps:

### 1. Add the Hooks Repo to Your `.pre-commit-config.yaml`

Include the following configuration in your main project's `.pre-commit-config.yaml`:

```  
repos:
-   repo: https://github.com/jskontorp-akerbp/abp-digtwin-hooks
    rev: main  # Replace with the desired branch or tag
    hooks:
    -   id: cdf-deployment-dry-run
```  

### 2. Install the Pre-Commit Hooks
Run the following commands in your project directory:  
```  
pre-commit autoupdate # To get the latest version  
pre-commit install  
```  

### 3. Test the Hook
To test the `cdf-deployment-dry-run` hook locally, run:  
```  
pre-commit run --all-files  
```  

### 4. Troubleshooting
If running fails, review the toolkit logs for `UnresolvedVariableWarning`. If such warnings are present, make sure to add any missing variables (*case-sensitive* with `placeholder` values) as described in Step 5 of the Prerequisites.

## Adding New Hooks
1. Add a new Python script under the hooks directory.
2. Update the `.pre-commit-hooks.yaml` file with the new hook configuration.
3. Test the new hook by running it locally and verifying its functionality.
