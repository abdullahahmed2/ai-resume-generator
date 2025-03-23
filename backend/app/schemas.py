from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Resume schemas
class ResumeBase(BaseModel):
    title: str
    current_template_id: Optional[int] = None


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ResumeDetail(Resume):
    versions: List["ResumeVersion"] = []


# Resume Version schemas
class ResumeVersionBase(BaseModel):
    resume_id: int
    version_number: int
    description: Optional[str] = None


class ResumeVersionCreate(ResumeVersionBase):
    content: Dict[str, Any]


class ResumeVersion(BaseModel):
    id: int
    resume_id: int
    version_number: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Template schemas
class TemplateBase(BaseModel):
    name: str
    description: str
    html_content: str
    css_content: str
    role_type: Optional[str] = None
    is_default: bool = False


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TemplateDetail(Template):
    html_content: str
    css_content: str


# ShareLink schemas
class ShareBase(BaseModel):
    resume_id: int
    version_id: Optional[int] = None
    expiration_date: Optional[datetime] = None


class ShareCreate(ShareBase):
    pass


class Share(ShareBase):
    id: int
    user_id: int
    share_token: str
    created_at: datetime

    class Config:
        orm_mode = True


# AI Suggestion schemas
class SuggestionRequest(BaseModel):
    resume_section: str  # e.g., "work_experience", "skills", "summary"
    context: Dict[str, Any]  # Contextual data for the suggestion
    max_suggestions: int = 3


class SuggestionResponse(BaseModel):
    suggestions: List[str]


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# AI generation schemas
class GeneratedContent(BaseModel):
    content: str


class GeneratedJobDescriptions(BaseModel):
    descriptions: List[str]


class GeneratedSkills(BaseModel):
    skills: List[str]


# Resume content schemas for parsing PDFs and generating content
class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    website: str = ""


class WorkExperience(BaseModel):
    title: str = ""
    company: str = ""
    start_date: str = ""
    end_date: str = ""
    responsibilities: List[str] = []


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    start_date: str = ""
    end_date: str = ""
    details: str = ""


class Project(BaseModel):
    name: str = ""
    date: str = ""
    description: str = ""


class ResumeContent(BaseModel):
    personal_info: PersonalInfo
    summary: str = ""
    work_experience: List[WorkExperience] = []
    education: List[Education] = []
    skills: List[str] = []
    projects: List[Project] = []


# Update ResumeDetail to reference ResumeVersion
ResumeDetail.update_forward_refs() 