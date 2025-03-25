import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Spinner, Alert } from 'react-bootstrap';
import { apiService } from '../../services/apiService';
import '../../styles/ResumeForm.css';

// Form sections components
const PersonalInfoSection = ({ formData, handleChange }) => (
  <Card className="form-section">
    <Card.Header>Personal Information</Card.Header>
    <Card.Body>
      <Row>
        <Col md={12}>
          <Form.Group className="mb-3">
            <Form.Label>Full Name</Form.Label>
            <Form.Control
              type="text"
              name="personal_info.name"
              value={formData.personal_info.name}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="personal_info.email"
              value={formData.personal_info.email}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group className="mb-3">
            <Form.Label>Phone</Form.Label>
            <Form.Control
              type="text"
              name="personal_info.phone"
              value={formData.personal_info.phone}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
        <Col md={12}>
          <Form.Group className="mb-3">
            <Form.Label>Location</Form.Label>
            <Form.Control
              type="text"
              name="personal_info.location"
              value={formData.personal_info.location}
              onChange={handleChange}
              placeholder="City, State"
              required
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group className="mb-3">
            <Form.Label>LinkedIn</Form.Label>
            <Form.Control
              type="text"
              name="personal_info.linkedin"
              value={formData.personal_info.linkedin}
              onChange={handleChange}
              placeholder="linkedin.com/in/username"
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group className="mb-3">
            <Form.Label>Website/Portfolio</Form.Label>
            <Form.Control
              type="text"
              name="personal_info.website"
              value={formData.personal_info.website}
              onChange={handleChange}
              placeholder="https://yourportfolio.com"
            />
          </Form.Group>
        </Col>
      </Row>
    </Card.Body>
  </Card>
);

const SummarySection = ({ formData, handleChange, handleAIGenerate, isGenerating }) => (
  <Card className="form-section">
    <Card.Header className="d-flex justify-content-between align-items-center">
      <div>Professional Summary</div>
      <Button
        variant="outline-primary"
        size="sm"
        onClick={handleAIGenerate}
        disabled={isGenerating}
      >
        {isGenerating ? (
          <>
            <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
            <span className="ms-2">Generating...</span>
          </>
        ) : (
          "Generate with AI"
        )}
      </Button>
    </Card.Header>
    <Card.Body>
      <Form.Group>
        <Form.Control
          as="textarea"
          rows={4}
          name="summary"
          value={formData.summary}
          onChange={handleChange}
          placeholder="Write a brief summary of your professional background and strengths..."
        />
        <Form.Text className="text-muted">
          A strong summary highlights your key skills and career goals in 3-4 sentences.
        </Form.Text>
      </Form.Group>
    </Card.Body>
  </Card>
);

