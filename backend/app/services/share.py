import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from .. import models, schemas


def generate_unique_token():
    """Generate a unique random token for sharing."""
    return secrets.token_urlsafe(16)


def create_share_link(db: Session, share_link: schemas.ShareLinkCreate):
    """Create a new share link for a resume."""
    token = generate_unique_token()
    
    # Create the share link in the database
    db_share_link = models.ShareLink(
        token=token,
        resume_id=share_link.resume_id,
        resume_version_id=share_link.resume_version_id,
        expires_at=share_link.expires_at,
        is_active=True
    )
    db.add(db_share_link)
    db.commit()
    db.refresh(db_share_link)
    return db_share_link


def get_share_link(db: Session, token: str):
    """Get a share link by token."""
    return db.query(models.ShareLink).filter(models.ShareLink.token == token).first()


def deactivate_share_link(db: Session, share_id: int, user_id: int):
    """Deactivate a share link."""
    # Get the share link
    share_link = db.query(models.ShareLink).filter(models.ShareLink.id == share_id).first()
    
    # Check if the share link exists
    if not share_link:
        return False
    
    # Check if the user owns the resume
    resume = db.query(models.Resume).filter(
        models.Resume.id == share_link.resume_id,
        models.Resume.user_id == user_id
    ).first()
    
    if not resume:
        return False
    
    # Deactivate the link
    share_link.is_active = False
    db.commit()
    db.refresh(share_link)
    return True


def get_user_share_links(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    """Get all share links for a user's resumes."""
    return db.query(models.ShareLink).join(
        models.Resume, models.ShareLink.resume_id == models.Resume.id
    ).filter(
        models.Resume.user_id == user_id
    ).offset(skip).limit(limit).all()


def is_share_link_valid(share_link: models.ShareLink):
    """Check if a share link is valid (active and not expired)."""
    if not share_link or not share_link.is_active:
        return False
    
    # Check if the link has expired
    if share_link.expires_at and share_link.expires_at < datetime.now():
        return False
    
    return True 