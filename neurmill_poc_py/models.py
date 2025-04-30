"""
Database models for the CNC Tool Recommender system.
This file defines the SQLAlchemy models that represent the core entities of the system:
- Machines: CNC machines with their capabilities
- Materials: Workpiece materials with their properties
- Tools: Cutting tools with their specifications
"""

from ast import List
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create base class for declarative models
Base = declarative_base()

class Tool(Base):
    """
    Represents a cutting tool in the system.
    Stores tool specifications and capabilities that affect cutting performance.
    """
    __tablename__ = "tools"

    tool_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    diameter = Column(Float)
    shank_diameter = Column(Float)
    flute_count = Column(Integer)
    material = Column(String)
    coating = Column(String)
    max_speed = Column(Float)
    max_feed = Column(Float)
    cutting_length = Column(Float)
    overall_length = Column(Float)
    helix_angle = Column(Float)
    workpiece_materials = Column(String)
    center_cutting = Column(String)
    price_usd = Column(Float)
    manufacturer = Column(String)
    max_depth_of_cut = Column(Float)
    max_rpm = Column(Float)
    speed_feed_link = Column(String)
    product_link = Column(String)
    image_link = Column(String)


class Machine(Base):
    """
    Represents a CNC machine in the system.
    Stores machine capabilities and specifications that affect tool selection and cutting parameters.
    """
    __tablename__ = "machines"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)                # VF-1
    description = Column(String)                      # Short description
    product_link = Column(String)                     # Link to product page
    price_json = Column(Text)                         # Price in currencies (stored as JSON string)
    travels_json = Column(Text)                       # X/Y/Z travels
    spindle_json = Column(Text)                       # Spindle info
    table_json = Column(Text)                         # Table size
    feedrates_json = Column(Text)                     # Feedrates
    axis_motors_json = Column(Text)                   # Axis motors thrust
    tool_changer_json = Column(Text)                  # Tool changer info
    general_json = Column(Text)                       # Coolant etc
    air_requirements_json = Column(Text)              # Air requirements
    electrical_spec_json = Column(Text)               # Electrical requirements
    shipping_dims_json = Column(Text)                 # Shipping dimensions
    trunnion_json = Column(Text, nullable=True)       # (optional)

class Material(Base):
    """
    Represents a workpiece material in the system.
    Stores material properties that affect tool selection and cutting parameters.
    """
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hardness = Column(Float)
    machinability = Column(Float)

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    recommended_speed = Column(Float)
    recommended_feed = Column(Float) 