const WorkExperienceSection = ({ formData, setFormData, handleNestedChange, handleAIImprove, isImproving }) => {
  const addExperience = () => {
    const newExperience = {
      title: "",
      company: "",
      start_date: "",
      end_date: "",
      responsibilities: [""]
    };
    setFormData({
      ...formData,
      work_experience: [...formData.work_experience, newExperience]
    });
  };

  const removeExperience = (index) => {
    const updatedExperience = [...formData.work_experience];
    updatedExperience.splice(index, 1);
    setFormData({
      ...formData,
      work_experience: updatedExperience
    });
  };

  const addResponsibility = (jobIndex) => {
    const updatedExperience = [...formData.work_experience];
    updatedExperience[jobIndex].responsibilities.push("");
    setFormData({
      ...formData,
      work_experience: updatedExperience
    });
  };

  const removeResponsibility = (jobIndex, respIndex) => {
    const updatedExperience = [...formData.work_experience];
    updatedExperience[jobIndex].responsibilities.splice(respIndex, 1);
    setFormData({
      ...formData,
      work_experience: updatedExperience
    });
  };

  return (
    <Card className="form-section">
      <Card.Header>Work Experience</Card.Header>
      <Card.Body>
        {formData.work_experience.map((job, jobIndex) => (
          <div key={jobIndex} className="job-entry mb-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Job {jobIndex + 1}</h5>
              {jobIndex > 0 && (
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => removeExperience(jobIndex)}
                >
                  Remove
                </Button>
              )}
            </div>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Job Title</Form.Label>
                  <Form.Control
                    type="text"
                    name={`work_experience[${jobIndex}].title`}
                    value={job.title}
                    onChange={handleNestedChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Company</Form.Label>
                  <Form.Control
                    type="text"
                    name={`work_experience[${jobIndex}].company`}
                    value={job.company}
                    onChange={handleNestedChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Date</Form.Label>
                  <Form.Control
                    type="text"
                    name={`work_experience[${jobIndex}].start_date`}
                    value={job.start_date}
                    onChange={handleNestedChange}
                    placeholder="e.g., January 2020"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>End Date</Form.Label>
                  <Form.Control
                    type="text"
                    name={`work_experience[${jobIndex}].end_date`}
                    value={job.end_date}
                    onChange={handleNestedChange}
                    placeholder="e.g., Present or December 2022"
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <div className="d-flex justify-content-between align-items-center mb-2">
              <Form.Label>Responsibilities</Form.Label>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={() => handleAIImprove(jobIndex)}
                disabled={isImproving}
              >
                {isImproving === jobIndex ? (
                  <>
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                    <span className="ms-2">Improving...</span>
                  </>
                ) : (
                  "Improve with AI"
                )}
              </Button>
            </div>

            {job.responsibilities.map((resp, respIndex) => (
              <div key={respIndex} className="d-flex mb-2 align-items-start">
                <Form.Control
                  as="textarea"
                  rows={2}
                  name={`work_experience[${jobIndex}].responsibilities[${respIndex}]`}
                  value={resp}
                  onChange={handleNestedChange}
                  placeholder="Describe your responsibility or achievement..."
                  className="me-2"
                  required
                />
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => removeResponsibility(jobIndex, respIndex)}
                  disabled={job.responsibilities.length <= 1}
                >
                  &times;
                </Button>
              </div>
            ))}
            <Button
              variant="outline-secondary"
              size="sm"
              onClick={() => addResponsibility(jobIndex)}
              className="mt-2"
            >
              + Add Responsibility
            </Button>
          </div>
        ))}
        
        <Button
          variant="primary"
          onClick={addExperience}
          className="w-100 mt-3"
        >
          + Add Job Experience
        </Button>
      </Card.Body>
    </Card>
  );
};

const EducationSection = ({ formData, setFormData, handleNestedChange }) => {
  const addEducation = () => {
    const newEducation = {
      degree: "",
      institution: "",
      start_date: "",
      end_date: "",
      details: ""
    };
    setFormData({
      ...formData,
      education: [...formData.education, newEducation]
    });
  };

  const removeEducation = (index) => {
    const updatedEducation = [...formData.education];
    updatedEducation.splice(index, 1);
    setFormData({
      ...formData,
      education: updatedEducation
    });
  };

  return (
    <Card className="form-section">
      <Card.Header>Education</Card.Header>
      <Card.Body>
        {formData.education.map((edu, eduIndex) => (
          <div key={eduIndex} className="education-entry mb-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Education {eduIndex + 1}</h5>
              {eduIndex > 0 && (
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => removeEducation(eduIndex)}
                >
                  Remove
                </Button>
              )}
            </div>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Degree</Form.Label>
                  <Form.Control
                    type="text"
                    name={`education[${eduIndex}].degree`}
                    value={edu.degree}
                    onChange={handleNestedChange}
                    placeholder="e.g., Bachelor of Science in Computer Science"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Institution</Form.Label>
                  <Form.Control
                    type="text"
                    name={`education[${eduIndex}].institution`}
                    value={edu.institution}
                    onChange={handleNestedChange}
                    placeholder="e.g., University of California, Berkeley"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Date</Form.Label>
                  <Form.Control
                    type="text"
                    name={`education[${eduIndex}].start_date`}
                    value={edu.start_date}
                    onChange={handleNestedChange}
                    placeholder="e.g., September 2016"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>End Date</Form.Label>
                  <Form.Control
                    type="text"
                    name={`education[${eduIndex}].end_date`}
                    value={edu.end_date}
                    onChange={handleNestedChange}
                    placeholder="e.g., June 2020"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Additional Details</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    name={`education[${eduIndex}].details`}
                    value={edu.details}
                    onChange={handleNestedChange}
                    placeholder="e.g., GPA, honors, relevant coursework, etc."
                  />
                </Form.Group>
              </Col>
            </Row>
          </div>
        ))}
        
        <Button
          variant="primary"
          onClick={addEducation}
          className="w-100 mt-3"
        >
          + Add Education
        </Button>
      </Card.Body>
    </Card>
  );
};

