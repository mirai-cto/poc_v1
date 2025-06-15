import os
import traceback
import math
import numpy as np
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Circle, GeomAbs_Cylinder, GeomAbs_Line, GeomAbs_Plane, GeomAbs_Cone, GeomAbs_Ellipse, GeomAbs_BSplineCurve, GeomAbs_BezierCurve
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepIntCurveSurface import BRepIntCurveSurface_Inter
from OCC.Core.gp import gp_Lin

class CADAnalyzer:
    """
    A class for analyzing CAD models from STEP files.
    Provides comprehensive analysis of manufacturing features, tolerances, and geometric properties.
    """
    
    def __init__(self, filepath):
        """
        Initialize the CAD analyzer with a STEP file.
        
        Args:
            filepath (str): Path to the STEP file to analyze
            
        Raises:
            ValueError: If the file cannot be read or contains invalid data
        """
        try:
            print(f"Initializing CADAnalyzer with file: {filepath}")
            self.reader = STEPControl_Reader()
            print("Created STEPControl_Reader")
            
            transfer_result = self.reader.ReadFile(filepath)
            print(f"ReadFile result: {transfer_result}")
            if transfer_result != IFSelect_RetDone:
                raise ValueError(f"Failed to read STEP file - file may be corrupted or have incorrect syntax. Error code: {transfer_result}")
            
            transfer_result = self.reader.TransferRoots()
            print(f"TransferRoots result: {transfer_result}")
            if transfer_result != IFSelect_RetDone:
                raise ValueError(f"Failed to transfer STEP file contents - file may be corrupted or have incorrect syntax. Error code: {transfer_result}")
            
            self.shape = self.reader.OneShape()
            print(f"Shape is null: {self.shape.IsNull()}")
            if self.shape.IsNull():
                raise ValueError("No valid shape found in STEP file")
            
            print("CADAnalyzer initialization successful")
        except Exception as e:
            print(f"Error in CADAnalyzer initialization: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            raise
        
    def get_bounding_box(self):
        """
        Compute the bounding box dimensions of the CAD model.

        Uses OpenCASCADE's BRepBndLib to calculate the outermost bounds
        of the shape loaded from the STEP file, returning the dimensions
        along the X, Y, and Z axes in millimeters.

        Returns
        -------
        dict
            A dictionary containing:
            - 'x' : float
                Length of the bounding box along the X-axis (mm).
            - 'y' : float
                Length of the bounding box along the Y-axis (mm).
            - 'z' : float
                Length of the bounding box along the Z-axis (mm).

        Notes
        -----
        The units are assumed to be in millimeters (default for most STEP files).
        If you need min/max corner points, consider extending this method.
        """
        bbox = Bnd_Box()
        brepbndlib.Add(self.shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return {
            'x': xmax - xmin,
            'y': ymax - ymin,
            'z': zmax - zmin
        }
    
    def export_stl(self, out_path):
        print(f"Exporting STL to: {out_path}")
        try:
            # Create a mesh from the shape
            print("Creating mesh from shape...")
            mesh = BRepMesh_IncrementalMesh(self.shape, 0.1)  # 0.1 is the linear deflection
            mesh.Perform()
            print("Mesh creation completed")
            
            if not mesh.IsDone():
                raise Exception("Failed to create mesh from shape")
            
            # Create a new writer
            writer = StlAPI_Writer()
            print("Created StlAPI_Writer")
            
            # Get the shape and verify it's valid
            if self.shape.IsNull():
                raise Exception("Shape is null")
            print("Shape is valid")
            
            # Try to write the file
            print("Attempting to write STL file...")
            try:
                writer.Write(self.shape, out_path)
                print("Write completed")
            except Exception as write_error:
                print(f"Write error: {str(write_error)}")
                raise Exception(f"Failed to write STL file: {str(write_error)}")
            
            # Verify the file was created
            if not os.path.exists(out_path):
                raise Exception(f"STL file was not created at {out_path}")
            
            file_size = os.path.getsize(out_path)
            print(f"STL file exists after export: {os.path.exists(out_path)}")
            print(f"STL file size: {file_size} bytes")
            
            if file_size == 0:
                raise Exception("STL file was created but is empty")
            
            # Verify the file is readable and has correct format
            try:
                with open(out_path, 'r') as f:
                    content = f.read(100)  # Read first 100 characters
                    if not content.startswith('solid'):
                        raise Exception(f"STL file appears to be invalid. Content starts with: {content[:20]}")
            except Exception as read_error:
                print(f"Error reading STL file: {str(read_error)}")
                raise Exception(f"Failed to verify STL file: {str(read_error)}")
            
            print("STL export completed successfully")
            return True
            
        except Exception as e:
            print(f"Error in STL export: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            # If file was created but is invalid, remove it
            if os.path.exists(out_path):
                try:
                    os.remove(out_path)
                    print(f"Removed invalid STL file: {out_path}")
                except:
                    pass
            raise
    
    def post_process_features(self, features):
        """Clean up and validate features and extract manufacturing insights."""
        print(f"Post-processing {len(features)} features...")
        
        unique_features = []
        TOLERANCE = 0.001  # 1 micron tolerance

        def are_coords_similar(c1, c2):
            return abs(c1 - c2) < TOLERANCE

        for feature in features:
            center = feature.get('center', {})
            x, y, z = center.get('x'), center.get('y'), center.get('z')

            if x is None or y is None or z is None:
                print(f"Skipping feature with missing coordinates: {feature}")
                continue

            is_duplicate = False
            for seen in unique_features:
                seen_center = seen.get('center', {})
                sx, sy, sz = seen_center.get('x'), seen_center.get('y'), seen_center.get('z')
                if (feature['type'] == seen['type'] and
                    are_coords_similar(x, sx) and
                    are_coords_similar(y, sy) and
                    are_coords_similar(z, sz)):
                    is_duplicate = True
                    print(f"Found duplicate: {feature['type']} at ({x:.3f}, {y:.3f}, {z:.3f})")
                    break

            if not is_duplicate:
                unique_features.append(feature)

        print(f"Removed {len(features) - len(unique_features)} duplicates")

        # ---- Group similar features ----
        grouped_features = {}
        for feature in unique_features:
            ftype = feature['type']
            grouped_features.setdefault(ftype, []).append(feature)

        # ---- Analyze feature patterns ----
        analysis = {
            'total_features': len(unique_features),
            'feature_types': {k: len(v) for k, v in grouped_features.items()},
            'feature_groups': grouped_features
        }

        insights = []

        # ---- Cylindrical Surface Analysis ----
        if 'cylinder' in grouped_features:
            cylinders = grouped_features['cylinder']
            if len(cylinders) > 0:
                z_coords = []
                for c in cylinders:
                    cz = c.get('center', {}).get('z')
                    if cz is not None:
                        z_coords.append(cz)

                unique_z_levels = set()
                for z in z_coords:
                    found_similar = any(are_coords_similar(z, existing) for existing in unique_z_levels)
                    if not found_similar:
                        unique_z_levels.add(z)

                if len(unique_z_levels) == 1:
                    insights.append(f"All {len(cylinders)} cylindrical surfaces are at the same Z-level")
                else:
                    insights.append(f"Cylindrical surfaces span {len(unique_z_levels)} different Z-levels")

        # ---- Planar Surface Analysis ----
        if 'planar_surface' in grouped_features:
            count = len(grouped_features['planar_surface'])
            insights.append(f"Found {count} planar surfaces - check for reference or parallel planes")

        # ---- Conical Surface Analysis ----
        if 'conical_surface' in grouped_features:
            count = len(grouped_features['conical_surface'])
            insights.append(f"Found {count} conical surfaces - possible chamfers or complex tapers")

        # ---- Circle Surface Analysis ----
        if 'circle' in grouped_features:
            count = len(grouped_features['circle'])
            insights.append(f"Found {count} circless ")

        analysis['insights'] = insights

        return unique_features, analysis


    def analyze_manufacturing_features(self):
        """
        Perform comprehensive manufacturing analysis of the CAD model.
        
        Returns:
            dict: Manufacturing analysis including:
                - wall_thickness: Min, max, and average wall thickness
                - surface_finish: Analysis of surface types and finish requirements
                - tolerances: Recommended tolerances for features
                - material_volume: Total volume of the part
                - surface_area: Total surface area
                - manufacturing_notes: List of manufacturing considerations
        """
        manufacturing_analysis = {
            'wall_thickness': self.analyze_wall_thickness(),
            'surface_finish': self.analyze_surface_finish(),
            'tolerances': self.analyze_tolerances(),
            'material_volume': self.calculate_volume(),
            'surface_area': self.calculate_surface_area(),
            'manufacturing_notes': []
        }
        
        # Add manufacturing recommendations based on analysis
        if manufacturing_analysis['wall_thickness']['min'] < 1.0:
            manufacturing_analysis['manufacturing_notes'].append(
                f"Warning: Minimum wall thickness ({manufacturing_analysis['wall_thickness']['min']:.2f}mm) is very thin. Consider increasing to at least 1mm for better manufacturability."
            )
        
        if manufacturing_analysis['surface_finish']['complex_surfaces'] > 0:
            manufacturing_analysis['manufacturing_notes'].append(
                f"Found {manufacturing_analysis['surface_finish']['complex_surfaces']} complex surfaces that may require special machining considerations."
            )
        
        return manufacturing_analysis

    def analyze_wall_thickness(self):
        """
        Analyze the wall thickness distribution of the part using ray casting.
        
        Returns:
            dict: Wall thickness analysis containing:
                - min: Minimum wall thickness
                - avg: Average wall thickness
                - max: Maximum wall thickness
                - distribution: List of thickness measurements
        """
        try:
            print("Starting wall thickness analysis...")
            bbox = Bnd_Box()
            brepbndlib.Add(self.shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            
            # Define sampling parameters - increased spacing for better performance
            sample_spacing = 10.0  # mm between sample points
            ray_directions = [
                gp_Dir(1, 0, 0),   # X direction
                gp_Dir(0, 1, 0),   # Y direction
                gp_Dir(0, 0, 1),   # Z direction
            ]
            
            thicknesses = []
            total_samples = 0
            max_samples = 1000  # Limit total samples for performance
            
            print(f"Bounding box: X({xmin:.1f} to {xmax:.1f}), Y({ymin:.1f} to {ymax:.1f}), Z({zmin:.1f} to {zmax:.1f})")
            
            # Sample points across the model with progress tracking
            x_range = range(int(xmin), int(xmax), int(sample_spacing))
            y_range = range(int(ymin), int(ymax), int(sample_spacing))
            z_range = range(int(zmin), int(zmax), int(sample_spacing))
            
            total_points = len(x_range) * len(y_range) * len(z_range)
            print(f"Total possible sample points: {total_points}")
            
            for x in x_range:
                for y in y_range:
                    for z in z_range:
                        if total_samples >= max_samples:
                            print(f"Reached maximum sample limit of {max_samples}")
                            break
                            
                        point = gp_Pnt(x, y, z)
                        try:
                            thickness = self._estimate_thickness_at_point(point, ray_directions)
                            if thickness > 0:
                                thicknesses.append(thickness)
                            total_samples += 1
                            
                            if total_samples % 100 == 0:
                                print(f"Processed {total_samples} points...")
                                
                        except Exception as e:
                            print(f"Error processing point ({x}, {y}, {z}): {str(e)}")
                            continue
                    
                    if total_samples >= max_samples:
                        break
                if total_samples >= max_samples:
                    break
            
            print(f"Completed sampling. Total points processed: {total_samples}")
            
            if not thicknesses:
                print("No valid thickness measurements found")
                return {'min': 0, 'avg': 0, 'max': 0, 'distribution': []}
            
            # Calculate statistics
            thicknesses.sort()
            min_thickness = thicknesses[0]
            max_thickness = thicknesses[-1]
            avg_thickness = sum(thicknesses) / len(thicknesses)
            
            # Calculate percentiles for distribution analysis
            p25 = thicknesses[int(len(thicknesses) * 0.25)]
            p75 = thicknesses[int(len(thicknesses) * 0.75)]
            
            print(f"Analysis complete. Min: {min_thickness:.2f}, Avg: {avg_thickness:.2f}, Max: {max_thickness:.2f}")
            
            return {
                'min': min_thickness,
                'avg': avg_thickness,
                'max': max_thickness,
                'distribution': {
                    'p25': p25,
                    'p75': p75,
                    'samples': len(thicknesses),
                    'total_points': total_samples
                }
            }
            
        except Exception as e:
            print(f"Error in wall thickness analysis: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            return {'min': 0, 'avg': 0, 'max': 0, 'distribution': []}

    def _estimate_thickness_at_point(self, point, ray_directions):
        """
        Estimate wall thickness at a given point using ray casting.
        
        Args:
            point (gp_Pnt): The point to analyze
            ray_directions (list): List of ray directions to check
            
        Returns:
            float: Estimated wall thickness at the point
        """
        try:
            min_thickness = float('inf')
            
            for direction in ray_directions:
                # Create ray from point
                ray = gp_Lin(point, direction)
                
                # Find intersections with the shape
                intersector = BRepIntCurveSurface_Inter()
                intersector.Init(self.shape, ray, 0.001)  # 0.001 is the tolerance
                
                intersections = []
                while intersector.More():
                    p = intersector.Pnt()
                    intersections.append(p)
                    intersector.Next()
                
                # Calculate thickness if we have at least 2 intersections
                if len(intersections) >= 2:
                    # Sort intersections by distance from point
                    intersections.sort(key=lambda p: point.Distance(p))
                    
                    # Calculate thickness as distance between first two intersections
                    thickness = intersections[0].Distance(intersections[1])
                    min_thickness = min(min_thickness, thickness)
            
            return min_thickness if min_thickness != float('inf') else 0.0
            
        except Exception as e:
            print(f"Error in thickness estimation at point ({point.X()}, {point.Y()}, {point.Z()}): {str(e)}")
            return 0.0

    def analyze_surface_finish(self):
        """
        Analyze the surface types and finish requirements.
        
        Returns:
            dict: Surface analysis containing:
                - planar_surfaces: Count of flat surfaces
                - cylindrical_surfaces: Count of cylindrical surfaces
                - complex_surfaces: Count of complex surfaces
                - surface_roughness_estimate: Recommended surface finish
        """
        surface_analysis = {
            'planar_surfaces': 0,
            'cylindrical_surfaces': 0,
            'complex_surfaces': 0,
            'surface_roughness_estimate': 'N/A'
        }
        
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        while explorer.More():
            face = explorer.Current()
            surface = BRepAdaptor_Surface(face)
            surface_type = surface.GetType()
            
            if surface_type == GeomAbs_Plane:
                surface_analysis['planar_surfaces'] += 1
            elif surface_type == GeomAbs_Cylinder:
                surface_analysis['cylindrical_surfaces'] += 1
            else:
                surface_analysis['complex_surfaces'] += 1
            
            explorer.Next()
        
        # Estimate surface roughness based on surface types
        if surface_analysis['complex_surfaces'] > 0:
            surface_analysis['surface_roughness_estimate'] = 'Fine machining required'
        elif surface_analysis['cylindrical_surfaces'] > 0:
            surface_analysis['surface_roughness_estimate'] = 'Standard machining'
        else:
            surface_analysis['surface_roughness_estimate'] = 'Basic machining'
        
        return surface_analysis

    def analyze_tolerances(self):
        """
        Analyze geometric tolerances and fits for manufacturing.
        
        Returns:
            dict: Tolerance analysis containing:
                - hole_fits: List of standard hole sizes and recommended tolerances
                - parallel_surfaces: List of parallel surface pairs
                - perpendicular_surfaces: List of perpendicular surface pairs
                - concentric_features: List of concentric features
                - tolerance_grades: Recommended tolerance grades based on feature size
        """
        tolerance_analysis = {
            'hole_fits': [],
            'parallel_surfaces': [],
            'perpendicular_surfaces': [],
            'concentric_features': [],
            'tolerance_grades': {}
        }
        
        # Standard tolerance grades (IT grades)
        it_grades = {
            'fine': {'IT6': 0.016, 'IT7': 0.025, 'IT8': 0.040},
            'medium': {'IT7': 0.025, 'IT8': 0.040, 'IT9': 0.063},
            'coarse': {'IT8': 0.040, 'IT9': 0.063, 'IT10': 0.100}
        }
        
        # Analyze holes for standard fits
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        while explorer.More():
            face = explorer.Current()
            surface = BRepAdaptor_Surface(face)
            
            if surface.GetType() == GeomAbs_Cylinder:
                # Get cylinder parameters
                cylinder = surface.Cylinder()
                radius = cylinder.Radius()
                diameter = radius * 2
                
                # Calculate recommended tolerance based on size
                if diameter <= 3:
                    grade = 'IT7'  # Fine tolerance for small holes
                elif diameter <= 10:
                    grade = 'IT8'  # Medium tolerance for medium holes
                else:
                    grade = 'IT9'  # Coarse tolerance for large holes
                
                # Calculate actual tolerance value
                tolerance_value = it_grades['medium'][grade] * diameter
                
                tolerance_analysis['hole_fits'].append({
                    'diameter': diameter,
                    'type': 'Standard size hole',
                    'recommended_tolerance': grade,
                    'tolerance_value': tolerance_value,
                    'fit_type': 'H7' if diameter <= 10 else 'H8'
                })
            
            explorer.Next()
        
        # Add general tolerance recommendations based on feature size
        bbox = Bnd_Box()
        brepbndlib.Add(self.shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        max_dimension = max(xmax - xmin, ymax - ymin, zmax - zmin)
        
        # Recommend tolerance grades based on part size
        if max_dimension <= 50:
            tolerance_analysis['tolerance_grades'] = {
                'linear': 'IT7',
                'angular': '±0.5°',
                'surface': 'Ra 1.6'
            }
        elif max_dimension <= 200:
            tolerance_analysis['tolerance_grades'] = {
                'linear': 'IT8',
                'angular': '±1°',
                'surface': 'Ra 3.2'
            }
        else:
            tolerance_analysis['tolerance_grades'] = {
                'linear': 'IT9',
                'angular': '±2°',
                'surface': 'Ra 6.3'
            }
        
        return tolerance_analysis

    def calculate_volume(self):
        """
        Calculate the total volume of the part.
        
        Returns:
            float: Volume in cubic millimeters
        """
        props = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, props)
        return props.Mass()  # Mass is equivalent to volume for uniform density

    def calculate_surface_area(self):
        """
        Calculate the total surface area of the part.
        
        Returns:
            float: Surface area in square millimeters
        """
        props = GProp_GProps()
        brepgprop.SurfaceProperties(self.shape, props)
        return props.Mass()  # Mass is equivalent to area for surface properties

    def detect_features(self):
        """
        Extract and return raw geometric primitives (cylindrical, planar, and conical surfaces) from the CAD model.

        Returns:
            tuple: (features, analysis)
                - features: List of raw surface features
                - analysis: Dictionary (currently empty, reserved for downstream use)
        """
        features = []
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)  # Traverse all faces
        edge_explorer = TopExp_Explorer(self.shape, TopAbs_EDGE)
 

        while explorer.More():
            face = explorer.Current()  # Get current face
            surface = BRepAdaptor_Surface(face)  # Get surface geometry
            surface_type = surface.GetType()  # Identify surface type

            props = GProp_GProps()
            brepgprop.SurfaceProperties(face, props)  # Compute area, center of mass
            center = props.CentreOfMass()
            coords = {
                'x': center.X(),
                'y': center.Y(),
                'z': center.Z()
            }

            if surface_type == GeomAbs_Cylinder:
                cylinder = surface.Cylinder()
                features.append({
                    'type': 'cylinder',
                    'radius': cylinder.Radius(),
                    'axis': {
                        'x': cylinder.Axis().Direction().X(),
                        'y': cylinder.Axis().Direction().Y(),
                        'z': cylinder.Axis().Direction().Z(),
                    },
                    'center': coords
                })

            elif surface_type == GeomAbs_Plane:
                normal = surface.Plane().Axis().Direction()
                features.append({
                    'type': 'planar_surface',
                    'normal': {
                        'x': normal.X(),
                        'y': normal.Y(),
                        'z': normal.Z()
                    },
                    'surface_area': props.Mass(),
                    'center': coords
                })

            elif surface_type == GeomAbs_Cone:
                cone = surface.Cone()
                features.append({
                    'type': 'conical_surface',
                    'angle_degrees': math.degrees(cone.SemiAngle()),
                    'center': coords
                })

            explorer.Next()

        while edge_explorer.More():
            edge = edge_explorer.Current()
            curve = BRepAdaptor_Curve(edge)
            curve_type = curve.GetType()

            if curve_type == GeomAbs_Circle:
                circ = curve.Circle()
                center = circ.Location()
                axis = circ.Axis().Direction()
                features.append({
                    'type': 'circle',
                    'radius': circ.Radius(),
                    'axis': {
                        'x': axis.X(),
                        'y': axis.Y(),
                        'z': axis.Z(),
                    },
                    'center': {
                        'x': center.X(),
                        'y': center.Y(),
                        'z': center.Z(),
                    }
                })
            edge_explorer.Next()

        # Post-process features and add manufacturing analysis
        cleaned_features, analysis = self.post_process_features(features)
        manufacturing_analysis = self.analyze_manufacturing_features()
        analysis['manufacturing'] = manufacturing_analysis

        # Flatten center coordinates for frontend compatibility
        for feature in cleaned_features:
            center = feature.get('center', {})
            feature['x'] = center.get('x')
            feature['y'] = center.get('y')
            feature['z'] = center.get('z')

        print("Feature analysis:", analysis)
        return cleaned_features, analysis


    def _is_through_hole(self, face):
        """
        [TODO: PLACEHOLDER] Determine if a cylindrical face represents a through hole.
        This is a simplified check - in practice, you'd want to analyze the topology
        to determine if the hole goes through the part.
        
        Args:
            face: The cylindrical face to analyze
            
        Returns:
            bool: True if the hole appears to go through the part
        """
        return True  # Placeholder implementation 