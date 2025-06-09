# CAD Feature Analyzer

A web-based CAD file analyzer that processes STEP files, detects features, and provides manufacturing insights. Built with Python, Flask, and Three.js.

## Features

- STEP file processing and analysis
- 3D model visualization
- Feature detection (holes, planar faces, chamfers)
- Manufacturing insights and quality checks
- Duplicate feature detection
- Interactive 3D viewer with orbit controls

## Prerequisites

- Python 3.9 or higher
- Conda (Miniconda or Anaconda)
- A modern web browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cad-analyzer
```

2. Create and activate a conda environment:
```bash
# Create environment with Python 3.9
conda create -n cad_analyzer python=3.9 -y
conda activate cad_analyzer

# Install pythonocc-core via conda
conda install -c conda-forge pythonocc-core -y

# Install other dependencies via pip
pip install -r requirements.txt
```

## Project Structure

```
cad-analyzer/
├── app/
│   ├── __init__.py
│   ├── analyzer/
│   │   ├── __init__.py
│   │   └── cad_analyzer.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       └── index.html
├── uploads/
├── config.py
├── requirements.txt
└── run.py
```

## Usage

1. Activate the conda environment:
```bash
conda activate cad_analyzer
```

2. Start the Flask server:
```bash
python app.py
```

<!-- /Users/nmitra28/miniconda3/envs/cad_analyzer/bin/python app.py -->

3. Open your web browser and navigate to:
```
http://localhost:5000
```

4. Upload a STEP file (.step or .stp) using the interface

5. View the 3D model and analysis results

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Write unit tests for new features

### Adding New Features

1. Create a new branch
2. Implement the feature
3. Add tests
4. Submit a pull request

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File processing errors
- Feature detection issues
- STL export problems

## Performance Considerations

- Large files (>50MB) may take longer to process
- The application uses incremental mesh generation for better performance
- Feature detection includes duplicate removal to reduce processing time

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'OCC'**
   - Ensure you're using the conda environment
   - Verify pythonocc-core is installed via conda:
     ```bash
     conda list pythonocc-core
     ```

2. **STEP File Processing Errors**
   - Check if the STEP file is valid and not corrupted
   - Ensure the file is in a supported STEP format (AP203 or AP214)

3. **3D Viewer Issues**
   - Check browser console for JavaScript errors
   - Verify that the STL file is being generated and served correctly
   - Try using a different browser if issues persist

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Features
- Upload STEP files
- Detects holes, planar faces, and chamfers
- 3D viewer with feature markers (three.js)
- Backup: Tabular feature list if 3D viewer fails
- Download STL mesh

## Setup Instructions

### 1. Environment Setup
- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if not already installed.
- Create and activate the environment:
  ```bash
  conda create -n cad_analyzer python=3.9 -y
  conda activate cad_analyzer
  ```
- Install OpenCascade Python bindings:
  ```bash
  conda install -c conda-forge pythonocc-core -y
  ```
- Install other dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Run the Application
```bash
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### 3. Troubleshooting
- If you see `**** ERR StepFile : Incorrect Syntax : Fails Count : 1 ****`, your STEP file may be malformed.
- If the 3D viewer is blank:
  - Check browser console for errors
  - Check that STL is being served (see Network tab)
  - Use the tabular feature list as a backup
- If you see import errors for OCC modules, ensure you are using the conda environment and have installed `pythonocc-core` via conda.

### 4. Clean Up
- Uploaded files are stored in the `uploads/` directory and are deleted after processing.

## Code Structure
- `app.py`: Flask backend, feature detection, STL export
- `templates/index.html`: Frontend UI, 3D viewer, feature table
- `requirements.txt`: Python dependencies

## Backup: Tabular Feature List
If the 3D viewer does not work, detected features will always be shown in a table below the upload area, including type, details, confidence, and centroid coordinates.

---

## Comments & Code Cleanliness
- The code is commented for clarity.
- Deprecated function usage is avoided; static methods are used for OCC operations.
- All imports are explicit and correct for pythonocc-core 7.7+. 