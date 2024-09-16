import subprocess
import cli_setup
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
import json
from config_handler import get_datasphere_host

DATASPHERE_HOST = get_datasphere_host()

def run_command(command: str):
    """Utility to run shell commands."""
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Command failed: {result.stderr}")
    return result.stdout


async def run_task_chain(space, object):
    """Run the task chain"""
    try:
        await run_in_threadpool(cli_setup.login)  # Wait for login to finish

        command = f'datasphere tasks chains run --space "{space}" --object "{object}" --host "{DATASPHERE_HOST}"'
        logid = await run_in_threadpool(run_command, command)
        print(logid)
        return logid
    finally:
        await run_in_threadpool(cli_setup.logout)  # Ensure logout happens after command execution


async def get_logs(space, object):
    """Returns log information for all runs of a specific task or task chain"""
    try:
        await run_in_threadpool(cli_setup.login)  # Wait for login to finish

        command = f'datasphere tasks logs list --space "{space}" --object "{object}" --host "{DATASPHERE_HOST}"'
        logid = await run_in_threadpool(run_command, command)
        print(logid)
        return logid
    finally:
        await run_in_threadpool(cli_setup.logout)  # Ensure logout happens after command execution

async def get_logs_get(space, log_id, info_level="status"):
    """Returns log information given the log ID of a specific task or task chain. """
    """An optional argument --info-level specifies the level of log detail you wish to display. """
    """The default status option returns simple status information: running, completed, or failed. """
    """The details option returns full details of status information for a given task chain, including subtasks."""
    try:
        await run_in_threadpool(cli_setup.login)  # Wait for login to finish

        # Modify command to include the optional --info-level argument
        command = (
            f'datasphere tasks logs get '
            f'--space "{space}" '
            f'--log-id "{log_id}" '
            f'--info-level "{info_level}" '
            f'--host "{DATASPHERE_HOST}"'
        )
        logid = await run_in_threadpool(run_command, command)
        print(logid)
        return logid
    finally:
        await run_in_threadpool(cli_setup.logout)  # Ensure logout happens after command execution

