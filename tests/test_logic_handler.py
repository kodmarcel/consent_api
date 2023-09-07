import pytest
from fastapi import HTTPException
from tests.test_data import logic_handler_with_data, database_mockup_with_data
from app.models import Consent
from datetime import timedelta

def test_get_all_users(logic_handler_with_data):
    users = logic_handler_with_data.get_all_users()
    assert "John" in users
    assert "Linda" in users
    assert "Mike" in users

def test_get_all_consents(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    consents = logic_handler_with_data.get_all_consents()
    assert "telemarketing" in consents
    assert "promotions" in consents
    assert "catalogues" in consents

def test_get_user_consents(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    user_consents = logic_handler_with_data.get_user_consents("John").consents
    assert "telemarketing" in user_consents
    assert "promotions" not in user_consents

def test_check_user_consent_valid(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    # Test for a valid consent
    response = logic_handler_with_data.check_user_consent_valid("John", "telemarketing")
    assert response["valid"] is True
    assert response["reason"] == "User has given consent"

    # Test for an expired consent
    response = logic_handler_with_data.check_user_consent_valid("John", "catalogues")
    assert response["valid"] is False
    assert response["reason"] == "User consent has expired"

    # Test for not given consent
    response = logic_handler_with_data.check_user_consent_valid("John", "promotions")
    assert response["valid"] is False
    assert response["reason"] == "User has not given consent"


    # Test for a non-existent user
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.check_user_consent_valid("NonexistentUser", "telemarketing")
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail

    # Test for a non-existent consent
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.check_user_consent_valid("John", "nonexistent_consent")
    assert excinfo.value.status_code == 404
    assert "Consent not found" in excinfo.value.detail

# Additional test cases
def test_create_consent(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    # Test creating a new valid consent
    new_consent = Consent(consent_name="test_consent1", validity=timedelta(days=30))
    response = logic_handler_with_data.create_consent(new_consent)
    assert response == new_consent
    assert logic_handler_with_data.database_adapter.consent_exists("test_consent1") is True

    # Test creating a consent with an invalid name
    with pytest.raises(HTTPException) as excinfo:
        duplicate_consent = Consent(consent_name="*?!dsa", validity=timedelta(days=30))
        logic_handler_with_data.create_consent(duplicate_consent)
    assert excinfo.value.status_code == 400
    assert "Invalid consent name" in excinfo.value.detail

def test_add_user_consent(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    # Test adding a valid consent to a user
    logic_handler_with_data.add_user_consent("Linda", "telemarketing")
    assert logic_handler_with_data.database_adapter.user_has_consent("Linda", "telemarketing") is True

    # Test adding a consent to a non-existent user
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.add_user_consent("NonexistentUser", "telemarketing")
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail

    # Test adding a non-existent consent
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.add_user_consent("Linda", "nonexistent_consent")
    assert excinfo.value.status_code == 404
    assert "Consent not found" in excinfo.value.detail

def test_revoke_user_consent(logic_handler_with_data):
    logic_handler = logic_handler_with_data
    # Test revoking a valid consent from a user
    logic_handler_with_data.revoke_user_consent("John", "telemarketing")
    assert logic_handler_with_data.database_adapter.user_has_consent("John", "telemarketing") is False

    # Test revoking consent user did not give or was already revoked does not return error
    logic_handler_with_data.revoke_user_consent("John", "telemarketing")
    assert logic_handler_with_data.database_adapter.user_has_consent("John", "telemarketing") is False

    # Test revoking a consent from a non-existent user
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.revoke_user_consent("NonexistentUser", "telemarketing")
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail

    # Test revoking a non-existent consent
    with pytest.raises(HTTPException) as excinfo:
        logic_handler_with_data.revoke_user_consent("John", "nonexistent_consent")
    assert excinfo.value.status_code == 404
    assert "Consent not found" in excinfo.value.detail
