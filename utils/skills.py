import re  

SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c sharp", "php", 
    "ruby", "go", "golang", "kotlin", "swift", "rust", "scala", "r programming",
    
    # Web Technologies
    "html", "html5", "css", "css3", "react", "reactjs", "angular", "vue", "vuejs",
    "nodejs", "node.js", "express", "expressjs", "flask", "django", "fastapi", 
    "spring boot", "springboot", "asp.net", "dotnet",
    
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "mongo", "redis", "oracle", 
    "sql server", "sqlite", "cassandra", "dynamodb", "firebase", "sql",
    
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "microsoft azure", "gcp", 
    "google cloud", "docker", "kubernetes", "k8s", "jenkins", "git", 
    "github", "gitlab", "terraform", "ansible", "ci/cd", "cicd",
    
    # Data Science & ML
    "machine learning", "ml", "deep learning", "dl", "tensorflow", "pytorch",
    "scikit-learn", "sklearn", "pandas", "numpy", "data analysis", "nlp",
    "natural language processing", "computer vision", "statistics", 
    "matplotlib", "seaborn", "jupyter",
    
    # Other Skills
    "agile", "scrum", "rest api", "restful", "graphql", "microservices",
    "testing", "unit testing", "junit", "selenium", "jira", "leadership",
    "problem solving", "oop", "object oriented", "api", "json", "xml"
]

def extract_skills(text):
    """
    Extract skills from text using improved matching.
    Handles multi-word skills and variations.
    """
    text = text.lower()
    found = []
    
    # Sort skills by length (longest first) to match multi-word skills first
    sorted_skills = sorted(SKILLS, key=len, reverse=True)
    
    for skill in sorted_skills:
        # Use word boundaries to avoid partial matches
        # e.g., "java" shouldn't match "javascript"
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    
    return unique_skills

def missing_skills(resume_skills, jd_skills):
    """
    Find skills present in job description but missing in resume.
    """
    return list(set(jd_skills) - set(resume_skills))
