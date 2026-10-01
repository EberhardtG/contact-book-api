

# **Student API – Updated README**

## **Overview**
The Student API is a full FastAPI application demonstrating modern REST design, SQLAlchemy 2.0 typed ORM models, Pydantic v2 validation, JWT‑based authentication, and modular router organization. It provides complete CRUD operations for student records along with secure registration, login, and protected endpoints. The project was developed as an assignment to showcase proper schema design, authentication flow, database modeling, and clean application structure.

---

## **Assignment Requirements**
This project satisfies all assignment requirements, including:

- A **typed SQLAlchemy 2.0 model** for students  
- Full CRUD functionality (Create, List, Retrieve, Update, Patch, Delete)  
- Proper schema validation using Pydantic v2  
- A complete **JWT authentication system**  
- Protected endpoints using FastAPI dependencies  
- Modular routers (`/students` and `/auth`)  
- Centralized exception handling  
- Clean FastAPI application setup in `main.py`  

---

## **Student Model**
The API uses a SQLAlchemy 2.0 typed ORM model to represent student records.

### **Fields**
| Field | Type | Description |
|-------|-------|-------------|
| id | int | Primary key |
| username | string | Required, unique, max 75 chars |
| email | string | Required, unique, max 100 chars |
| hashed_password | string | Required, securely hashed |
| major | string (optional) | Max 50 chars |
| gpa | float (optional) | Must be between 0.0 and 4.0 |

### **Database Constraints**
- `username` and `email` are **unique**  
- `gpa` is validated using a SQL `CheckConstraint`  
- All fields use SQLAlchemy’s typed `Mapped[]` annotations  

This ensures strong typing, predictable behavior, and alignment with Pydantic v2 response models.

---

## **Authentication System**
The API includes a complete authentication flow using JWT tokens.

### **Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/token` | Log in and receive a JWT |
| GET | `/auth/me` | Retrieve the current authenticated user |
| GET | `/auth/dashboard` | Example protected endpoint |

### **Password Hashing**
The API uses:

```
pbkdf2_sha256
```

instead of bcrypt due to Windows runtime instability with bcrypt’s native C extensions.  
This ensures secure, stable hashing across all environments.

### **JWT Tokens**
- Signed using HS256  
- Include an expiration timestamp  
- Store the user ID in the `sub` claim  
- Used via the `Authorization: Bearer <token>` header  

Protected endpoints rely on `get_current_user` to validate and decode tokens.

---

## **Pydantic Schemas**
Implemented schemas include:

- `StudentCreate` – required fields for creating a student  
- `StudentUpdate` – full replacement updates  
- `StudentPatch` – partial updates using `exclude_unset=True`  
- `StudentResponse` – safe output model using `from_attributes=True`  
- `UserCreate`, `LoginRequest`, `UserResponse`, `TokenResponse` for auth  

This ensures strict validation and clean separation between input and output models.

---

## **Router Structure**
All endpoints are organized into two routers:

```
app/routers/students.py
app/routers/auth.py
```

### **Students Router**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create student |
| GET | `/students` | List students (optional filters) |
| GET | `/students/{id}` | Retrieve student |
| PUT | `/students/{id}` | Full update |
| PATCH | `/students/{id}` | Partial update |
| DELETE | `/students/{id}` | Delete student |

### **Auth Router**
Handles registration, login, and protected routes.

This modular structure keeps authentication concerns separate from CRUD logic.

---

## **Custom Exceptions**
The API uses centralized custom exceptions:

- `NotFoundError` – missing resources  
- `DuplicateError` – unique constraint violations  
- `AppValidationError` – business‑rule validation  
- `AppException` – base class  

`main.py` registers exception handlers to ensure consistent JSON error responses.

---

## **Application Structure**
```
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── student.py
│   ├── routers/
│   │   ├── students.py
│   │   └── auth.py
│   ├── schemas/
│   │   ├── studentcreate.py
│   │   ├── studentupdate.py
│   │   ├── studentpatch.py
│   │   ├── studentresponse.py
│   │   ├── auth.py
│   ├── exceptions.py
│   └── auth.py
│
└── requirements.txt
```

### **main.py Responsibilities**
- Creates database tables  
- Registers routers  
- Registers exception handlers  
- Configures FastAPI metadata  

---

## **Testing**
All endpoints were tested using Swagger UI:

### **Authentication**
- Register user  
- Log in and receive JWT  
- Authorize using Swagger’s lock icon  
- Access protected endpoints  
- Confirm 401 behavior without a token  

### **CRUD**
- Create student  
- Retrieve student  
- List students with filters  
- Update and patch student  
- Validate GPA range  
- Confirm duplicate email protection  
- Confirm correct 404 behavior  
- Delete student  

---

## **Key Features Implemented**
- ✔ Typed SQLAlchemy 2.0 model  
- ✔ Secure password hashing with pbkdf2_sha256  
- ✔ JWT authentication with protected routes  
- ✔ Full CRUD functionality  
- ✔ Pydantic v2 schemas with from_attributes=True  
- ✔ Centralized custom exceptions  
- ✔ Clean router organization  
- ✔ Consistent error responses  
- ✔ Complete Swagger documentation  


---
