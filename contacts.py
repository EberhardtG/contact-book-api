"""
WHY:
The contacts router is implemented as a single module to meet the assignment
requirement of consolidating all endpoints into one file. Using an in‑memory
list for storage keeps the API simple and focused on demonstrating FastAPI
routing, validation, and CRUD behavior without introducing database complexity.
The router provides a complete set of operations—create, list, retrieve, and
update—while enforcing essential validation such as duplicate email prevention
and proper error responses. This ensures predictable behavior and consistent
data handling across all endpoints.

DESIGN:
1. All endpoints are grouped under a single APIRouter with the /contacts prefix.
   This keeps the API organized and makes the module easy to navigate.

2. contacts_db and next_id simulate persistent storage using an in‑memory list
   and incremental ID assignment. This is appropriate for a lightweight,
   assignment‑focused implementation.

3. Duplicate email checks in POST ensure data integrity and prevent conflicting
   records from being created.

4. GET supports optional filtering by contact_type, demonstrating how query
   parameters refine API results and improving usability for clients.

5. PATCH uses model_dump(exclude_unset=True) to apply partial updates safely.
   Only fields provided by the client are modified, while existing values are
   preserved. updated_at is refreshed on every modification.

6. Timestamps are stored using ISO‑formatted datetime strings, ensuring clean,
   JSON‑friendly serialization and consistent output across all endpoints.

Overall, the router is intentionally simple, readable, and aligned with FastAPI
best practices, providing a clear example of CRUD operations within a single,
self‑contained module.
"""



from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.schemas.contact_create import ContactCreate
from app.schemas.contact_update import ContactUpdate
from app.schemas.contact_response import ContactResponse, ContactType

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# In‑memory "database"
contacts_db: list[ContactResponse] = []
next_id = 1


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    """
    Create a new contact with full validation.
    Prevents duplicate emails.
    """
    global next_id

    # Duplicate email check
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
    Partially update a contact.
    Only fields provided by the user are updated.
    """
    for idx, existing in enumerate(contacts_db):
        if existing.id == contact_id:

            # Convert existing model to dict
            updated_data = existing.model_dump()

            # Only apply fields the user actually sent
            update_fields = updates.model_dump(exclude_unset=True)

            updated_data.update(update_fields)
            updated_data["updated_at"] = datetime.now().isoformat()

            updated_contact = ContactResponse(**updated_data)
            contacts_db[idx] = updated_contact
            return updated_contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contact not found.",
    )
