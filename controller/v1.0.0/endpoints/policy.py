from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from controller.v1.0.0.models import Container, Database, App, Policy, engine # type: ignore

# Create a new router for policy management
router = APIRouter()

# Models for request bodies
class PolicyRequest(BaseModel):
    policy_id: int
    tool: str
    copies: int
    frequency: str

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

# Update container policy
@router.put("/api/policy/container/{id}")
async def update_container_policy(id: int, request: PolicyRequest, session: Session = Depends(get_session)):
    container = session.execute(select(Container).filter(Container.id == id)).scalars().first()
    if container:
        container.policy_id = request.policy_id
        container.tool = request.tool
        container.copies = request.copies
        container.frequency = request.frequency
        session.commit()
        return {"message": "Container policy updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Container not found")

# Update database policy
@router.put("/api/policy/db/{id}")
async def update_database_policy(id: int, request: PolicyRequest, session: Session = Depends(get_session)):
    database = session.execute(select(Database).filter(Database.id == id)).scalars().first()
    if database:
        database.policy_id = request.policy_id
        database.tool = request.tool
        database.copies = request.copies
        database.frequency = request.frequency
        session.commit()
        return {"message": "Database policy updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Database not found")

# Update app policy
@router.put("/api/policy/app/{id}")
async def update_app_policy(id: int, request: PolicyRequest, session: Session = Depends(get_session)):
    app = session.execute(select(App).filter(App.id == id)).scalars().first()
    if app:
        app.policy_id = request.policy_id
        app.tool = request.tool
        app.copies = request.copies
        app.frequency = request.frequency
        session.commit()
        return {"message": "App policy updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="App not found")
