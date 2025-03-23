"""
PDF parser utility for extracting resume content from uploaded PDF files.
"""
import io
import re
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List, Any

import PyPDF2
import spacy
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

# Load spaCy NER model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is not installed, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

# Configure logging
logger = logging.getLogger(__name__)

# Define regex patterns for different resume sections
SECTION_PATTERNS = {
    "summary": re.compile(r"(?i)(summary|profile|objective|about me)"),
    "experience": re.compile(r"(?i)(experience|work|employment|career|professional background)"),
    "education": re.compile(r"(?i)(education|academic|degree|qualification)"),
    "skills": re.compile(r"(?i)(skills|expertise|technical skills|competencies|proficiencies)"),
    "projects": re.compile(r"(?i)(projects|personal projects|portfolio|case studies)")
}

# Common list of skills for matching
COMMON_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go", "Rust", 
    "TypeScript", "Scala", "Perl", "R", "MATLAB", "SQL", "HTML", "CSS", "Shell", "Bash",
    
    # Frameworks & Libraries
    "React", "Angular", "Vue.js", "Django", "Flask", "Spring", "Express.js", "Node.js", "Ruby on Rails",
    "ASP.NET", "Laravel", "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy", "Scikit-learn",
    "jQuery", "Bootstrap", "Tailwind CSS", "Redux", "Next.js", "FastAPI",
    
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server", "SQLite", "Redis", "Cassandra",
    "DynamoDB", "Firebase", "Neo4j", "MariaDB", "Elasticsearch",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
    "Terraform", "Ansible", "Puppet", "Chef", "Nginx", "Apache", "Serverless", "CloudFormation",
    
    # Data Science & AI
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Analysis", "Data Visualization",
    "Big Data", "Hadoop", "Spark", "Data Mining", "Statistical Analysis", "Reinforcement Learning",
    
    # Design & UI/UX
    "Figma", "Adobe XD", "Sketch", "Photoshop", "Illustrator", "InDesign", "UI Design", "UX Design",
    "Wireframing", "Prototyping", "User Research", "A/B Testing",
    
    # Project Management & Methodologies
    "Agile", "Scrum", "Kanban", "Jira", "Trello", "Confluence", "Asana", "Project Management",
    "SDLC", "Waterfall", "Lean", "Six Sigma",
    
    # Testing & QA
    "Unit Testing", "Integration Testing", "End-to-End Testing", "Test Automation", "Selenium",
    "JUnit", "Jest", "Cypress", "Mocha", "Chai", "TestNG", "Quality Assurance",
    
    # Marketing Skills
    "SEO", "SEM", "Social Media Marketing", "Content Marketing", "Email Marketing", "Google Analytics",
    "Facebook Ads", "Google Ads", "Marketing Automation", "CRM", "Salesforce", "HubSpot",
    
    # Finance & Business
    "Financial Analysis", "Budgeting", "Forecasting", "Excel", "PowerPoint", "Data Entry",
    "Accounting", "QuickBooks", "SAP", "ERP", "Business Intelligence", "Tableau", "Power BI"
]

def parse_pdf(file_content: bytes) -> Dict[str, Any]:
    """
    Parse a PDF file and extract structured resume information.
    
    Args:
        file_content: Bytes content of the uploaded PDF file
        
    Returns:
        Dictionary containing structured resume information
    """
    try:
        # Use a temporary file to handle the PDF
        with NamedTemporaryFile(suffix=".pdf", delete=True) as temp_file:
            # Write content to temp file
            temp_file.write(file_content)
            temp_file.flush()
            
            # Extract text using pdfminer for better text extraction
            text = extract_text(temp_file.name, laparams=LAParams())
            
            # Also use PyPDF2 as a fallback for metadata
            pdf_reader = PyPDF2.PdfReader(temp_file.name)
            
            # Check if text extraction was successful
            if not text.strip():
                logger.warning("No text extracted from PDF")
                return {
                    "personal_info": {},
                    "summary": "",
                    "skills": [],
                    "work_experience": [],
                    "education": [],
                    "projects": []
                }
            
            # Process the extracted text
            return process_resume_text(text)
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        raise Exception(f"Failed to parse PDF: {str(e)}")

