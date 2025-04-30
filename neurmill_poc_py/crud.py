from sqlalchemy.orm import Session
from models import Tool, Material, Operation

def get_tool(db: Session, tool_id: int):
    return db.query(Tool).filter(Tool.id == tool_id).first()

def get_tools_by_material(db: Session, material: str):
    return db.query(Tool).filter(Tool.material == material).all()

def get_material(db: Session, material_id: int):
    return db.query(Material).filter(Material.id == material_id).first()

def get_material_by_name(db: Session, name: str):
    return db.query(Material).filter(Material.name == name).first()

def get_operation(db: Session, operation_id: int):
    return db.query(Operation).filter(Operation.id == operation_id).first()

def get_operation_by_name(db: Session, name: str):
    return db.query(Operation).filter(Operation.name == name).first()

def create_tool(db: Session, tool_data: dict):
    db_tool = Tool(**tool_data)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def create_material(db: Session, material_data: dict):
    db_material = Material(**material_data)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def create_operation(db: Session, operation_data: dict):
    db_operation = Operation(**operation_data)
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation 