def get_faces(shape: TopoDS_Shape) -> list[TopoDS_Face]:
    ...

def classify_surface(face) -> str:
    """Return surface type: plane, cylinder, cone, etc."""
    ...

def build_adjacency_map(faces: list[TopoDS_Face]) -> dict:
    """Return dict mapping each face to its adjacent faces"""
    ...