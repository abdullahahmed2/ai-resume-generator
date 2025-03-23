import json
import os
import tempfile
import asyncio
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv
import pyppeteer
from jinja2 import Template

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get PDF engine from environment variables
PDF_ENGINE = os.getenv("PDF_ENGINE", "pyppeteer").lower()  # Options: pyppeteer, weasyprint


async def _generate_pdf_with_pyppeteer(html_file_path: str) -> bytes:
    """
    Generate a PDF file using Pyppeteer (Puppeteer for Python).
    
    Args:
        html_file_path: Path to the HTML file to convert
    
    Returns:
        PDF file as bytes
    """
    browser = await pyppeteer.launch(headless=True)
    page = await browser.newPage()
    
    # Load HTML from file
    await page.goto(f'file://{html_file_path}', {'waitUntil': 'networkidle0'})
    
    # Set PDF options (Letter size: 8.5in x 11in)
    pdf_options = {
        'format': 'Letter',
        'printBackground': True,
        'margin': {
            'top': '0.5in',
            'right': '0.5in',
            'bottom': '0.5in',
            'left': '0.5in',
        }
    }
    
    # Generate PDF
    pdf_bytes = await page.pdf(pdf_options)
    
    # Close browser
    await browser.close()
    
    return pdf_bytes


def _generate_pdf_with_weasyprint(html_content: str, css_content: str) -> bytes:
    """
    Generate a PDF file using WeasyPrint.
    
    Args:
        html_content: HTML content to convert
        css_content: CSS content for styling
    
    Returns:
        PDF file as bytes
    """
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        css = CSS(string=css_content, font_config=font_config)
        
        # Generate PDF
        return html.write_pdf(stylesheets=[css], font_config=font_config)
    
    except ImportError:
        logger.warning("WeasyPrint not installed. Falling back to Pyppeteer.")
        # Create temporary files for Pyppeteer fallback
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
            html_file.write(html_content.encode('utf-8'))
            html_file_path = html_file.name
        
        # Get the absolute path for the HTML file
        html_file_abs_path = os.path.abspath(html_file_path)
        
        # Generate the PDF using Pyppeteer fallback
        pdf_bytes = asyncio.run(_generate_pdf_with_pyppeteer(html_file_abs_path))
        
        # Clean up temporary files
        os.unlink(html_file_path)
        
        return pdf_bytes


