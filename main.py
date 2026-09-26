"""
WHY:
The main application file serves as the entry point for the Contact Book API.
Its purpose is to initialize the FastAPI application, register all routers, and
provide a clear, organized structure for how the API is assembled. By keeping
routing logic in separate modules and using main.py only for application setup,
the project remains modular, maintainable, and easy to extend.

DESIGN:
1. A FastAPI instance is created with a title, description, and version. This
   metadata improves documentation in Swagger UI and provides clarity for anyone
   interacting with the API.

2. Routers are imported from separate modules and included using
   app.include_router(). This modular design keeps endpoint logic isolated,
   improves readability, and allows each router to focus on a specific part of
   the application (creation, retrieval, updating).

3. The / root endpoint provides a simple welcome message. While not required,
   it offers a quick way to verify that the API is running and reachable.

4. The file contains no business logic or validation rules. Instead, it acts as
   the central assembly point for the API, ensuring a clean separation of
   concerns between application setup and endpoint behavior.

Overall, main.py provides a clean, minimal, and well-structured foundation for
the Contact Book API. It demonstrates proper FastAPI application organization
and supports scalability as additional routers or features are added.
"""



from fastapi import FastAPI
from app.routers.create_contact_route import router as create_contact_route
from app.routers.response_contact_route import router as response_contact_route
from app.routers.update_contact_route import router as update_contact_route


# Create the application instance - this is your API
app = FastAPI(
    title="Contact Book API",
    description="A simple API for managing contacts",
    version="1.0.0"
)

app.include_router(create_contact_route)
app.include_router(response_contact_route)
app.include_router(update_contact_route)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Book API!"}