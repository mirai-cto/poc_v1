#!/usr/bin/env python3
"""
Flask API for the CNC Tool Recommender ML module.

This API provides endpoints for:
1. Parsing STEP files to extract geometric features
2. Classifying geometric features
"""

import os
import json
import logging
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from parser import parse_step_file
from classifier import classify_features

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure upload settings
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'cnc_uploads')
ALLOWED_EXTENSIONS = {'stp', 'step'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'ml_module'})


@app.route('/api/parse', methods=['POST'])
def parse_cad():
    """
    Parse a STEP file to extract geometric features.
    
    Expects a file upload with key 'file'.
    """
    # Check if file was included in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"File saved at {file_path}")
        
        # Parse the file
        result = parse_step_file(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error parsing file: {str(e)}")
        return jsonify({'error': f'Error parsing file: {str(e)}'}), 500


@app.route('/api/classify', methods=['POST'])
def classify_cad_features():
    """
    Classify geometric features from parsed CAD data.
    
    Expects a JSON payload with features data.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'Invalid input: no features found in payload'}), 400
            
        # Classify features
        result = classify_features(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error classifying features: {str(e)}")
        return jsonify({'error': f'Error classifying features: {str(e)}'}), 500


@app.route('/api/process', methods=['POST'])
def process_cad_file():
    """
    Combined endpoint to parse a STEP file and classify its features.
    
    Expects a file upload with key 'file'.
    """
    # Check if file was included in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"File saved at {file_path}")
        
        # Parse the file
        parsed_data = parse_step_file(file_path)
        
        # Classify features
        result = classify_features(parsed_data)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


if __name__ == '__main__':
    # Use the environment variable for the port, defaulting to 5050 if not set
    port = int(os.environ.get('FLASK_PORT', 5050))
    
    # Run app
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development') 