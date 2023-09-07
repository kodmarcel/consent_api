"""
database.py - Data Persistence

This module handles data persistence using an in-memory database.

Classes:
- MemoryDB: In-memory database class for storing consents and user data.

"""
from datetime import datetime, timedelta
from typing import Optional
from .models import Consent, User


class DBMockup:
    """
    In-memory database for storing consents and user data.
    """

    def __init__(self, create_sample_data=False):
        self.consents = {}
        self.users = {}
        if create_sample_data:
            self.initialize_data()

    def initialize_data(self):
        self.add_consent(Consent(consent_name="telemarketing", validity=timedelta(minutes=2)))
        self.add_consent(
            Consent(consent_name="promotions", validity=timedelta(weeks=1))
        )
        self.add_consent(Consent(consent_name="catalogues", validity=timedelta(seconds=10)))
        users = []
        users.append(
            User(
                username="John",
                consents={
                    "telemarketing": datetime.now(),
                    "catalogues": datetime.now(),
                },
            )
        )
        users.append(User(username="Linda", consents=dict()))
        users.append(User(username="Maria", consents=dict()))
        users.append(User(username="Mike", consents=dict()))
        users.append(
            User(
                username="Wayne",
                consents={
                    "telemarketing": datetime.now(),
                    "catalogues": datetime.now(),
                    "promotions": datetime.now(),
                },
            )
        )
        for user in users:
            self.users[user.username] = user

    def get_users(self):
        "Get all users in the data source"
        return list(self.users.keys())

    def get_consents(self):
        """Get all consents in the datasource"""
        return self.consents

    def user_exists(self, username):
        """Check if user is present in the datasource"""
        if username in self.users:
            return True
        return False

    def consent_exists(self, consent_name):
        """Check if consent is present in the datasource"""
        if consent_name in self.consents:
            return True
        return False

    def get_user_consents(self, username):
        """Returns all consents of the user"""
        return self.users[username]

    def user_has_consent(self, username, consent_name):
        """Returns True if user has consent, False otherwise"""
        if consent_name in self.users[username].consents:
            return True
        return False

    def user_has_valid_consent(self, username, consent_name):
        """Returns True if user has valid consent, False otherwise"""
        consent_expires_on = (
            self.users[username].consents[consent_name]
            + self.consents[consent_name].validity
        )
        if datetime.now() <= consent_expires_on:
            return True
        return False

    def add_consent(self, consent: Consent):
        """
        Add a new consent to the database.
        """
        self.consents[consent.consent_name] = consent

    def add_user_consent(self, username, consent_name):
        """
        Add a consent to user.
        """
        self.users[username].consents[consent_name] = datetime.now()

    def revoke_user_consent(self, username, consent_name):
        """
        Add a consent to user.
        """
        del self.users[username].consents[consent_name]
