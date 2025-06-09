from sqlalchemy.orm import Session
from app.db.models import Machine, Tool, Material, Operation


# ---------------------- TOOL CRUD ----------------------

def get_tool(db: Session, tool_id: int) -> Tool | None:
    """Fetch a tool by its ID."""
    return db.query(Tool).filter(Tool.id == tool_id).first()


def get_tools_by_material(db: Session, material: str) -> list[Tool]:
    """Return all tools compatible with a specific material."""
    return db.query(Tool).filter(Tool.material == material).all()


def create_tool(db: Session, tool_data: dict) -> Tool:
    """Create a new tool entry from a dictionary of tool attributes."""
    db_tool = Tool(**tool_data)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


# ---------------------- MATERIAL CRUD ----------------------

def get_material(db: Session, material_id: int) -> Material | None:
    """Fetch a material by its ID."""
    return db.query(Material).filter(Material.id == material_id).first()


def get_material_by_name(db: Session, name: str) -> Material | None:
    """Fetch a material by name (case-insensitive)."""
    return db.query(Material).filter(Material.name.ilike(name)).first()


def create_material(db: Session, material_data: dict) -> Material:
    """Create a new material entry from a dictionary of material attributes."""
    db_material = Material(**material_data)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


# ---------------------- OPERATION CRUD ----------------------

def get_operation(db: Session, operation_id: int) -> Operation | None:
    """Fetch an operation by its ID."""
    return db.query(Operation).filter(Operation.id == operation_id).first()


def get_operation_by_name(db: Session, name: str) -> Operation | None:
    """Fetch an operation by name (case-insensitive)."""
    return db.query(Operation).filter(Operation.name.ilike(name)).first()


def create_operation(db: Session, operation_data: dict) -> Operation:
    """Create a new operation entry from a dictionary of operation attributes."""
    db_operation = Operation(**operation_data)
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

# ---------------------- MACHINE CRUD ----------------------
def get_machine(db: Session, machine_id: int) -> Machine | None:
    return db.query(Machine).filter(Machine.id == machine_id).first()

def get_machine_by_title(db: Session, title: str) -> Machine | None:
    return db.query(Machine).filter(Machine.title.ilike(title)).first()

def get_all_machines(db: Session) -> list[Machine]:
    return db.query(Machine).all()

def create_machine(db: Session, machine_data: dict) -> Machine:
    db_machine = Machine(**machine_data)
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine