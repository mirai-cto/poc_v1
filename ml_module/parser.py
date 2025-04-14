#!/usr/bin/env python3
"""
Mock STEP file parser for the CNC Tool Recommender.

This script simulates parsing a STEP file by returning predefined geometric features.
In a real implementation, this would use a library like PythonOCC or FreeCAD API.
"""

import os
import json
import logging
import uuid
from typing import Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_cad.json')


class StepParser:
    """
    Mock implementation of a STEP file parser.
    """
    
    def __init__(self, sample_data_path: str = SAMPLE_DATA_PATH):
        """
        Initialize the parser with sample data path.
        
        Args:
            sample_data_path: Path to the sample CAD data JSON file
        """
        self.sample_data_path = sample_data_path
        
    def parse(self, file_path: str) -> Dict:
        """
        Mock parse a STEP file and return predefined features.
        
        Args:
            file_path: Path to the STEP file to parse
            
        Returns:
            Dictionary containing extracted geometric features
        """
        logger.info(f"Simulating parsing of file: {file_path}")
        
        # In a real implementation, this would use a CAD parsing library
        # to extract geometric features from the STEP file

        # Check if file exists and has .stp or .step extension
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in ['.stp', '.step']:
            logger.warning(f"File may not be a STEP file. Extension: {file_ext}")
            
        # Load mock data from sample file
        try:
            if os.path.exists(self.sample_data_path):
                with open(self.sample_data_path, 'r') as f:
                    mock_data = json.load(f)
                    logger.info(f"Loaded mock data from {self.sample_data_path}")
                    return mock_data
            else:
                # If sample file doesn't exist, return hardcoded mock data
                logger.warning(f"Sample data file not found: {self.sample_data_path}")
                logger.info("Using hardcoded mock data")
                return self._generate_mock_data()
                
        except Exception as e:
            logger.error(f"Error loading mock data: {str(e)}")
            return self._generate_mock_data()
            
    def _generate_mock_data(self) -> Dict:
        """
        Generate hardcoded mock geometric features.
        
        Returns:
            Dictionary containing mock features
        """
        return {
            "features": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Hole_1",
                    "type": "hole",
                    "x": 10.0,
                    "y": 20.0,
                    "z": 0.0,
                    "diameter": 8.5,
                    "depth": 15.0
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Slot_1",
                    "type": "slot",
                    "x": 50.0,
                    "y": 30.0,
                    "z": 0.0,
                    "width": 12.0,
                    "length": 40.0,
                    "depth": 8.0
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Pocket_1",
                    "type": "pocket",
                    "x": 100.0,
                    "y": 80.0,
                    "z": 0.0,
                    "width": 50.0,
                    "length": 60.0,
                    "depth": 25.0,
                    "corner_radius": 5.0
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Chamfer_1",
                    "type": "chamfer",
                    "x": 150.0,
                    "y": 150.0,
                    "z": 0.0,
                    "length": 30.0,
                    "angle": 45.0
                }
            ],
            "metadata": {
                "units": "mm",
                "source_file": "mock_data.step",
                "parsed_at": "2023-07-15T12:00:00Z"
            }
        }


# Function to be used by API directly
def parse_step_file(file_path: str) -> Dict:
    """
    Parse a STEP file and extract geometric features.
    
    Args:
        file_path: Path to the STEP file
        
    Returns:
        Dictionary containing extracted features
    """
    parser = StepParser()
    return parser.parse(file_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "sample.step"  # Example file
        
    result = parse_step_file(file_path)
    print(json.dumps(result, indent=2)) 