import pytest
from app.database_mockup import DBMockup
from app.logic_handler import LogicHandler
from app.models import Consent, User
from datetime import datetime, timedelta

# Define a fixture to initialize DBMockup with test data
@pytest.fixture
def database_mockup_with_data():
    db_mockup = DBMockup()
    users = []
    users.append(User(username="Mike", consents=dict()))
    users.append(User(username="John", consents=dict()))
    users.append(User(username="Mike", consents=dict()))
    users.append(User(username="Wayne", consents=dict()))
    users.append(User(username="Linda", consents=dict()))
    for user in users:
        db_mockup.users[user.username] = user

    # Add test consents
    db_mockup.add_consent(Consent(consent_name="telemarketing", validity=timedelta(hours=2)))
    db_mockup.add_consent(Consent(consent_name="promotions", validity=timedelta(weeks=1)))
    db_mockup.add_consent(Consent(consent_name="catalogues", validity=timedelta(seconds=0)))

    # Add test users with consents
    db_mockup.add_user_consent("John", "telemarketing")
    db_mockup.add_user_consent("John", "catalogues")
    db_mockup.add_user_consent("Linda", "catalogues")
    db_mockup.add_user_consent("Mike", "telemarketing")
    db_mockup.add_user_consent("Wayne", "telemarketing")
    db_mockup.add_user_consent("Wayne", "promotions")

    return db_mockup

@pytest.fixture
def logic_handler_with_data(database_mockup_with_data):
    return LogicHandler(database_mockup_with_data)