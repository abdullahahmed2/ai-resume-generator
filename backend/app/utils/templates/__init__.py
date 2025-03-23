"""
Templates module for loading and managing resume templates.
"""
from typing import Dict, Any, List

# Import all template modules
from . import software_engineer
from . import product_manager
from . import frontend_developer
from . import data_scientist
from . import marketing_specialist


def get_all_templates() -> List[Dict[str, Any]]:
    """
    Get all available templates with their metadata and content.
    Returns a list of dictionaries containing template information.
    """
    templates = []
    
    # Software Engineer template
    se_template = software_engineer.get_template_metadata()
    se_template["html_content"] = software_engineer.get_html_template()
    se_template["css_content"] = software_engineer.get_css_template()
    templates.append(se_template)
    
    # Product Manager template
    pm_template = product_manager.get_template_metadata()
    pm_template["html_content"] = product_manager.get_html_template()
    pm_template["css_content"] = product_manager.get_css_template()
    templates.append(pm_template)
    
    # Frontend Developer template
    fe_template = frontend_developer.get_template_metadata()
    fe_template["html_content"] = frontend_developer.get_html_template()
    fe_template["css_content"] = frontend_developer.get_css_template()
    templates.append(fe_template)
    
    # Data Scientist template
    ds_template = data_scientist.get_template_metadata()
    ds_template["html_content"] = data_scientist.get_html_template()
    ds_template["css_content"] = data_scientist.get_css_template()
    templates.append(ds_template)
    
    # Marketing Specialist template
    ms_template = marketing_specialist.get_template_metadata()
    ms_template["html_content"] = marketing_specialist.get_html_template()
    ms_template["css_content"] = marketing_specialist.get_css_template()
    templates.append(ms_template)
    
    return templates


def get_template_by_role(role_type: str) -> Dict[str, Any]:
    """
    Get a specific template by role type.
    
    Args:
        role_type: Type of role (e.g., "software_engineer", "product_manager")
        
    Returns:
        Template data including metadata and content
    """
    all_templates = get_all_templates()
    for template in all_templates:
        if template["role_type"] == role_type:
            return template
    
    # If role not found, return software engineer as default
    for template in all_templates:
        if template["role_type"] == "software_engineer":
            return template
    
    # If all else fails, return the first template
    return all_templates[0] 