import os
import json
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

# Initialize OpenAI client with API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)

# Define section types for suggestions
SECTION_TYPES = {
    "summary": "professional summary or objective statement",
    "work_experience": "job experience bullet points",
    "skills": "professional skills",
    "education": "education details",
    "achievements": "professional achievements",
    "projects": "project descriptions",
}


def generate_suggestions(
    resume_section: str, 
    context: Dict[str, Any], 
    max_suggestions: int = 3
) -> List[str]:
    """
    Generate AI-powered suggestions for a resume section.
    
    Args:
        resume_section: The section type (e.g., "work_experience")
        context: Context data for better suggestions
        max_suggestions: Maximum number of suggestions to generate
    
    Returns:
        A list of suggestion strings
    """
    if not OPENAI_API_KEY:
        # Return default suggestions if no API key is set
        return [f"Sample {SECTION_TYPES.get(resume_section, 'content')} (API key not set)"]
    
    try:
        # Format context data for the AI prompt
        context_str = ""
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                context_str += f"{key}: {json.dumps(value)}\n"
            else:
                context_str += f"{key}: {value}\n"
        
        section_type = SECTION_TYPES.get(resume_section, "content")
        
        # Create the prompt for the AI
        prompt = f"""
        You are an expert resume writer specializing in creating effective, ATS-friendly resume content.
        
        Please generate {max_suggestions} different professional {section_type} based on the following information:
        
        {context_str}
        
        Make the content specific, quantifiable with metrics when possible, and focused on achievements and impact rather than just responsibilities.
        Format each suggestion as a separate item in a numbered list.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume writing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        
        # Extract and process the response
        content = response.choices[0].message.content.strip()
        
        # Parse numbered list from content
        suggestions = []
        current_item = ""
        
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            if line[0].isdigit() and ". " in line[:5]:
                if current_item:
                    suggestions.append(current_item.strip())
                current_item = line[line.find(".")+1:].strip()
            else:
                current_item += " " + line
        
        if current_item:
            suggestions.append(current_item.strip())
        
        # Ensure we're returning the requested number of suggestions
        if not suggestions:
            suggestions = [f"Unable to generate {section_type} suggestions. Please try again."]
        
        return suggestions[:max_suggestions]
    
    except Exception as e:
        print(f"Error generating AI suggestions: {str(e)}")
        return [f"Error generating suggestions: {str(e)}"] 