def process_resume_text(text: str) -> Dict[str, Any]:
    """
    Process extracted text and organize into structured resume sections.
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Dictionary containing structured resume information
    """
    # Initialize result structure
    result = {
        "personal_info": {},
        "summary": "",
        "skills": [],
        "work_experience": [],
        "education": [],
        "projects": []
    }
    
    # Split text into lines and clean up
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Extract personal information using NER
    result["personal_info"] = extract_personal_info(text)
    
    # Identify sections in the resume
    sections = identify_sections(lines)
    
    # Extract summary
    if "summary" in sections:
        start, end = sections["summary"]
        summary_text = " ".join(lines[start:end])
        # Clean up the summary (remove section title)
        summary_text = re.sub(SECTION_PATTERNS["summary"], "", summary_text).strip()
        result["summary"] = summary_text
    
    # Extract skills
    result["skills"] = extract_skills(text, sections)
    
    # Extract work experience
    if "experience" in sections:
        result["work_experience"] = extract_work_experience(lines, sections["experience"])
    
    # Extract education
    if "education" in sections:
        result["education"] = extract_education(lines, sections["education"])
    
    # Extract projects
    if "projects" in sections:
        result["projects"] = extract_projects(lines, sections["projects"])
    
    return result

def identify_sections(lines: List[str]) -> Dict[str, tuple]:
    """
    Identify different sections in the resume and their line ranges.
    
    Args:
        lines: List of text lines from the resume
        
    Returns:
        Dictionary mapping section names to (start_line, end_line) tuples
    """
    sections = {}
    section_starts = []
    
    # Identify the start of each section
    for i, line in enumerate(lines):
        for section, pattern in SECTION_PATTERNS.items():
            if pattern.search(line):
                section_starts.append((i, section))
    
    # Sort by line number
    section_starts.sort()
    
    # Define section ranges
    for i, (start, section) in enumerate(section_starts):
        end = section_starts[i+1][0] if i < len(section_starts) - 1 else len(lines)
        sections[section] = (start, end)
    
    return sections

def extract_personal_info(text: str) -> Dict[str, str]:
    """
    Extract personal information from resume text using NER and patterns.
    
    Args:
        text: Full text of the resume
        
    Returns:
        Dictionary containing personal information
    """
    personal_info = {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "website": ""
    }
    
    # Use spaCy for named entity recognition
    doc = nlp(text[:1000])  # Process just the first part where personal info usually appears
    
    # Extract name (assuming the first PERSON entity might be the resume owner)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not personal_info["name"]:
            personal_info["name"] = ent.text
    
    # Extract email using regex
    email_pattern = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
    email_match = email_pattern.search(text)
    if email_match:
        personal_info["email"] = email_match.group(0)
    
    # Extract phone using regex
    phone_pattern = re.compile(r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    phone_match = phone_pattern.search(text)
    if phone_match:
        personal_info["phone"] = phone_match.group(0)
    
    # Extract location (look for cities or addresses)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"] and not personal_info["location"]:
            personal_info["location"] = ent.text
    
    # Look for LinkedIn and website URLs
    linkedin_pattern = re.compile(r'(?:linkedin\.com/in/|linkedin\.com/profile/view\?id=)[\w-]+')
    linkedin_match = linkedin_pattern.search(text)
    if linkedin_match:
        personal_info["linkedin"] = linkedin_match.group(0)
    
    # General website (non-LinkedIn)
    website_pattern = re.compile(r'(?:https?://)?(?:www\.)?[\w.-]+\.[a-zA-Z]{2,}(?:/\S*)?')
    for match in website_pattern.finditer(text):
        url = match.group(0)
        if "linkedin" not in url and not personal_info["website"]:
            personal_info["website"] = url
    
    return personal_info

def extract_skills(text: str, sections: Dict[str, tuple]) -> List[str]:
    """
    Extract skills from the resume text.
    
    Args:
        text: Full text of the resume
        sections: Dictionary mapping section names to line ranges
        
    Returns:
        List of identified skills
    """
    skills = []
    
    # Look for skills in the skills section if it exists
    if "skills" in sections:
        start, end = sections["skills"]
        skills_text = text[start:end]
        
        # Look for common skills in the skills section
        for skill in COMMON_SKILLS:
            # Use word boundaries to avoid partial matches
            skill_pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            if skill_pattern.search(skills_text):
                skills.append(skill)
    
    # If no skills found in the skills section or if no skills section exists,
    # look for skills throughout the document
    if not skills:
        for skill in COMMON_SKILLS:
            skill_pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            if skill_pattern.search(text):
                skills.append(skill)
    
    return skills[:30]  # Limit to top 30 skills to prevent overwhelming results

def extract_work_experience(lines: List[str], section_range: tuple) -> List[Dict[str, str]]:
    """
    Extract work experience entries from the resume.
    
    Args:
        lines: List of text lines from the resume
        section_range: (start_line, end_line) tuple for the experience section
        
    Returns:
        List of work experience entries
    """
    start, end = section_range
    experience_lines = lines[start+1:end]  # Skip the section heading
    
    experiences = []
    current_exp = {}
    exp_text = []
    
    # Simple heuristic: look for lines that might indicate a new job entry
    # This is a simplified approach; a more robust solution would use more patterns
    for line in experience_lines:
        # Check if this line might be a new job entry start
        # Usually contains company name and possibly dates
        date_pattern = re.compile(r'\b(19|20)\d{2}\b')  # Years like 1999 or 2020
        
        # If we find a line with a year and it's not too long (likely a header, not description)
        if date_pattern.search(line) and len(line) < 100:
            # If we were already building an experience entry, save it
            if current_exp:
                current_exp["description"] = " ".join(exp_text)
                experiences.append(current_exp)
                current_exp = {}
                exp_text = []
            
            # Parse the new job entry header
            current_exp = parse_job_header(line)
        else:
            # This is likely part of the job description
            exp_text.append(line)
    
    # Don't forget to add the last experience
    if current_exp:
        current_exp["description"] = " ".join(exp_text)
        experiences.append(current_exp)
    
    return experiences

def parse_job_header(header_line: str) -> Dict[str, str]:
    """
    Parse job header line to extract company, position, location, and dates.
    
    Args:
        header_line: Line containing job header information
        
    Returns:
        Dictionary with job information fields
    """
    result = {
        "company": "",
        "position": "",
        "location": "",
        "start_date": "",
        "end_date": ""
    }
    
    # Extract dates
    date_pattern = re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)(\s+\d{4})?\s*(-|–|to)\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*(\d{4}|Present|Current|Now)?|\b(19|20)\d{2}\s*(-|–|to)\s*(19|20)\d{2}|Present|Current|Now\b', re.IGNORECASE)
    
    date_match = date_pattern.search(header_line)
    if date_match:
        # Extract the full date string
        date_str = date_match.group(0)
        
        # Split by common separators
        date_parts = re.split(r'\s*(-|–|to)\s*', date_str)
        
        if len(date_parts) >= 2:
            result["start_date"] = date_parts[0].strip()
            result["end_date"] = date_parts[-1].strip()
        
        # Remove the date part from the header to simplify company/position extraction
        header_no_date = header_line.replace(date_str, "").strip()
    else:
        header_no_date = header_line
    
    # Try to identify company vs position
    # This is a simplified approach - a more robust solution would use ML or more patterns
    parts = [p.strip() for p in re.split(r'\s*[,|]\s*', header_no_date) if p.strip()]
    
    if len(parts) >= 2:
        result["company"] = parts[0]
        result["position"] = parts[1]
    elif len(parts) == 1:
        # If only one part, assume it's the company name
        result["company"] = parts[0]
    
    return result

def extract_education(lines: List[str], section_range: tuple) -> List[Dict[str, str]]:
    """
    Extract education entries from the resume.
    
    Args:
        lines: List of text lines from the resume
        section_range: (start_line, end_line) tuple for the education section
        
    Returns:
        List of education entries
    """
    start, end = section_range
    education_lines = lines[start+1:end]  # Skip the section heading
    
    educations = []
    current_edu = {}
    edu_text = []
    
    # Similar approach to work experience extraction
    for line in education_lines:
        date_pattern = re.compile(r'\b(19|20)\d{2}\b')  # Years like 1999 or 2020
        degree_pattern = re.compile(r'\b(bachelor|master|phd|doctorate|bs|ba|ms|ma|phd|mba|b\.s\.|m\.s\.|b\.a\.|m\.a\.)\b', re.IGNORECASE)
        
        # If we find a line with a year or degree and it's not too long
        if (date_pattern.search(line) or degree_pattern.search(line)) and len(line) < 100:
            # If we were already building an education entry, save it
            if current_edu:
                current_edu["description"] = " ".join(edu_text)
                educations.append(current_edu)
                current_edu = {}
                edu_text = []
            
            # Parse the new education entry header
            current_edu = parse_education_header(line)
        else:
            # This is likely part of the education description
            edu_text.append(line)
    
    # Don't forget to add the last education entry
    if current_edu:
        current_edu["description"] = " ".join(edu_text)
        educations.append(current_edu)
    
    return educations

