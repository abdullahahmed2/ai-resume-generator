"""
Software Engineer resume template with modern, clean design
optimized for ATS systems and highlighting technical skills.
"""

def get_html_template():
    return """
    <div class="resume">
        <div class="header">
            <h1>{{ personal_info.name }}</h1>
            <div class="contact-info">
                <div class="contact-row">
                    <span>{{ personal_info.email }}</span>
                    <span>{{ personal_info.phone }}</span>
                </div>
                <div class="contact-row">
                    <span>{{ personal_info.location }}</span>
                    {% if personal_info.linkedin %}
                    <span>LinkedIn: {{ personal_info.linkedin }}</span>
                    {% endif %}
                    {% if personal_info.website %}
                    <span>Portfolio: {{ personal_info.website }}</span>
                    {% endif %}
                </div>
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2>Summary</h2>
            <div class="summary">
                <p>{{ summary }}</p>
            </div>
        </div>
        {% endif %}
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2>Technical Skills</h2>
            <div class="skills-container">
                {% for skill in skills %}
                <span class="skill-tag">{{ skill }}</span>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if work_experience and work_experience|length > 0 %}
        <div class="section">
            <h2>Work Experience</h2>
            {% for job in work_experience %}
            <div class="experience-item">
                <div class="job-header">
                    <div class="job-title-company">
                        <h3>{{ job.title }}</h3>
                        <h4>{{ job.company }}</h4>
                    </div>
                    <div class="job-date">
                        <span>{{ job.start_date }} - {{ job.end_date if job.end_date else 'Present' }}</span>
                    </div>
                </div>
                <ul class="responsibilities">
                    {% for responsibility in job.responsibilities %}
                    <li>{{ responsibility }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if projects and projects|length > 0 %}
        <div class="section">
            <h2>Projects</h2>
            {% for project in projects %}
            <div class="project-item">
                <div class="project-header">
                    <h3>{{ project.name }}</h3>
                    {% if project.date %}
                    <span class="project-date">{{ project.date }}</span>
                    {% endif %}
                </div>
                <p>{{ project.description }}</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if education and education|length > 0 %}
        <div class="section">
            <h2>Education</h2>
            {% for edu in education %}
            <div class="education-item">
                <div class="education-header">
                    <div class="degree-institution">
                        <h3>{{ edu.degree }}</h3>
                        <h4>{{ edu.institution }}</h4>
                    </div>
                    <div class="education-date">
                        <span>{{ edu.start_date }} - {{ edu.end_date if edu.end_date else 'Present' }}</span>
                    </div>
                </div>
                {% if edu.details %}
                <p>{{ edu.details }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    """


def get_css_template():
    return """
    /* Software Engineer Resume Template */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #dbeafe;
        --dark-color: #1e293b;
        --text-color: #334155;
        --light-text: #64748b;
        --background-color: #ffffff;
        --section-border: #e2e8f0;
    }
    
    body {
        font-family: 'Inter', 'Roboto', 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: var(--text-color);
        background-color: var(--background-color);
        margin: 0;
        padding: 0;
    }
    
    .resume {
        max-width: 8.5in;
        margin: 0 auto;
        padding: 0.6in;
    }
    
    /* Header Section */
    .header {
        margin-bottom: 20px;
    }
    
    .header h1 {
        font-size: 18pt;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 10px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .contact-info {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .contact-row {
        display: flex;
        justify-content: flex-start;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .contact-row span {
        font-size: 10pt;
        color: var(--light-text);
    }
    
    /* Sections */
    .section {
        margin-bottom: 16px;
        page-break-inside: avoid;
    }
    
    .section h2 {
        font-size: 12pt;
        font-weight: 600;
        color: var(--dark-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 4px;
        margin: 0 0 10px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Summary */
    .summary p {
        margin: 0;
        font-size: 10pt;
        text-align: justify;
    }
    
    /* Skills */
    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .skill-tag {
        background-color: var(--secondary-color);
        color: var(--primary-color);
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 9pt;
        font-weight: 500;
    }
    
    /* Experience */
    .experience-item, .project-item, .education-item {
        margin-bottom: 14px;
    }
    
    .job-header, .project-header, .education-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 4px;
    }
    
    .job-title-company, .degree-institution {
        flex: 1;
    }
    
    .job-date, .project-date, .education-date {
        text-align: right;
        white-space: nowrap;
        color: var(--light-text);
        font-size: 9pt;
        font-style: italic;
    }
    
    h3 {
        font-size: 11pt;
        font-weight: 600;
        color: var(--dark-color);
        margin: 0;
    }
    
    h4 {
        font-size: 10pt;
        font-weight: 400;
        color: var(--primary-color);
        margin: 0;
    }
    
    .responsibilities {
        margin: 4px 0 0 20px;
        padding: 0;
    }
    
    .responsibilities li {
        font-size: 10pt;
        margin-bottom: 3px;
        position: relative;
    }
    
    .project-item p, .education-item p {
        margin: 5px 0 0 0;
        font-size: 10pt;
    }
    """


def get_template_metadata():
    return {
        "name": "Modern Software Engineer",
        "description": "A clean, technical template highlighting skills and projects for software engineering roles.",
        "role_type": "software_engineer",
        "is_default": True
    } 