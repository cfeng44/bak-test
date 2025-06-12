from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from controller.v1.0.0.models import Container, Database, App, Policy, engine # type: ignore

# Create a new router for handling these requests
router = APIRouter()

# Models for request bodies
class ContainerRequest(BaseModel):
    container_id: str
    container_name: str
    image: str
    policy_id: int  # Changed to policy_id instead of Policy model

class DatabaseRequest(BaseModel):
    db_id: str
    type: str
    port: int
    user: str
    password: str

class AppRequest(BaseModel):
    app_id: int
    name: str
    data_location: str
    config_location: str
    database_id: str
    runtime: str

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

# Register a container
@router.post("/api/register/container")
async def register_container(request: ContainerRequest, session: Session = Depends(get_session)):
    # Check if the policy exists
    policy = session.execute(select(Policy).filter(Policy.id == request.policy_id)).scalars().first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    container = Container(
        container_id=request.container_id,
        container_name=request.container_name,
        image=request.image,
        policy_id=request.policy_id,  # Foreign key for Policy
    )
    session.add(container)
    session.commit()
    return {"message": "Container registered successfully"}

# Register a database
@router.post("/api/register/db")
async def register_database(request: DatabaseRequest, session: Session = Depends(get_session)):
    database = Database(
        db_id=request.db_id,
        type=request.type,
        port=request.port,
        user=request.user,
        password=request.password,
    )
    session.add(database)
    session.commit()
    return {"message": "Database registered successfully"}

# Register an app
@router.post("/api/register/app")
async def register_app(request: AppRequest, session: Session = Depends(get_session)):
    app = App(
        app_id=request.app_id,
        name=request.name,
        data_location=request.data_location,
        config_location=request.config_location,
        database_id=request.database_id,
        runtime=request.runtime
    )
    session.add(app)
    session.commit()
    return {"message": "App registered successfully"}
