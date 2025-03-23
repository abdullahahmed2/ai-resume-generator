from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas


def get_template(db: Session, template_id: int) -> Optional[models.Template]:
    """Get a template by ID."""
    return db.query(models.Template).filter(models.Template.id == template_id).first()


def get_template_by_name(db: Session, name: str) -> Optional[models.Template]:
    """Get a template by name."""
    return db.query(models.Template).filter(models.Template.name == name).first()


def get_template_by_role(db: Session, role_type: str) -> Optional[models.Template]:
    """Get a template by role type."""
    return db.query(models.Template).filter(
        models.Template.role_type == role_type,
        models.Template.is_default == True
    ).first()


def get_templates(db: Session, skip: int = 0, limit: int = 100) -> List[models.Template]:
    """Get all templates."""
    return db.query(models.Template).offset(skip).limit(limit).all()


def create_template(db: Session, template: schemas.TemplateCreate) -> models.Template:
    """Create a new template."""
    db_template = models.Template(
        name=template.name,
        description=template.description,
        html_content=template.html_content,
        css_content=template.css_content,
        role_type=template.role_type,
        is_default=template.is_default
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def update_template(db: Session, template_id: int, template: schemas.TemplateCreate) -> Optional[models.Template]:
    """Update a template."""
    db_template = get_template(db, template_id=template_id)
    if db_template is None:
        return None
    
    # Update fields
    db_template.name = template.name
    db_template.description = template.description
    db_template.html_content = template.html_content
    db_template.css_content = template.css_content
    db_template.role_type = template.role_type
    db_template.is_default = template.is_default
    
    db.commit()
    db.refresh(db_template)
    return db_template


def delete_template(db: Session, template_id: int) -> bool:
    """Delete a template."""
    db_template = get_template(db, template_id=template_id)
    if db_template is None:
        return False
    
    db.delete(db_template)
    db.commit()
    return True 