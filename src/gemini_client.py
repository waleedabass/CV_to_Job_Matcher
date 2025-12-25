"""
Gemini AI Client - Integration with Google Gemini models for semantic matching
"""

import os
from typing import Optional, List, Dict, Any
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiClient:
    """Client for interacting with Google Gemini models"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google AI API key. If None, will try to get from environment variable
        """
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai is required. Install it with: pip install google-generativeai"
            )
        
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Google AI API key is required. "
                "Set it as environment variable GOOGLE_AI_API_KEY or pass it to constructor."
            )
        
        genai.configure(api_key=self.api_key)
        
        # Primary model: Gemini 2.0 Flash (experimental - latest)
        # Try gemini-2.0-flash-exp first, fallback to gemini-1.5-flash if not available
        self.primary_model = "gemini-3-pro-preview"
        # Fallback model: Gemini 1.5 Flash (stable)
        self.fallback_model = "gemini-1.5-flash"
        
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the primary model, with fallback if needed"""
        try:
            # Try primary model (Gemini 2.0 Flash)
            self.model = genai.GenerativeModel(self.primary_model)
            # Test if model is available with a simple query
            try:
                self.model.generate_content("test", generation_config={"max_output_tokens": 10})
            except Exception as test_error:
                # If test fails, try fallback
                raise Exception(f"Model test failed: {test_error}")
        except Exception as e:
            print(f"Warning: Primary model {self.primary_model} not available: {e}")
            print(f"Falling back to {self.fallback_model}")
            try:
                # Use fallback model (Gemini 1.5 Flash)
                self.model = genai.GenerativeModel(self.fallback_model)
                # Test fallback model
                self.model.generate_content("test", generation_config={"max_output_tokens": 10})
            except Exception as e2:
                raise RuntimeError(
                    f"Neither primary nor fallback model available. "
                    f"Primary error: {e}, Fallback error: {e2}"
                )
    
    def compute_semantic_similarity(self, cv_text: str, jd_text: str) -> float:
        """
        Compute semantic similarity between CV and JD using Gemini
        
        Args:
            cv_text: CV text content
            jd_text: Job description text
            
        Returns:
            Similarity score between 0 and 1
        """
        prompt = f"""You are an expert at matching CVs with job descriptions. 
Analyze the semantic similarity between the following CV and Job Description.

CV:
{cv_text[:2000]}

Job Description:
{jd_text[:2000]}

Provide a similarity score between 0 and 1 (where 1 is perfect match) based on:
- Overall fit and alignment
- Skills and qualifications match
- Experience relevance
- Education requirements

Respond with ONLY a number between 0 and 1 (e.g., 0.85), no explanation needed."""

        try:
            response = self.model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract number from response
            import re
            match = re.search(r'0?\.\d+|1\.0|0', score_text)
            if match:
                score = float(match.group())
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            else:
                # Fallback: try to parse as float
                try:
                    score = float(score_text)
                    return max(0.0, min(1.0, score))
                except:
                    return 0.5  # Default if parsing fails
        except Exception as e:
            print(f"Error computing semantic similarity: {e}")
            # Fallback to secondary model if primary fails
            if self.model.name != self.fallback_model:
                try:
                    self.model = genai.GenerativeModel(self.fallback_model)
                    return self.compute_semantic_similarity(cv_text, jd_text)
                except:
                    pass
            return 0.5  # Default fallback score
    
    def extract_skills_advanced(self, text: str) -> List[str]:
        """
        Extract skills from text using Gemini AI
        
        Args:
            text: Input text (CV or JD)
            
        Returns:
            List of extracted skills
        """
        prompt = f"""Extract all technical skills, programming languages, tools, frameworks, and technologies mentioned in the following text.
Return ONLY a JSON array of skill names, one per line, no explanations.

Text:
{text[:3000]}