const SkillsSection = ({ formData, setFormData, handleChange, handleAISkills, isGeneratingSkills }) => {
  const [newSkill, setNewSkill] = useState("");

  const addSkill = () => {
    if (newSkill.trim()) {
      setFormData({
        ...formData,
        skills: [...formData.skills, newSkill.trim()]
      });
      setNewSkill("");
    }
  };

  const removeSkill = (index) => {
    const updatedSkills = [...formData.skills];
    updatedSkills.splice(index, 1);
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill();
    }
  };

  return (
    <Card className="form-section">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <div>Skills</div>
        <Button
          variant="outline-primary"
          size="sm"
          onClick={handleAISkills}
          disabled={isGeneratingSkills || !formData.work_experience[0]?.title}
        >
          {isGeneratingSkills ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              <span className="ms-2">Suggesting Skills...</span>
            </>
          ) : (
            "Suggest Skills with AI"
          )}
        </Button>
      </Card.Header>
      <Card.Body>
        <div className="skills-input-container mb-3">
          <Form.Control
            type="text"
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Add a skill (e.g., JavaScript, Project Management)"
          />
          <Button 
            variant="outline-primary"
            onClick={addSkill}
            disabled={!newSkill.trim()}
          >
            Add
          </Button>
        </div>
        
        {formData.skills.length === 0 && (
          <p className="text-muted">No skills added yet. Add skills that are relevant to your target job.</p>
        )}
        
        <div className="skills-list">
          {formData.skills.map((skill, index) => (
            <div key={index} className="skill-tag">
              {skill}
              <Button 
                variant="link" 
                className="skill-remove-btn"
                onClick={() => removeSkill(index)}
              >
                &times;
              </Button>
            </div>
          ))}
        </div>
      </Card.Body>
    </Card>
  );
};

const ProjectsSection = ({ formData, setFormData, handleNestedChange }) => {
  const addProject = () => {
    const newProject = {
      name: "",
      date: "",
      description: ""
    };
    setFormData({
      ...formData,
      projects: [...formData.projects, newProject]
    });
  };

  const removeProject = (index) => {
    const updatedProjects = [...formData.projects];
    updatedProjects.splice(index, 1);
    setFormData({
      ...formData,
      projects: updatedProjects
    });
  };

  return (
    <Card className="form-section">
      <Card.Header>Projects</Card.Header>
      <Card.Body>
        {formData.projects.map((project, projectIndex) => (
          <div key={projectIndex} className="project-entry mb-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Project {projectIndex + 1}</h5>
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => removeProject(projectIndex)}
              >
                Remove
              </Button>
            </div>
            <Row>
              <Col md={8}>
                <Form.Group className="mb-3">
                  <Form.Label>Project Name</Form.Label>
                  <Form.Control
                    type="text"
                    name={`projects[${projectIndex}].name`}
                    value={project.name}
                    onChange={handleNestedChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Date</Form.Label>
                  <Form.Control
                    type="text"
                    name={`projects[${projectIndex}].date`}
                    value={project.date}
                    onChange={handleNestedChange}
                    placeholder="e.g., June 2023"
                  />
                </Form.Group>
              </Col>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>Description</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    name={`projects[${projectIndex}].description`}
                    value={project.description}
                    onChange={handleNestedChange}
                    placeholder="Describe the project, your role, technologies used, and outcomes..."
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
          </div>
        ))}
        
        <Button
          variant="primary"
          onClick={addProject}
          className="w-100 mt-3"
        >
          + Add Project
        </Button>
      </Card.Body>
    </Card>
  );
};

