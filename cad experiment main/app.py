import os
import uuid
import traceback
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from cad_analyzer import CADAnalyzer
from cad_classifier import CADClassifier
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

# Get absolute path to the uploads directory
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
print(f"Upload folder path: {UPLOAD_FOLDER}")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['DEBUG'] = True  # Enable debug mode

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print(f"Upload directory exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
print(f"Upload directory contents: {os.listdir(app.config['UPLOAD_FOLDER'])}")

ALLOWED_EXTENSIONS = {'step', 'stp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    print("Serving index page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("\n=== Starting file upload process ===")
    step_path = None
    stl_path = None
    
    try:
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        print(f"Received file: {file.filename}")
        
        if file.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if not file and not allowed_file(file.filename):
            print(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        step_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file_id}.step')
        stl_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file_id}.stl')
        
        print(f"Saving file to {step_path}")
        file.save(step_path)
        print(f"STEP file exists after save: {os.path.exists(step_path)}")
        print(f"STEP file size: {os.path.getsize(step_path)} bytes")
        
        try:
            print(f"Attempting to analyze STEP file: {filename}")
            analyzer = CADAnalyzer(step_path)
            print("Successfully created analyzer")
            
            bounding_box = analyzer.get_bounding_box()
            print(f"Got bounding box: {bounding_box}")
            
            features, analysis = analyzer.detect_features()
            print(f"Detected {len(features)} features after post-processing")
            
            print(f"Exporting STL to {stl_path}")
            analyzer.export_stl(stl_path)
            print(f"STL file exists after export: {os.path.exists(stl_path)}")
            print(f"STL file size: {os.path.getsize(stl_path)} bytes")
            
            response_data = {
                'success': True,
                'filename': filename,
                'bounding_box': bounding_box,
                'features': features,
                'analysis': analysis,
                'mesh_url': f'/mesh/{file_id}.stl'
            }
            print(f"Sending response: {response_data}")
            return jsonify(response_data)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error processing file: {error_msg}")
            print("Traceback:")
            print(traceback.format_exc())
            # Clean up files on error
            if step_path and os.path.exists(step_path):
                print(f"Cleaning up STEP file due to error: {step_path}")
                os.remove(step_path)
            if stl_path and os.path.exists(stl_path):
                print(f"Cleaning up STL file due to error: {stl_path}")
                os.remove(stl_path)
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        print(f"Unexpected error in upload_file: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        # Clean up files on error
        if step_path and os.path.exists(step_path):
            print(f"Cleaning up STEP file due to error: {step_path}")
            os.remove(step_path)
        if stl_path and os.path.exists(stl_path):
            print(f"Cleaning up STL file due to error: {stl_path}")
            os.remove(stl_path)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/mesh/<filename>')
def serve_mesh(filename):
    try:
        print(f"Serving mesh file: {filename}")
        print(f"Looking for file in: {app.config['UPLOAD_FOLDER']}")
        print(f"Directory contents: {os.listdir(app.config['UPLOAD_FOLDER'])}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Full file path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"File size: {os.path.getsize(file_path)} bytes")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving mesh file {filename}: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({'error': 'Failed to serve mesh file'}), 500

@app.route('/classify', methods=['POST'])
def classify_features():
    try:
        # Get the most recently uploaded file
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        step_files = [f for f in files if f.endswith(('.step', '.stp'))]
        
        if not step_files:
            return jsonify({'error': 'No STEP file found'}), 400
            
        # Sort by modification time and get the most recent
        latest_file = max(step_files, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)
        
        # Initialize classifier
        classifier = CADClassifier(file_path)
        
        # Classify features
        features = classifier.classify_features()
        
        return jsonify({
            'features': features
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Flask app with upload folder: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True, port=5000) 