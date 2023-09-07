from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class Consent(BaseModel):
    consent_name: str
    validity: timedelta


class User(BaseModel):
    username: str
    consents: dict[str, datetime] = {}
