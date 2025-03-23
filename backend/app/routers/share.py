import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import auth, resume, share

router = APIRouter(
    prefix="/share",
    tags=["share"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/generate", response_model=schemas.ShareLink)
def generate_share_link(
    share_data: schemas.ShareLinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Generate a share link for a resume."""
    # Check if the resume exists and belongs to the user
    db_resume = resume.get_resume(db, resume_id=share_data.resume_id, user_id=current_user.id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Create the share link
    db_share_link = share.create_share_link(db, share_link=share_data)
    return db_share_link


@router.get("/list", response_model=List[schemas.ShareLink])
def read_share_links(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get all share links for a user's resumes."""
    share_links = share.get_user_share_links(db, user_id=current_user.id, skip=skip, limit=limit)
    return share_links


@router.put("/deactivate/{share_id}", response_model=bool)
def deactivate_share_link(
    share_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Deactivate a share link."""
    result = share.deactivate_share_link(db, share_id=share_id, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Share link not found or not authorized")
    return True


@router.get("/resume/{token}")
def get_shared_resume(token: str, db: Session = Depends(get_db)):
    """Get a resume via a share link."""
    # Get the share link
    db_share_link = share.get_share_link(db, token=token)
    
    # Check if the share link exists and is valid
    if not db_share_link or not share.is_share_link_valid(db_share_link):
        raise HTTPException(status_code=404, detail="Share link not found or expired")
    
    # Get the resume
    db_resume = resume.get_resume_by_id(db, resume_id=db_share_link.resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get the resume version
    if db_share_link.resume_version_id:
        db_version = resume.get_resume_version(db, version_id=db_share_link.resume_version_id)
    else:
        # If no specific version is specified, get the latest version
        versions = resume.get_resume_versions(db, resume_id=db_resume.id, limit=1)
        if not versions:
            raise HTTPException(status_code=404, detail="No resume versions found")
        db_version = versions[0]
    
    # Get the template
    db_template = resume.get_template(db, template_id=db_resume.current_template_id)
    
    # Parse the content JSON
    if isinstance(db_version.content, str):
        try:
            content = json.loads(db_version.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid resume content format")
    else:
        content = db_version.content
    
    # Return the resume data
    from fastapi.responses import JSONResponse
    
    return JSONResponse(content={
        "resume": {
            "id": db_resume.id,
            "title": db_resume.title,
            "version": {
                "id": db_version.id,
                "version_number": db_version.version_number,
                "label": db_version.label,
                "created_at": db_version.created_at.isoformat(),
                "content": content
            },
            "template": {
                "id": db_template.id if db_template else None,
                "name": db_template.name if db_template else "Default",
            }
        }
    })