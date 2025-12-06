"""
Skill Extractor - Extracts skills and qualifications from text
"""

import re
from typing import List, Set
from collections import Counter


class SkillExtractor:
    """Extract skills and qualifications from CV and JD text"""
    
    def __init__(self):
        # Common technical skills taxonomy
        self.skill_keywords = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'spring', 'asp.net', 'laravel', 'rails', 'next.js', 'nuxt',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra',
            'elasticsearch', 'dynamodb', 'neo4j',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd', 'terraform',
            'ansible', 'chef', 'puppet', 'linux', 'unix',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'data analysis', 'data visualization', 'tableau', 'power bi',
            'statistics', 'nlp', 'computer vision',
            
            # Mobile
            'android', 'ios', 'react native', 'flutter', 'xamarin',
            
            # Other
            'agile', 'scrum', 'project management', 'leadership', 'communication', 'teamwork',
            'problem solving', 'analytical thinking', 'time management'
        }
        
        # Education keywords
        self.education_keywords = {
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'diploma', 'certification',
            'bsc', 'msc', 'mba', 'ba', 'ma'
        }
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text
        
        Args:
            text: Input text (CV or JD)
            
        Returns:
            List of extracted skills
        """
        text_lower = text.lower()
        found_skills = []
        
        # Direct keyword matching
        for skill in self.skill_keywords:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                found_skills.append(skill.title())
        
        # Extract skills from common patterns
        # Pattern: "Skills: Python, Java, React"
        skills_section = re.search(r'skills?[:\-]?\s*([^\.\n]+)', text_lower, re.IGNORECASE)
        if skills_section:
            skills_text = skills_section.group(1)
            # Split by common delimiters
            potential_skills = re.split(r'[,;|•\-\n]', skills_text)
            for skill in potential_skills:
                skill = skill.strip()
                if len(skill) > 2 and skill.lower() in self.skill_keywords:
                    if skill.title() not in found_skills:
                        found_skills.append(skill.title())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in found_skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        text_lower = text.lower()
        
        # Look for education section
        edu_section = re.search(r'education[:\-]?\s*([^\.\n]+)', text_lower, re.IGNORECASE)
        if edu_section:
            education.append(edu_section.group(1).strip())
        
        # Look for degree mentions
        for keyword in self.education_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                # Extract surrounding context
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    if context not in education:
                        education.append(context)
        
        return education
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience mentioned"""
        text_lower = text.lower()
        
        # Patterns like "5 years", "3+ years", "10+ years of experience"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'experience[:\-]?\s*(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                try:
                    years.append(int(match))
                except ValueError:
                    pass
        
        return max(years) if years else 0
    
    def extract_job_titles(self, text: str) -> List[str]:
        """Extract job titles from text"""
        titles = []
        
        # Common job title patterns
        title_patterns = [
            r'(?:senior\s+|junior\s+|lead\s+)?(?:software\s+|web\s+|mobile\s+)?(?:engineer|developer|programmer)',
            r'(?:data\s+)?(?:scientist|analyst|engineer)',
            r'(?:product|project|technical)\s+manager',
            r'architect',
            r'consultant',
            r'designer'
        ]
        
        for pattern in title_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                title = match.group(0).strip()
                if title not in titles:
                    titles.append(title)
        
        return titles

