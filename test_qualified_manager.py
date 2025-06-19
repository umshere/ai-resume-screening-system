#!/usr/bin/env python3

"""
Test with a qualified Engineering Manager candidate to ensure 
the system still recognizes good matches.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.plugins.resume_screening import ResumeScreeningPlugin
import json

def test_qualified_manager():
    """Test with a qualified Engineering Manager candidate"""
    
    # Same Engineering Manager job profile
    job_profile = """
    Engineering Manager - Senior Position
    
    We are seeking an experienced Engineering Manager to lead our software development team.
    
    Requirements:
    - 7+ years of software engineering experience
    - 3+ years of engineering management experience
    - Experience leading teams of 5-15 engineers
    - Strong technical background in modern web technologies
    - Experience with agile development methodologies
    - Proven track record of delivering complex software projects
    - Experience with hiring, mentoring, and performance management
    - Bachelor's degree in Computer Science or related field
    - Experience with cloud platforms (AWS/Azure/GCP)
    - Strong communication and leadership skills
    """
    
    # Qualified Engineering Manager resume
    qualified_resume = """
    SARAH CHEN
    Senior Engineering Manager
    Email: sarah.chen@email.com
    Phone: (555) 123-4567
    
    PROFESSIONAL EXPERIENCE
    
    Senior Engineering Manager | TechCorp Inc. | 2020 - Present (4 years)
    • Lead a team of 12 software engineers across 3 product squads
    • Responsible for hiring, performance management, and career development of engineering staff
    • Implemented agile development methodologies resulting in 40% faster delivery
    • Managed engineering budget of $2.5M annually
    • Collaborated with product management and design teams on strategic initiatives
    • Led migration to microservices architecture on AWS, improving system scalability by 300%
    • Established CI/CD pipelines using Jenkins and Docker
    
    Engineering Manager | StartupXYZ | 2018 - 2020 (2 years)  
    • Managed team of 8 engineers building customer-facing web applications
    • Led recruitment efforts, successfully hiring 15+ engineers over 2 years
    • Implemented code review processes and mentoring programs
    • Drove adoption of modern development practices including Git workflows and automated testing
    
    Senior Software Engineer | CloudTech Solutions | 2015 - 2018 (3 years)
    • Technical lead for customer platform built with React, Node.js, and PostgreSQL
    • Mentored junior developers and led technical design reviews
    • Implemented DevOps practices and infrastructure automation
    • Led cross-functional projects with product and design teams
    
    Software Engineer | DataSoft Corp | 2012 - 2015 (3 years)
    • Full-stack development using Python, JavaScript, and SQL databases
    • Built scalable web applications serving 100k+ daily active users
    • Collaborated in agile development environment using Scrum methodologies
    
    EDUCATION
    Master of Science in Computer Science | Stanford University | 2012
    Bachelor of Science in Computer Science | UC Berkeley | 2010
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, Java, SQL
    Frameworks: React, Node.js, Django, Flask
    Cloud: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes
    Tools: Git, Jenkins, JIRA, Confluence
    Databases: PostgreSQL, MongoDB, Redis
    
    MANAGEMENT SKILLS
    • Team Leadership & People Management
    • Performance Management & Career Development  
    • Agile/Scrum Methodologies
    • Technical Strategy & Architecture
    • Budget & Resource Planning
    • Hiring & Talent Acquisition
    • Stakeholder Communication
    • Project Management
    
    ACHIEVEMENTS
    • Grew engineering team from 5 to 20 people over 3 years
    • Reduced deployment time from 2 hours to 15 minutes through CI/CD automation
    • Improved team velocity by 45% through process improvements
    • Led successful migration serving 1M+ users with zero downtime
    """

    print("🧪 Testing with Qualified Engineering Manager")
    print("=" * 60)
    print(f"📋 Job Profile: Engineering Manager (Senior Level)")
    print(f"👤 Candidate: Sarah Chen (Qualified Manager)")
    print("=" * 60)

    # Test the screening
    plugin = ResumeScreeningPlugin()
    
    try:
        result_json = plugin.analyze_resume(
            resume_content=qualified_resume,
            job_profile=job_profile,
            candidate_name="Sarah Chen"
        )
        
        result = json.loads(result_json)
        
        print(f"📊 SCREENING RESULTS:")
        print(f"   Overall Score: {result['overall_score']}%")
        print(f"   Skill Match: {result['skill_score']}%") 
        print(f"   Experience Match: {result['experience_score']}%")
        print(f"   Education Match: {result['education_score']}%")
        print(f"   Role Level Match: {result['role_match_score']}%")
        print()
        print(f"📝 DETAILED EXPLANATION:")
        print(result['explanation'])
        print()
        print(f"🔍 EXTRACTED DATA:")
        print(f"   Skills: {result['extracted_skills'][:10]}")  # Show first 10 skills
        print(f"   Experience: {result['extracted_experience']}")
        print(f"   Education: {result['extracted_education']}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_qualified_manager()
