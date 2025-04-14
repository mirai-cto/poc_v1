# CNC Tool Recommender - System Architecture

This document outlines the architecture of the CNC Tool Recommender and Speed & Feed Recommendation System.

## System Overview

The system is a full-stack application that recommends optimal CNC cutting tools and machining parameters based on CAD models, machine specifications, and tool wear data. It consists of the following components:

1. **Frontend**: React-based user interface for file uploads, machine selection, and displaying recommendations
2. **Backend**: Spring Boot API server that handles business logic and database access
3. **ML Module**: Python service for CAD file parsing and feature classification
4. **Database**: PostgreSQL for storing tools, machines, and recommendation history
5. **LLM Integration**: OpenAI API integration for advanced recommendations

## Component Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│    Frontend     │◄────────►     Backend     │◄────────►    Database     │
│   (React/Vite)  │         │  (Spring Boot)  │         │  (PostgreSQL)   │
│                 │         │                 │         │                 │
└─────────────────┘         └────────┬────────┘         └─────────────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                            │    ML Module    │
                            │    (Python)     │
                            │                 │
                            └────────┬────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                            │    OpenAI API   │
                            │                 │
                            └─────────────────┘
```

## Data Flow

1. User uploads a CAD file (STEP format) via the frontend
2. Frontend sends the file to the backend
3. Backend forwards the file to the ML module for parsing
4. ML module extracts geometric features and returns them to the backend
5. Backend queries the database for available machines and tools
6. User selects a machine from the dropdown
7. Backend filters tools based on machine constraints and feature requirements
8. Backend prepares a prompt for OpenAI with the filtered tools and features
9. OpenAI returns tool recommendations with explanations
10. Backend stores the recommendations in the database
11. Frontend displays the recommendations to the user
12. User provides wear scores for selected tools
13. Backend adjusts speed/feed parameters based on wear scores
14. After job completion, user provides feedback
15. Feedback is stored in the database for future improvements

## Component Details

### Frontend (React/Vite)

- **Purpose**: Provide user interface for file uploading, machine selection, and displaying recommendations
- **Key Components**:
  - File Upload: Allows users to upload STEP files
  - Machine Selector: Dropdown for selecting a CNC machine
  - Feature Viewer: Displays extracted geometric features
  - Recommendation Display: Shows recommended tools with explanations
  - Wear Score Input: Allows users to provide tool wear scores
  - Feedback Form: Allows users to provide post-job feedback

### Backend (Spring Boot)

- **Purpose**: Handle business logic, database access, and integration with external services
- **Key Components**:
  - File Upload Controller: Handles file uploads and forwards to ML module
  - Machine Controller: Provides machine data from the database
  - Tool Controller: Manages tool data and filtering
  - Recommendation Service: Integrates with OpenAI and adjusts parameters
  - Feedback Service: Processes and stores user feedback

### ML Module (Python/Flask)

- **Purpose**: Parse CAD files and classify geometric features
- **Key Components**:
  - CAD Parser: Extracts geometric features from STEP files
  - Feature Classifier: Identifies feature types (holes, slots, pockets, etc.)
  - Flask API: Provides endpoints for parsing and classification

### Database (PostgreSQL)

- **Purpose**: Store persistent data about tools, machines, and recommendations
- **Key Tables**:
  - Tools: Information about cutting tools
  - Machines: Information about CNC machines
  - CAD Files: Metadata about uploaded files
  - Features: Extracted geometric features
  - Recommendations: Tool recommendations with parameters
  - Feedback: User feedback on tool performance

### LLM Integration (OpenAI API)

- **Purpose**: Provide advanced tool recommendations based on geometric features
- **Key Features**:
  - Tool Selection: Recommend tools for different operations
  - Parameter Optimization: Suggest optimal speed and feed rates
  - Explanations: Provide rationale for recommendations

## Current Implementation Status

The current implementation is a proof of concept with the following limitations:

- CAD parsing is mocked using hardcoded sample data
- OpenAI integration is simulated with static responses
- Speed/feed calculations use simplified formulas
- Classification uses rule-based logic instead of ML

## Future Enhancements

Planned improvements for future versions:

1. Implement actual STEP file parsing using a CAD library
2. Replace rule-based classification with a trained ML model
3. Implement a real integration with OpenAI API
4. Add CAD visualization in the frontend
5. Enhance speed/feed calculations with more sophisticated formulas
6. Implement a learning system that improves recommendations based on feedback
7. Add support for more complex machining operations
8. Implement user authentication and project management 