# ML Module

This module contains the machine learning components of the CNC Tool Recommender system.

## Components

- `parser.py`: Parses CAD files (STEP format) and extracts geometric features
- `classifier.py`: Classifies geometric features (hole, slot, pocket, etc.)
- `app.py`: Flask API server that wraps the ML functionality
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container definition for the ML service

## API Endpoints

### CAD File Parsing

```
POST /api/parse
Content-Type: multipart/form-data
Body: file=<CAD file in STEP format>

Response:
{
  "features": [
    {
      "id": "1",
      "type": "hole",
      "x": 10.5,
      "y": 20.3,
      "z": 0,
      "diameter": 5.0,
      "depth": 10.0
    },
    ...
  ]
}
```

### Feature Classification

```
POST /api/classify
Content-Type: application/json
Body: {
  "features": [
    {
      "id": "1",
      "x": 10.5,
      "y": 20.3,
      "z": 0,
      "diameter": 5.0,
      "depth": 10.0
    },
    ...
  ]
}

Response:
{
  "features": [
    {
      "id": "1",
      "type": "hole",
      "confidence": 0.95,
      "x": 10.5,
      "y": 20.3,
      "z": 0,
      "diameter": 5.0,
      "depth": 10.0
    },
    ...
  ]
}
```

## Current Implementation

This is currently a mock implementation:

- The STEP parser returns predefined features from `sample_cad.json`
- The classifier assigns types based on simple rules rather than ML

## Setup Instructions

### With Docker (Recommended)

```bash
# From project root
docker-compose up -d ml_module
```

### Manual Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python app.py
   ```

## Extending the ML Module

### Implementing a Real STEP Parser

To replace the mock parser with a real one:

1. Update `parser.py` with an actual STEP file parser, keeping the same output format
2. Libraries to consider:
   - PythonOCC
   - FreeCAD Python API
   - Open CASCADE

### Implementing a Real Classifier

To replace the mock classifier with a real ML-based one:

1. Collect training data of CAD features with labels
2. Train a model (e.g., RandomForest, CNN)
3. Update `classifier.py` to use the trained model
4. Ensure outputs maintain the same format 