def parse_education_header(header_line: str) -> Dict[str, str]:
    """
    Parse education header line to extract institution, degree, and dates.
    
    Args:
        header_line: Line containing education header information
        
    Returns:
        Dictionary with education information fields
    """
    result = {
        "institution": "",
        "degree": "",
        "location": "",
        "start_date": "",
        "end_date": ""
    }
    
    # Extract dates
    date_pattern = re.compile(r'\b(19|20)\d{2}\s*(-|–|to)\s*(19|20)\d{2}|Present|Current|Now\b|\b(19|20)\d{2}\b', re.IGNORECASE)
    
    date_matches = list(date_pattern.finditer(header_line))
    if len(date_matches) >= 2:
        result["start_date"] = date_matches[0].group(0)
        result["end_date"] = date_matches[1].group(0)
    elif len(date_matches) == 1:
        # If only one date, assume it's the end date
        result["end_date"] = date_matches[0].group(0)
    
    # Try to identify degree
    degree_pattern = re.compile(r'\b(Bachelor|Master|PhD|Doctorate|BS|BA|MS|MA|PhD|MBA|B\.S\.|M\.S\.|B\.A\.|M\.A\.)(\s+of|\s+in)?\s+(Science|Arts|Business|Engineering|Fine Arts|Education|Computer Science|Information Technology|Mathematics|Physics|Chemistry|Biology|Psychology|Sociology|Economics|Finance|Marketing|Management|Communications|Journalism|Law|Medicine|Nursing|Philosophy|Political Science|History|English|Literature|Languages|Architecture|Design|Music|Theater|Film|Health|Public Health|Public Administration|Social Work|Criminal Justice|Human Resources|International Relations|Liberal Arts|General Studies|Applied Science|Technology|Information Systems)?\b', re.IGNORECASE)
    
    degree_match = degree_pattern.search(header_line)
    if degree_match:
        result["degree"] = degree_match.group(0)
    
    # Extract institution (simplified approach)
    # Assume the institution is at the beginning or after the degree
    parts = [p.strip() for p in re.split(r'[,|-]', header_line) if p.strip()]
    
    if parts:
        # If we have a degree match, check if it's in the first part
        if degree_match and degree_match.group(0) in parts[0]:
            # If the first part contains the degree, the second part might be the institution
            if len(parts) > 1:
                result["institution"] = parts[1]
        else:
            # Otherwise, assume the first part is the institution
            result["institution"] = parts[0]
    
    return result

def extract_projects(lines: List[str], section_range: tuple) -> List[Dict[str, str]]:
    """
    Extract project entries from the resume.
    
    Args:
        lines: List of text lines from the resume
        section_range: (start_line, end_line) tuple for the projects section
        
    Returns:
        List of project entries
    """
    start, end = section_range
    project_lines = lines[start+1:end]  # Skip the section heading
    
    projects = []
    current_project = {}
    project_text = []
    
    for line in project_lines:
        # Simplistic approach to identify new project entries
        # Look for short lines that might be project titles
        if len(line) < 50 and not line.startswith(" ") and not line.startswith("\t"):
            # If we were already building a project entry, save it
            if current_project:
                current_project["description"] = " ".join(project_text)
                projects.append(current_project)
                current_project = {}
                project_text = []
            
            # Start a new project entry
            current_project = {"name": line, "date": "", "description": ""}
            
            # Look for a date in the project title
            date_pattern = re.compile(r'\b(19|20)\d{2}\b')
            date_match = date_pattern.search(line)
            if date_match:
                current_project["date"] = date_match.group(0)
                # Remove the date from the name
                current_project["name"] = line.replace(date_match.group(0), "").strip()
        else:
            # This is likely part of the project description
            project_text.append(line)
    
    # Don't forget to add the last project
    if current_project:
        current_project["description"] = " ".join(project_text)
        projects.append(current_project)
    
    return projects 