"""
Product Manager resume template with a modern, professional design
optimized for ATS systems and highlighting strategic and leadership skills.
"""

def get_html_template():
    return """
    <div class="resume">
        <div class="header">
            <h1>{{ personal_info.name }}</h1>
            <div class="contact-info">
                <div class="contact-row">
                    <span><i class="icon-email"></i>{{ personal_info.email }}</span>
                    <span><i class="icon-phone"></i>{{ personal_info.phone }}</span>
                </div>
                <div class="contact-row">
                    <span><i class="icon-location"></i>{{ personal_info.location }}</span>
                    {% if personal_info.linkedin %}
                    <span><i class="icon-linkedin"></i>{{ personal_info.linkedin }}</span>
                    {% endif %}
                    {% if personal_info.website %}
                    <span><i class="icon-website"></i>{{ personal_info.website }}</span>
                    {% endif %}
                </div>
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2>Professional Summary</h2>
            <div class="summary">
                <p>{{ summary }}</p>
            </div>
        </div>
        {% endif %}
        
        {% if work_experience and work_experience|length > 0 %}
        <div class="section">
            <h2>Professional Experience</h2>
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
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2>Core Competencies</h2>
            <div class="skills-grid">
                {% for skill in skills %}
                <div class="skill-item">{{ skill }}</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if projects and projects|length > 0 %}
        <div class="section">
            <h2>Key Products & Initiatives</h2>
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
    /* Product Manager Resume Template */
    :root {
        --primary-color: #0f766e;
        --secondary-color: #e2f8f5;
        --dark-color: #134e4a;
        --text-color: #1e293b;
        --light-text: #64748b;
        --background-color: #ffffff;
        --section-border: #cbd5e1;
    }
    
    body {
        font-family: 'Lato', 'Helvetica Neue', 'Arial', sans-serif;
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
        margin-bottom: 25px;
        text-align: center;
    }
    
    .header h1 {
        font-size: 22pt;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 12px 0;
        letter-spacing: 1px;
    }
    
    .contact-info {
        display: flex;
        flex-direction: column;
        gap: 5px;
        align-items: center;
    }
    
    .contact-row {
        display: flex;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
    }
    
    .contact-row span {
        font-size: 10pt;
        color: var(--light-text);
        display: flex;
        align-items: center;
    }
    
    /* Pseudo-elements for icons */
    .icon-email::before,
    .icon-phone::before,
    .icon-location::before,
    .icon-linkedin::before,
    .icon-website::before {
        content: "";
        display: inline-block;
        width: 14px;
        margin-right: 5px;
    }
    
    /* Sections */
    .section {
        margin-bottom: 20px;
        page-break-inside: avoid;
    }
    
    .section h2 {
        font-size: 13pt;
        font-weight: 600;
        color: var(--dark-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 5px;
        margin: 0 0 12px 0;
        text-transform: uppercase;
    }
    
    /* Summary */
    .summary p {
        margin: 0;
        font-size: 10.5pt;
        text-align: justify;
        line-height: 1.6;
    }
    
    /* Experience */
    .experience-item, .project-item, .education-item {
        margin-bottom: 16px;
    }
    
    .job-header, .project-header, .education-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 5px;
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
        font-size: 11.5pt;
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
    
    .achievements {
        margin: 5px 0 0 20px;
        padding: 0;
    }
    
    .achievements li {
        font-size: 10pt;
        margin-bottom: 4px;
        position: relative;
    }
    
    /* Skills */
    .skills-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    
    .skill-item {
        background-color: var(--secondary-color);
        color: var(--primary-color);
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 9.5pt;
        font-weight: 500;
        text-align: center;
    }
    
    /* Projects */
    .project-item p, .education-item p {
        margin: 5px 0 0 0;
        font-size: 10pt;
    }
    """


def get_template_metadata():
    return {
        "name": "Strategic Product Manager",
        "description": "A professional template emphasizing leadership experience and strategic initiatives for product management roles.",
        "role_type": "product_manager",
        "is_default": True
    } 