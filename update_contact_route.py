"""
WHY:
The update_contact endpoint provides partial update functionality for existing
contacts in the ContactBook API. While the creation endpoint enforces full
validation of all fields, the update endpoint is intentionally flexible: it
allows clients to modify only the specific fields they want to change. This
supports true PATCH semantics and ensures that updates remain safe, controlled,
and predictable.

DESIGN:
1. The endpoint accepts a ContactUpdate schema, where all fields are optional.
   This allows clients to send only the fields they intend to modify without
   needing to resend the entire contact record. Any field not provided remains
   unchanged.

2. The router locates the existing contact by its id. If the contact does not
   exist, a clear 404 error is returned. This prevents silent failures and
   ensures reliable lookup behavior.

3. The update logic uses updates.model_dump(exclude_unset=True), which extracts
   only the fields explicitly provided by the client. This prevents accidental
   overwriting of existing values and ensures that partial updates behave
   correctly.

4. The updated_at timestamp is refreshed on every modification. This allows
   clients to track when the contact was last changed and supports auditability
   and synchronization across systems.

5. The final updated contact is reconstructed as a ContactResponse object,
   ensuring that all outgoing data follows a consistent structure. This improves
   API clarity and guarantees that clients always receive a complete and
   validated representation of the updated contact.

Overall, the update_contact endpoint provides a clean, safe, and flexible
mechanism for modifying contact records. It demonstrates proper PATCH semantics,
strong schema integration, and predictable API behavior.
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
