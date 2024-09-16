# CLI Wrapper Application

This project is a **FastAPI-based CLI wrapper** that interacts with SAP Datasphere and is deployed using **Cloud Foundry (CF)** on **SAP Business Technology Platform (BTP)**. It provides RESTful endpoints for authentication, running CLI task chains, managing secrets securely, and retrieving task logs. **This is still a Proof of Concept (POC) and can be improved further**.

---

*This project received valuable support from ChatGPT for content structuring and documentation guidance. 😊*


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Cloud Foundry Deployment on SAP BTP](#cloud-foundry-deployment-on-sap-btp)
- [Usage](#usage)
  - [Authentication](#authentication)
  - [Run Task Chain](#run-task-chain)
  - [Get Task Logs](#get-task-logs)
  - [Get Logs for All Task Runs](#get-logs-for-all-task-runs)
  - [Secrets Management](#secrets-management)
  - [Datasphere Host Configuration](#datasphere-host-configuration)
- [Additional Information](#additional-information)

## Overview

The project uses FastAPI to build an API that performs the following tasks:

- **Authenticate API requests** using Basic Authentication.
- **Run task chains** on SAP Datasphere using CLI commands.
- **Retrieve logs for specific task chains**.
- **Manage secrets** securely by reading from and writing to a `secrets.json` file.

The application is deployed and runs on SAP BTP using Cloud Foundry (CF).

## Features

1. **Authentication**: Ensures that only authorized requests are processed.
2. **Task Chain Execution**: Executes predefined CLI task chains and provides feedback.
3. **Task Logs Retrieval**: Retrieves detailed logs for specific tasks or task chains.
4. **Secrets Management**: Handles sensitive data using a secure `secrets.json` file.
5. **Datasphere Host Configuration**: Manage the Datasphere host configuration dynamically via API endpoints.
6. **Cloud Deployment**: Deploy and manage the application on SAP BTP using Cloud Foundry.

## Project Structure

- `app.py`: Main application logic with FastAPI endpoints.
- `auth.py`: Handles authentication using Basic Auth and validates credentials.
- `cli_commands.py`: Manages execution of task chains via CLI commands.
- `cli_setup.py`: Installs necessary CLI tools and handles login/logout operations.
- `get_logs.py`: Handles log retrieval from SAP Datasphere task chains.
- `secrets_handler.py`: Manages reading and updating secrets stored in `secrets.json`.
- `config_handler.py`: Handles the configuration of the Datasphere host.
- `credentials.json`: Stores user credentials for authentication.
- `secrets.json`: Stores API secrets and configuration data.
- `config.json`: Stores the Datasphere host configuration.
- `manifest.yaml`: Configuration for Cloud Foundry deployment.
- `Procfile`: Defines the start command for the application on CF.
- `mta.yaml`: Multi-target application descriptor for SAP BTP deployment.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/cli_wrapper.git
    cd cli_wrapper
    ```

2. Create a Python virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install **npm** and **Datasphere CLI** if not already installed:

    The project will automatically attempt to install these tools if they're not found during runtime.

## Environment Setup

- The project requires two key configuration files:
  - `credentials.json`: Contains user credentials for authentication.
  - `secrets.json`: Contains sensitive API secrets (created or updated via API calls).
  - `config.json`: Contains the Datasphere host configuration.

- You can use `credentials_template.json`, `secrets_template.json`, and `config_template.json` to structure your configuration files.

## Cloud Foundry Deployment on SAP BTP

To deploy this application on SAP BTP using Cloud Foundry, follow the steps below:

1. **Log in to SAP BTP**:

    ```bash
    cf login -a https://api.<region>.cf.sap.hana.ondemand.com
    ```

2. **Set the target space** where the application will be deployed:

    ```bash
    cf target -o <your-org> -s <your-space>
    ```

3. **Update the `manifest.yaml`** file:

    - Ensure the `manifest.yaml` file contains the correct details like app name, memory limits, and routes.
    - For example:

    ```yaml
    ---
    applications:
      - name: cliwrapper
        path: ./  # Keep the current path
        memory: 512M  # Adjust memory based on your requirements
        disk_quota: 2G  # Increase disk space to handle npm packages
        stack: cflinuxfs4  # Keep the current stack
        buildpacks:
          - python_buildpack
          - nodejs_buildpack  # Include Node.js for npm to work
        command: npm install @sap/datasphere-cli && echo "Datasphere CLI installed" && ./node_modules/.bin/datasphere --version && echo "Datasphere version printed" && uvicorn app:app --reload --host 0.0.0.0 --port $PORT
        env:
          NODE_ENV: development  # Explicitly setting NODE_ENV to avoid the warning
        services:
          - python_dest_service
    ```

4. **Deploy the application** using the following command:

    ```bash
    cf push
    ```

5. **Verify the deployment** by checking the logs and the application route. Use `cf apps` to check the status and `cf logs <app-name>` to view the logs.

6. **Access the application** using the route provided in the `manifest.yaml`, for example: `https://<your-app-name>.<region>.cfapps.sap.hana.ondemand.com`.

### Multi-Target Application (MTA)

The project includes an `mta.yaml` file, which can be used to package and deploy the application as a multi-target application (MTA) on SAP BTP. To use this:

1. **Build the MTA archive**:

    ```bash
    mbt build
    ```

2. **Deploy the MTA** to SAP BTP:

    ```bash
    cf deploy mta_archives/<app>.mtar
    ```

## Usage

Once the application is deployed, you can interact with it using the provided API endpoints.

### Authentication

- All requests must be authenticated using Basic Authentication.
- Credentials for authentication are stored in the `credentials.json` file under the `users` field.

### Run Task Chain

Endpoint: `/run_task_chain`

- **Method**: `POST`
- **Description**: Executes a task chain using the provided `space` and `object`.
- **Parameters**:
  - `space` (string): The space in which the task chain will run.
  - `object` (string): The object to run the task chain on.

Example request body:

```json
{
  "space": "your-space",
  "object": "your-object"
}
```

### Get Task Logs
**Endpoint**: `/get_log_details`

**Method**: `POST`  
**Description**: Retrieves logs for a specific task or task chain based on the `log_id`.  
**Parameters**:
- `space` (string): The space in which the task chain was run.
- `log_id` (string): The log ID of the specific task or task chain.
- `info_level` (optional, string): Level of log details. Defaults to `"status"`, but can be set to `"details"` for more information.

**Example request body**:

```json
{
  "space": "your-space-id",
  "log_id": "your-log-id",
  "info_level": "details"  # Optional
}
```
### Get Logs for All Task Runs
**Endpoint**: `/get_logs_list`

**Method**: `POST`  
**Description**: Retrieves log information for all runs of a specific task or task chain.  
**Parameters**:

- `space` (string): The space in which the task or task chain is running.
- `object` (string): The object or task chain for which logs are being retrieved.

**Example request body**:

```json
{
  "space": "your-space-id",
  "object": "your-object-id"
}
```

### Secrets Management
The application uses a `secrets.json` file to store sensitive data, like API tokens or other confidential information, securely. The following endpoints allow you to manage this file:

#### Get Secrets  
- **Endpoint**: `/get_secrets/`
- **Method**: `GET`
- **Description**: Retrieves the content of the `secrets.json` file.  
  If the secrets file does not exist, an HTTP 404 error is returned.

#### Update Secrets  
- **Endpoint**: `/update_secrets/`
- **Method**: `POST`
- **Description**: Updates or creates the `secrets.json` file with new data.
- **Request Body**: A JSON payload with the secrets data.

**Example request body**:

```json
{
  "api_key": "your-api-key",
  "token": "your-token"
}

```

### Datasphere Host Configuration
The application allows dynamic management of the Datasphere host configuration using the `config.json` file. The following endpoints allow you to retrieve and update this configuration:

#### Get Host
- **Endpoint**: `/get_host/`
- **Method**: `GET`
- **Description**: Retrieves the current Datasphere host URL from the `config.json` file.

#### Update Host
- **Endpoint**: `/update_host/`
- **Method**: `POST`
- **Description**: Updates the Datasphere host URL in the `config.json` file.
- **Request Body**: A string with the new host URL.

**Example request body**:

```json
{
  "new_host": "https://your-new-datasphere-host.com"
}
```