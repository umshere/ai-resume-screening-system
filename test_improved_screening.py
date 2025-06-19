#!/usr/bin/env python3

"""
Test the improved resume screening system with the student resume
to verify it gives more realistic scores.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.plugins.resume_screening import ResumeScreeningPlugin
import json

def test_student_resume():
    """Test the student resume that was previously scoring 80%"""
    
    # Engineering Manager job profile
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
    
    Preferred:
    - Master's degree in Computer Science or MBA
    - Experience with distributed systems and microservices
    - DevOps and CI/CD experience
    - Previous experience at high-growth technology companies
    """
    
    # Student resume (Priyanshu Jain)
    student_resume = """
    PRIYANSHU JAIN
    B.E. (Hons.), Electrical & Electronics, 2026
    Email: f20220538@pilani.bits-pilani.ac.in
    Mobile: 9678128228
    CGPA: 7.73

    ACADEMIC DETAILS
    COURSE: CLASS XII - B.M Jain National Academy, Assam Higher Secondary Education Council (AHSEC), 2022
    COURSE: CLASS X - Fatima Convent Senior Secondary School, CBSE, 2020

    Subjects / Electives
    Supply Chain Management, Artificial Intelligence, Organisational Psychology, Effective Public Speaking

    Technical Proficiency
    Product Management, Mixpanel, SQL, Metabase, JavaScript, Application Development, Postman

    SUMMER INTERNSHIP / WORK EXPERIENCE
    Product Intern, Grip Invest - May 2024 - Nov 2024
    Product Management Intern, MindPeers - Feb 2024 - May 2024
    • Designed the IFA dashboard and managed its development, enhancing partner experience in tracking and managing their investors
    • Developed an internal tool using Retool to update users' KRA in bulk via REST API, reducing manual labour by 30 hours per week
    • Led the event tracking plan for the app and enhanced website event tracking, boosting data reliability and improving user insights
    • Analysed user drop-off points in the therapy booking funnel using MixPanel, suggesting changes that increased completion rates by 8%
    • Articulated PRD for the therapist dashboard, streamlining and automating mundane tasks related to therapists, saving 25 hours weekly
    • Implemented UI tweaks in the therapy booking section, enhancing user experience and reducing the TAT of therapy booking by 14%

    POSITION OF RESPONSIBILITY
    Marketing and Tech Lead - PIEDS Student Team - May 2023 - Present
    Senior Member, Training Unit - Placement Unit - Aug 2024 - Dec 2024
    • Sourced and Assessed 150+ startups under the NIDHI SSP Govt Scheme, which provides seed grants up to INR 1 Crore per start-up
    • Coordinated a 2-day BootCamp and 8-week mentorship program, partnering with 20+ organisations and raising INR 12.5 lakhs
    • Organised Enspire, an on-campus panel discussion featuring distinguished BITSian entrepreneurs, with an influx of 150+ attendees

    VOLUNTEER EXPERIENCE
    NSS - Nov 2022 - Oct 2023 - Role: Volunteer | Cause: Education
    • Boosted a 15% increase in funds raised during the 3-day fundraiser, enabling scholarships for 100+ economically backward students

    PROJECTS
    Optimizing Medical Waste Management in Healthcare Facilities - Supply Chain Model and Empirical Analysis - Aug 2024 - Oct 2024
    Supply Chain Analysis on Cisco - Supply Chain Management - Aug 2024 - Oct 2024
    • Developed a decision-making model to optimise waste management in healthcare facilities using Multi-Criteria Decision Analysis
    • Analysed Cisco's supply chain and strategic fit under Prof. Srikanta Routroy, identifying inefficiencies and areas of improvement

    EXTRA CURRICULAR ACTIVITIES
    • Secured 1st position in Virtual Stock Market competition conducted by E-Cell IIT Bombay among 10k+ participants nationwide
    • Served as the House Captain at Fatima Convent School, leading 4+ sports teams and coordinating Inter-House competition
    """

    print("🧪 Testing Improved Resume Screening System")
    print("=" * 60)
    print(f"📋 Job Profile: Engineering Manager (Senior Level)")
    print(f"👤 Candidate: Priyanshu Jain (Student)")
    print("=" * 60)

    # Test the screening
    plugin = ResumeScreeningPlugin()
    
    try:
        result_json = plugin.analyze_resume(
            resume_content=student_resume,
            job_profile=job_profile,
            candidate_name="Priyanshu Jain"
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
        print(f"   Skills: {result['extracted_skills']}")
        print(f"   Experience: {result['extracted_experience']}")
        print(f"   Education: {result['extracted_education']}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_student_resume()
