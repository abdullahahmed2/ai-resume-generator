import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import auth, resume
from ..utils import pdf, pdf_parser
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/create", response_model=schemas.Resume)
def create_resume(
    resume_data: schemas.ResumeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Create a new resume."""
    return resume.create_resume(db=db, resume=resume_data, user_id=current_user.id)


@router.post("/create_with_content", response_model=schemas.ResumeDetail)
def create_resume_with_content(
    resume_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Create a new resume with content in one call."""
    try:
        # Create the base resume
        resume_create = schemas.ResumeCreate(
            title=resume_data.get("title", "My Resume"),
            current_template_id=resume_data.get("current_template_id")
        )
        
        db_resume = resume.create_resume(db=db, resume=resume_create, user_id=current_user.id)
        
        # If we have content, create the first version
        if "content" in resume_data:
            version_data = schemas.ResumeVersionCreate(
                resume_id=db_resume.id,
                version_number=1,
                description="Initial version",
                content=resume_data["content"]
            )
            
            db_version = resume.create_resume_version(db=db, version=version_data)
            
            # Create a ResumeDetail object with the version
            resume_detail = schemas.ResumeDetail(
                id=db_resume.id,
                title=db_resume.title,
                user_id=db_resume.user_id,
                current_template_id=db_resume.current_template_id,
                created_at=db_resume.created_at,
                updated_at=db_resume.updated_at,
                versions=[db_version]
            )
            
            return resume_detail
        
        # If no content, return just the resume
        return schemas.ResumeDetail(
            id=db_resume.id,
            title=db_resume.title,
            user_id=db_resume.user_id,
            current_template_id=db_resume.current_template_id,
            created_at=db_resume.created_at,
            updated_at=db_resume.updated_at,
            versions=[]
        )
    except Exception as e:
        logger.error(f"Error creating resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create resume: {str(e)}"
        )


@router.get("/list", response_model=List[schemas.Resume])
def read_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get all resumes for the current user."""
    resumes = resume.get_resumes(db, user_id=current_user.id, skip=skip, limit=limit)
    return resumes


@router.get("/{resume_id}", response_model=schemas.ResumeDetail)
def read_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get a specific resume by ID."""
    db_resume = resume.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get the resume versions
    versions = resume.get_resume_versions(db, resume_id=resume_id)
    
    # Create a ResumeDetail object
    resume_detail = schemas.ResumeDetail(
        id=db_resume.id,
        title=db_resume.title,
        user_id=db_resume.user_id,
        current_template_id=db_resume.current_template_id,
        created_at=db_resume.created_at,
        updated_at=db_resume.updated_at,
        versions=versions
    )
    
    return resume_detail


@router.put("/{resume_id}", response_model=schemas.Resume)
def update_resume(
    resume_id: int,
    resume_data: schemas.ResumeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Update a resume."""
    db_resume = resume.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return resume.update_resume(db, resume_id=resume_id, resume_update=resume_data, user_id=current_user.id)


@router.delete("/{resume_id}", response_model=bool)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Delete a resume."""
    db_resume = resume.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    result = resume.delete_resume(db, resume_id=resume_id, user_id=current_user.id)
    return result


@router.post("/version/create", response_model=schemas.ResumeVersion)
def create_version(
    version_data: schemas.ResumeVersionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Create a new version of a resume."""
    # Check if the resume exists and belongs to the user
    db_resume = resume.get_resume(db, resume_id=version_data.resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Create the version
    db_version = resume.create_resume_version(db, version=version_data)
    
    # Parse the content JSON for the response
    if isinstance(db_version.content, str):
        try:
            content_dict = json.loads(db_version.content)
            db_version.content = content_dict
        except json.JSONDecodeError:
            pass
    
    return db_version


@router.get("/version/{version_id}", response_model=schemas.ResumeVersion)
def read_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get a specific version of a resume."""
    # Get the version
    db_version = resume.get_resume_version(db, version_id=version_id)
    if db_version is None:
        raise HTTPException(status_code=404, detail="Resume version not found")
    
    # Check if the resume belongs to the user
    db_resume = resume.get_resume(db, resume_id=db_version.resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume version")
    
    # Parse the content JSON for the response
    if isinstance(db_version.content, str):
        try:
            content_dict = json.loads(db_version.content)
            db_version.content = content_dict
        except json.JSONDecodeError:
            pass
    
    return db_version


@router.get("/versions/{resume_id}", response_model=List[schemas.ResumeVersionBase])
def read_versions(
    resume_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get all versions of a resume."""
    # Check if the resume exists and belongs to the user
    db_resume = resume.get_resume(db, resume_id=resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get the versions
    versions = resume.get_resume_versions(db, resume_id=resume_id, skip=skip, limit=limit)
    return versions


@router.get("/download/{version_id}")
def download_resume(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Generate and download a PDF of a resume version."""
    from fastapi.responses import Response
    
    # Get the version
    db_version = resume.get_resume_version(db, version_id=version_id)
    if db_version is None:
        raise HTTPException(status_code=404, detail="Resume version not found")
    
    # Check if the resume belongs to the user
    db_resume = resume.get_resume(db, resume_id=db_version.resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
    
    # Get the template
    db_template = resume.get_template(db, template_id=db_resume.current_template_id)
    if db_template is None:
        # Use default template if the assigned one doesn't exist
        template_html = pdf.get_default_template_html()
        template_css = pdf.get_default_template_css()
    else:
        template_html = db_template.html_content
        template_css = db_template.css_content
    
    # Parse the content JSON
    if isinstance(db_version.content, str):
        try:
            resume_content = json.loads(db_version.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid resume content format")
    else:
        resume_content = db_version.content
    
    # Generate the PDF
    try:
        pdf_bytes = pdf.generate_resume_pdf(
            resume_content=resume_content,
            template_html=template_html,
            template_css=template_css
        )
        
        # Return the PDF file
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="resume_{db_resume.title}_{db_version.version_number}.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@router.post("/upload-pdf", response_model=schemas.PDFExtractResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Upload and parse a PDF resume to extract structured data.
    """
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a PDF file."
        )
    
    # Read file content
    file_content = await file.read()
    
    # Check file size (limit to 5MB)
    if len(file_content) > 5 * 1024 * 1024:  # 5MB in bytes
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum allowed size is 5MB."
        )
    
    try:
        # Import the PDF parser here to avoid circular imports
        from app.utils.pdf_parser import parse_pdf
        
        # Parse the PDF file
        parsed_data = parse_pdf(file_content)
        
        return parsed_data
    
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse PDF: {str(e)}"
        ) 