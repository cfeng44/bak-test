from pathlib import Path
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine


APP_NOT_FOUND = "App not found"  # Constant for error message

# Create the FastAPI app instance
api_app = FastAPI()

# Define the SQLModel class
class App(SQLModel, table=True):
    """
    App model for storing application metadata, including runtime and database association.
    """
    app_id: int = Field(primary_key=True)
    name: str
    data_location: Path
    config_location: Path
    database_id: int
    runtime: str

# Database setup
DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL
engine = create_engine(DATABASE_URL, echo=True)

# Function to create tables in the database
def create_db():
    SQLModel.metadata.create_all(bind=engine)

# Endpoint to create an app record (POST request)
@api_app.post("/apps/")
def create_app(app: App):
    """
    Create a new app record in the database.

    Args:
        app (App): The app object to be created.

    Returns:
        dict: A confirmation message with the created app.
    """
    with Session(engine) as session:
        session.add(app)  # Add the app to the session
        session.commit()  # Commit changes to the database
    return {"message": "App created successfully!", "app": app}

# Endpoint to get a specific app by ID (GET request)
@api_app.get("/apps/{app_id}")
def get_app(app_id: int):
    """
    Retrieve an app record by ID from the database.

    Args:
        app_id (int): The ID of the app.

    Returns:
        dict: The app details or an error message if not found.
    """
    with Session(engine) as session:
        app = session.query(App).filter(App.app_id == app_id).first()
        if app is None:
            raise HTTPException(status_code=404, detail=APP_NOT_FOUND)
        return {"app": app}

# Endpoint to list all apps (GET request)
@api_app.get("/apps/")
def list_apps():
    """
    List all app records from the database.

    Returns:
        dict: A list of all apps.
    """
    with Session(engine) as session:
        apps = session.query(App).all()
        return {"apps": apps}

# Endpoint to update an app record by ID (PUT request)
@api_app.put("/apps/{app_id}")
def update_app(app_id: int, app: App):
    """
    Update an existing app record by ID.

    Args:
        app_id (int): The ID of the app to update.
        app (App): The updated app data.

    Returns:
        dict: A success message and updated app details.
    """
    with Session(engine) as session:
        db_app = session.query(App).filter(App.app_id == app_id).first()
        if db_app is None:
            raise HTTPException(status_code=404, detail=APP_NOT_FOUND)
        db_app.name = app.name
        db_app.data_location = app.data_location
        db_app.config_location = app.config_location
        db_app.database_id = app.database_id
        db_app.runtime = app.runtime
        session.commit()
        return {"message": "App updated successfully!", "app": db_app}

# Endpoint to delete an app record by ID (DELETE request)
@api_app.delete("/apps/{app_id}")
def delete_app(app_id: int):
    """
    Delete an app record by ID from the database.

    Args:
        app_id (int): The ID of the app to delete.

    Returns:
        dict: A confirmation message.
    """
    with Session(engine) as session:
        app = session.query(App).filter(App.app_id == app_id).first()
        if app is None:
            raise HTTPException(status_code=404, detail=APP_NOT_FOUND)
        session.delete(app)
        session.commit()
        return {"message": "App deleted successfully!"}

# Run the database creation function when the app starts
@api_app.on_event("startup")
def on_startup():
    """
    Create the database and tables on FastAPI startup.
    """
    create_db()

# Basic root endpoint to verify the server is running
@api_app.get("/")
def read_root():
    """
    Basic root endpoint to check if the server is running.

    Returns:
        dict: A simple message indicating the server is running.
    """
    return {"message": "Welcome to the FastAPI app!"}
