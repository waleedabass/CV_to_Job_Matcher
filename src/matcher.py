"""
CV-Job Matcher - Computes match scores and skill gap analysis
"""

from typing import List, Dict, Any, Optional
import re
from collections import Counter
import os

# Try to import Gemini client
try:
    from src.gemini_client import GeminiClient
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GeminiClient = None


class CVJobMatcher:
    """Match CV against Job Description and compute scores"""
    
    def __init__(self, use_ai: bool = True, api_key: Optional[str] = None):
        """
        Initialize matcher
        
        Args:
            use_ai: Whether to use Gemini AI for enhanced matching
            api_key: Google AI API key (optional, will use env var if not provided)
        """
        # Weights for different match components
        self.weights = {
            'skill_overlap': 0.35,
            'semantic_similarity': 0.40,  # Increased weight for AI-powered semantic matching
            'experience_match': 0.15,
            'education_match': 0.10
        }
        
        # Initialize Gemini client if available and requested
        self.gemini_client = None
        self.use_ai = use_ai and GEMINI_AVAILABLE
        
        if self.use_ai:
            try:
                self.gemini_client = GeminiClient(api_key=api_key)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini AI: {e}")
                print("Falling back to rule-based matching")
                self.use_ai = False
                self.gemini_client = None
    
    def compute_match(
        self,
        cv_text: str,
        jd_text: str,
        cv_skills: List[str],
        jd_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Compute comprehensive match score
        
        Args:
            cv_text: CV text content
            jd_text: Job description text
            cv_skills: Extracted CV skills
            jd_skills: Extracted JD required skills
            
        Returns:
            Dictionary with match results
        """
        # Normalize skills for comparison
        cv_skills_normalized = [s.lower() for s in cv_skills]
        jd_skills_normalized = [s.lower() for s in jd_skills]
        
        # 1. Skill Overlap Score
        skill_overlap_score = self._compute_skill_overlap(
            cv_skills_normalized,
            jd_skills_normalized
        )
        
        # 2. Semantic Similarity (AI-powered if available, else keyword-based)
        if self.use_ai and self.gemini_client:
            try:
                semantic_score = self.gemini_client.compute_semantic_similarity(cv_text, jd_text)
            except Exception as e:
                print(f"Error using Gemini for semantic similarity: {e}")
                semantic_score = self._compute_semantic_similarity(cv_text, jd_text)
        else:
            semantic_score = self._compute_semantic_similarity(cv_text, jd_text)
        
        # 3. Experience Match
        experience_score = self._compute_experience_match(cv_text, jd_text)
        
        # 4. Education Match
        education_score = self._compute_education_match(cv_text, jd_text)
        
        # Calculate weighted composite score
        composite_score = (
            skill_overlap_score * self.weights['skill_overlap'] +
            semantic_score * self.weights['semantic_similarity'] +
            experience_score * self.weights['experience_match'] +
            education_score * self.weights['education_match']
        ) * 100  # Convert to percentage
        
        # Identify missing skills (AI-powered if available)
        if self.use_ai and self.gemini_client:
            try:
                ai_gaps = self.gemini_client.get_skill_gap_analysis(
                    cv_skills,
                    jd_skills
                )
                if ai_gaps:
                    missing_skills = ai_gaps
                else:
                    missing_skills = self._identify_missing_skills(
                        cv_skills_normalized,
                        jd_skills_normalized
                    )
            except Exception as e:
                print(f"Error using Gemini for skill gap analysis: {e}")
                missing_skills = self._identify_missing_skills(
                    cv_skills_normalized,
                    jd_skills_normalized
                )
        else:
            missing_skills = self._identify_missing_skills(
                cv_skills_normalized,
                jd_skills_normalized
            )
        
        # Get matched skills
        matched_skills = self._get_matched_skills(
            cv_skills_normalized,
            jd_skills_normalized
        )
        
        # Generate explainability data
        cv_contributions = self._analyze_cv_contributions(cv_text, jd_text)
        jd_matches = self._analyze_jd_requirements(cv_text, jd_text)
        
        return {
            'match_score': round(composite_score, 2),
            'skills_matched': len(matched_skills),
            'total_required_skills': len(jd_skills),
            'missing_skills': missing_skills,
            'matched_skills': [s.title() for s in matched_skills],
            'score_breakdown': {
                'skill_overlap': skill_overlap_score * 100,
                'semantic_similarity': semantic_score * 100,
                'experience_match': experience_score * 100,
                'education_match': education_score * 100
            },
            'cv_contributions': cv_contributions,
            'jd_matches': jd_matches
        }
    
    def _compute_skill_overlap(self, cv_skills: List[str], jd_skills: List[str]) -> float:
        """Compute skill overlap score (0-1)"""
        if not jd_skills:
            return 0.0
        
        cv_set = set(cv_skills)
        jd_set = set(jd_skills)
        
        # Direct matches
        direct_matches = len(cv_set.intersection(jd_set))
        
        # Partial matches (fuzzy matching for similar skills)
        partial_matches = 0
        for jd_skill in jd_set:
            if jd_skill not in cv_set:
                # Check for partial matches
                for cv_skill in cv_set:
                    if jd_skill in cv_skill or cv_skill in jd_skill:
                        partial_matches += 0.5
                        break
        
        total_matches = direct_matches + partial_matches
        return min(total_matches / len(jd_set), 1.0)
    
    def _compute_semantic_similarity(self, cv_text: str, jd_text: str) -> float:
        """Compute semantic similarity using keyword overlap"""
        # Extract important keywords (excluding common words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        cv_words = set(re.findall(r'\b\w+\b', cv_text.lower())) - stop_words
        jd_words = set(re.findall(r'\b\w+\b', jd_text.lower())) - stop_words
        
        if not jd_words:
            return 0.0
        
        # Common words indicate similarity
        common_words = cv_words.intersection(jd_words)
        similarity = len(common_words) / len(jd_words)
        
        return min(similarity, 1.0)
    
    def _compute_experience_match(self, cv_text: str, jd_text: str) -> float:
        """Match experience requirements"""
        # Extract years from both
        cv_years = self._extract_years(cv_text)
        jd_years = self._extract_years(jd_text)
        
        if jd_years == 0:
            return 1.0  # No requirement means match
        
        if cv_years >= jd_years:
            return 1.0
        elif cv_years > 0:
            return cv_years / jd_years
        else:
            return 0.0
    
    def _compute_education_match(self, cv_text: str, jd_text: str) -> float:
        """Match education requirements"""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'bsc', 'msc', 'mba']
        
        cv_lower = cv_text.lower()
        jd_lower = jd_text.lower()
        
        jd_edu_mentions = [kw for kw in education_keywords if kw in jd_lower]
        cv_edu_mentions = [kw for kw in education_keywords if kw in cv_lower]
        
        if not jd_edu_mentions:
            return 1.0  # No requirement
        
        # Check if CV mentions any required education
        matches = sum(1 for jd_edu in jd_edu_mentions if jd_edu in cv_edu_mentions)
        return matches / len(jd_edu_mentions) if jd_edu_mentions else 1.0
    
    def _identify_missing_skills(
        self,
        cv_skills: List[str],
        jd_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify missing or weakly-matched skills"""
        cv_set = set(cv_skills)
        jd_set = set(jd_skills)
        
        missing = []
        for jd_skill in jd_set:
            if jd_skill not in cv_set:
                # Check for partial match
                has_partial = any(jd_skill in cv or cv in jd_skill for cv in cv_set)
                
                if not has_partial:
                    missing.append({
                        'skill': jd_skill.title(),
                        'priority': 'High' if jd_skill in jd_set else 'Medium',
                        'reason': f"Required skill '{jd_skill}' not found in CV",
                        'suggestions': [
                            f"Consider learning {jd_skill}",
                            f"Add {jd_skill} to your skills section if you have experience",
                            f"Look for courses or certifications in {jd_skill}"
                        ]
                    })
        
        # Sort by priority
        missing.sort(key=lambda x: 0 if x['priority'] == 'High' else 1)
        
        return missing
    
    def _get_matched_skills(self, cv_skills: List[str], jd_skills: List[str]) -> List[str]:
        """Get list of matched skills"""
        cv_set = set(cv_skills)
        jd_set = set(jd_skills)
        
        return list(cv_set.intersection(jd_set))
    
    def _analyze_cv_contributions(self, cv_text: str, jd_text: str) -> Dict[str, float]:
        """Analyze which CV sections contribute to the score"""
        sections = {
            'Skills Section': 0.0,
            'Experience Section': 0.0,
            'Education Section': 0.0,
            'Summary Section': 0.0
        }
        
        # Simple heuristic: count keyword matches in each section
        jd_keywords = set(re.findall(r'\b\w+\b', jd_text.lower()))
        
        # Skills section
        skills_match = re.search(r'skills?[:\-]?\s*([^\.\n]+)', cv_text.lower(), re.IGNORECASE)
        if skills_match:
            skills_text = skills_match.group(1)
            skills_words = set(re.findall(r'\b\w+\b', skills_text.lower()))
            sections['Skills Section'] = len(skills_words.intersection(jd_keywords)) / max(len(jd_keywords), 1) * 100
        
        # Experience section
        exp_match = re.search(r'experience[:\-]?\s*([^\.\n]+)', cv_text.lower(), re.IGNORECASE)
        if exp_match:
            exp_text = exp_match.group(1)
            exp_words = set(re.findall(r'\b\w+\b', exp_text.lower()))
            sections['Experience Section'] = len(exp_words.intersection(jd_keywords)) / max(len(jd_keywords), 1) * 100
        
        return sections
    
    def _analyze_jd_requirements(self, cv_text: str, jd_text: str) -> Dict[str, bool]:
        """Analyze which JD requirements are matched"""
        requirements = {}
        
        # Extract requirement sentences from JD
        jd_sentences = re.split(r'[.!?]\s+', jd_text)
        
        for sentence in jd_sentences[:10]:  # Limit to first 10 sentences
            if len(sentence) > 20:  # Meaningful sentences
                # Check if CV mentions similar content
                sentence_keywords = set(re.findall(r'\b\w{4,}\b', sentence.lower()))
                cv_keywords = set(re.findall(r'\b\w{4,}\b', cv_text.lower()))
                
                match_ratio = len(sentence_keywords.intersection(cv_keywords)) / max(len(sentence_keywords), 1)
                requirements[sentence[:50] + "..."] = match_ratio > 0.3
        
        return requirements
    
    def _extract_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower(), re.IGNORECASE)
            for match in matches:
                try:
                    years.append(int(match))
                except ValueError:
                    pass
        
        return max(years) if years else 0

