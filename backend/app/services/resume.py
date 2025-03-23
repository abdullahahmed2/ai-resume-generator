import json
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas


def get_resume(db: Session, resume_id: int, user_id: int):
    """Get a resume by ID for a specific user."""
    return db.query(models.Resume).filter(
        models.Resume.id == resume_id, 
        models.Resume.user_id == user_id
    ).first()


def get_resume_by_id(db: Session, resume_id: int):
    """Get a resume by ID."""
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()


def get_resumes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all resumes for a user."""
    return db.query(models.Resume).filter(
        models.Resume.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_resume(db: Session, resume: schemas.ResumeCreate, user_id: int):
    """Create a new resume for a user."""
    db_resume = models.Resume(
        title=resume.title,
        user_id=user_id,
        current_template_id=resume.template_id
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def update_resume(db: Session, resume_id: int, resume_update: schemas.ResumeCreate, user_id: int):
    """Update an existing resume."""
    db_resume = get_resume(db, resume_id, user_id)
    if db_resume:
        db_resume.title = resume_update.title
        db_resume.current_template_id = resume_update.template_id
        db.commit()
        db.refresh(db_resume)
    return db_resume


def delete_resume(db: Session, resume_id: int, user_id: int):
    """Delete a resume."""
    db_resume = get_resume(db, resume_id, user_id)
    if db_resume:
        db.delete(db_resume)
        db.commit()
        return True
    return False


def get_resume_version(db: Session, version_id: int):
    """Get a resume version by ID."""
    return db.query(models.ResumeVersion).filter(models.ResumeVersion.id == version_id).first()


def get_resume_versions(db: Session, resume_id: int, skip: int = 0, limit: int = 50):
    """Get all versions of a resume."""
    return db.query(models.ResumeVersion).filter(
        models.ResumeVersion.resume_id == resume_id
    ).order_by(models.ResumeVersion.version_number.desc()).offset(skip).limit(limit).all()


def create_resume_version(db: Session, version: schemas.ResumeVersionCreate):
    """Create a new version of a resume."""
    # Get the resume to ensure it exists
    resume = get_resume_by_id(db, version.resume_id)
    if not resume:
        return None
    
    # Get the latest version number to increment
    latest_version = db.query(models.ResumeVersion).filter(
        models.ResumeVersion.resume_id == version.resume_id
    ).order_by(models.ResumeVersion.version_number.desc()).first()
    
    version_number = 1
    if latest_version:
        version_number = latest_version.version_number + 1
    
    # Create new version
    db_version = models.ResumeVersion(
        resume_id=version.resume_id,
        version_number=version_number,
        label=version.label,
        content=json.dumps(version.content)  # Convert dict to JSON string
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def get_templates(db: Session, skip: int = 0, limit: int = 20, active_only: bool = True):
    """Get all available templates."""
    query = db.query(models.Template)
    if active_only:
        query = query.filter(models.Template.is_active == True)
    return query.offset(skip).limit(limit).all()


def get_template(db: Session, template_id: int):
    """Get a template by ID."""
    return db.query(models.Template).filter(models.Template.id == template_id).first() 