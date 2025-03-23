import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Spinner } from 'react-bootstrap';
import { apiService } from '../../services/apiService';
import '../../styles/TemplateSelector.css';

function TemplateSelector({ onSelectTemplate, selectedTemplateId }) {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch templates from the API
    const fetchTemplates = async () => {
      try {
        setLoading(true);
        const response = await apiService.get('/template/list');
        setTemplates(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching templates:', err);
        setError('Failed to load templates. Please try again later.');
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  const handleSelectTemplate = (templateId) => {
    onSelectTemplate(templateId);
  };

  if (loading) {
    return (
      <div className="template-loader">
        <Spinner animation="border" variant="primary" />
        <p>Loading templates...</p>
      </div>
    );
  }

  if (error) {
    return <div className="template-error">{error}</div>;
  }

  // Group templates by role type
  const groupedTemplates = templates.reduce((acc, template) => {
    const roleType = template.role_type || 'general';
    if (!acc[roleType]) {
      acc[roleType] = [];
    }
    acc[roleType].push(template);
    return acc;
  }, {});

  // Format role type for display
  const formatRoleType = (roleType) => {
    return roleType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="template-selector">
      <h3 className="section-title">Choose a Resume Template</h3>
      <p className="section-description">
        Select a template tailored to your target role or industry.
      </p>

      {Object.keys(groupedTemplates).map((roleType) => (
        <div key={roleType} className="template-category">
          <h4 className="role-title">{formatRoleType(roleType)} Templates</h4>
          <Row xs={1} md={2} lg={3} className="g-4">
            {groupedTemplates[roleType].map((template) => (
              <Col key={template.id}>
                <Card 
                  className={`template-card ${selectedTemplateId === template.id ? 'selected' : ''}`}
                  onClick={() => handleSelectTemplate(template.id)}
                >
                  <div className="template-preview">
                    <div className="preview-placeholder">
                      {/* This would ideally show a thumbnail of the template */}
                      <span className="template-icon">📄</span>
                    </div>
                  </div>
                  <Card.Body>
                    <Card.Title>{template.name}</Card.Title>
                    <Card.Text>{template.description}</Card.Text>
                    <Button 
                      variant={selectedTemplateId === template.id ? "primary" : "outline-primary"}
                      className="select-btn"
                    >
                      {selectedTemplateId === template.id ? "Selected" : "Select"}
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      ))}
    </div>
  );
}

export default TemplateSelector; 