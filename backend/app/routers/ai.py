from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from .. import schemas
from ..utils import ai_generator
from ..services import auth
from ..models import User
from app.database import get_db
from app.utils.ai_service import (
    generate_resume_summary, 
    improve_job_descriptions, 
    get_relevant_skills,
    analyze_keywords_from_job
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    responses={401: {"description": "Unauthorized"}},
    dependencies=[Depends(auth.get_current_active_user)]
)


class GenerateSummaryRequest(BaseModel):
    job_title: str
    experience_years: int
    skills: List[str]


class ImproveContentRequest(BaseModel):
    content: str
    content_type: str
    job_title: Optional[str] = None


class GenerateJobDescriptionsRequest(BaseModel):
    job_title: str
    company_name: str
    responsibilities: List[str]
    years_experience: int


class GetRelevantSkillsRequest(BaseModel):
    job_title: str
    industry: Optional[str] = None
    experience_level: str = "mid-level"


class SummaryRequest(BaseModel):
    job_title: str
    experience_years: int = 3
    skills: List[str] = []


class SummaryResponse(BaseModel):
    content: str


class JobDescriptionRequest(BaseModel):
    job_title: str
    company_name: str
    responsibilities: List[str]
    years_experience: int = 1


class JobDescriptionResponse(BaseModel):
    descriptions: List[str]


class SkillsRequest(BaseModel):
    job_title: str
    experience_level: str = "mid-level"  # junior, mid-level, senior


class SkillsResponse(BaseModel):
    skills: List[str]


class JobDescriptionAnalysisRequest(BaseModel):
    job_description: str
    resume_content: Dict[str, Any] = None


class JobDescriptionAnalysisResponse(BaseModel):
    keywords: List[str]
    missing_skills: List[str]
    suggestions: Dict[str, Any]


@router.post("/generate-summary", response_model=SummaryResponse)
async def create_resume_summary(
    request: SummaryRequest,
    current_user: User = Depends(auth.get_current_active_user),
):
    """
    Generate a professional summary for a resume based on job title and skills.
    """
    try:
        summary = generate_resume_summary(
            job_title=request.job_title,
            experience_years=request.experience_years,
            skills=request.skills
        )
        return {"content": summary}
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate summary. Please try again later."
        )


@router.post("/improve-content", response_model=schemas.GeneratedContent)
async def improve_content(
    request: ImproveContentRequest,
    current_user: User = Depends(auth.get_current_active_user)
):
    """Improve existing content to make it more professional and impactful."""
    try:
        improved_content = ai_generator.improve_content(
            content=request.content,
            content_type=request.content_type,
            job_title=request.job_title
        )
        return schemas.GeneratedContent(content=improved_content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to improve content: {str(e)}"
        )


@router.post("/generate-job-descriptions", response_model=JobDescriptionResponse)
async def optimize_job_descriptions(
    request: JobDescriptionRequest,
    current_user: User = Depends(auth.get_current_active_user),
):
    """
    Optimize and improve job descriptions for better impact and ATS compatibility.
    """
    try:
        improved_descriptions = improve_job_descriptions(
            job_title=request.job_title,
            company_name=request.company_name,
            responsibilities=request.responsibilities,
            years_experience=request.years_experience
        )
        return {"descriptions": improved_descriptions}
    except Exception as e:
        logger.error(f"Error improving job descriptions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to improve job descriptions. Please try again later."
        )


@router.post("/get-relevant-skills", response_model=SkillsResponse)
async def suggest_relevant_skills(
    request: SkillsRequest,
    current_user: User = Depends(auth.get_current_active_user),
):
    """
    Suggest relevant skills for a specific job title and experience level.
    """
    try:
        skills = get_relevant_skills(
            job_title=request.job_title,
            experience_level=request.experience_level
        )
        return {"skills": skills}
    except Exception as e:
        logger.error(f"Error generating skills: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate skills. Please try again later."
        )


@router.post("/analyze-job-description", response_model=JobDescriptionAnalysisResponse)
async def analyze_job_description(
    request: JobDescriptionAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    """
    Analyze a job description to extract keywords and provide suggestions.
    """
    try:
        results = analyze_keywords_from_job(
            job_description=request.job_description,
            resume_content=request.resume_content
        )
        
        # Store the analysis results if needed
        # This could be done in a background task if it's a heavy operation
        # background_tasks.add_task(store_analysis_results, db=db, user_id=current_user.id, results=results)
        
        return results
    except Exception as e:
        logger.error(f"Error analyzing job description: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze job description. Please try again later."
        )


@router.post("/suggest-improvements", response_model=Dict[str, Any])
async def suggest_improvements(
    resume_content: Dict[str, Any] = Body(...),
    current_user: User = Depends(auth.get_current_active_user)
):
    """Analyze a resume and suggest improvements for various sections."""
    try:
        suggestions = ai_generator.suggest_resume_improvements(resume_content)
        return suggestions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate improvement suggestions: {str(e)}"
        ) 