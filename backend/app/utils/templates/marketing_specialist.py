"""
Marketing Specialist resume template with a modern, creative design
optimized for ATS systems and highlighting marketing skills and achievements.
"""

def get_html_template():
    return """
    <div class="resume">
        <div class="header">
            <div class="name-container">
                <h1>{{ personal_info.name }}</h1>
                <div class="title-bar">Marketing Specialist</div>
            </div>
            <div class="contact-info">
                <div class="contact-group">
                    <div class="contact-item">
                        <span class="contact-label">Email:</span>
                        <span>{{ personal_info.email }}</span>
                    </div>
                    <div class="contact-item">
                        <span class="contact-label">Phone:</span>
                        <span>{{ personal_info.phone }}</span>
                    </div>
                </div>
                <div class="contact-group">
                    <div class="contact-item">
                        <span class="contact-label">Location:</span>
                        <span>{{ personal_info.location }}</span>
                    </div>
                    {% if personal_info.linkedin %}
                    <div class="contact-item">
                        <span class="contact-label">LinkedIn:</span>
                        <span>{{ personal_info.linkedin }}</span>
                    </div>
                    {% endif %}
                    {% if personal_info.website %}
                    <div class="contact-item">
                        <span class="contact-label">Portfolio:</span>
                        <span>{{ personal_info.website }}</span>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2><span class="section-marker"></span>Professional Profile</h2>
            <div class="summary">
                <p>{{ summary }}</p>
            </div>
        </div>
        {% endif %}
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2><span class="section-marker"></span>Key Marketing Skills</h2>
            <div class="skills-container">
                {% for skill in skills %}
                <div class="skill-badge">{{ skill }}</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if work_experience and work_experience|length > 0 %}
        <div class="section">
            <h2><span class="section-marker"></span>Marketing Experience</h2>
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
                <ul class="achievements">
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
            <h2><span class="section-marker"></span>Marketing Campaigns & Projects</h2>
            {% for project in projects %}
            <div class="project-item">
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
        {% endif %}
        
        {% if education and education|length > 0 %}
        <div class="section">
            <h2><span class="section-marker"></span>Education</h2>
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
    /* Marketing Specialist Resume Template */
    :root {
        --primary-color: #ec4899;
        --primary-light: #fce7f3;
        --primary-dark: #be185d;
        --secondary-color: #f472b6;
        --accent-color: #a855f7;
        --dark-color: #1e293b;
        --text-color: #334155;
        --light-text: #64748b;
        --background-color: #ffffff;
    }
    
    body {
        font-family: 'Montserrat', 'Open Sans', 'Helvetica Neue', sans-serif;
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
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 2px solid var(--primary-light);
    }
    
    .name-container {
        text-align: center;
    }
    
    .header h1 {
        font-size: 22pt;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 5px 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .title-bar {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        padding: 4px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 11pt;
        display: inline-block;
        margin: 5px auto;
    }
    
    .contact-info {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
    }
    
    .contact-group {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .contact-item {
        display: flex;
        gap: 5px;
        font-size: 9.5pt;
        align-items: center;
    }
    
    .contact-label {
        font-weight: 600;
        color: var(--primary-dark);
        min-width: 60px;
    }
    
    /* Sections */
    .section {
        margin-bottom: 20px;
        page-break-inside: avoid;
    }
    
    .section h2 {
        font-size: 13pt;
        font-weight: 600;
        color: var(--primary-dark);
        position: relative;
        padding-left: 15px;
        margin: 0 0 15px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
    }
    
    .section-marker {
        position: absolute;
        left: 0;
        width: 8px;
        height: 100%;
        background-color: var(--primary-color);
        border-radius: 4px;
    }
    
    /* Summary */
    .summary p {
        margin: 0;
        font-size: 10.5pt;
        line-height: 1.6;
        text-align: justify;
    }
    
    /* Skills */
    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }
    
    .skill-badge {
        background: linear-gradient(135deg, var(--primary-light), var(--primary-light));
        color: var(--primary-dark);
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 9.5pt;
        font-weight: 500;
        border: 1px solid var(--primary-color);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Experience */
    .experience-item, .project-item, .education-item {
        margin-bottom: 20px;
    }
    
    .job-header, .project-header, .education-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    
    .job-title-company, .degree-institution {
        flex: 1;
    }
    
    .job-date, .project-date, .education-date {
        text-align: right;
        white-space: nowrap;
        color: var(--light-text);
        font-size: 9.5pt;
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
        color: var(--accent-color);
        margin: 0;
    }
    
    .achievements {
        margin: 8px 0 0 20px;
        padding: 0;
    }
    
    .achievements li {
        font-size: 10pt;
        margin-bottom: 4px;
        position: relative;
    }
    
    .achievements li::marker {
        color: var(--primary-color);
    }
    
    /* Projects */
    .project-item {
        background-color: var(--primary-light);
        padding: 12px 15px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    
    .project-description {
        margin: 5px 0 0 0;
        font-size: 10pt;
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
        "name": "Creative Marketing Specialist",
        "description": "A colorful, engaging template that showcases marketing campaigns and digital skills for marketing roles.",
        "role_type": "marketing_specialist",
        "is_default": True
    } 