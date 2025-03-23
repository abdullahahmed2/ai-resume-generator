# AI Resume Generator Frontend

This is the frontend for the AI Resume Generator application, built with React.

## Features

- User Authentication (Login/Register)
- Dashboard for Managing Resumes
- Resume Editor with AI-Powered Content Suggestions
- Multiple Resume Templates
- PDF Export
- Resume Sharing

## Setup and Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Set environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   REACT_APP_API_URL=http://localhost:8000  # URL of your backend
   ```

3. Run the development server:
   ```
   npm start
   ```

The app will be available at http://localhost:3000.

## Project Structure

- `src/components/`: Reusable UI components
- `src/pages/`: Page components for different routes
- `src/context/`: React Context for state management (Auth, etc.)
- `src/services/`: API services for backend communication
- `src/styles/`: CSS styles

## Building for Production

```
npm run build
```

This will create a production-ready build in the `build` folder that can be deployed to any static hosting service. 