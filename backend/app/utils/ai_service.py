"""
AI Service for resume content generation and enhancements.
"""
import os
import logging
import requests
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # openai, azure, etc.
API_ENDPOINT = os.getenv("AI_API_ENDPOINT", "https://api.openai.com/v1/chat/completions")

# Log configuration info (without sensitive data)
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY is not set in environment variables. AI features will use mock responses.")
logger.info(f"AI Provider: {AI_PROVIDER}, Model: {AI_MODEL}")

def make_ai_request(prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
    """
    Make a request to the AI service with the given prompt.
    
    Args:
        prompt: The prompt to send to the AI service
        max_tokens: Maximum tokens in the response
        temperature: Controls randomness (0-1)
        
    Returns:
        Generated text response
    """
    try:
        if not OPENAI_API_KEY:
            logger.warning("No API key found for AI service. Using mock response.")
            return generate_mock_response(prompt)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        data = {
            "model": AI_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert resume writer and career coach with years of experience helping people land their dream jobs."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(API_ENDPOINT, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Check for valid response structure
            if 'choices' not in result or not result['choices'] or 'message' not in result['choices'][0]:
                logger.error(f"Unexpected API response structure: {result}")
                return generate_mock_response(prompt)
                
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return generate_mock_response(prompt)
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "unknown"
            logger.error(f"HTTP error {status_code} from API: {str(e)}")
            
            # Check if it's an authentication error
            if e.response and e.response.status_code == 401:
                logger.error("Authentication failed. Check your OpenAI API key.")
            
            return generate_mock_response(prompt)
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error when contacting API service")
            return generate_mock_response(prompt)
            
        except json.JSONDecodeError:
            logger.error("Failed to parse API response as JSON")
            return generate_mock_response(prompt)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        # Fall back to mock response if API call fails
        return generate_mock_response(prompt)
    
    except Exception as e:
        logger.error(f"Error making AI request: {str(e)}")
        return generate_mock_response(prompt)

def generate_mock_response(prompt: str) -> str:
    """
    Generate a mock response for testing when API key is not available.
    
    Args:
        prompt: The prompt that would be sent to the AI
        
    Returns:
        A mock response based on the prompt type
    """
    logger.info("Generating mock response for prompt")
    
    if "summary" in prompt.lower():
        return "Experienced professional with a proven track record of delivering results. Skilled in problem-solving, communication, and team leadership. Committed to continuous learning and driving innovation in the workplace."
    
    elif "job description" in prompt.lower():
        return "Led cross-functional team in developing and implementing strategic initiatives that increased efficiency by 20%. Collaborated with stakeholders to identify opportunities for process improvement."
    
    elif "skills" in prompt.lower():
        return "Project Management, Team Leadership, Strategic Planning, Problem Solving, Communication, Data Analysis"
    
    else:
        return "This is a mock response for testing purposes. Please configure your API key for actual AI-generated content."

def generate_resume_summary(job_title: str, experience_years: int = 3, skills: List[str] = None) -> str:
    """
    Generate a professional summary for a resume tailored to the job title and skills.
    
    Args:
        job_title: Target job title
        experience_years: Years of experience in the field
        skills: List of key skills to emphasize
        
    Returns:
        Generated professional summary
    """
    skills_str = ", ".join(skills) if skills else "various relevant skills"
    
    experience_level = "entry-level"
    if experience_years > 2 and experience_years <= 5:
        experience_level = "mid-level"
    elif experience_years > 5 and experience_years <= 10:
        experience_level = "senior-level"
    elif experience_years > 10:
        experience_level = "expert-level"
    
    prompt = f"""
    Write a professional, ATS-friendly resume summary for a {experience_level} {job_title} with {experience_years} years of experience.
    The summary should be concise (3-4 sentences), highlight skills including {skills_str}, and be written in first person.
    Focus on achievements and value-add rather than just responsibilities.
    """
    
    return make_ai_request(prompt, max_tokens=200, temperature=0.7)

def improve_job_descriptions(job_title: str, company_name: str, responsibilities: List[str], years_experience: int = 1) -> List[str]:
    """
    Improve job descriptions to be more impactful and ATS-friendly.
    
    Args:
        job_title: Job title
        company_name: Company name
        responsibilities: List of responsibilities to improve
        years_experience: Years of experience in this role
        
    Returns:
        List of improved job descriptions
    """
    if not responsibilities:
        return []
    
    resp_text = "\n".join([f"- {r}" for r in responsibilities])
    
    prompt = f"""
    Improve the following job responsibilities for a {job_title} position at {company_name} with {years_experience} year(s) of experience.
    Make them more impactful, quantifiable where possible, and optimized for ATS systems.
    Start each bullet with a strong action verb, be specific about achievements, and include metrics when possible.
    
    Original responsibilities:
    {resp_text}
    
    Please provide exactly {len(responsibilities)} improved bullets, maintaining the same general topics but making them more professional and impressive.
    """
    
    response = make_ai_request(prompt, max_tokens=800, temperature=0.7)
    
    # Parse the response into individual bullet points
    improved_bullets = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line.startswith('-') or line.startswith('•')):
            # Clean up the bullet point
            bullet = line[1:].strip()
            improved_bullets.append(bullet)
    
    # If parsing failed, just split by newlines and take the appropriate number
    if not improved_bullets or len(improved_bullets) < len(responsibilities):
        improved_bullets = [line.strip() for line in response.split('\n') if line.strip()]
    
    # Ensure we return the same number of responsibilities
    return improved_bullets[:len(responsibilities)]

def get_relevant_skills(job_title: str, experience_level: str = "mid-level") -> List[str]:
    """
    Get a list of relevant skills for a specific job title.
    
    Args:
        job_title: Target job title
        experience_level: Level of experience (junior, mid-level, senior)
        
    Returns:
        List of relevant skills
    """
    prompt = f"""
    List 15 specific, relevant technical and soft skills for a {experience_level} {job_title} position.
    Focus on skills that would be valuable keywords for ATS systems.
    Include only the skills as a comma-separated list, with no explanations or introduction.
    """
    
    response = make_ai_request(prompt, max_tokens=300, temperature=0.7)
    
    # Parse the response into a list of skills
    skills = []
    for item in response.split(','):
        skill = item.strip()
        if skill:
            skills.append(skill)
    
    # If response wasn't properly formatted, try alternative parsing
    if not skills:
        skills = [line.strip() for line in response.split('\n') if line.strip()]
        skills = [s for s in skills if not s.startswith('Skills:') and not s.startswith('-')]
    
    return skills

def analyze_keywords_from_job(job_description: str, resume_content: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Analyze a job description to extract keywords and provide suggestions.
    
    Args:
        job_description: The job posting text
        resume_content: Optional resume content to compare against
        
    Returns:
        Dictionary with keywords, missing skills, and suggestions
    """
    prompt = f"""
    Extract the 15 most important keywords and skills from the following job description that an ATS system would look for.
    Include both hard technical skills and soft skills.
    
    Job Description:
    {job_description}
    
    Format your response as a JSON object with the following structure:
    {{
        "keywords": ["keyword1", "keyword2", ...],
        "hard_skills": ["skill1", "skill2", ...],
        "soft_skills": ["skill1", "skill2", ...],
        "education_requirements": "Description of education requirements",
        "experience_level": "junior/mid-level/senior"
    }}
    """
    
    response = make_ai_request(prompt, max_tokens=600, temperature=0.5)
    
    # Parse the JSON response
    try:
        analysis = json.loads(response)
    except json.JSONDecodeError:
        # If the response isn't valid JSON, extract what we can
        logger.warning("Could not parse AI response as JSON, using fallback extraction")
        keywords = extract_list_items(response, "keywords")
        hard_skills = extract_list_items(response, "hard skills")
        soft_skills = extract_list_items(response, "soft skills")
        
        analysis = {
            "keywords": keywords,
            "hard_skills": hard_skills,
            "soft_skills": soft_skills,
            "education_requirements": extract_text_after(response, "education requirements"),
            "experience_level": extract_text_after(response, "experience level")
        }
    
    # If we have resume content, compare and provide suggestions
    result = {
        "keywords": analysis.get("keywords", []),
        "missing_skills": [],
        "suggestions": {
            "hard_skills": analysis.get("hard_skills", []),
            "soft_skills": analysis.get("soft_skills", []),
            "education": analysis.get("education_requirements", ""),
            "experience_level": analysis.get("experience_level", "")
        }
    }
    
    if resume_content:
        # Compare skills in job vs resume
        resume_skills = set(resume_content.get("skills", []))
        job_skills = set(analysis.get("hard_skills", []) + analysis.get("soft_skills", []))
        
        missing_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in resume_skills]]
        result["missing_skills"] = missing_skills
        
        # Add suggestions based on comparison
        if missing_skills:
            prompt_suggestions = f"""
            Based on the job skills {', '.join(missing_skills)} that are missing from the candidate's resume,
            provide 3 specific suggestions for how they could improve their resume.
            Format as a numbered list without any introduction.
            """
            suggestions_response = make_ai_request(prompt_suggestions, max_tokens=300, temperature=0.7)
            
            # Extract suggestions as a list
            suggestions = [line.strip() for line in suggestions_response.split('\n') if line.strip()]
            suggestions = [s[2:].strip() if s.startswith('1.') or s.startswith('2.') or s.startswith('3.') else s for s in suggestions]
            
            result["suggestions"]["improvement_tips"] = suggestions
    
    return result

def extract_list_items(text: str, section_name: str) -> List[str]:
    """
    Extract list items from a section in the text.
    """
    lines = text.split('\n')
    items = []
    capturing = False
    
    for line in lines:
        if section_name.lower() in line.lower() and ':' in line:
            capturing = True
            continue
        
        if capturing:
            if ':' in line or line.strip() == '':
                capturing = False
                continue
            
            # Clean up the line
            item = line.strip()
            if item.startswith('-') or item.startswith('•'):
                item = item[1:].strip()
            
            if item:
                items.append(item)
    
    return items

def extract_text_after(text: str, section_name: str) -> str:
    """
    Extract text after a section name in the text.
    """
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if section_name.lower() in line.lower() and ':' in line:
            # Return the text after the colon
            parts = line.split(':', 1)
            if len(parts) > 1:
                return parts[1].strip()
    
    return "" 