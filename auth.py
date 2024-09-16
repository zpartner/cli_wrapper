import json
import base64
from fastapi import HTTPException, status
from fastapi.requests import Request

# Load credentials from JSON file
def load_credentials():
    with open("credentials.json", "r") as file:
        credentials = json.load(file)
    return credentials["users"]  # Return the list of users

# Function to verify the Authorization header
def verify_basic_auth(auth_header: str):
    try:
        # Extract and decode the base64 encoded username and password from the "Authorization" header
        auth_type, credentials = auth_header.split()
        if auth_type.lower() != "basic":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication type",
                headers={"WWW-Authenticate": "Basic"},
            )

        # Decode the base64 string to retrieve username and password
        decoded_credentials = base64.b64decode(credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")

        # Load the stored users from the JSON file
        stored_users = load_credentials()

        # Verify the provided username and password against the stored users
        for user in stored_users:
            if user["username"] == username and user["password_hash"] == password:
                return True
        
        # If no match is found
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    except (ValueError, IndexError, base64.binascii.Error):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials format",
            headers={"WWW-Authenticate": "Basic"},
        )

# Function to get the Authorization header from the request and call the verification function
def authenticate_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Basic"},
        )
    verify_basic_auth(auth_header)
