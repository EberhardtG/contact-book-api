"""
WHY:
The ContactUpdate schema defines the structure and validation rules for partial
updates to an existing contact in the ContactBook API. Unlike ContactCreate,
which requires all fields, ContactUpdate is intentionally flexible: every field
is optional so clients can update only the specific pieces of information they
need to change. This design supports true PATCH semantics, prevents accidental
overwrites, and ensures that updates remain safe and predictable.

DESIGN:
1. All fields are declared as Optional and default to None. This allows clients
   to send only the fields they want to modify without needing to resend the
   entire contact record. Any field not provided remains unchanged.

2. first_name and last_name include the same min/max length constraints used in
   ContactCreate. This ensures that updated names remain valid and prevents
   malformed or empty values from being introduced during partial updates.

3. phone includes length validation (10–15 characters). Even though the field is
   optional, any provided phone number must still meet the required format. This
   maintains consistency with ContactCreate and ensures data integrity.

4. contact_type uses the same ContactType Enum as the other schemas. This keeps
   the update process aligned with the allowed values and ensures that filtering
   by contact_type remains reliable across the API.

5. The email field uses a Pydantic v2 field_validator that only runs when an
   email is provided. This conditional validation prevents unnecessary errors
   while still enforcing proper email format when updates include a new email
   address.

6. Examples are included for each field to improve clarity in Swagger UI. This
   helps developers understand what valid update payloads look like and makes
   the API easier to use.

Overall, the ContactUpdate schema provides a safe, flexible, and well‑validated
mechanism for modifying existing contact records. It ensures that updates are
intentional, controlled, and consistent with the rules defined in ContactCreate.
"""




from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
import re

from app.schemas.contact_create import ContactType


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="John", min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, example="Doe", min_length=1, max_length=50)
    email: Optional[str] = Field(None, example="john.doe@example.com")
    phone: Optional[str] = Field(None, example="+1-555-555-5555", min_length=10, max_length=15)
    contact_type: Optional[ContactType] = Field(None, example="personal")

    @field_validator("email")
    def validate_email(cls, value):
        if value is not None and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value
