import React, { useState } from 'react';
import { Card, Button, Form, Alert, Spinner, ProgressBar } from 'react-bootstrap';
import { apiService } from '../../services/apiService';
import '../../styles/PDFUploader.css';

function PDFUploader({ onParsedData }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    // Reset states
    setError(null);
    setSuccess(false);
    setUploadProgress(0);
    
    // Validate file type
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      setError('Please select a PDF file.');
      setFile(null);
      e.target.value = null; // Reset the input
      return;
    }
    
    // Validate file size (max 5MB)
    if (selectedFile && selectedFile.size > 5 * 1024 * 1024) {
      setError('File size exceeds 5MB limit.');
      setFile(null);
      e.target.value = null; // Reset the input
      return;
    }
    
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file to upload.');
      return;
    }

    try {
      setIsUploading(true);
      setError(null);
      setSuccess(false);
      
      // Create FormData object to send the file
      const formData = new FormData();
      formData.append('file', file);

      // Configure request with progress tracking
      const config = {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      };

      // Upload the file
      const response = await apiService.post('/resume/upload-pdf', formData, config);
      
      // Handle successful response
      if (response.data) {
        setSuccess(true);
        
        // Pass the parsed data to the parent component
        onParsedData(response.data);
      }
    } catch (err) {
      console.error('Error uploading PDF:', err);
      
      // Handle API error
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to upload and parse the PDF. Please try again.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="pdf-uploader">
      <Card.Header>
        <h5>Upload Existing Resume</h5>
      </Card.Header>
      <Card.Body>
        <p className="upload-description">
          Upload an existing PDF resume to import its content. Our system will analyze and extract information to save you time.
        </p>
        
        {error && (
          <Alert variant="danger" onClose={() => setError(null)} dismissible>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert variant="success" onClose={() => setSuccess(false)} dismissible>
            Resume parsed successfully! You can now edit the extracted information.
          </Alert>
        )}
        
        <div className="upload-container">
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>Select your resume PDF</Form.Label>
            <Form.Control 
              type="file" 
              onChange={handleFileChange} 
              accept="application/pdf"
              disabled={isUploading}
            />
            <Form.Text className="text-muted">
              Maximum file size: 5MB. Only PDF files are supported.
            </Form.Text>
          </Form.Group>
          
          {isUploading && (
            <div className="upload-progress">
              <ProgressBar now={uploadProgress} label={`${uploadProgress}%`} animated />
              <p className="progress-text">Uploading and parsing resume...</p>
            </div>
          )}
          
          <Button 
            variant="primary" 
            onClick={handleUpload} 
            disabled={!file || isUploading}
            className="upload-btn"
          >
            {isUploading ? (
              <>
                <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                <span className="ms-2">Processing...</span>
              </>
            ) : (
              "Upload and Parse Resume"
            )}
          </Button>
        </div>
        
        <div className="upload-note">
          <small>
            <strong>Note:</strong> The PDF parsing is not perfect and may require some manual adjustments after import. 
            For best results, use a simple, well-structured resume without complex formatting.
          </small>
        </div>
      </Card.Body>
    </Card>
  );
}

export default PDFUploader; 