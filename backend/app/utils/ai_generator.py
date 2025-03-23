import os
import json
import openai
from typing import Dict, Any, List, Optional

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI client
if OPENAI_API_KEY:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None
    print("WARNING: OpenAI API key not found. AI features will be disabled.")


def generate_summary(job_title: str, experience_years: int, skills: List[str]) -> str:
    """
    Generate a professional summary for a resume based on job title,
    years of experience, and skills.
    
    Args:
        job_title: The job title
        experience_years: Years of experience
        skills: List of skills
        
    Returns:
        Generated professional summary
    """
    if not openai_client:
        return "AI summary generation is currently unavailable. Please provide your own summary."
    
    try:
        # Format skills for prompt
        skills_text = ", ".join(skills)
        
        prompt = f"""
        Create a professional summary for a {job_title} with {experience_years} years of experience. 
        Their key skills include: {skills_text}.
        
        The summary should be concise (3-4 sentences), professional, and highlight their expertise and value proposition.
        Focus on achievements and impact rather than just responsibilities.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who specializes in creating professional, ATS-friendly resume content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "An error occurred while generating the summary. Please provide your own summary."


def improve_content(content: str, content_type: str, job_title: Optional[str] = None) -> str:
    """
    Improve existing content by making it more professional, impactful, and ATS-friendly.
    
    Args:
        content: The content to improve
        content_type: Type of content (e.g., "summary", "job_description", "skill")
        job_title: Optional job title for context
        
    Returns:
        Improved content
    """
    if not openai_client:
        return content  # Return original content if OpenAI is not available
    
    try:
        job_context = f"for a {job_title} position" if job_title else ""
        
        # Different prompts based on content type
        if content_type == "summary":
            instruction = f"Rewrite the following professional summary {job_context} to be more impactful, concise, and ATS-friendly. Focus on value and achievements."
        elif content_type == "job_description":
            instruction = f"Rewrite the following job responsibility {job_context} to be more impactful, using strong action verbs and quantifying achievements where possible. Make it ATS-friendly."
        elif content_type == "skill":
            instruction = f"Rewrite the following skill description {job_context} to be more specific, professional, and ATS-friendly."
        else:
            instruction = f"Rewrite the following content {job_context} to be more professional, impactful, and ATS-friendly."
        
        prompt = f"{instruction}\n\nOriginal: {content}\n\nImproved:"
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who specializes in creating professional, ATS-friendly resume content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        improved_content = response.choices[0].message.content.strip()
        return improved_content
    
    except Exception as e:
        print(f"Error improving content: {str(e)}")
        return content  # Return original content on error


def generate_job_descriptions(job_title: str, company_name: str, 
                              responsibilities: List[str], 
                              years_experience: int) -> List[str]:
    """
    Generate improved job descriptions and responsibilities.
    
    Args:
        job_title: The job title
        company_name: The company name
        responsibilities: List of responsibilities
        years_experience: Years of experience in this role
        
    Returns:
        List of improved responsibility descriptions
    """
    if not openai_client:
        return responsibilities  # Return original content if OpenAI is not available
    
    try:
        # Compile responsibilities into a string
        resp_text = "\n".join([f"- {r}" for r in responsibilities])
        
        prompt = f"""
        Improve the following job responsibilities for a {job_title} position at {company_name} with {years_experience} years of experience.
        Make them more impactful, using strong action verbs and quantifying achievements where possible.
        Ensure they are ATS-friendly with relevant keywords for this role.

        Original responsibilities:
        {resp_text}

        Provide exactly {len(responsibilities)} improved bullet points, one per line. 
        Each should start with a strong action verb. Make them specific and impactful.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who specializes in creating professional, ATS-friendly resume content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        improved_text = response.choices[0].message.content.strip()
        
        # Extract bullet points
        bullet_points = []
        for line in improved_text.split('\n'):
            # Clean up the line
            clean_line = line.strip()
            # Remove bullet point markers
            clean_line = clean_line.lstrip('-•* ').strip()
            if clean_line:
                bullet_points.append(clean_line)
        
        # If we didn't get as many bullet points as we should, return the original
        if len(bullet_points) < len(responsibilities):
            return responsibilities
            
        return bullet_points
    
    except Exception as e:
        print(f"Error generating job descriptions: {str(e)}")
        return responsibilities  # Return original content on error


