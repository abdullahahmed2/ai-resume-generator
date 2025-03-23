from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import auth, template
from ..utils.templates import get_all_templates

router = APIRouter(
    prefix="/template",
    tags=["template"],
    responses={401: {"description": "Unauthorized"}},
)


@router.get("/list", response_model=List[schemas.Template])
def get_templates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get all available resume templates."""
    return template.get_templates(db)


@router.get("/{template_id}", response_model=schemas.Template)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Get a specific template by ID."""
    db_template = template.get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template


@router.post("/create", response_model=schemas.Template)
def create_template(
    template_data: schemas.TemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Create a new template (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create templates")
    
    return template.create_template(db=db, template=template_data)


@router.post("/seed", response_model=List[schemas.Template])
def seed_templates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Seed the database with predefined templates (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to seed templates")
    
    # Get predefined templates
    predefined_templates = get_all_templates()
    
    created_templates = []
    for template_data in predefined_templates:
        # Check if template with same name already exists
        existing = template.get_template_by_name(db, name=template_data["name"])
        if existing:
            continue
            
        # Create template schema
        template_schema = schemas.TemplateCreate(
            name=template_data["name"],
            description=template_data["description"],
            html_content=template_data["html_content"],
            css_content=template_data["css_content"],
            role_type=template_data["role_type"],
            is_default=template_data["is_default"]
        )
        
        # Create template in database
        created = template.create_template(db=db, template=template_schema)
        created_templates.append(created)
    
    return created_templates 