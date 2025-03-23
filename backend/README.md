# AI Resume Generator Backend

This is the backend API for the AI Resume Generator application, built with FastAPI and SQLAlchemy.

## Features

- User Authentication with JWT
- Resume Creation and Management
- Multiple Resume Versions
- AI-Powered Content Suggestions (via OpenAI)
- Resume Templates
- PDF Export (via Pyppeteer)
- Resume Sharing

## Setup and Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export DATABASE_URL=your_database_url  # Default is SQLite
   ```

4. First-time Pyppeteer setup (installs Chromium):
   ```
   python setup_pyppeteer.py
   ```

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000.

## API Documentation

Once the application is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Project Structure

- `app/main.py`: Main application entry point
- `app/database.py`: Database connection and session management
- `app/models.py`: SQLAlchemy ORM models
- `app/schemas.py`: Pydantic schemas for request/response validation
- `app/routers/`: API route handlers
- `app/services/`: Business logic and service functions
- `app/utils/`: Utility functions (PDF generation with Pyppeteer, etc.)

## Troubleshooting

### Chromium Installation Issues

If you encounter issues with Chromium installation:

1. On macOS, you might need to install additional dependencies:
   ```
   brew install chromium
   ```

2. On Linux, you might need to install the following packages:
   ```
   sudo apt-get install chromium-browser libatk-bridge2.0-0 libgtk-3-0
   ```

3. To use a specific Chromium/Chrome executable, set the environment variable:
   ```
   export PYPPETEER_CHROMIUM_EXECUTABLE=/path/to/chromium
   ``` 