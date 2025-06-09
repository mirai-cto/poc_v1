from pydantic import BaseModel

class Tool(BaseModel):
    id: str
    name: str
    diameter_mm: float
    material: str
    coating: str
    tool_type: str  # drill, flat_endmill, ball_endmill
    ...

class ScoredTool(Tool):
    score: float

class PlannedTool(BaseModel):
    tool: Tool
    operation: str  # "roughing", "finishing", etc.
    feature_id: str