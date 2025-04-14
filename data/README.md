# Data Module

This module contains sample data and mocked responses for the CNC Tool Recommender system.

## Contents

- `tools.csv`: Sample tool data (copy of `nmitra28/tool_ds_v1.csv`)
- `machines.csv`: Sample machine data (copy of `nmitra28/cleaned_machines.csv`)
- `sample_cad.json`: Mocked output from CAD file parser
- `tool_selector_prompt.json`: Sample prompt sent to OpenAI API
- `tool_selector_response.json`: Sample response from OpenAI API

## Data Files Description

### tools.csv

Contains data about cutting tools with attributes such as:
- ID
- Name
- Type
- Material
- Dimensions (diameter, length, etc.)
- Operational parameters (max RPM, max depth of cut, etc.)

### machines.csv

Contains data about CNC machines with attributes such as:
- ID
- Name
- Manufacturer
- Model
- Specifications (max RPM, power, etc.)
- Limits (max feed rate, max tool diameter, etc.)

### sample_cad.json

Simulates the output from parsing a STEP file, containing:
- List of geometric features with dimensional data
- Metadata about the CAD file

### tool_selector_prompt.json

Example of the prompt structure sent to OpenAI API, containing:
- System message defining the AI's role
- User message with part data, machine constraints, and available tools

### tool_selector_response.json

Mocked response from the OpenAI API, containing:
- Recommendations for tools by operation type (roughing, finishing, drilling)
- Speed and feed parameters
- Explanations for each recommendation

## Usage

These files are used by various parts of the system:

1. `tools.csv` and `machines.csv` are loaded into the PostgreSQL database during initialization
2. `sample_cad.json` is used by the ML module to simulate parsing a STEP file
3. `tool_selector_prompt.json` and `tool_selector_response.json` are used to mock LLM API calls

## Extending the Data

### Adding New Tool Data

To add new tool data:
1. Add new rows to `tools.csv` following the same schema
2. Re-run the database seeder to load the updated data

### Adding New Machine Data

To add new machine data:
1. Add new rows to `machines.csv` following the same schema
2. Re-run the database seeder to load the updated data

### Creating New Sample CAD Files

To create new sample CAD outputs:
1. Create a new JSON file with the same structure as `sample_cad.json`
2. Update the parser to use the new file

### Updating LLM Prompts

To update the LLM interaction:
1. Modify `tool_selector_prompt.json` to change the input format
2. Update `tool_selector_response.json` to match the expected output format
3. Update the relevant backend service to handle the new format 