"""
consent_logic.py - Consent Logic

This module contains the logic for creating consents.

Functions:
- create_consent(consent: Consent): Create a new consent.

"""
from datetime import datetime, timedelta
from fastapi import HTTPException
from .models import Consent


class LogicHandler:
    def __init__(self, database_adapter):
        self.database_adapter = database_adapter

    def get_all_users(self):
        """
        Get all users from the database
        """
        return self.database_adapter.get_users()

    def get_all_consents(self):
        """
        Get all consents from the database
        """
        return self.database_adapter.get_consents()

    def get_user_consents(self, username: str):
        """
        Get a user's consents.

        Parameters:
        - username (str): The username of the user.
        """
        # Check if the username exists
        if not self.database_adapter.user_exists(username):
            raise HTTPException(status_code=404, detail="User not found")

        # Get the user's consents
        return self.database_adapter.get_user_consents(username)

    def check_user_consent_valid(self, username: str, consent_name: str):
        """
        Check if user has given specific consent and that it is still valid.

        Parameters:
        - username (str): The username of the user.
        - consent_name (str): The name of the consent.
        """
        # Check if the username exists
        if not self.database_adapter.user_exists(username):
            raise HTTPException(status_code=404, detail="User not found")
        # Check if the consent exists
        if not self.database_adapter.consent_exists(consent_name):
            raise HTTPException(status_code=404, detail="Consent not found")
        respone = {
            "username": username,
            "consent_name": consent_name,
            "valid": False,
            "reason": "User has not given consent",
        }
        if self.database_adapter.user_has_consent(username, consent_name):
            if self.database_adapter.user_has_valid_consent(username, consent_name):
                respone["valid"] = True
                respone["reason"] = "User has given consent"
            else:
                respone["reason"] = "User consent has expired"
        return respone

    def create_consent(self, consent: Consent):
        """
        Create a new consent.

        Parameters:
        - consent (Consent): Consent data including name and expiration date. Name should include only alphanumeric characthers and _
        """
        # Check if consent name is valid (no spaces or special characters)
        if not consent.consent_name.replace("_", "").isalnum():
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid consent name. It should include only alphanumeric"
                    ' characters and _'
                ),
            )
        # Create the consent
        self.database_adapter.add_consent(consent)
        return consent

    def add_user_consent(self, username: str, consent_name: str):
        """
        Add a consent to a user.

        Parameters:
        - username (str): The username of the user.
        - consent_name (str): The name of the consent to add.
        """
        # Check if both the username and consent exist
        if not self.database_adapter.user_exists(username):
            raise HTTPException(status_code=404, detail="User not found")

        if not self.database_adapter.consent_exists(consent_name):
            raise HTTPException(status_code=404, detail="Consent not found")

        # Add consent to the user
        self.database_adapter.add_user_consent(username, consent_name)

    def revoke_user_consent(self, username: str, consent_name: str):
        """
        Revoke a consent from a user.

        Parameters:
        - username (str): The username of the user.
        - consent_name (str): The name of the consent to revoke.
        """
        # Check if both the username and consent exist
        if not self.database_adapter.user_exists(username):
            raise HTTPException(status_code=404, detail="User not found")

        if not self.database_adapter.consent_exists(consent_name):
            raise HTTPException(status_code=404, detail="Consent not found")

        if self.database_adapter.user_has_consent(username, consent_name):
            self.database_adapter.revoke_user_consent(username, consent_name)