def get_relevant_skills(job_title: str, industry: Optional[str] = None, 
                        experience_level: str = "mid-level") -> List[str]:
    """
    Generate a list of relevant skills for a specific job title.
    
    Args:
        job_title: The job title
        industry: Optional industry context
        experience_level: Experience level (junior, mid-level, senior)
        
    Returns:
        List of relevant skills
    """
    if not openai_client:
        return []  # Return empty list if OpenAI is not available
    
    try:
        industry_context = f" in the {industry} industry" if industry else ""
        
        prompt = f"""
        Generate a list of 10-15 relevant skills for a {experience_level} {job_title}{industry_context}.
        Include both technical and soft skills that would make a candidate competitive for this role.
        The skills should be specific and tailored to what ATS systems typically look for.
        Format each skill as a single word or short phrase.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in job requirements and professional skills for various industries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        skills_text = response.choices[0].message.content.strip()
        
        # Extract skills into a list
        skills = []
        for line in skills_text.split('\n'):
            # Clean up the line
            clean_line = line.strip()
            # Remove numbers and bullet point markers
            clean_line = clean_line.lstrip('0123456789.-•* ').strip()
            if clean_line:
                skills.append(clean_line)
        
        return skills
    
    except Exception as e:
        print(f"Error generating skills: {str(e)}")
        return []  # Return empty list on error


def suggest_resume_improvements(resume_content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a resume and suggest improvements for various sections.
    
    Args:
        resume_content: The resume content as a dictionary
        
    Returns:
        Dictionary with improvement suggestions
    """
    if not openai_client:
        return {"error": "AI suggestions are currently unavailable. Please try again later."}
    
    try:
        # Extract key information from the resume
        job_title = ""
        for job in resume_content.get("work_experience", []):
            if job.get("title"):
                job_title = job.get("title")
                break
        
        # Serialize the resume content for the prompt
        resume_json = json.dumps(resume_content, indent=2)
        
        prompt = f"""
        Analyze the following resume content and provide specific improvements for each section.
        
        Resume content:
        ```
        {resume_json}
        ```
        
        Provide improvement suggestions in the following format:
        
        1. Summary: [Specific suggestions to improve the summary]
        2. Work Experience: [Specific suggestions to improve job descriptions]
        3. Skills: [Suggestions for additional skills or improvements to existing skills]
        4. Education: [Any improvements needed]
        5. Overall: [General suggestions to make the resume more ATS-friendly]
        
        Be specific and practical in your suggestions, focusing on what would make this resume more competitive for a {job_title} position.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who specializes in creating professional, ATS-friendly resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        suggestions = response.choices[0].message.content.strip()
        
        # Process suggestions into a structured format
        sections = ["Summary", "Work Experience", "Skills", "Education", "Overall"]
        structured_suggestions = {}
        
        current_section = None
        current_text = []
        
        for line in suggestions.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts a new section
            found_section = False
            for section in sections:
                if line.startswith(f"{section}:") or line.startswith(f"{sections.index(section) + 1}. {section}:"):
                    # Save the previous section if there was one
                    if current_section and current_text:
                        structured_suggestions[current_section.lower()] = '\n'.join(current_text)
                        current_text = []
                    
                    # Start the new section
                    current_section = section
                    # Extract the content after the section header
                    section_content = line.split(':', 1)[1].strip() if ':' in line else ""
                    if section_content:
                        current_text.append(section_content)
                    found_section = True
                    break
            
            # If this isn't a new section, add it to the current section's text
            if not found_section and current_section:
                current_text.append(line)
        
        # Add the last section
        if current_section and current_text:
            structured_suggestions[current_section.lower()] = '\n'.join(current_text)
        
        return structured_suggestions
    
    except Exception as e:
        print(f"Error generating improvement suggestions: {str(e)}")
        return {"error": f"An error occurred while generating suggestions: {str(e)}"} 