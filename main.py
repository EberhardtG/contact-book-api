"""
WHY:
The main application file serves as the entry point for the Contact Book API.
Its purpose is to initialize the FastAPI application, register the unified
contacts router, and provide a clean, centralized structure for assembling the
API. By keeping all endpoint logic inside contacts.py and using main.py solely
for application setup, the project remains modular, easy to navigate, and
simple to extend. This separation of concerns ensures that routing, validation,
and business logic stay isolated from the core application configuration.

DESIGN:
1. A FastAPI instance is created with a title, description, and version. This
   metadata improves Swagger UI documentation and provides clarity for anyone
   interacting with the API.

2. The consolidated contacts router is imported from app.routers.contacts and
   registered using app.include_router(). This reflects the updated project
   structure where all contact-related endpoints exist in a single module.

3. The root (/) endpoint provides a simple welcome message, offering a quick
   way to verify that the API is running and reachable.

4. main.py contains no business logic, validation rules, or endpoint behavior.
   Instead, it acts strictly as the assembly point for the API, ensuring a
   clean separation between application setup and functional routing.

Overall, main.py provides a minimal, well‑structured foundation for the Contact
Book API. It demonstrates proper FastAPI organization and supports scalability
as additional routers or features are added.
"""



from fastapi import FastAPI
from app.routers.contacts import router as contacts_router

# Create the application instance
app = FastAPI(
    title="Contact Book API",
    description="A simple API for managing contacts",
    version="1.0.0"
)

# Register the unified contacts router
app.include_router(contacts_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Book API!"}
