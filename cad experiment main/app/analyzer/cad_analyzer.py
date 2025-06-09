from typing import Dict, List, Tuple, Any
import os
import traceback
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh

class CADAnalyzer:
    """
    A class for analyzing CAD files and detecting features.
    
    This class provides functionality for:
    - Loading and validating STEP files
    - Detecting geometric features
    - Exporting to STL format
    - Analyzing feature patterns and manufacturing insights
    """
    
    def __init__(self, filepath: str, tolerance: float = 0.001, mesh_deflection: float = 0.1):
        """
        Initialize the CAD analyzer.
        
        Args:
            filepath: Path to the STEP file
            tolerance: Tolerance for coordinate comparison (default: 0.001)
            mesh_deflection: Linear deflection for mesh generation (default: 0.1)
            
        Raises:
            ValueError: If the file cannot be read or is invalid
        """
        self.tolerance = tolerance
        self.mesh_deflection = mesh_deflection
        self._load_step_file(filepath)
    
    def _load_step_file(self, filepath: str) -> None:
        """Load and validate a STEP file."""
        try:
            self.reader = STEPControl_Reader()
            transfer_result = self.reader.ReadFile(filepath)
            
            if transfer_result != IFSelect_RetDone:
                raise ValueError(f"Failed to read STEP file. Error code: {transfer_result}")
            
            transfer_result = self.reader.TransferRoots()
            if transfer_result != IFSelect_RetDone:
                raise ValueError(f"Failed to transfer STEP file contents. Error code: {transfer_result}")
            
            self.shape = self.reader.OneShape()
            if self.shape.IsNull():
                raise ValueError("No valid shape found in STEP file")
                
        except Exception as e:
            print(f"Error loading STEP file: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            raise
    
    def get_bounding_box(self) -> Dict[str, float]:
        """Calculate the bounding box of the shape."""
        bbox = Bnd_Box()
        brepbndlib.Add(self.shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return {
            'x': xmax - xmin,
            'y': ymax - ymin,
            'z': zmax - zmin
        }
    
    def export_stl(self, out_path: str) -> bool:
        """
        Export the shape to STL format.
        
        Args:
            out_path: Path where the STL file should be saved
            
        Returns:
            bool: True if export was successful
            
        Raises:
            Exception: If export fails
        """
        try:
            # Create mesh
            mesh = BRepMesh_IncrementalMesh(self.shape, self.mesh_deflection)
            mesh.Perform()
            
            if not mesh.IsDone():
                raise Exception("Failed to create mesh from shape")
            
            # Write STL file
            writer = StlAPI_Writer()
            writer.Write(self.shape, out_path)
            
            # Verify file
            if not os.path.exists(out_path):
                raise Exception(f"STL file was not created at {out_path}")
            
            file_size = os.path.getsize(out_path)
            if file_size == 0:
                raise Exception("STL file was created but is empty")
            
            return True
            
        except Exception as e:
            print(f"Error in STL export: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            if os.path.exists(out_path):
                os.remove(out_path)
            raise
    
    def _are_coords_similar(self, coord1: float, coord2: float) -> bool:
        """Compare coordinates with tolerance."""
        return abs(coord1 - coord2) < self.tolerance
    
    def _is_duplicate_feature(self, feature: Dict[str, Any], unique_features: List[Dict[str, Any]]) -> bool:
        """Check if a feature is a duplicate of any existing feature."""
        for seen_feature in unique_features:
            if (feature['type'] == seen_feature['type'] and
                self._are_coords_similar(feature['x'], seen_feature['x']) and
                self._are_coords_similar(feature['y'], seen_feature['y']) and
                self._are_coords_similar(feature['z'], seen_feature['z'])):
                return True
        return False
    
    def post_process_features(self, features: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Clean up and validate features.
        
        Args:
            features: List of detected features
            
        Returns:
            Tuple containing:
            - List of cleaned features
            - Dictionary with analysis results
        """
        # Remove duplicates
        unique_features = []
        for feature in features:
            if not self._is_duplicate_feature(feature, unique_features):
                unique_features.append(feature)
        
        # Validate feature positions
        valid_features = [
            f for f in unique_features
            if all(abs(coord) < 10000 for coord in [f['x'], f['y'], f['z']])
        ]
        
        # Group features by type
        grouped_features = {}
        for feature in valid_features:
            feature_type = feature['type']
            if feature_type not in grouped_features:
                grouped_features[feature_type] = []
            grouped_features[feature_type].append(feature)
        
        # Generate analysis
        analysis = self._generate_analysis(valid_features, grouped_features)
        
        return valid_features, analysis
    
    def _generate_analysis(self, features: List[Dict[str, Any]], 
                          grouped_features: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate analysis results and manufacturing insights."""
        analysis = {
            'total_features': len(features),
            'feature_types': {k: len(v) for k, v in grouped_features.items()},
            'feature_groups': grouped_features,
            'insights': self._generate_insights(grouped_features)
        }
        return analysis
    
    def _generate_insights(self, grouped_features: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate manufacturing insights based on feature patterns."""
        insights = []
        
        # Analyze holes
        if 'hole' in grouped_features:
            holes = grouped_features['hole']
            if holes:
                z_coords = [h['z'] for h in holes]
                unique_z_levels = set()
                for z in z_coords:
                    if not any(self._are_coords_similar(z, existing_z) for existing_z in unique_z_levels):
                        unique_z_levels.add(z)
                
                if len(unique_z_levels) == 1:
                    insights.append(f"All {len(holes)} holes are at the same Z-level")
                else:
                    insights.append(f"Holes are at {len(unique_z_levels)} different Z-levels")
        
        # Analyze planar faces
        if 'planar_face' in grouped_features:
            faces = grouped_features['planar_face']
            if faces:
                insights.append(f"Found {len(faces)} planar faces - check for parallel surfaces")
        
        # Analyze chamfers
        if 'chamfer' in grouped_features:
            chamfers = grouped_features['chamfer']
            if chamfers:
                insights.append(f"Found {len(chamfers)} chamfers - verify angles and dimensions")
        
        return insights
    
    def detect_features(self) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Detect features in the CAD model.
        
        Returns:
            Tuple containing:
            - List of detected features
            - Dictionary with analysis results
        """
        features = []
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        
        while explorer.More():
            face = explorer.Current()
            surface = BRepAdaptor_Surface(face)
            surface_type = surface.GetType()
            
            props = GProp_GProps()
            brepgprop.SurfaceProperties(face, props)
            pnt = props.CentreOfMass()
            
            feature_type = None
            if surface_type == GeomAbs_Cylinder:
                feature_type = 'hole'
            elif surface_type == GeomAbs_Plane:
                feature_type = 'planar_face'
            elif surface_type == GeomAbs_Cone:
                feature_type = 'chamfer'
            
            if feature_type:
                features.append({
                    'type': feature_type,
                    'confidence': 0.8 if feature_type == 'hole' else 1.0,
                    'details': f'{feature_type.replace("_", " ").title()} detected',
                    'x': pnt.X(),
                    'y': pnt.Y(),
                    'z': pnt.Z()
                })
            
            explorer.Next()
        
        return self.post_process_features(features) 