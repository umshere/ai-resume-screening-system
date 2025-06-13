from typing import Annotated, List, Dict
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import json
import re


class ResumeScreeningPlugin:
    """The Resume Screening Plugin can be used to analyze resumes and calculate matching scores."""

    @kernel_function(description="Analyze a resume against a job profile and calculate matching score.")
    def analyze_resume(self, 
                      resume_content: Annotated[str, "The content of the resume to analyze"],
                      job_profile: Annotated[str, "The job profile/description to match against"],
                      candidate_name: Annotated[str, "The name or identifier of the candidate"] = "Unknown"
                      ) -> Annotated[str, "Analysis result with matching score and explanation."]:
        """
        Analyze a single resume against a job profile and return matching score with explanation.
        """
        try:
            # Extract key information from resume
            skills = self._extract_skills(resume_content)
            experience = self._extract_experience(resume_content)
            education = self._extract_education(resume_content)
            
            # Extract requirements from job profile
            job_requirements = self._extract_job_requirements(job_profile)
            
            # Calculate matching scores for different aspects
            skill_score = self._calculate_skill_match(skills, job_requirements.get('skills', []))
            experience_score = self._calculate_experience_match(experience, job_requirements.get('experience', []))
            education_score = self._calculate_education_match(education, job_requirements.get('education', []))
            
            # Calculate overall score (weighted average)
            overall_score = (skill_score * 0.5) + (experience_score * 0.3) + (education_score * 0.2)
            
            # Generate detailed explanation
            explanation = self._generate_explanation(
                overall_score, skill_score, experience_score, education_score,
                skills, experience, education, job_requirements
            )
            
            result = {
                "candidate": candidate_name,
                "overall_score": round(overall_score, 1),
                "skill_score": round(skill_score, 1),
                "experience_score": round(experience_score, 1),
                "education_score": round(education_score, 1),
                "explanation": explanation,
                "extracted_skills": skills,
                "extracted_experience": experience,
                "extracted_education": education
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error analyzing resume: {str(e)}"

    @kernel_function(description="Compare multiple resumes and rank them by matching score.")
    def rank_candidates(self,
                       analysis_results: Annotated[List[str], "List of individual analysis results"],
                       top_n: Annotated[int, "Number of top candidates to return"] = 5
                       ) -> Annotated[str, "Ranked list of candidates with scores."]:
        """
        Rank multiple candidates based on their analysis results.
        """
        try:
            candidates = []
            for result_str in analysis_results:
                result = json.loads(result_str)
                candidates.append(result)
            
            # Sort by overall score (descending)
            candidates.sort(key=lambda x: x['overall_score'], reverse=True)
            
            # Return top N candidates
            top_candidates = candidates[:top_n]
            
            ranking = {
                "total_candidates": len(candidates),
                "top_candidates": top_candidates,
                "ranking_summary": [
                    {
                        "rank": i + 1,
                        "candidate": candidate["candidate"],
                        "score": candidate["overall_score"],
                        "recommendation": self._get_recommendation(candidate["overall_score"])
                    }
                    for i, candidate in enumerate(top_candidates)
                ]
            }
            
            return json.dumps(ranking, indent=2)
            
        except Exception as e:
            return f"Error ranking candidates: {str(e)}"

    def _extract_skills(self, resume_content: str) -> List[str]:
        """Extract skills from resume content."""
        # Common skill keywords
        skill_patterns = [
            r'\b(?:Python|Java|JavaScript|React|Angular|Vue|Node\.js|Django|Flask)\b',
            r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git)\b',
            r'\b(?:Machine Learning|AI|Data Science|Analytics|Statistics)\b',
            r'\b(?:Project Management|Agile|Scrum|Leadership|Communication)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, resume_content, re.IGNORECASE)
            skills.extend([match.lower() for match in matches])
        
        return list(set(skills))  # Remove duplicates

    def _extract_experience(self, resume_content: str) -> List[str]:
        """Extract work experience from resume content."""
        # Look for experience indicators
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*in',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*working'
        ]
        
        experiences = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, resume_content, re.IGNORECASE)
            experiences.extend(matches)
        
        return experiences

    def _extract_education(self, resume_content: str) -> List[str]:
        """Extract education information from resume content."""
        education_patterns = [
            r'\b(?:Bachelor|Master|PhD|MBA|B\.S\.|M\.S\.|B\.A\.|M\.A\.)\b',
            r'\b(?:Computer Science|Engineering|Mathematics|Business|Marketing)\b',
            r'\b(?:University|College|Institute|School)\b'
        ]
        
        education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, resume_content, re.IGNORECASE)
            education.extend([match.lower() for match in matches])
        
        return list(set(education))

    def _extract_job_requirements(self, job_profile: str) -> Dict:
        """Extract requirements from job profile."""
        # This is a simplified extraction - in real implementation, 
        # you'd use more sophisticated NLP techniques
        requirements = {
            'skills': self._extract_skills(job_profile),
            'experience': self._extract_experience(job_profile),
            'education': self._extract_education(job_profile)
        }
        return requirements

    def _calculate_skill_match(self, candidate_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill matching score."""
        if not required_skills:
            return 80.0  # Default score if no specific skills required
        
        matched_skills = set(candidate_skills) & set(required_skills)
        match_ratio = len(matched_skills) / len(required_skills)
        
        return min(match_ratio * 100, 100.0)

    def _calculate_experience_match(self, candidate_experience: List[str], required_experience: List[str]) -> float:
        """Calculate experience matching score."""
        if not required_experience:
            return 75.0  # Default score
        
        # Simple heuristic based on years of experience
        try:
            candidate_years = max([int(exp) for exp in candidate_experience], default=0)
            required_years = max([int(exp) for exp in required_experience], default=0)
            
            if candidate_years >= required_years:
                return 100.0
            elif candidate_years >= required_years * 0.7:
                return 80.0
            else:
                return max(candidate_years / required_years * 100, 20.0)
        except:
            return 60.0  # Default if cannot parse experience

    def _calculate_education_match(self, candidate_education: List[str], required_education: List[str]) -> float:
        """Calculate education matching score."""
        if not required_education:
            return 70.0  # Default score
        
        matched_education = set(candidate_education) & set(required_education)
        if matched_education:
            return 90.0
        else:
            return 50.0  # Partial credit for having education

    def _generate_explanation(self, overall_score: float, skill_score: float, 
                            experience_score: float, education_score: float,
                            skills: List[str], experience: List[str], education: List[str],
                            job_requirements: Dict) -> str:
        """Generate detailed explanation of the matching score."""
        
        explanation = f"Overall Matching Score: {overall_score:.1f}%\n\n"
        
        explanation += f"Skill Match: {skill_score:.1f}%\n"
        explanation += f"- Candidate Skills: {', '.join(skills[:5]) if skills else 'Not clearly specified'}\n"
        explanation += f"- Required Skills: {', '.join(job_requirements.get('skills', [])[:5])}\n\n"
        
        explanation += f"Experience Match: {experience_score:.1f}%\n"
        explanation += f"- Candidate Experience: {', '.join(experience) if experience else 'Not clearly specified'} years\n\n"
        
        explanation += f"Education Match: {education_score:.1f}%\n"
        explanation += f"- Candidate Education: {', '.join(education[:3]) if education else 'Not clearly specified'}\n\n"
        
        # Add recommendation
        if overall_score >= 80:
            explanation += "Recommendation: Excellent candidate - Strong match for the position."
        elif overall_score >= 65:
            explanation += "Recommendation: Good candidate - Consider for interview with some skill gap analysis."
        elif overall_score >= 50:
            explanation += "Recommendation: Moderate match - May require additional training or assessment."
        else:
            explanation += "Recommendation: Limited match - Consider only if candidate pool is limited."
        
        return explanation

    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on score."""
        if score >= 80:
            return "Highly Recommended"
        elif score >= 65:
            return "Recommended"
        elif score >= 50:
            return "Consider with Caution"
        else:
            return "Not Recommended"
