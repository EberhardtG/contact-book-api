"""
WHY:
The contacts router defines how the ContactBook API exposes its core operations
for creating, retrieving, listing, and updating contact records. While the
schemas enforce strict validation rules, the router determines how those
validated objects move through the system, how they are stored, and how they are
returned to clients. This separation of concerns ensures that the API remains
predictable, maintainable, and easy to extend. The router acts as the central
controller for all contact-related behavior.

DESIGN:
1. The router is mounted under the /contacts prefix and tagged as "Contacts" to
   keep the API organized and clearly documented in Swagger UI. This makes the
   API intuitive for developers and ensures related endpoints are grouped
   together.

2. An in-memory list (contacts_db) stores ContactResponse objects. Although
   simple, this approach allows the API to demonstrate full CRUD behavior
   without requiring a database. Storing validated Pydantic models ensures that
   all data remains structured and consistent throughout the application.

3. The POST /contacts endpoint accepts a ContactCreate schema, guaranteeing that
   all incoming data is validated before being stored. It checks for duplicate
   emails to prevent conflicting records and assigns id, created_at, and
   updated_at timestamps. The validated input is converted into a
   ContactResponse object, ensuring that all responses follow a consistent
   structure.

4. The GET /contacts endpoint supports optional filtering by contact_type. This
   allows clients to retrieve either all contacts or only those matching a
   specific type (personal or business). Filtering is performed using the
   ContactType Enum, ensuring strict and predictable behavior.

5. The GET /contacts/{id} endpoint retrieves a single contact by its unique id.
   If the contact does not exist, the router returns a clear 404 error. This
   provides reliable lookup behavior and prevents ambiguous responses.

6. The PATCH /contacts/{id} endpoint accepts a ContactUpdate schema, enabling
   partial updates. Only fields provided by the client are applied, while
   existing values remain unchanged. The updated_at timestamp is refreshed to
   reflect the modification, and the final result is returned as a
   ContactResponse object. This ensures that updates remain intentional and
   traceable.

7. All endpoints declare response_model types, ensuring that every response
   matches the ContactResponse schema. This improves API clarity, enforces
   consistent output formatting, and enhances Swagger documentation.

Overall, this router provides a clean, predictable, and fully validated interface
for managing contacts. It demonstrates proper FastAPI routing patterns, strong
schema integration, and clear separation between validation, storage, and API
behavior.
"""




from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.schemas.contact_create import ContactCreate
from app.schemas.contact_update import ContactUpdate
from app.schemas.contact_response import ContactResponse, ContactType

router = APIRouter(prefix="/contacts", tags=["Contacts"])

contacts_db: list[ContactResponse] = []
next_id = 1


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    """
    Create a new contact with full validation.
    """

    global next_id

    # Prevent duplicate email
    for existing in contacts_db:
        if existing.email == contact.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A contact with this email already exists.",
            )

    new_contact = ContactResponse(
        id=next_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **contact.model_dump()
    )

    contacts_db.append(new_contact)
    next_id += 1
    return new_contact


@router.get("/", response_model=list[ContactResponse])
def list_contacts(contact_type: ContactType | None = None):
    """
    List all contacts, optionally filtered by contact_type.
    """
    if contact_type:
        return [c for c in contacts_db if c.contact_type == contact_type]
    return contacts_db


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    """
    Retrieve a single contact by ID.
    """
    for contact in contacts_db:
        if contact.id == contact_id:
            return contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contact not found.",
    )


@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updates: ContactUpdate):
    """
    Update a contact using partial fields.
    """

    for idx, existing in enumerate(contacts_db):
        if existing.id == contact_id:

            updated_data = existing.model_dump()
            update_fields = updates.model_dump(exclude_unset=True)

            updated_data.update(update_fields)
            updated_data["updated_at"] = datetime.now()

            updated_contact = ContactResponse(**updated_data)
            contacts_db[idx] = updated_contact
            return updated_contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contact not found.",
    )
