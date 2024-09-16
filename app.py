from fastapi import FastAPI, Request, Body, HTTPException
from auth import authenticate_request
#import cli_setup
from cli_commands import run_task_chain, get_logs, get_logs_get
import secrets_handler
from config_handler import get_datasphere_host, set_datasphere_host

app = FastAPI()

#run CLI Check and install on startup
#cli_setup.check_and_install_tools()

@app.post("/")
async def auth_check(request: Request):
    # Authenticate the request using the authentication logic from auth.py
    authenticate_request(request)
    # If authentication is successful, return HTTP 200 OK
    return {"message": "Authentication successful", "status": "200 OK"}

@app.api_route("/hello", methods=["GET", "POST"])
async def say_hello(request: Request):
    # Authenticate the request using the authentication logic from auth.py
    authenticate_request(request)

    return {"message": "Hello, World"}

@app.post("/run_task_chain")
async def execute_task_chain(request: Request, space: str = Body(...), object: str = Body(...)):
    """
    Execute the task chain with the provided space and object parameters.
    """
    try:
        # Authenticate the request before running the task chain
        authenticate_request(request)

        # Run the task chain using the provided space and object
        logid = await run_task_chain(space, object)
        return {"message": "Task chain executed successfully", "log_id": logid}

    except HTTPException as e:
        # Return HTTPException errors to the client
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/get_logs")
async def get_logs_list(request: Request, space: str = Body(...), object: str = Body(...)):
    """
    Returns log information for all runs of a specific task or task chain
    """
    try:
        # Authenticate the request before running the task chain
        authenticate_request(request)

        # Run the task chain using the provided space and object
        logs= await get_logs(space, object)
        return {"message": "Logs retreived successfully", "logs": logs}

    except HTTPException as e:
        # Return HTTPException errors to the client
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/get_log_details")
async def get_log_details(request: Request, 
                          space: str = Body(...), 
                          log_id: str = Body(...), 
                          info_level: str = Body("status")):
    """
    Returns log information given the log ID of a specific task or task chain.
    The `info_level` parameter is optional and defaults to 'status'. 
    It can be set to 'details' for more detailed log information.
    """
    try:
        # Authenticate the request before processing
        authenticate_request(request)

        # Fetch the logs using the provided space, log_id, and optional info_level
        logs = await get_logs_get(space, log_id, info_level)
        return {"message": "Logs retrieved successfully", "logs": logs}

    except HTTPException as e:
        # Handle HTTP exceptions raised by the app
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        # Handle unexpected exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/get_secrets/")
async def get_secrets():
    """
    Endpoint to get the current secrets.json content.
    """
    secrets_data = secrets_handler.get_secrets()
    if not secrets_data:
        raise HTTPException(status_code=404, detail="Secrets file not found")
    
    return secrets_data

@app.post("/update_secrets/")
async def update_secrets(payload: secrets_handler.SecretsPayload):
    """
    Endpoint to update or create the secrets.json file.
    Receives a payload and writes it to secrets.json.
    """
    secrets_data = payload.dict()
    result = secrets_handler.save_secrets(secrets_data)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.get("/get_host/")
async def get_host():
    """
    Get the current Datasphere host URL.
    """
    return {"datasphere_host": get_datasphere_host()}

@app.post("/update_host/")
async def update_host(new_host: str = Body(...)):
    """
    Update the Datasphere host URL.
    """
    try:
        set_datasphere_host(new_host)
        return {"message": f"Datasphere host updated to {new_host}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update Datasphere host: {str(e)}")