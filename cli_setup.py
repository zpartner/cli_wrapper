import subprocess
from fastapi import FastAPI, HTTPException
from config_handler import get_datasphere_host

DATASPHERE_HOST = get_datasphere_host()
SECRETS_FILE = "secrets.json"

def run_command(command: str):
    """Utility to run shell commands."""
    print (command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Command failed: {result.stderr}")
    return result.stdout

def login():
    """Perform login to Datasphere."""
    print("Logging in to Datasphere...")
    try:
        run_command(f'datasphere login --secrets-file "{SECRETS_FILE}" --host "{DATASPHERE_HOST}"')
        print("Login successful.")
    except HTTPException as e:
        print(f"Login failed: {e.detail}")
        raise

def logout():
    """Perform logout from Datasphere (if applicable)."""
    # Note: If `datasphere` CLI has no explicit logout, this can be left out or be a placeholder
    print("Logging out from Datasphere... (optional)")
    run_command(f'datasphere logout')

def is_installed(command: str) -> bool:
    """Check if a command is installed by attempting to run it."""
    try:
        # Try to run the command, if successful return True
        subprocess.run([command, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_npm():
    """Install npm if it's not installed."""
    print("npm is not installed. Installing npm...")
    try:
        subprocess.run('pip install npm', check=True)
        print("npm installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install npm: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to install npm: {e}")

def install_datasphere():
    """Install Datasphere CLI if it's not installed."""
    print("Datasphere CLI is not installed. Installing Datasphere...")
    try:
        subprocess.run('npm install -g @sap/datasphere-cli', check=True)
        print("Datasphere installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Datasphere: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to install Datasphere: {e}")

def check_and_install_tools():
    """Check for npm and Datasphere CLI, install if necessary."""
    npm_installed = is_installed('npm')
    datasphere_installed = is_installed('datasphere')


    if not npm_installed:
        install_npm()
    else:
        print("npm is already installed.")

    if not datasphere_installed:
        install_datasphere()
    else:
        print("Datasphere CLI is already installed.")