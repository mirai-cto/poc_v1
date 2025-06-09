from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.db import crud
from app.db.models import Tool, Material, Operation

router = APIRouter()
# ----- OPERATION ROUTES -----

@router.get("/operations/{operation_id}")
def get_operation_by_id(operation_id: int, db: Session = Depends(get_db)):
    operation = crud.get_operation(db, operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation

@router.get("/operations/by-name/{name}")
def get_operation_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_operation_by_name(db, name)

@router.post("/operations")
def create_operation(operation_data: dict, db: Session = Depends(get_db)):
    return crud.create_operation(db, operation_data)
