import re

DOMAIN_TERMS = {
    "Java": ("Java", "Spring"),
    "Python": ("Python",),
    "SQL": ("SQL", "PostgreSQL", "MySQL", "database"),
    "DSA": ("DSA", "data structures", "algorithms"),
    "Web Development": ("web development", "frontend", "JavaScript", "React", "HTML", "CSS"),
    "System Design": ("system design", "microservices", "architecture", "scalable systems"),
    "Cloud & DevOps": ("cloud", "AWS", "Azure", "Docker", "Kubernetes", "DevOps", "CI/CD"),
    "Data Science & ML": ("data science", "machine learning", "pandas", "scikit-learn"),
}

def parse_resume(text: str) -> dict:
    lowered = text.lower()
    mentions = {
        domain: sum(len(re.findall(r"\b" + re.escape(term.lower()) + r"\b", lowered)) for term in terms)
        for domain, terms in DOMAIN_TERMS.items()
    }
    found = [domain for domain, count in mentions.items() if count]
    confidence = {domain: round(min(.65, .25 + .08 * mentions[domain]), 2) for domain in found}
    return {"skills": found, "competencies": confidence, "source": "resume"}
