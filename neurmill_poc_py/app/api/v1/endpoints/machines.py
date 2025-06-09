from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.db import crud

router = APIRouter()

@router.get("/machines")
def get_all_machines(db: Session = Depends(get_db)):
    return crud.get_all_machines(db)

@router.get("/machines/{machine_id}")
def get_machine_by_id(machine_id: int, db: Session = Depends(get_db)):
    machine = crud.get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.get("/machines/by-title/{title}")
def get_machine_by_title(title: str, db: Session = Depends(get_db)):
    machine = crud.get_machine_by_title(db, title)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.post("/machines")
def create_machine(machine_data: dict, db: Session = Depends(get_db)):
    return crud.create_machine(db, machine_data)
