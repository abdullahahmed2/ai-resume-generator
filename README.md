# AI Resume Generator

An AI-powered resume generator application that helps users create professional, ATS-friendly resumes. The system provides user authentication, AI content suggestions, multiple resume templates, version control, and sharing features.

## Project Structure

The project is divided into two main parts:

- **Backend**: FastAPI application with SQLAlchemy ORM for database operations
- **Frontend**: React application with modern UI and state management

## Features

- 🔒 **User Authentication**: Secure registration and login with JWT tokens
- 📝 **Resume Creation and Editing**: Create and manage multiple resumes
- 🤖 **AI-Powered Content Suggestions**: Get professional content suggestions powered by OpenAI
- 🎨 **Multiple Templates**: Choose from various modern, ATS-friendly templates
- 📄 **PDF Export**: Export resumes as professionally formatted PDFs using Pyppeteer
- 📚 **Version Control**: Maintain multiple versions of each resume
- 🔗 **Sharing**: Generate shareable links for your resumes

## Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables (optional):
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export DATABASE_URL=your_database_url  # Default is SQLite
   ```

5. First-time Pyppeteer setup (installs Chromium):
   ```
   python setup_pyppeteer.py
   ```

6. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000.

### Troubleshooting Chromium Installation

If you encounter issues with Chromium installation:

- On macOS, you might need to install additional dependencies:
  ```
  brew install chromium
  ```

- On Linux, you might need to install the following packages:
  ```
  sudo apt-get install chromium-browser libatk-bridge2.0-0 libgtk-3-0
  ```

- To use a specific Chromium/Chrome executable, set the environment variable:
  ```
  export PYPPETEER_CHROMIUM_EXECUTABLE=/path/to/chromium
  ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file with:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```
   npm start
   ```

The frontend will be available at http://localhost:3000.

## API Documentation

Once the backend is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Technologies Used

- **Backend**:
  - FastAPI: Modern, fast web framework for building APIs
  - SQLAlchemy: SQL toolkit and ORM
  - Pydantic: Data validation and settings management
  - JWT: Authentication using JSON Web Tokens
  - OpenAI: AI-powered content generation
  - Pyppeteer: Headless Chrome/Chromium for PDF generation

- **Frontend**:
  - React: Frontend library for building user interfaces
  - React Router: Declarative routing for React
  - Axios: Promise-based HTTP client
  - CSS: Modern styling with responsive design

## License

This project is licensed under the MIT License.

## Environment Configuration

This project uses environment variables for secure configuration. These should be stored in `.env` files and never committed to version control.

### Backend Configuration

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Copy the example environment file:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file to add your OpenAI API key and other settings:
   ```
   # Open the file in your preferred editor
   nano .env
   ```

### Frontend Configuration

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Copy the example environment file:
   ```
   cp .env.example .env
   ```

3. Update the `.env` file if your backend runs on a different address:
   ```
   # Open the file in your preferred editor
   nano .env
   ```

### Available Environment Variables

#### Backend Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for AI features
- `AI_MODEL`: The AI model to use (default: "gpt-3.5-turbo")
- `AI_PROVIDER`: The AI provider (default: "openai")
- `AI_API_ENDPOINT`: The API endpoint for the AI provider
- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `DEBUG`: Debug mode (True/False)
- `PDF_ENGINE`: PDF generation engine (pyppeteer or weasyprint)

#### Frontend Environment Variables

- `REACT_APP_API_URL`: URL of the backend API (default: http://localhost:8000)
- `REACT_APP_ENABLE_AI_FEATURES`: Enable/disable AI features in the UI

### Security Considerations

- Never commit `.env` files to version control
- Generate strong random keys for `SECRET_KEY` and other sensitive configurations
- Rotate API keys periodically
- In production, use environment variables provided by your hosting platform instead of `.env` files 