Example format:
["Python", "JavaScript", "React", "AWS", "Docker"]"""

        try:
            response = self.model.generate_content(prompt)
            skills_text = response.text.strip()
            
            # Try to parse as JSON
            import json
            # Remove markdown code blocks if present
            skills_text = skills_text.replace('```json', '').replace('```', '').strip()
            
            try:
                skills = json.loads(skills_text)
                if isinstance(skills, list):
                    return [s.strip() for s in skills if s.strip()]
            except json.JSONDecodeError:
                # Fallback: extract from text
                import re
                # Look for array-like patterns
                matches = re.findall(r'["\']([^"\']+)["\']', skills_text)
                if matches:
                    return [m.strip() for m in matches]
                # Last resort: split by common delimiters
                return [s.strip() for s in skills_text.split(',') if s.strip()]
            
            return []
        except Exception as e:
            print(f"Error extracting skills with Gemini: {e}")
            # Fallback to secondary model
            if self.model.name != self.fallback_model:
                try:
                    self.model = genai.GenerativeModel(self.fallback_model)
                    return self.extract_skills_advanced(text)
                except:
                    pass
            return []
    
    def analyze_match_details(self, cv_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Get detailed match analysis from Gemini
        
        Args:
            cv_text: CV text content
            jd_text: Job description text
            
        Returns:
            Dictionary with detailed analysis
        """
        prompt = f"""Analyze how well the CV matches the Job Description. Provide a detailed analysis.

CV:
{cv_text[:2000]}

Job Description:
{jd_text[:2000]}

Provide a JSON response with the following structure:
{{
    "overall_match_score": 0.85,
    "strengths": ["skill1", "skill2"],
    "weaknesses": ["missing_skill1", "missing_skill2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "key_matches": ["match1", "match2"]
}}

Return ONLY valid JSON, no markdown formatting."""

        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text.strip()
            
            # Remove markdown code blocks if present
            analysis_text = analysis_text.replace('```json', '').replace('```', '').strip()
            
            try:
                analysis = json.loads(analysis_text)
                return analysis
            except json.JSONDecodeError:
                # Fallback parsing
                return {
                    "overall_match_score": 0.5,
                    "strengths": [],
                    "weaknesses": [],
                    "recommendations": [],
                    "key_matches": []
                }
        except Exception as e:
            print(f"Error getting match details: {e}")
            # Fallback to secondary model
            if self.model.name != self.fallback_model:
                try:
                    self.model = genai.GenerativeModel(self.fallback_model)
                    return self.analyze_match_details(cv_text, jd_text)
                except:
                    pass
            return {
                "overall_match_score": 0.5,
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "key_matches": []
            }
    
    def get_skill_gap_analysis(self, cv_skills: List[str], jd_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Get AI-powered skill gap analysis
        
        Args:
            cv_skills: Skills found in CV
            jd_skills: Skills required in JD
            
        Returns:
            List of skill gap dictionaries with recommendations
        """
        prompt = f"""Analyze the skill gap between the candidate's skills and job requirements.

Candidate Skills:
{', '.join(cv_skills[:50])}

Required Skills:
{', '.join(jd_skills[:50])}

For each missing or weak skill, provide:
- The skill name
- Priority (High/Medium/Low)
- Why it's important for this role
- Specific learning recommendations

Return a JSON array of objects with this structure:
[
    {{
        "skill": "Python",
        "priority": "High",
        "reason": "Required for backend development",
        "suggestions": ["Take Python course", "Build projects"]
    }}
]

Return ONLY valid JSON array."""

        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text.strip()
            
            # Remove markdown code blocks
            analysis_text = analysis_text.replace('```json', '').replace('```', '').strip()
            
            try:
                gaps = json.loads(analysis_text)
                if isinstance(gaps, list):
                    return gaps
            except json.JSONDecodeError:
                pass
            
            return []
        except Exception as e:
            print(f"Error getting skill gap analysis: {e}")
            # Fallback to secondary model
            if self.model.name != self.fallback_model:
                try:
                    self.model = genai.GenerativeModel(self.fallback_model)
                    return self.get_skill_gap_analysis(cv_skills, jd_skills)
                except:
                    pass
            return []

