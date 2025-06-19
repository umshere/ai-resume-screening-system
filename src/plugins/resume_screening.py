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
            
            # NEW: Add role seniority validation
            role_match_score = self._calculate_role_match(resume_content, job_profile)
            
            # Calculate overall score (weighted average) - now includes role matching
            overall_score = (skill_score * 0.35) + (experience_score * 0.25) + (education_score * 0.15) + (role_match_score * 0.25)
            
            # Generate detailed explanation
            explanation = self._generate_explanation(
                overall_score, skill_score, experience_score, education_score, role_match_score,
                skills, experience, education, job_requirements
            )
            
            result = {
                "candidate": candidate_name,
                "overall_score": round(overall_score, 1),
                "skill_score": round(skill_score, 1),
                "experience_score": round(experience_score, 1),
                "education_score": round(education_score, 1),
                "role_match_score": round(role_match_score, 1),
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
        # More comprehensive and role-specific skill patterns
        skill_patterns = [
            # Technical skills
            r'\b(?:Python|Java|JavaScript|React|Angular|Vue|Node\.js|Django|Flask|Spring)\b',
            r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|CI/CD|DevOps)\b',
            r'\b(?:Machine Learning|AI|Data Science|Analytics|Statistics|TensorFlow|PyTorch)\b',
            
            # Management and leadership skills
            r'\b(?:Team Lead|Engineering Manager|Technical Lead|Project Manager|Scrum Master)\b',
            r'\b(?:Leadership|Management|Team Building|Mentoring|Coaching|People Management)\b',
            r'\b(?:Agile|Scrum|Kanban|JIRA|Project Management|Stakeholder Management)\b',
            r'\b(?:Strategic Planning|Budget Management|Resource Planning|Hiring|Performance Management)\b',
            
            # Business skills
            r'\b(?:Product Management|Business Analysis|Requirements Gathering|Stakeholder Communication)\b',
            r'\b(?:Cross-functional|Collaboration|Communication|Presentation|Documentation)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, resume_content, re.IGNORECASE)
            skills.extend([match.lower() for match in matches])
        
        return list(set(skills))  # Remove duplicates

    def _extract_experience(self, resume_content: str) -> List[str]:
        """Extract work experience from resume content."""
        # Look for experience indicators with more patterns
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*in',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*working',
            # Additional patterns for date ranges
            r'(\d{4})\s*-\s*(?:Present|\d{4})',  # Years like "2020 - Present" or "2018 - 2020"
            r'(\d+)\s*years?\s*experience',
            r'over\s*(\d+)\s*years?',
            r'more\s*than\s*(\d+)\s*years?'
        ]
        
        experiences = []
        years_of_experience = []
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, resume_content, re.IGNORECASE)
            experiences.extend(matches)
        
        # Calculate years from date ranges (e.g., "2020 - Present" = 4 years)
        current_year = 2025  # Update this to current year
        date_ranges = re.findall(r'(\d{4})\s*-\s*(?:Present|(\d{4}))', resume_content, re.IGNORECASE)
        
        for start_year, end_year in date_ranges:
            start = int(start_year)
            end = int(end_year) if end_year else current_year
            years = end - start
            if years > 0 and years < 50:  # Reasonable bounds
                years_of_experience.append(str(years))
        
        # Combine both types of experience extraction
        all_experience = experiences + years_of_experience
        return list(set(all_experience))  # Remove duplicates

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
            return 40.0  # Much lower default score - lack of clear requirements is a red flag
        
        matched_skills = set(candidate_skills) & set(required_skills)
        if not matched_skills:
            return 10.0  # Very low score for no matching skills
        
        match_ratio = len(matched_skills) / len(required_skills)
        
        # More strict scoring - need at least 50% skill match to get decent score
        if match_ratio >= 0.8:
            return min(match_ratio * 100, 100.0)
        elif match_ratio >= 0.5:
            return match_ratio * 80  # Cap at 80% if not excellent match
        else:
            return match_ratio * 60  # Cap at 60% for poor matches

    def _calculate_experience_match(self, candidate_experience: List[str], required_experience: List[str]) -> float:
        """Calculate experience matching score."""
        if not required_experience:
            return 30.0  # Low default score - unclear requirements
        
        # Simple heuristic based on years of experience
        try:
            # Convert all experience strings to integers and find reasonable years
            candidate_years_list = []
            for exp in candidate_experience:
                try:
                    year_val = int(exp)
                    # Filter out unrealistic values (like years 2020, 2018 etc.)
                    if 1 <= year_val <= 50:  # Reasonable years of experience
                        candidate_years_list.append(year_val)
                except:
                    continue
            
            # Take the maximum reasonable years found
            candidate_years = max(candidate_years_list) if candidate_years_list else 0
            required_years = max([int(exp) for exp in required_experience], default=0)
            
            if candidate_years >= required_years:
                return 100.0
            elif candidate_years >= required_years * 0.8:
                return 85.0
            elif candidate_years >= required_years * 0.6:
                return 70.0
            elif candidate_years >= required_years * 0.4:
                return 50.0
            else:
                return max((candidate_years / required_years) * 40, 5.0)  # Much lower floor
        except:
            return 20.0  # Much lower default if cannot parse experience

    def _calculate_education_match(self, candidate_education: List[str], required_education: List[str]) -> float:
        """Calculate education matching score."""
        if not required_education:
            return 50.0  # Neutral score - education requirements not specified
        
        matched_education = set(candidate_education) & set(required_education)
        if matched_education:
            return 85.0  # Good but not perfect - education is just one factor
        else:
            # Check if candidate has any higher education
            higher_ed_keywords = ['bachelor', 'master', 'phd', 'mba', 'b.s.', 'm.s.', 'b.a.', 'm.a.', 'university', 'college']
            has_higher_ed = any(keyword in ' '.join(candidate_education).lower() for keyword in higher_ed_keywords)
            return 40.0 if has_higher_ed else 20.0  # Lower score for no matching education

    def _calculate_role_match(self, resume_content: str, job_profile: str) -> float:
        """Calculate how well the candidate's role level matches the job requirements."""
        resume_lower = resume_content.lower()
        job_lower = job_profile.lower()
        
        # Define role hierarchies
        senior_roles = ['senior', 'lead', 'principal', 'staff', 'architect', 'manager', 'director', 'vp', 'cto', 'ceo']
        management_roles = ['manager', 'director', 'head of', 'vp', 'vice president', 'chief', 'team lead', 'engineering manager']
        entry_level_indicators = ['intern', 'junior', 'entry level', 'associate', 'assistant', 'trainee', 'fresh graduate']
        
        # Check what level the job requires
        job_requires_management = any(role in job_lower for role in management_roles)
        job_requires_senior = any(role in job_lower for role in senior_roles)
        
        # Check candidate's current level
        candidate_is_management = any(role in resume_lower for role in management_roles)
        candidate_is_senior = any(role in resume_lower for role in senior_roles)
        candidate_is_entry_level = any(indicator in resume_lower for indicator in entry_level_indicators)
        
        # Calculate role match score
        if job_requires_management:
            if candidate_is_management:
                return 90.0  # Good match
            elif candidate_is_senior:
                return 60.0  # Potential - senior but not manager
            elif candidate_is_entry_level:
                return 10.0  # Poor match - entry level for management role
            else:
                return 30.0  # Unknown level for management role
        
        elif job_requires_senior:
            if candidate_is_senior or candidate_is_management:
                return 85.0  # Good match
            elif candidate_is_entry_level:
                return 25.0  # Poor match - entry level for senior role
            else:
                return 50.0  # Mid-level for senior role
        
        else:
            # Job doesn't specify level clearly
            if candidate_is_entry_level:
                return 60.0  # Neutral - entry level candidate
            elif candidate_is_senior or candidate_is_management:
                return 70.0  # Good - experienced candidate
            else:
                return 55.0  # Unknown level

    def _generate_explanation(self, overall_score: float, skill_score: float, 
                            experience_score: float, education_score: float, role_match_score: float,
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
        
        explanation += f"Role Level Match: {role_match_score:.1f}%\n"
        explanation += f"- Assesses whether candidate's seniority level matches job requirements\n\n"
        
        # Add recommendation with stricter thresholds
        if overall_score >= 75:
            explanation += "Recommendation: Strong candidate - Excellent match for the position."
        elif overall_score >= 60:
            explanation += "Recommendation: Good candidate - Consider for interview with targeted assessment."
        elif overall_score >= 45:
            explanation += "Recommendation: Moderate match - Significant gaps need evaluation."
        elif overall_score >= 30:
            explanation += "Recommendation: Weak match - Consider only if candidate pool is very limited."
        else:
            explanation += "Recommendation: Poor match - Not recommended for this position."
        
        return explanation

    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on score."""
        if score >= 75:
            return "Highly Recommended"
        elif score >= 60:
            return "Recommended"
        elif score >= 45:
            return "Consider with Caution"
        elif score >= 30:
            return "Weak Match"
        else:
            return "Not Recommended"
