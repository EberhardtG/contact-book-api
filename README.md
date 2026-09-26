
# 📘 **ContactBook API — README**

A lightweight FastAPI application for creating, retrieving, updating, and managing contacts.  
This project demonstrates proper API design, schema validation, modular routing, configuration management, and clean separation of concerns using Pydantic v2 and FastAPI.

---

## 🚀 Overview

The ContactBook API provides:

- Creating new contacts  
- Listing all contacts  
- Filtering by `contact_type`  
- Retrieving a single contact  
- Updating contacts using PATCH  
- Centralized configuration via `config.py`  
- Full validation using Pydantic v2  
- Clean, modular routers  
- Strongly typed response models  

Swagger UI is available at:

```
/docs
```

---

## 🧱 Project Structure

```
app/
│
├── main.py
│
├── config.py
│
├── routers/
│   ├── create_contact_route.py
│   ├── response_contact_route.py
│   └── update_contact_route.py
│
└── schemas/
    ├── contact_create.py
    ├── contact_update.py
    └── contact_response.py
```

---

## ⚙️ Configuration (`config.py`)

The ContactBook API uses a centralized configuration system powered by **Pydantic Settings**.

### **Purpose**

The `Config` class loads environment variables from a `.env` file and exposes them as strongly typed settings. This keeps configuration separate from business logic and makes the application easier to deploy across different environments.

### **Design Summary**

- **BaseSettings inheritance** automatically loads environment variables.  
- **SettingsConfigDict** provides Pydantic v2‑compatible configuration.  
- **Defaults** ensure the API runs even without a `.env` file.  
- **Single `config` instance** ensures settings are loaded once and shared across the app.

### **Fields**

- `app_name`: Name of the API  
- `debug`: Boolean flag  
- `database_url`: SQLite database path (placeholder for future DB integration)

---

## 📦 Schemas

### **ContactCreate**  
Used for POST `/contacts`.

Validated fields:

- **first_name** — required, 1–50 chars  
- **last_name** — required, 1–50 chars  
- **email** — required, validated with custom `field_validator`  
- **phone** — optional, 10–15 chars  
- **contact_type** — Enum (`personal`, `business`)

### **ContactUpdate**  
Used for PATCH `/contacts/{id}`.

- All fields optional  
- Same validation rules as ContactCreate  
- Email validator only runs when email is provided  

### **ContactResponse**  
Returned by all endpoints.

Includes:

- `id: int`  
- `first_name`  
- `last_name`  
- `email`  
- `phone`  
- `contact_type`  
- `created_at: datetime`  
- `updated_at: datetime`

---

## 🔌 Routers

### **POST /contacts**  
Creates a new contact.

- Validates using `ContactCreate`  
- Prevents duplicate emails  
- Assigns `id`, `created_at`, `updated_at`  
- Returns `ContactResponse`

### **GET /contacts**  
Lists all contacts.

Optional filter:

```
/contacts?contact_type=personal
```

### **GET /contacts/{id}**  
Retrieves a single contact by ID.

Returns 404 if not found.

### **PATCH /contacts/{id}**  
Updates a contact using partial fields.

- Validates using `ContactUpdate`  
- Only updates fields provided  
- Refreshes `updated_at`  
- Returns updated `ContactResponse`

---

## 🧪 Validation Behavior

The API returns clear `422 Unprocessable Entity` errors for:

- Invalid email format  
- Names shorter than 1 or longer than 50 characters  
- Phone numbers outside 10–15 characters  
- Invalid enum values  
- Incorrect field types  

All validation is handled by Pydantic v2.

---

## 🏁 Running the API

Start the server:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## 🏷️ Root Endpoint

```
GET /
```

Returns:

```json
{"message": "Welcome to the Contact Book API!"}
```

---

## 📌 Next Steps

- Add DELETE endpoint  
- Add search endpoint  
- Add pagination  
- Convert to SQLAlchemy

