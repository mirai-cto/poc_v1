# Frontend Module

This module contains the React frontend for the CNC Tool Recommender system.

## Architecture

The frontend is built using:
- React (UI library)
- Vite (Build tool)
- React Router (Routing)
- React Query (Data fetching)
- Styled Components (Styling)
- Axios (HTTP client)

## Key Components

The frontend is organized into the following directories:

- `components/`: Reusable UI components
- `pages/`: Page components that correspond to routes
- `services/`: API service functions
- `hooks/`: Custom React hooks
- `context/`: React context providers

## Features

- CAD file upload with drag-and-drop functionality
- Machine selection
- Feature visualization
- Tool recommendations display
- Wear score input
- Feedback submission
- Responsive design

## Setup Instructions

### Prerequisites

- Node.js 16 or higher
- npm 7 or higher

### With Docker (Recommended)

```bash
# From project root
docker-compose up -d frontend
```

### Manual Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

### Environment Variables

Create a `.env` file with the following variables:

```
VITE_API_URL=http://localhost:8080
```

## Development Guide

### Adding a New Page

1. Create a new page component in the `pages` directory
2. Add a route in `src/App.jsx`
3. Link to the page from the appropriate components

### Adding a New Component

1. Create a new component in the `components` directory
2. Define props and types
3. Style the component using styled-components
4. Add tests for the component

### Implementing API Calls

1. Add a new service function in the `services` directory
2. Use React Query hooks for data fetching
3. Handle loading, error, and success states

## Testing

Run tests with:

```bash
npm test
```

## Building for Production

```bash
npm run build
```

This creates optimized production files in the `dist` directory. 