function ResumeForm({ onSubmit, initialData, templateId, resumeTitle }) {
  const emptyResumeData = {
    personal_info: {
      name: "",
      email: "",
      phone: "",
      location: "",
      linkedin: "",
      website: ""
    },
    summary: "",
    work_experience: [
      {
        title: "",
        company: "",
        start_date: "",
        end_date: "",
        responsibilities: [""]
      }
    ],
    education: [
      {
        degree: "",
        institution: "",
        start_date: "",
        end_date: "",
        details: ""
      }
    ],
    skills: [],
    projects: []
  };

  const [formData, setFormData] = useState(initialData || emptyResumeData);
  const [alert, setAlert] = useState({ show: false, message: "", variant: "" });
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [isImprovingJob, setIsImprovingJob] = useState(null);
  const [isGeneratingSkills, setIsGeneratingSkills] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Handle simple form field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData({
        ...formData,
        [parent]: {
          ...formData[parent],
          [child]: value
        }
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  // Handle nested form fields (arrays and objects)
  const handleNestedChange = (e) => {
    const { name, value } = e.target;
    
    // Match patterns like 'work_experience[0].title' or 'work_experience[0].responsibilities[1]'
    const match = name.match(/([a-zA-Z_]+)\[(\d+)\]\.([a-zA-Z_]+)(?:\[(\d+)\])?/);
    
    if (match) {
      const [_, section, index, property, subIndex] = match;
      const sectionIndex = parseInt(index);
      
      if (subIndex !== undefined) {
        // Handle nested arrays (e.g., responsibilities)
        const subIndexInt = parseInt(subIndex);
        const updatedSection = [...formData[section]];
        updatedSection[sectionIndex][property][subIndexInt] = value;
        
        setFormData({
          ...formData,
          [section]: updatedSection
        });
      } else {
        // Handle first-level nesting
        const updatedSection = [...formData[section]];
        updatedSection[sectionIndex] = {
          ...updatedSection[sectionIndex],
          [property]: value
        };
        
        setFormData({
          ...formData,
          [section]: updatedSection
        });
      }
    }
  };

  // Generate summary using AI
  const handleGenerateSummary = async () => {
    // Ensure we have enough data to generate a good summary
    if (!formData.personal_info.name || !formData.work_experience[0].title) {
      setAlert({
        show: true,
        message: "Please add your name and at least one job title to generate a summary.",
        variant: "warning"
      });
      return;
    }

    try {
      setIsGeneratingSummary(true);
      
      // Extract latest job title and skills
      const jobTitle = formData.work_experience[0].title;
      
      // Calculate approximate years of experience from work history
      let yearsExperience = formData.work_experience.reduce((total, job) => {
        if (job.start_date && (job.end_date || "present")) {
          // Very basic calculation - could be improved
          const startYear = parseInt(job.start_date.match(/\d{4}/)?.[0] || "0");
          const endYear = job.end_date?.toLowerCase() === "present" 
            ? new Date().getFullYear() 
            : parseInt(job.end_date.match(/\d{4}/)?.[0] || "0");
          
          if (startYear && endYear) {
            return total + (endYear - startYear);
          }
        }
        return total;
      }, 0);
      
      if (yearsExperience === 0) {
        yearsExperience = 3; // Default if we couldn't calculate
      }
      
      const response = await apiService.post('/ai/generate-summary', {
        job_title: jobTitle,
        experience_years: yearsExperience,
        skills: formData.skills.length ? formData.skills : ["your key skills"]
      });
      
      setFormData({
        ...formData,
        summary: response.data.content
      });
      
      setAlert({
        show: true,
        message: "Summary generated successfully! Feel free to edit it further.",
        variant: "success"
      });
    } catch (error) {
      console.error('Error generating summary:', error);
      setAlert({
        show: true,
        message: "Failed to generate summary. Please try again or write your own.",
        variant: "danger"
      });
    } finally {
      setIsGeneratingSummary(false);
    }
  };

  // Improve job descriptions using AI
  const handleImproveJobDescriptions = async (jobIndex) => {
    const job = formData.work_experience[jobIndex];
    
    if (!job.title || !job.company || job.responsibilities.filter(r => r.trim()).length === 0) {
      setAlert({
        show: true,
        message: "Please add job title, company, and at least one responsibility to improve.",
        variant: "warning"
      });
      return;
    }

    try {
      setIsImprovingJob(jobIndex);
      
      // Calculate approximate years in this role
      let yearsInRole = 1; // Default
      if (job.start_date && (job.end_date || "present")) {
        const startYear = parseInt(job.start_date.match(/\d{4}/)?.[0] || "0");
        const endYear = job.end_date?.toLowerCase() === "present" 
          ? new Date().getFullYear() 
          : parseInt(job.end_date.match(/\d{4}/)?.[0] || "0");
        
        if (startYear && endYear) {
          yearsInRole = Math.max(1, endYear - startYear);
        }
      }
      
      const response = await apiService.post('/ai/generate-job-descriptions', {
        job_title: job.title,
        company_name: job.company,
        responsibilities: job.responsibilities.filter(r => r.trim()),
        years_experience: yearsInRole
      });
      
      if (response.data.descriptions && response.data.descriptions.length > 0) {
        const updatedExperience = [...formData.work_experience];
        updatedExperience[jobIndex].responsibilities = response.data.descriptions;
        
        setFormData({
          ...formData,
          work_experience: updatedExperience
        });
        
        setAlert({
          show: true,
          message: "Job descriptions improved successfully!",
          variant: "success"
        });
      }
    } catch (error) {
      console.error('Error improving job descriptions:', error);
      setAlert({
        show: true,
        message: "Failed to improve job descriptions. Please try again or edit them manually.",
        variant: "danger"
      });
    } finally {
      setIsImprovingJob(null);
    }
  };

  // Generate relevant skills using AI
  const handleGenerateSkills = async () => {
    if (!formData.work_experience[0].title) {
      setAlert({
        show: true,
        message: "Please add at least one job title to suggest relevant skills.",
        variant: "warning"
      });
      return;
    }

    try {
      setIsGeneratingSkills(true);
      
      // Get the most recent job title
      const jobTitle = formData.work_experience[0].title;
      
      const response = await apiService.post('/ai/get-relevant-skills', {
        job_title: jobTitle,
        experience_level: "mid-level" // Could be determined based on work history
      });
      
      if (response.data.skills && response.data.skills.length > 0) {
        // Merge existing skills with AI suggestions, removing duplicates
        const existingSkills = new Set(formData.skills.map(s => s.toLowerCase()));
        const newSkills = response.data.skills.filter(
          skill => !existingSkills.has(skill.toLowerCase())
        );
        
        setFormData({
          ...formData,
          skills: [...formData.skills, ...newSkills]
        });
        
        setAlert({
          show: true,
          message: `Added ${newSkills.length} suggested skills to your resume.`,
          variant: "success"
        });
      }
    } catch (error) {
      console.error('Error generating skills:', error);
      setAlert({
        show: true,
        message: "Failed to suggest skills. Please try again or add them manually.",
        variant: "danger"
      });
    } finally {
      setIsGeneratingSkills(false);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form data
    if (!formData.personal_info.name || !formData.personal_info.email) {
      setAlert({
        show: true,
        message: "Please fill in your name and email address.",
        variant: "warning"
      });
      return;
    }
    
    try {
      setIsSubmitting(true);
      
      // Prepare resume data for submission
      const resumeData = {
        title: resumeTitle || "My Resume",
        current_template_id: templateId,
        content: formData
      };
      
      // Pass the data to the parent component
      await onSubmit(resumeData);
      
      setAlert({
        show: true,
        message: "Resume saved successfully!",
        variant: "success"
      });
    } catch (error) {
      console.error('Error saving resume:', error);
      setAlert({
        show: true,
        message: "Failed to save resume. Please try again.",
        variant: "danger"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="resume-form">
      <h2 className="form-title">Build Your Resume</h2>
      
      {alert.show && (
        <Alert variant={alert.variant} onClose={() => setAlert({ ...alert, show: false })} dismissible>
          {alert.message}
        </Alert>
      )}
      
      <Form onSubmit={handleSubmit}>
        <PersonalInfoSection formData={formData} handleChange={handleChange} />
        
        <SummarySection 
          formData={formData} 
          handleChange={handleChange} 
          handleAIGenerate={handleGenerateSummary}
          isGenerating={isGeneratingSummary}
        />
        
        <WorkExperienceSection 
          formData={formData} 
          setFormData={setFormData} 
          handleNestedChange={handleNestedChange}
          handleAIImprove={handleImproveJobDescriptions}
          isImproving={isImprovingJob}
        />
        
        <EducationSection 
          formData={formData} 
          setFormData={setFormData} 
          handleNestedChange={handleNestedChange} 
        />
        
        <SkillsSection 
          formData={formData} 
          setFormData={setFormData} 
          handleChange={handleChange}
          handleAISkills={handleGenerateSkills}
          isGeneratingSkills={isGeneratingSkills}
        />
        
        <ProjectsSection 
          formData={formData} 
          setFormData={setFormData} 
          handleNestedChange={handleNestedChange} 
        />
        
        <div className="form-actions">
          <Button 
            variant="primary" 
            type="submit" 
            size="lg" 
            disabled={isSubmitting}
            className="save-btn"
          >
            {isSubmitting ? (
              <>
                <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                <span className="ms-2">Saving...</span>
              </>
            ) : (
              "Save Resume"
            )}
          </Button>
        </div>
      </Form>
    </div>
  );
}

export default ResumeForm; 