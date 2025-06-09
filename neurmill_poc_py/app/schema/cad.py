class Feature(BaseModel):
    id: str
    type: str  # "hole", "pocket", "slot", etc.
    diameter: float | None = None
    depth: float | None = None
    surface_area: float | None = None
    orientation_vector: tuple[float, float, float] | None = None

class CADMetadata(BaseModel):
    bounding_box: tuple[float, float, float]
    material: str