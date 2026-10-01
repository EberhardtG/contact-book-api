

# **Contact Book API – Updated README**

## **Overview**
The Contact Book API is a lightweight FastAPI application that demonstrates core REST principles, Pydantic validation, and modular API design. It provides a complete set of CRUD‑style operations for managing contacts using an in‑memory data store. The project was developed as an assignment to showcase proper schema design, endpoint implementation, and clean application structure.

---

## **Assignment Requirements**
This project satisfies all assignment requirements, including:

- A **single router file** (`app/routers/contacts.py`) containing all endpoints  
- Proper schema validation using Pydantic v2  
- Enum‑based contact categories  
- Correct response model structure  
- Full CRUD‑style functionality (Create, List, Retrieve, Update)  
- Clean FastAPI application setup in `main.py`  

---

## **Contact Model**
The API uses Pydantic schemas to define the structure of contact data.

### **Fields**
| Field | Type | Description |
|-------|-------|-------------|
| first_name | string | Required, 1–50 chars |
| last_name | string | Required, 1–50 chars |
| email | string | Required, validated |
| phone | string | Optional, 10–15 chars |
| category | Enum | Required: `personal`, `work`, `family` |
| id | int | Auto‑assigned |
| created_at | string | ISO timestamp |
| updated_at | string | ISO timestamp |

### **Enum Correction**
The assignment requires the following valid categories:

- `personal`
- `work`
- `family`

The API now uses these exact values.

---

## **Pydantic Schemas**
Implemented schemas:

- `ContactCreate` – required fields for creating a contact  
- `ContactUpdate` – partial update schema using `exclude_unset=True`  
- `ContactResponse` – inherits from `ContactCreate` and adds `id`, `created_at`, `updated_at`  

This keeps the code DRY and ensures consistent field definitions across operations.

---

## **Router Structure**
All endpoints are now consolidated into:

```
app/routers/contacts.py
```

This corrects the previous issue where multiple router files caused duplicated routes, multiple in‑memory databases, and unpredictable behavior.

The router includes:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/contacts` | Create a new contact |
| GET | `/contacts` | List all contacts (optional filtering) |
| GET | `/contacts/{id}` | Retrieve a single contact |
| PATCH | `/contacts/{id}` | Partially update a contact |

---

## **In‑Memory Database**
The API uses:

```python
contacts_db: list[ContactResponse] = []
next_id = 1
```

This keeps the project simple and focused on endpoint behavior rather than database configuration.

---

## **Endpoint Behavior**

### **Create Contact — POST `/contacts`**
- Validates all fields  
- Prevents duplicate emails  
- Assigns a unique ID  
- Stores timestamps in ISO format  

### **List Contacts — GET `/contacts`**
Supports optional filtering:

```
GET /contacts?category=work
```

**Fix applied:**  
The unfiltered case now correctly returns `contacts_db` instead of causing a 500 error.

### **Retrieve Contact — GET `/contacts/{id}`**
Returns:

- `200 OK` for valid IDs  
- `404 Not Found` for missing contacts  

### **Update Contact — PATCH `/contacts/{id}`**
- Uses `model_dump(exclude_unset=True)`  
- Only updates fields provided by the client  
- Refreshes `updated_at` timestamp  

---

## **Validation Rules**
- **first_name / last_name:** 1–50 characters  
- **email:** required, validated  
- **phone:** optional, 10–15 characters  
- **category:** must be one of `personal`, `work`, `family`  
- **created_at / updated_at:** ISO‑formatted strings  

---

## **Application Structure**
```
project/
│
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── contacts.py
│   ├── schemas/
│   │   ├── contact_create.py
│   │   ├── contact_update.py
│   │   └── contact_response.py
│
└── requirements.txt
```

### **main.py Updates**
- Imports only the unified `contacts` router  
- Registers it with `app.include_router()`  
- Provides a simple root endpoint  
- Contains no business logic  

---

## **Testing**
All endpoints were tested using Swagger UI:

- Create contact  
- Retrieve contact  
- List contacts  
- Filter contacts  
- Update contact  
- Verify timestamps  
- Verify enum validation  
- Confirm duplicate email protection  
- Confirm correct 404 behavior  

---

## **Key Fixes Implemented**
- ✔ Unified router file  
- ✔ Corrected enum values  
- ✔ Standardized field names (`category`)  
- ✔ Fixed GET return behavior  
- ✔ Cleaned response model inheritance  
- ✔ Removed duplicated router logic  
- ✔ Ensured consistent timestamp formatting  

---
