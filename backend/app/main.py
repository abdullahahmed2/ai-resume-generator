from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os
from .routers import auth, resume, template, ai, share
from .database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables at app startup
load_dotenv()
logger.info("Environment variables loaded from .env file")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(
    title="AI Resume Generator API",
    description="API for generating and managing AI-powered resumes",
    version="1.0.0"
)

# Configure CORS
# Read allowed origins from environment variable, fallback to default list
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000")
origins = allowed_origins.split(",")

logger.info(f"CORS allowed origins: {origins}")

#app.add_middleware(
    #CORSMiddleware,
    #allow_origins=["https://frontend.d2u29wywsqwu0k.amplifyapp.com"],
    #allow_credentials=True,
    #allow_methods=["*"],
    #allow_headers=["*"],
#)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(template.router)
app.include_router(ai.router)
app.include_router(share.router)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the AI Resume Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    # Check if critical environment variables are set
    openai_key = "Set" if os.getenv("OPENAI_API_KEY") else "Not Set"
    
    return {
        "status": "healthy",
        "environment": {
            "OPENAI_API_KEY": openai_key,
            "AI_MODEL": os.getenv("AI_MODEL", "default:gpt-3.5-turbo"),
            "PDF_ENGINE": os.getenv("PDF_ENGINE", "default:pyppeteer")
        }
    }