def generate_resume_pdf(resume_content: Dict[str, Any], template_html: str, template_css: str) -> bytes:
    """
    Generate a PDF file from resume content and template.
    
    Args:
        resume_content: Dict containing resume data
        template_html: HTML template with placeholders
        template_css: CSS for styling the template
    
    Returns:
        PDF file as bytes
    """
    try:
        # Parse the resume content JSON if it's a string
        if isinstance(resume_content, str):
            resume_content = json.loads(resume_content)
        
        # Create a Jinja2 template from the HTML
        template = Template(template_html)
        
        # Render the template with the resume content
        html_content = template.render(**resume_content)
        
        # Determine which PDF engine to use
        if PDF_ENGINE == "weasyprint":
            logger.info("Using WeasyPrint for PDF generation")
            
            # Create complete HTML document
            complete_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Resume</title>
                <style>
                    @page {{
                        margin: 0;
                        size: letter;
                    }}
                    body {{
                        margin: 0;
                        padding: 0;
                    }}
                    {template_css}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Generate PDF using WeasyPrint
            return _generate_pdf_with_weasyprint(complete_html, template_css)
        else:
            logger.info("Using Pyppeteer for PDF generation")
            
            # Create a temporary CSS file
            with tempfile.NamedTemporaryFile(suffix='.css', delete=False) as css_file:
                css_file.write(template_css.encode('utf-8'))
                css_file_path = css_file.name
                
            # Get the absolute path for the CSS file
            css_file_abs_path = os.path.abspath(css_file_path)
                
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
                html_file.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Resume</title>
                    <link rel="stylesheet" href="file://{css_file_abs_path}">
                    <style>
                        @page {{
                            margin: 0;
                            size: letter;
                        }}
                        body {{
                            margin: 0;
                            padding: 0;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """.encode('utf-8'))
                html_file_path = html_file.name
            
            # Get the absolute path for the HTML file
            html_file_abs_path = os.path.abspath(html_file_path)
            
            # Generate the PDF using Pyppeteer
            # We need to run the async function in an event loop
            pdf_bytes = asyncio.run(_generate_pdf_with_pyppeteer(html_file_abs_path))
            
            # Clean up temporary files
            os.unlink(html_file_path)
            os.unlink(css_file_path)
            
            return pdf_bytes
    
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise e


def get_default_template_html() -> str:
    """Return a default template HTML if no template is specified."""
    return """
    <div class="resume">
        <div class="header">
            <h1>{{ personal_info.name }}</h1>
            <div class="contact-info">
                <p>{{ personal_info.email }} | {{ personal_info.phone }}</p>
                <p>{{ personal_info.location }}</p>
                {% if personal_info.linkedin %}
                <p>LinkedIn: {{ personal_info.linkedin }}</p>
                {% endif %}
                {% if personal_info.website %}
                <p>Website: {{ personal_info.website }}</p>
                {% endif %}
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2>Professional Summary</h2>
            <p>{{ summary }}</p>
        </div>
        {% endif %}
        
        {% if work_experience and work_experience|length > 0 %}
        <div class="section">
            <h2>Work Experience</h2>
            {% for job in work_experience %}
            <div class="item">
                <div class="item-header">
                    <h3>{{ job.title }}</h3>
                    <h4>{{ job.company }}</h4>
                    <p class="date">{{ job.start_date }} - {{ job.end_date if job.end_date else 'Present' }}</p>
                </div>
                <ul class="responsibilities">
                    {% for responsibility in job.responsibilities %}
                    <li>{{ responsibility }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if education and education|length > 0 %}
        <div class="section">
            <h2>Education</h2>
            {% for edu in education %}
            <div class="item">
                <div class="item-header">
                    <h3>{{ edu.degree }}</h3>
                    <h4>{{ edu.institution }}</h4>
                    <p class="date">{{ edu.start_date }} - {{ edu.end_date if edu.end_date else 'Present' }}</p>
                </div>
                {% if edu.details %}
                <p>{{ edu.details }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2>Skills</h2>
            <ul class="skills-list">
                {% for skill in skills %}
                <li>{{ skill }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        {% if projects and projects|length > 0 %}
        <div class="section">
            <h2>Projects</h2>
            {% for project in projects %}
            <div class="item">
                <div class="item-header">
                    <h3>{{ project.name }}</h3>
                    {% if project.date %}
                    <p class="date">{{ project.date }}</p>
                    {% endif %}
                </div>
                <p>{{ project.description }}</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    """


def get_default_template_css() -> str:
    """Return default template CSS if no template is specified."""
    return """
    body {
        font-family: 'Arial', sans-serif;
        font-size: 12px;
        line-height: 1.4;
        color: #333;
    }
    
    .resume {
        max-width: 8.5in;
        margin: 0 auto;
        padding: 0.5in;
    }
    
    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .header h1 {
        margin: 0;
        font-size: 24px;
        text-transform: uppercase;
    }
    
    .contact-info {
        margin-top: 10px;
    }
    
    .contact-info p {
        margin: 5px 0;
    }
    
    .section {
        margin-bottom: 20px;
    }
    
    .section h2 {
        margin: 0 0 10px 0;
        font-size: 16px;
        text-transform: uppercase;
        border-bottom: 1px solid #999;
        padding-bottom: 5px;
    }
    
    .item {
        margin-bottom: 15px;
    }
    
    .item-header {
        margin-bottom: 5px;
    }
    
    .item-header h3 {
        margin: 0;
        font-size: 14px;
    }
    
    .item-header h4 {
        margin: 0;
        font-size: 13px;
        font-weight: normal;
        font-style: italic;
    }
    
    .date {
        margin: 0;
        font-style: italic;
        color: #666;
    }
    
    .responsibilities {
        margin: 10px 0 0 20px;
        padding: 0 0 0 20px;
    }
    
    .responsibilities li {
        margin-bottom: 3px;
    }
    
    .skills-list {
        margin: 0;
        padding: 0 0 0 20px;
        columns: 2;
    }
    
    .skills-list li {
        margin-bottom: 3px;
    }
    """ 