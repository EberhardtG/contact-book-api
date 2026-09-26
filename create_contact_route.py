"""
WHY:
The contacts router defines the core API operations for creating, retrieving,
listing, and updating contacts within the ContactBook application. While the
schemas enforce data validation, the router controls how contacts flow through
the system, how they are stored, and how clients interact with them. This layer
ensures that the API behaves predictably, handles errors gracefully, and returns
consistent response models for every operation.

DESIGN:
1. The router is mounted under the /contacts prefix and tagged as "Contacts" to
   keep the API organized and clearly documented in Swagger UI.

2. An in-memory list (contacts_db) is used to store ContactResponse objects.
   Although simple, this approach allows the API to demonstrate full CRUD
   behavior without requiring a database. Each contact is stored as a validated
   Pydantic model, ensuring that all data remains structured and safe.

3. The POST /contacts endpoint accepts a ContactCreate schema, guaranteeing that
   all incoming data is validated before being stored. It also checks for
   duplicate emails to prevent conflicting records. The router assigns an id,
   created_at, and updated_at timestamp, then converts the validated input into
   a ContactResponse object for consistent output.

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
   ContactResponse object.

7. All endpoints use response_model declarations to ensure that every response
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

    # Check for duplicate email
    for existing in contacts_db:
        if existing.email == contact.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A contact with this email already exists.",
            )

    new_contact = ContactResponse(
        id=next_id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        **contact.model_dump()
    )

    contacts_db.append(new_contact)
    next_id += 1
    return new_contact


@router.get("/", response_model=list[ContactResponse])
def get_contacts(contact_type: ContactType | None = None):
    """
    Retrieve all contacts, optionally filtered by contact_type.
    """
    if contact_type:
        return [c for c in contacts_db if c.contact_type == contact_type]



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
            updated_data["updated_at"] = datetime.now().isoformat()


            updated_data.update(update_fields)

            updated_contact = ContactResponse(**updated_data)
            contacts_db[idx] = updated_contact
            return updated_contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contact not found.",
    )

