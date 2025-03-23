import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import TemplateSelector from '../components/ResumeBuilder/TemplateSelector';
import ResumeForm from '../components/ResumeBuilder/ResumeForm';
import PDFUploader from '../components/ResumeBuilder/PDFUploader';
import { apiService } from '../services/apiService';
import '../styles/CreateResume.css';

function CreateResume() {
  const { id } = useParams(); // For editing existing resume
  const navigate = useNavigate();
  
  const [step, setStep] = useState(id ? 2 : 1); // 1: Template, 2: Form
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [resumeTitle, setResumeTitle] = useState('My Resume');
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  // If we have an ID, fetch the existing resume
  useEffect(() => {
    if (id) {
      fetchResumeData(id);
    }
  }, [id]);

  const fetchResumeData = async (resumeId) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.get(`/resume/${resumeId}`);
      const resumeData = response.data;
      
      setResumeTitle(resumeData.title);
      setSelectedTemplate(resumeData.current_template_id);
      setInitialData(resumeData.content);
      
      setLoading(false);
    } catch (err) {
      console.error('Error fetching resume:', err);
      setError('Failed to load resume data. Please try again.');
      setLoading(false);
    }
  };

  const handleTemplateSelect = (templateId) => {
    setSelectedTemplate(templateId);
  };

  const handleContinue = () => {
    if (!selectedTemplate) {
      setError('Please select a template to continue.');
      return;
    }
    
    setError(null);
    setStep(2);
  };

  const handleBack = () => {
    setStep(1);
  };

  const handleParsedData = (data) => {
    setInitialData(data);
    setStep(2);
  };

  const handleSaveResume = async (resumeData) => {
    try {
      setLoading(true);
      setError(null);
      
      let response;
      
      if (id) {
        // Update existing resume
        response = await apiService.put(`/resume/${id}`, resumeData);
      } else {
        // Create new resume with content
        response = await apiService.createResumeWithContent(resumeData);
      }
      
      setSuccess(true);
      
      // Redirect to dashboard after a short delay
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
      
      setLoading(false);
    } catch (err) {
      console.error('Error saving resume:', err);
      setError('Failed to save resume. Please try again.');
      setLoading(false);
    }
  };

  if (loading && !initialData) {
    return (
      <Container className="mt-5 text-center">
        <div className="spinner-container">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </Container>
    );
  }

  return (
    <Container className="create-resume-container">
      <Row className="mb-4">
        <Col>
          <h1 className="page-title">{id ? 'Edit Resume' : 'Create New Resume'}</h1>
          <div className="progress-tracker">
            <div className={`progress-step ${step >= 1 ? 'active' : ''}`}>
              <div className="step-number">1</div>
              <div className="step-label">Choose Template</div>
            </div>
            <div className="progress-connector"></div>
            <div className={`progress-step ${step >= 2 ? 'active' : ''}`}>
              <div className="step-number">2</div>
              <div className="step-label">Fill Details</div>
            </div>
          </div>
        </Col>
      </Row>
      
      {error && (
        <Row className="mb-4">
          <Col>
            <Alert variant="danger" onClose={() => setError(null)} dismissible>
              {error}
            </Alert>
          </Col>
        </Row>
      )}
      
      {success && (
        <Row className="mb-4">
          <Col>
            <Alert variant="success" onClose={() => setSuccess(false)} dismissible>
              Resume saved successfully! Redirecting to dashboard...
            </Alert>
          </Col>
        </Row>
      )}
      
      {step === 1 && (
        <>
          <Row className="mb-4">
            <Col>
              <Card className="title-card">
                <Card.Body>
                  <Form.Group>
                    <Form.Label>Resume Title</Form.Label>
                    <Form.Control
                      type="text"
                      value={resumeTitle}
                      onChange={(e) => setResumeTitle(e.target.value)}
                      placeholder="Enter a title for your resume"
                    />
                  </Form.Group>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row className="mb-4">
            <Col md={4}>
              <PDFUploader onParsedData={handleParsedData} />
            </Col>
            <Col md={8}>
              <TemplateSelector 
                selectedId={selectedTemplate}
                onSelect={handleTemplateSelect}
              />
            </Col>
          </Row>
          
          <Row className="text-center mt-4">
            <Col>
              <Button 
                variant="primary" 
                size="lg" 
                onClick={handleContinue}
                className="continue-btn"
              >
                Continue to Next Step
              </Button>
            </Col>
          </Row>
        </>
      )}
      
      {step === 2 && (
        <>
          <Row className="mb-3">
            <Col>
              <Button 
                variant="outline-secondary" 
                onClick={handleBack}
                className="back-btn"
              >
                &larr; Back to Templates
              </Button>
            </Col>
          </Row>
          
          <Row>
            <Col>
              <ResumeForm
                onSubmit={handleSaveResume}
                initialData={initialData}
                templateId={selectedTemplate}
                resumeTitle={resumeTitle}
              />
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
}

export default CreateResume; 