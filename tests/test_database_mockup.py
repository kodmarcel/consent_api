import pytest
from datetime import datetime, timedelta
from app.models import Consent, User
from app.database_mockup import DBMockup
from tests.test_data import database_mockup_with_data

# Original test cases
def test_get_users(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    users = db_mockup.get_users()
    assert "John" in users
    assert "Linda" in users
    assert "Mike" in users
    assert "Wayne" in users

def test_get_consents(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    consents = db_mockup.get_consents()
    assert "telemarketing" in consents
    assert "promotions" in consents
    assert "catalogues" in consents

def test_user_exists(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    assert db_mockup.user_exists("John") is True
    assert db_mockup.user_exists("NonexistentUser") is False

def test_consent_exists(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    assert db_mockup.consent_exists("telemarketing") is True
    assert db_mockup.consent_exists("NonexistentConsent") is False

def test_get_user_consents(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    user_consents = db_mockup.get_user_consents("John").consents
    assert "telemarketing" in user_consents
    assert "promotions" not in user_consents
    with pytest.raises(KeyError):
        db_mockup.get_user_consents("NonexistentUser")

def test_user_has_consent(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    assert db_mockup.user_has_consent("John", "telemarketing") is True
    assert db_mockup.user_has_consent("John", "promotions") is False
    with pytest.raises(KeyError):
        db_mockup.user_has_consent("NonexistentUser", "telemarketing")

def test_user_has_valid_consent(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    assert db_mockup.user_has_valid_consent("John", "telemarketing") is True

    assert db_mockup.user_has_valid_consent("Linda", "catalogues") is False

    with pytest.raises(KeyError):
        db_mockup.user_has_valid_consent("John", "nonExistentConsent")

    with pytest.raises(KeyError):
        db_mockup.user_has_valid_consent("NonexistentUser", "telemarketing")


def test_add_consent(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    new_consent = Consent(consent_name="test_consent1", validity=timedelta(days=30))
    db_mockup.add_consent(new_consent)
    assert db_mockup.consent_exists("test_consent1") is True

def test_add_user_consent(database_mockup_with_data):
    db_mockup = database_mockup_with_data
    db_mockup.add_user_consent("Linda", "telemarketing")
    assert db_mockup.user_has_consent("Linda", "telemarketing") is True

    with pytest.raises(KeyError):
        db_mockup.add_user_consent("NonexistentUser", "telemarketing")

def test_revoke_user_consent(database_mockup_with_data):
    db_mockup = database_mockup_with_data

    db_mockup.revoke_user_consent("John", "telemarketing")
    assert db_mockup.user_has_consent("John", "telemarketing") is False

    # Test revoking a consent from a non-existent user
    with pytest.raises(KeyError):
        db_mockup.revoke_user_consent("NonexistentUser", "telemarketing")

    # Test revoking a non-existent consent
    with pytest.raises(KeyError):
        db_mockup.revoke_user_consent("John", "nonexistent_consent")
