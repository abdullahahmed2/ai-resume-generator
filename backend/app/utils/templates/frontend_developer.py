"""
Frontend Developer resume template with a creative yet professional design
optimized for ATS systems and highlighting frontend skills and design sensibility.
"""

def get_html_template():
    return """
    <div class="resume">
        <div class="header">
            <div class="name-title">
                <h1>{{ personal_info.name }}</h1>
                <div class="title-bar">Frontend Developer</div>
            </div>
            <div class="contact-info">
                <div class="contact-item">
                    <span class="contact-icon">📧</span>
                    <span>{{ personal_info.email }}</span>
                </div>
                <div class="contact-item">
                    <span class="contact-icon">📱</span>
                    <span>{{ personal_info.phone }}</span>
                </div>
                <div class="contact-item">
                    <span class="contact-icon">📍</span>
                    <span>{{ personal_info.location }}</span>
                </div>
                {% if personal_info.linkedin %}
                <div class="contact-item">
                    <span class="contact-icon">🔗</span>
                    <span>{{ personal_info.linkedin }}</span>
                </div>
                {% endif %}
                {% if personal_info.website %}
                <div class="contact-item">
                    <span class="contact-icon">🌐</span>
                    <span>{{ personal_info.website }}</span>
                </div>
                {% endif %}
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2>About Me</h2>
            <div class="summary">
                <p>{{ summary }}</p>
            </div>
        </div>
        {% endif %}
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2>Technical Skills</h2>
            <div class="skills-section">
                <div class="skills-container">
                    {% for skill in skills %}
                    <div class="skill-badge">{{ skill }}</div>
                    {% endfor %}
                </div>
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
                <ul class="job-details">
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
            <div class="projects-grid">
                {% for project in projects %}
                <div class="project-card">
                    <div class="project-header">
                        <h3>{{ project.name }}</h3>
                        {% if project.date %}
                        <span class="project-date">{{ project.date }}</span>
                        {% endif %}
                    </div>
                    <p class="project-description">{{ project.description }}</p>
                </div>
                {% endfor %}
            </div>
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
    /* Frontend Developer Resume Template */
    :root {
        --primary-color: #8b5cf6;
        --primary-light: #ddd6fe;
        --primary-dark: #5b21b6;
        --secondary-color: #f0abfc;
        --secondary-light: #fce7f3;
        --dark-color: #1e293b;
        --text-color: #334155;
        --light-text: #64748b;
        --background-color: #ffffff;
    }
    
    body {
        font-family: 'Inter', 'Roboto', 'Open Sans', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: var(--text-color);
        background-color: var(--background-color);
        margin: 0;
        padding: 0;
    }
    
    .resume {
        max-width: 8.5in;
        margin: 0 auto;
        padding: 0.5in;
    }
    
    /* Header Section */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid var(--primary-light);
    }
    
    .name-title {
        flex: 1;
    }
    
    .header h1 {
        font-size: 24pt;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 5px 0;
        letter-spacing: 0.5px;
    }
    
    .title-bar {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 10pt;
        display: inline-block;
    }
    
    .contact-info {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 9pt;
        color: var(--light-text);
    }
    
    .contact-icon {
        color: var(--primary-color);
    }
    
    /* Sections */
    .section {
        margin-bottom: 20px;
        page-break-inside: avoid;
    }
    
    .section h2 {
        font-size: 14pt;
        font-weight: 600;
        color: var(--primary-dark);
        position: relative;
        padding-bottom: 5px;
        margin: 0 0 15px 0;
    }
    
    .section h2::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        width: 40px;
        height: 3px;
        background-color: var(--primary-color);
        border-radius: 3px;
    }
    
    /* Summary */
    .summary p {
        margin: 0;
        font-size: 10.5pt;
        line-height: 1.6;
    }
    
    /* Skills */
    .skills-section {
        margin-top: 15px;
    }
    
    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .skill-badge {
        background: linear-gradient(135deg, var(--primary-light), var(--primary-light));
        color: var(--primary-dark);
        border: 1px solid var(--primary-color);
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 9.5pt;
        font-weight: 500;
        text-align: center;
    }
    
    /* Experience */
    .experience-item, .education-item {
        margin-bottom: 18px;
        position: relative;
    }
    
    .job-header, .education-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 5px;
    }
    
    .job-title-company, .degree-institution {
        flex: 1;
    }
    
    .job-date, .education-date {
        text-align: right;
        white-space: nowrap;
        color: var(--light-text);
        font-size: 9pt;
        font-style: italic;
    }
    
    h3 {
        font-size: 12pt;
        font-weight: 600;
        color: var(--dark-color);
        margin: 0;
    }
    
    h4 {
        font-size: 10.5pt;
        font-weight: 500;
        color: var(--primary-color);
        margin: 0;
    }
    
    .job-details {
        margin: 5px 0 0 20px;
        padding: 0;
    }
    
    .job-details li {
        font-size: 10pt;
        margin-bottom: 4px;
        position: relative;
    }
    
    /* Projects */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
    
    .project-card {
        background-color: var(--primary-light);
        padding: 12px;
        border-radius: 6px;
        position: relative;
    }
    
    .project-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 5px;
    }
    
    .project-date {
        font-size: 9pt;
        color: var(--light-text);
        font-style: italic;
    }
    
    .project-description {
        margin: 0;
        font-size: 9.5pt;
    }
    
    /* Education */
    .education-item p {
        margin: 5px 0 0 0;
        font-size: 10pt;
    }
    
    /* Media Queries for Print */
    @media print {
        .resume {
            padding: 0;
        }
    }
    """


def get_template_metadata():
    return {
        "name": "Creative Frontend Developer",
        "description": "A visually appealing template with a modern design that showcases UI/UX sensibilities for frontend developer roles.",
        "role_type": "frontend_developer",
        "is_default": True
    } 