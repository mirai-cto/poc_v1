# CADClassifier: Robust CAD feature classification for machinist analysis
# Cleansed, commented, and ready for further extension
import math
import numpy as np
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Circle
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRep import BRep_Tool
from cad_analyzer import CADAnalyzer

class CADClassifier:
    def __init__(self, file_path):
        """Initialize classifier and geometric properties."""
        self.analyzer = CADAnalyzer(file_path)
        self.shape = self.analyzer.shape
        self.features = []
        self.face_types = {}
        self.adjacency_graph = {}
        self.analyzer_features = None
        self.analyzer_analysis = None
        self._initialize_geometric_properties()

    def _initialize_geometric_properties(self):
        """Compute bounding box and set tolerance."""
        bbox = Bnd_Box()
        brepbndlib.Add(self.shape, bbox)
        min_point = bbox.CornerMin()
        max_point = bbox.CornerMax()
        self.bbox = bbox
        self.overall_dimensions = {
            'x': float(max_point.X() - min_point.X()),
            'y': float(max_point.Y() - min_point.Y()),
            'z': float(max_point.Z() - min_point.Z())
        }
        min_dim = min(self.overall_dimensions.values())
        self.tolerance = min_dim * 0.001  # 0.1% tolerance
        print(f"Model dimensions: {self.overall_dimensions}")
        print(f"Using tolerance: {self.tolerance}")

    def classify_features(self):
        """Main entry: classify and return all features."""
        print("\nStarting feature classification...")
        self.analyzer_features, self.analyzer_analysis = self.analyzer.detect_features()
        print(f"Found {len(self.analyzer_features)} features from analyzer")
        self._analyze_faces()
        self._build_adjacency_graph()  # TODO: Implement adjacency graph logic
        self._classify_features()
        self._post_process_features()  # TODO: Enhance post-processing with more feature types
        print(f"Classification complete. Found {len(self.features)} features.")
        return self.features

    def _analyze_faces(self):
        """Group faces by geometric type."""
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        while explorer.More():
            face = explorer.Current()
            surf = BRepAdaptor_Surface(face)
            surf_type = surf.GetType()
            if surf_type not in self.face_types:
                self.face_types[surf_type] = []
            self.face_types[surf_type].append(face)
            explorer.Next()

    def _build_adjacency_graph(self):
        """Build a graph of adjacent faces for complex pattern recognition. TODO: Implement this."""
        pass  # TODO: Implement adjacency graph logic for advanced feature grouping

    def _classify_features(self):
        """Classify all features by type."""
        self.features = []
        self._classify_holes()
        self._classify_pockets()
        self._classify_slots()
        self._classify_bosses()
        self._classify_chamfers()
        self._classify_fillets()
        self._classify_flat_faces()
        self._classify_countersinks()

    def _classify_holes(self):
        """Cluster adjacent cylindrical faces and classify vertical holes."""
        if GeomAbs_Cylinder not in self.face_types:
            print("DEBUG: No cylindrical faces found")
            return
        def get_axis_and_radius(face):
            surf = BRepAdaptor_Surface(face)
            cyl = surf.Cylinder()
            axis = cyl.Axis().Direction()
            radius = cyl.Radius()
            return np.array([axis.X(), axis.Y(), axis.Z()]), radius
        clusters = []
        used = set()
        axis_tol = 0.1
        radius_tol = self.tolerance * 2
        faces = self.face_types[GeomAbs_Cylinder]
        for i, face in enumerate(faces):
            if i in used:
                continue
            if not hasattr(face, 'IsNull') or face.IsNull():
                continue
            axis_i, radius_i = get_axis_and_radius(face)
            cluster = [face]
            used.add(i)
            for j, other in enumerate(faces):
                if j == i or j in used:
                    continue
                if not hasattr(other, 'IsNull') or other.IsNull():
                    continue
                axis_j, radius_j = get_axis_and_radius(other)
                cos_sim = np.dot(axis_i, axis_j) / (np.linalg.norm(axis_i) * np.linalg.norm(axis_j))
                if abs(cos_sim) > 1 - axis_tol and abs(radius_i - radius_j) < radius_tol:
                    cluster.append(other)
                    used.add(j)
            clusters.append(cluster)
        print(f"DEBUG: Found {len(clusters)} cylindrical face clusters (potential holes)")
        for idx, cluster in enumerate(clusters):
            try:
                if not all(hasattr(f, 'IsNull') and not f.IsNull() for f in cluster):
                    continue
                ref_face = cluster[0]
                axis, radius = get_axis_and_radius(ref_face)
                if abs(axis[2]) < 0.85:
                    continue
                radii = [get_axis_and_radius(f)[1] for f in cluster]
                avg_radius = float(np.mean(radii))
                all_edges = []
                for f in cluster:
                    edges = self._get_face_edges(f)
                    for e in edges:
                        edge_obj = e[0] if isinstance(e, tuple) else e
                        if self._is_circular_edge(edge_obj):
                            all_edges.append(edge_obj)
                if not all_edges:
                    continue
                diameter = 2.0 * avg_radius
                min_z, max_z = None, None
                for f in cluster:
                    bbox = Bnd_Box()
                    brepbndlib.Add(f, bbox)
                    min_point = bbox.CornerMin()
                    max_point = bbox.CornerMax()
                    z0, z1 = float(min_point.Z()), float(max_point.Z())
                    if min_z is None or z0 < min_z:
                        min_z = z0
                    if max_z is None or z1 > max_z:
                        max_z = z1
                depth = abs(max_z - min_z)
                if diameter < self.tolerance or depth < max(self.tolerance, 0.1):
                    continue
                feature = {
                    'type': 'hole',
                    'diameter': diameter,
                    'depth': depth,
                    'face_count': len(cluster),
                    'axis': axis.tolist(),
                    'manufacturing_notes': [f"Clustered from {len(cluster)} faces"]
                }
                self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing hole cluster {idx}: {str(e)}")
                continue

    def _classify_pockets(self):
        """Classify enclosed pockets with minimum depth threshold."""
        if GeomAbs_Plane not in self.face_types:
            return
        min_depth = max(self.tolerance, 0.1)  # 0.1mm minimum depth
        for face in self.face_types[GeomAbs_Plane]:
            try:
                if not self._is_horizontal_face(face):
                    continue
                bbox = Bnd_Box()
                brepbndlib.Add(face, bbox)
                min_point = bbox.CornerMin()
                max_point = bbox.CornerMax()
                width = float(max_point.X() - min_point.X())
                length = float(max_point.Y() - min_point.Y())
                if width < self.tolerance or length < self.tolerance:
                    continue
                if not self._is_enclosed(face):
                    continue
                depth = self._get_pocket_depth(face)
                if depth <= min_depth:
                    continue
                aspect_ratio = max(width, length) / min(width, length)
                feature = {
                    'type': 'pocket',
                    'width': width,
                    'length': length,
                    'depth': depth,
                    'aspect_ratio': aspect_ratio,
                    'manufacturing_notes': []
                }
                if depth > 10:
                    feature['manufacturing_notes'].append("Deep pocket - consider step machining")
                if aspect_ratio > 3:
                    feature['manufacturing_notes'].append("Long narrow pocket - consider end mill selection")
                if width < 5 or length < 5:
                    feature['manufacturing_notes'].append("Small pocket - tight tolerances required")
                self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing pocket: {str(e)}")
                continue

    def _classify_slots(self):
        """Classify slots: elongated cylinders and high aspect ratio pockets."""
        slot_aspect_ratio = 2.5
        min_slot_length = 2 * self.tolerance
        # 1. Elongated non-vertical cylinders
        if GeomAbs_Cylinder in self.face_types:
            faces = self.face_types[GeomAbs_Cylinder]
            used = set()
            for i, face in enumerate(faces):
                if i in used:
                    continue
                surf = BRepAdaptor_Surface(face)
                cyl = surf.Cylinder()
                axis = np.array([cyl.Axis().Direction().X(), cyl.Axis().Direction().Y(), cyl.Axis().Direction().Z()])
                radius = cyl.Radius()
                if abs(axis[2]) > 0.85:
                    continue
                bbox = Bnd_Box()
                brepbndlib.Add(face, bbox)
                min_point = bbox.CornerMin()
                max_point = bbox.CornerMax()
                length = np.linalg.norm([max_point.X() - min_point.X(), max_point.Y() - min_point.Y(), max_point.Z() - min_point.Z()])
                if length < min_slot_length:
                    continue
                aspect_ratio = length / (2 * radius)
                if aspect_ratio > slot_aspect_ratio:
                    feature = {
                        'type': 'slot',
                        'length': length,
                        'radius': radius,
                        'aspect_ratio': aspect_ratio,
                        'axis': axis.tolist(),
                        'manufacturing_notes': ["Detected as elongated cylinder (slot)"]
                    }
                    self.features.append(feature)
                    used.add(i)
        # 2. Convert high aspect ratio pockets to slots
        for feature in self.features:
            if feature['type'] == 'pocket' and feature.get('aspect_ratio', 0) > slot_aspect_ratio:
                feature['type'] = 'slot'
                if 'manufacturing_notes' not in feature:
                    feature['manufacturing_notes'] = []
                feature['manufacturing_notes'].append("Converted from pocket due to high aspect ratio")

    def _classify_bosses(self):
        """Classify cylindrical bosses (vertical, convex, on top). TODO: Improve convexity/top checks."""
        if GeomAbs_Cylinder not in self.face_types:
            return
        for face in self.face_types[GeomAbs_Cylinder]:
            try:
                if not self._is_vertical_cylinder(face):
                    continue
                if not self._is_convex_face(face):  # TODO: Implement real convexity check
                    continue
                if not self._is_top_face(face):  # TODO: Implement real top face check
                    continue
                diameter = self._get_face_diameter(face)
                height = self._get_face_height(face)
                if diameter <= self.tolerance or height <= self.tolerance:
                    continue
                feature = {
                    'type': 'boss',
                    'diameter': diameter,
                    'height': height,
                    'manufacturing_notes': []
                }
                if height > 10:
                    feature['manufacturing_notes'].append("Tall boss - consider support during machining")
                if diameter < 5:
                    feature['manufacturing_notes'].append("Small diameter boss - tight tolerances required")
                self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing boss: {str(e)}")
                continue

    def _classify_chamfers(self):
        """Classify chamfers (45-degree bevels). TODO: Implement real chamfer detection."""
        if GeomAbs_Plane not in self.face_types:
            return
        for face in self.face_types[GeomAbs_Plane]:
            try:
                if not self._is_chamfer_face(face):  # TODO: Implement real chamfer detection
                    continue
                bbox = Bnd_Box()
                brepbndlib.Add(face, bbox)
                min_point = bbox.CornerMin()
                max_point = bbox.CornerMax()
                width = float(max_point.X() - min_point.X())
                length = float(max_point.Y() - min_point.Y())
                if width < self.tolerance or length < self.tolerance:
                    continue
                feature = {
                    'type': 'chamfer',
                    'width': width,
                    'length': length,
                    'angle': 45.0,  # Standard chamfer angle
                    'manufacturing_notes': []
                }
                if width < 2:
                    feature['manufacturing_notes'].append("Narrow chamfer - consider tool selection")
                if length > 20:
                    feature['manufacturing_notes'].append("Long chamfer - check tool path")
                self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing chamfer: {str(e)}")
                continue

    def _classify_fillets(self):
        """Classify fillets (rounded edges). TODO: Implement real fillet detection."""
        for surf_type in [GeomAbs_Cylinder, GeomAbs_Cone]:
            if surf_type not in self.face_types:
                continue
            for face in self.face_types[surf_type]:
                try:
                    if not self._is_fillet_face(face):  # TODO: Implement real fillet detection
                        continue
                    radius = self._get_face_radius(face)
                    if radius <= self.tolerance:
                        continue
                    feature = {
                        'type': 'fillet',
                        'radius': radius,
                        'manufacturing_notes': []
                    }
                    if radius < 1:
                        feature['manufacturing_notes'].append("Small radius fillet - consider tool selection")
                    elif radius > 5:
                        feature['manufacturing_notes'].append("Large radius fillet - check tool clearance")
                    self.features.append(feature)
                except Exception as e:
                    print(f"DEBUG: Error processing fillet: {str(e)}")
                    continue

    def _classify_flat_faces(self):
        """Classify flat vertical faces."""
        if GeomAbs_Plane not in self.face_types:
            return
        for face in self.face_types[GeomAbs_Plane]:
            try:
                if self._is_vertical_face(face):
                    bbox = Bnd_Box()
                    brepbndlib.Add(face, bbox)
                    min_point = bbox.CornerMin()
                    max_point = bbox.CornerMax()
                    width = float(max_point.X() - min_point.X())
                    height = float(max_point.Z() - min_point.Z())
                    feature = {
                        'type': 'flat_face',
                        'width': width,
                        'height': height
                    }
                    self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing flat face: {str(e)}")
                continue

    def _classify_countersinks(self):
        """Classify countersinks (conical faces). TODO: Implement real countersink detection."""
        if GeomAbs_Cone not in self.face_types:
            return
        for face in self.face_types[GeomAbs_Cone]:
            try:
                if not self._is_countersink_face(face):  # TODO: Implement real countersink detection
                    continue
                angle = self._get_cone_angle(face)
                if angle > 0:
                    feature = {
                        'type': 'countersink',
                        'angle': angle
                    }
                    self.features.append(feature)
            except Exception as e:
                print(f"DEBUG: Error processing countersink: {str(e)}")
                continue

    # --- Utility Methods ---
    def _is_vertical_cylinder(self, face):
        """Check if a cylindrical face is vertical."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            axis = surf.Cylinder().Axis().Direction()
            return abs(axis.Z()) > 0.9
        return False

    def _is_horizontal_face(self, face):
        """Check if a face is horizontal."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Plane:
            normal = surf.Plane().Axis().Direction()
            return abs(normal.Z()) > 0.9
        return False

    def _is_vertical_face(self, face):
        """Check if a face is vertical."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Plane:
            normal = surf.Plane().Axis().Direction()
            return abs(normal.Z()) < 0.1
        return False

    def _get_face_edges(self, face):
        """Return all edges of a face."""
        edges = []
        explorer = TopExp_Explorer(face, TopAbs_EDGE)
        while explorer.More():
            edges.append(explorer.Current())
            explorer.Next()
        return edges

    def _is_circular_edge(self, edge):
        """Check if an edge is circular (robust to OCC tuple output)."""
        try:
            curve_tuple = BRep_Tool.Curve(edge)
            if curve_tuple is None or not isinstance(curve_tuple, tuple) or len(curve_tuple) == 0:
                return False
            curve = curve_tuple[0]
            if curve is None:
                return False
            return curve.GetType() == GeomAbs_Circle
        except Exception as e:
            print(f"DEBUG: _is_circular_edge error: {e}")
            return False

    def _is_enclosed(self, face):
        """Check if a face is fully enclosed by walls. TODO: Implement real enclosure check."""
        return True  # TODO: Implement real enclosure check

    def _get_pocket_depth(self, face):
        """Get the depth of a pocket from its top surface."""
        return self._get_face_depth(face)

    def _get_face_depth(self, face):
        """Get the depth (Z span) of a face."""
        bbox = Bnd_Box()
        brepbndlib.Add(face, bbox)
        min_point = bbox.CornerMin()
        max_point = bbox.CornerMax()
        return float(max_point.Z() - min_point.Z())

    def _get_face_diameter(self, face):
        """Get the diameter of a cylindrical face."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            return float(surf.Cylinder().Radius()) * 2
        return 0

    def _get_face_height(self, face):
        """Get the height of a face (Z span)."""
        return self._get_face_depth(face)

    def _is_convex_face(self, face):
        """Check if a face is convex. TODO: Implement real convexity check."""
        return True  # TODO: Implement real convexity check

    def _is_top_face(self, face):
        """Check if a face is on the top of the part. TODO: Implement real top face check."""
        return True  # TODO: Implement real top face check

    def _is_chamfer_face(self, face):
        """Check if a face is a chamfer. TODO: Implement real chamfer detection."""
        return False  # TODO: Implement real chamfer detection

    def _is_fillet_face(self, face):
        """Check if a face is a fillet. TODO: Implement real fillet detection."""
        return False  # TODO: Implement real fillet detection

    def _get_face_radius(self, face):
        """Get the radius of a fillet face."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            return float(surf.Cylinder().Radius())
        return 0

    def _is_countersink_face(self, face):
        """Check if a face is a countersink (conical face)."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cone:
            angle = math.degrees(float(surf.Cone().SemiAngle()))
            return 82 <= angle <= 120
        return False

    def _get_cone_angle(self, face):
        """Get the angle of a conical face."""
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cone:
            return math.degrees(float(surf.Cone().SemiAngle()))
        return 0

    def _post_process_features(self):
        """Placeholder for advanced feature post-processing. TODO: Enhance with more advanced feature matching and confidence scoring."""
        pass 