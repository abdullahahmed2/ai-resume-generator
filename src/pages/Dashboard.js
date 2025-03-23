import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { resumeAPI } from '../services/api';
import '../styles/Dashboard.css';

function Dashboard() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  // Fetch user's resumes on component mount
  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await resumeAPI.getResumes();
      setResumes(response.data);
    } catch (err) {
      console.error('Error fetching resumes:', err);
      setError('Failed to fetch your resumes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this resume?')) {
      try {
        await resumeAPI.deleteResume(id);
        // Update the list of resumes
        setResumes(resumes.filter(resume => resume.id !== id));
      } catch (err) {
        console.error('Error deleting resume:', err);
        setError('Failed to delete the resume. Please try again.');
      }
    }
  };

  const handleDownload = async (versionId, resumeTitle) => {
    try {
      const response = await resumeAPI.downloadPdf(versionId);
      
      // Create a blob from the PDF data
      const blob = new Blob([response.data], { type: 'application/pdf' });
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob);
      
      // Create a link element
      const link = document.createElement('a');
      link.href = url;
      link.download = `${resumeTitle}.pdf`;
      
      // Append the link to the body, click it, and remove it
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Free up the URL
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading PDF:', err);
      setError('Failed to download the PDF. Please try again.');
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading your resumes...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>My Resumes</h1>
        <Link to="/resume/new" className="btn-primary">
          Create New Resume
        </Link>
      </div>
      
      {error && <div className="dashboard-error">{error}</div>}
      
      {resumes.length === 0 ? (
        <div className="empty-state">
          <h2>You don't have any resumes yet</h2>
          <p>Create your first resume to get started.</p>
          <Link to="/resume/new" className="btn-primary">
            Create Resume
          </Link>
        </div>
      ) : (
        <div className="resume-grid">
          {resumes.map(resume => {
            // Get the latest version ID for download
            const latestVersionId = resume.versions && resume.versions.length > 0 
              ? resume.versions[0].id 
              : null;
              
            return (
              <div key={resume.id} className="resume-card">
                <div className="resume-card-header">
                  <h3>{resume.title}</h3>
                  <span className="resume-date">
                    Last updated: {new Date(resume.updated_at || resume.created_at).toLocaleDateString()}
                  </span>
                </div>
                
                <div className="resume-card-actions">
                  <button 
                    onClick={() => navigate(`/resume/edit/${resume.id}`)}
                    className="btn-edit"
                  >
                    Edit
                  </button>
                  
                  {latestVersionId && (
                    <button 
                      onClick={() => handleDownload(latestVersionId, resume.title)}
                      className="btn-download"
                    >
                      Download PDF
                    </button>
                  )}
                  
                  <button 
                    onClick={() => navigate(`/resume/share/${resume.id}`)}
                    className="btn-share"
                  >
                    Share
                  </button>
                  
                  <button 
                    onClick={() => handleDelete(resume.id)}
                    className="btn-delete"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Dashboard; 