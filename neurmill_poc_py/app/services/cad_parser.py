from typing import List, Dict

# def process_cad_file(cad_bytes: bytes) -> List[Dict]:
#     """
#     Stub function to simulate CAD parsing.
#     Returns dummy feature data extracted from CAD input.

#     Args:
#         cad_bytes (bytes): Raw binary CAD file input

#     Returns:
#         List[Dict]: Dummy feature list
#     """
#     # In a real implementation, you'd parse STEP/IGES/etc.
#     print("📦 Received CAD file of size:", len(cad_bytes))

#     # Dummy features
#     return [
#         {
#             "id": "feature_1",
#             "type": "hole",
#             "diameter_mm": 5.0,
#             "depth_mm": 20.0
#         },
#         {
#             "id": "feature_2",
#             "type": "pocket",
#             "width_mm": 10.0,
#             "length_mm": 15.0,
#             "depth_mm": 5.0
#         }
#     ]



def process_cad_file(file_bytes) -> List[Dict]:
    """
    Simulates parsing a CAD file and extracting machining features.
    """
    print("🔍 Simulating CAD feature extraction...")
    return [
        {"feature": "pocket", "diameter": 12.0, "position": [10.0, 20.0]},
        {"feature": "hole", "diameter": .25, "position": [30.5, 45.2]},
        {"feature": "slot", "diameter": 8.0, "position": [60.0, 10.0]},
    ]
