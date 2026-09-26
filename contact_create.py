"""
WHY:
The ContactCreate schema defines the required structure and validation rules for
creating new contacts in the ContactBook API. By enforcing strict validation at
the schema level, the API ensures that all incoming data is clean, predictable,
and safe before it ever reaches the router or in‑memory database. This prevents
bad data from entering the system and guarantees consistent behavior across all
endpoints.

DESIGN:
1. first_name and last_name use min/max length constraints (1–50 characters) to
   prevent empty names and excessively long values. This keeps contact records
   readable and avoids malformed entries.

2. email is required and validated using a custom Pydantic v2 field_validator.
   The validator ensures the email contains an '@' symbol and follows a basic
   email pattern. This prevents invalid or unusable email addresses from being
   stored.

3. phone is optional but includes length constraints (10–15 characters). This
   allows flexibility—users may omit phone numbers—but still enforces structure
   when provided.

4. contact_type is implemented as an Enum (personal, business, family). Using an Enum
   guarantees that only valid, predefined categories can be assigned. This
   improves data consistency and makes filtering by contact_type reliable.

5. All fields use Pydantic's Field() metadata to provide examples in Swagger UI.
   This improves API usability by showing developers exactly what valid input
   looks like.

Overall, the ContactCreate schema acts as the first line of defense against
invalid data and ensures that every new contact entering the system meets the
required structure and validation rules.
"""





import re
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ContactType(str, Enum):
    personal = "personal"
    business = "business"
    family = "family"


class ContactCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: str = Field(..., example="john.doe@example.com")
    phone: Optional[str] = Field(None, min_length=10, max_length=15, example="5551234567")
    category: ContactType = Field(..., example="personal")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value