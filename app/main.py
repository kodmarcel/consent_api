from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .models import Consent
from .logic_handler import LogicHandler
from .database_mockup import DBMockup
from datetime import timedelta

databse_adapter = DBMockup(create_sample_data=True)
logicHandler = LogicHandler(databse_adapter)
app = FastAPI()


@app.get("/users/")
def get_users():
    """
    Get a list of all users registered in the database.
    
    Returns:
    - List[str]: A list of usernames.
    """
    try:
        return logicHandler.get_all_users()
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e


@app.get("/consents/")
def get_consents():
    """
    Get a list of all registered consents
    together with their validity duration in seconds.
    
    Returns:
    - dict: A dictionary of consent names as keys and their validity durations.
    """
    try:
        return logicHandler.get_all_consents()
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e


@app.get("/users/{username}/consents/")
def get_user_consents_endpoint(username: str):
    """
    Get all of user's consents.

    Parameters:
    - username (str): The username of the user.

    Returns:
    - dict: A dictionary of consent names as keys and the timestamps of their granting for the given user.
    """
    try:
        return logicHandler.get_user_consents(username)
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e

@app.get("/users/{username}/consents/{consent_name}")
def check_user_consent_valid(username: str, consent_name: str):
    """
    Check if user has a specific consent

    Parameters:
    - username (str): The username of the user.
    - consent_name (str): The name of the consent for which to check.
    
    Returns:
    - dict: A dictionary with information about the consent's validity status and reason for such result for the user.
    """
    try:
        return logicHandler.check_user_consent_valid(username, consent_name)
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e


@app.post("/consents/")
def create_consent_endpoint(consent_name: str, seconds: int = 0, days: int = 0):
    """
    Register a new consent, so it will be possible to attach it to a user.

    Parameters:
    - consent_name (str): The name of the consent.
    - seconds (int): Number of seconds of validity of the consent. This gets added to the number of days.
    - days (int): Number of days of validity of the consent. This gets added to the number of seconds.

    Returns:
    - A confirmation message.
    """
    try:
        consent = Consent(
            consent_name=consent_name, validity=timedelta(seconds=seconds, days=days)
        )
        logicHandler.create_consent(consent)
        return {"message": "Consent registered successfully"}
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e


@app.post("/users/{username}/consents/{consent_name}")
def add_user_consent_endpoint(username: str, consent_name: str):
    """
    Add a consent to a user.

    Parameters:
    - username (str): The username of the user.
    - consent_name (str): The name of the consent to add.

    Returns:
    - dict: A confirmation message.
    """
    try:
        logicHandler.add_user_consent(username, consent_name)
        return {"message": "Consent added successfully"}
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e

@app.delete("/users/{username}/consents/{consent_name}")
def revoke_user_consent_endpoint(username: str, consent_name: str):
    """
    Revoke a consent from a user.

    Parameters:
    - username (str): The username of the user.
    - consent_name (str): The name of the consent to revoke.

    Returns:
    - dict: A confirmation message.
    """
    try:
        logicHandler.revoke_user_consent(username, consent_name)
        return {"message": "Consent revoked successfully"}
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors())
    except HTTPException as e:
        return e
