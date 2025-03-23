"""
Data Scientist resume template with a professional, analytical design
optimized for ATS systems and highlighting technical and analytical skills.
"""

def get_html_template():
    return """
    <div class="resume">
        <div class="header">
            <h1>{{ personal_info.name }}</h1>
            <div class="subtitle">Data Scientist</div>
            <div class="contact-info">
                <div class="contact-row">
                    <span class="contact-item">{{ personal_info.email }}</span>
                    <span class="contact-item">{{ personal_info.phone }}</span>
                    <span class="contact-item">{{ personal_info.location }}</span>
                </div>
                <div class="contact-row">
                    {% if personal_info.linkedin %}
                    <span class="contact-item">{{ personal_info.linkedin }}</span>
                    {% endif %}
                    {% if personal_info.website %}
                    <span class="contact-item">{{ personal_info.website }}</span>
                    {% endif %}
                </div>
            </div>
        </div>
        
        {% if summary %}
        <div class="section">
            <h2><span class="section-icon">📊</span> Professional Summary</h2>
            <div class="summary">
                <p>{{ summary }}</p>
            </div>
        </div>
        {% endif %}
        
        {% if skills and skills|length > 0 %}
        <div class="section">
            <h2><span class="section-icon">🔧</span> Technical Skills</h2>
            <div class="skills-categories">
                <div class="skill-category">
                    <h3>Data Science</h3>
                    <div class="skills-list">
                        {% for skill in skills %}
                        {% if skill in ['Python', 'R', 'SQL', 'Machine Learning', 'Deep Learning', 'Statistics', 'Data Mining', 'Data Visualization', 'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy', 'SciPy', 'Feature Engineering', 'Natural Language Processing', 'Computer Vision', 'Time Series Analysis', 'A/B Testing', 'Hypothesis Testing'] %}
                        <span class="skill-item">{{ skill }}</span>
                        {% endif %}
                        {% endfor %}
                    </div>
                </div>
                
                <div class="skill-category">
                    <h3>Tools & Technologies</h3>
                    <div class="skills-list">
                        {% for skill in skills %}
                        {% if skill not in ['Python', 'R', 'SQL', 'Machine Learning', 'Deep Learning', 'Statistics', 'Data Mining', 'Data Visualization', 'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy', 'SciPy', 'Feature Engineering', 'Natural Language Processing', 'Computer Vision', 'Time Series Analysis', 'A/B Testing', 'Hypothesis Testing'] %}
                        <span class="skill-item">{{ skill }}</span>
                        {% endif %}
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
        
        {% if work_experience and work_experience|length > 0 %}
        <div class="section">
            <h2><span class="section-icon">💼</span> Professional Experience</h2>
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
            <h2><span class="section-icon">🧪</span> Research & Projects</h2>
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
            <h2><span class="section-icon">🎓</span> Education</h2>
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
    /* Data Scientist Resume Template */
    :root {
        --primary-color: #4f46e5;
        --primary-light: #e0e7ff;
        --primary-dark: #3730a3;
        --secondary-color: #3b82f6;
        --secondary-light: #dbeafe;
        --dark-color: #1e293b;
        --text-color: #334155;
        --light-text: #64748b;
        --background-color: #ffffff;
    }
    
    body {
        font-family: 'IBM Plex Sans', 'Roboto', 'Arial', sans-serif;
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
        text-align: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid var(--primary-light);
    }
    
    .header h1 {
        font-size: 20pt;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0 0 5px 0;
        letter-spacing: 0.5px;
    }
    
    .subtitle {
        font-size: 12pt;
        font-weight: 600;
        color: var(--secondary-color);
        margin-bottom: 10px;
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
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .contact-item {
        font-size: 9.5pt;
        color: var(--light-text);
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
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 5px;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
    }
    
    .section-icon {
        margin-right: 8px;
        font-size: 14pt;
    }
    
    /* Summary */
    .summary p {
        margin: 0;
        font-size: 10.5pt;
        line-height: 1.6;
        text-align: justify;
    }
    
    /* Skills */
    .skills-categories {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .skill-category {
        flex: 1;
        min-width: 200px;
    }
    
    .skill-category h3 {
        font-size: 11pt;
        color: var(--primary-color);
        margin: 0 0 8px 0;
        font-weight: 600;
    }
    
    .skills-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .skill-item {
        background-color: var(--secondary-light);
        color: var(--secondary-color);
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 9pt;
        font-weight: 500;
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
        font-size: 9pt;
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
    .project-item {
        padding: 10px;
        border-left: 3px solid var(--primary-light);
        margin-left: 5px;
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
    """


def get_template_metadata():
    return {
        "name": "Analytical Data Scientist",
        "description": "A professional template highlighting technical skills and quantitative achievements for data science roles.",
        "role_type": "data_scientist",
        "is_default": True
    } 