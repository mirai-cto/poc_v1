import os
import uuid
import traceback
from typing import Tuple, Dict, Any
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.analyzer.cad_analyzer import CADAnalyzer

# Create blueprint
main = Blueprint('main', __name__)

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def handle_file_upload() -> Tuple[Dict[str, Any], int]:
    """Handle file upload and processing."""
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    if not file or not allowed_file(file.filename):
        return {'error': 'Invalid file type'}, 400
    
    try:
        # Save STEP file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        step_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{file_id}.step')
        stl_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{file_id}.stl')
        
        file.save(step_path)
        
        # Process file
        analyzer = CADAnalyzer(
            step_path,
            tolerance=current_app.config['FEATURE_TOLERANCE'],
            mesh_deflection=current_app.config['MESH_DEFLECTION']
        )
        
        # Get analysis results
        bounding_box = analyzer.get_bounding_box()
        features, analysis = analyzer.detect_features()
        
        # Export STL
        analyzer.export_stl(stl_path)
        
        return {
            'success': True,
            'filename': filename,
            'bounding_box': bounding_box,
            'features': features,
            'analysis': analysis,
            'mesh_url': f'/mesh/{file_id}.stl'
        }, 200
        
    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Error processing file: {error_msg}")
        current_app.logger.error(traceback.format_exc())
        
        # Clean up files on error
        for path in [step_path, stl_path]:
            if path and os.path.exists(path):
                os.remove(path)
        
        return {'error': error_msg}, 500

@main.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload requests."""
    return handle_file_upload()

@main.route('/mesh/<filename>')
def serve_mesh(filename):
    """Serve STL files."""
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        current_app.logger.error(f"Error serving mesh file {filename}: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return {'error': 'Failed to serve mesh file'}, 500 