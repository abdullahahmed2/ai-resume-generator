import React, { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Button, Card, Spinner, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faShare, faEdit, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import { apiService } from '../services/apiService';
import html2pdf from 'html2pdf.js';
import '../styles/ViewResume.css';

function ViewResume() {
  const { id } = useParams();
  const navigate = useNavigate();
  const resumeRef = useRef(null);
  
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [shareLink, setShareLink] = useState(null);
  const [showShareAlert, setShowShareAlert] = useState(false);

  useEffect(() => {
    fetchResume();
  }, [id]);

  const fetchResume = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.get(`/resume/${id}/preview`);
      setResume(response.data);
      
      setLoading(false);
    } catch (err) {
      console.error('Error fetching resume:', err);
      setError('Failed to load resume. Please try again.');
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!resumeRef.current) return;

    try {
      setIsGeneratingPDF(true);
      
      const element = resumeRef.current;
      const opt = {
        margin: [10, 10],
        filename: `${resume.title || 'resume'}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };
      
      await html2pdf().set(opt).from(element).save();
      
      setIsGeneratingPDF(false);
    } catch (err) {
      console.error('Error generating PDF:', err);
      setIsGeneratingPDF(false);
      setError('Failed to generate PDF. Please try again.');
    }
  };

  const handleEdit = () => {
    navigate(`/resume/edit/${id}`);
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleShare = async () => {
    try {
      const response = await apiService.post(`/resume/${id}/share`);
      setShareLink(response.data.share_url);
      setShowShareAlert(true);
    } catch (err) {
      console.error('Error sharing resume:', err);
      setError('Failed to create share link. Please try again.');
    }
  };

  const copyShareLink = () => {
    if (shareLink) {
      navigator.clipboard.writeText(shareLink);
      alert('Share link copied to clipboard!');
    }
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <div className="spinner-container">
          <Spinner animation="border" role="status" variant="primary" />
          <p className="mt-3">Loading your resume...</p>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          {error}
        </Alert>
        <Button variant="primary" onClick={handleBack}>
          <FontAwesomeIcon icon={faArrowLeft} className="me-2" />
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  return (
    <Container className="view-resume-container">
      <Row className="mb-4">
        <Col>
          <Button variant="outline-secondary" onClick={handleBack} className="back-btn">
            <FontAwesomeIcon icon={faArrowLeft} className="me-2" />
            Back to Dashboard
          </Button>
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col>
          <Card className="resume-header">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center">
                <h1 className="resume-title">{resume?.title || 'My Resume'}</h1>
                <div className="resume-actions">
                  <Button 
                    variant="primary" 
                    onClick={handleEdit}
                    className="action-btn"
                  >
                    <FontAwesomeIcon icon={faEdit} className="me-2" />
                    Edit
                  </Button>
                  
                  <Button 
                    variant="success" 
                    onClick={handleDownloadPDF}
                    disabled={isGeneratingPDF}
                    className="action-btn"
                  >
                    {isGeneratingPDF ? (
                      <>
                        <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                        <span className="ms-2">Generating...</span>
                      </>
                    ) : (
                      <>
                        <FontAwesomeIcon icon={faDownload} className="me-2" />
                        Download PDF
                      </>
                    )}
                  </Button>
                  
                  <Button 
                    variant="info" 
                    onClick={handleShare}
                    className="action-btn"
                  >
                    <FontAwesomeIcon icon={faShare} className="me-2" />
                    Share
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      {showShareAlert && shareLink && (
        <Row className="mb-4">
          <Col>
            <Alert variant="info" onClose={() => setShowShareAlert(false)} dismissible>
              <Alert.Heading>Share your resume</Alert.Heading>
              <p>Anyone with this link can view your resume:</p>
              <div className="d-flex">
                <input 
                  type="text" 
                  value={shareLink} 
                  readOnly 
                  className="form-control share-link-input"
                />
                <Button variant="outline-secondary" onClick={copyShareLink}>
                  Copy
                </Button>
              </div>
            </Alert>
          </Col>
        </Row>
      )}
      
      <Row>
        <Col>
          <div className="resume-preview-container">
            <div 
              ref={resumeRef} 
              className="resume-preview"
              dangerouslySetInnerHTML={{ __html: resume?.preview_html || '<p>No preview available</p>' }}
            />
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default ViewResume; 