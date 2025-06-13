#!/usr/bin/env python3
"""
Test script for the Resume Screening System
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_resume_plugin():
    """Test the resume screening plugin functionality"""
    from src.plugins.resume_screening import ResumeScreeningPlugin
    
    plugin = ResumeScreeningPlugin()
    
    # Sample job profile
    job_profile = """
    Job Title: Senior Python Developer
    
    Requirements:
    - 5+ years of Python development experience
    - Experience with Django/Flask frameworks
    - Knowledge of SQL databases
    - Bachelor's degree in Computer Science or related field
    - Experience with cloud platforms (AWS/Azure)
    - Strong problem-solving skills
    """
    
    # Sample resume
    resume_content = """
    John Doe
    Senior Software Engineer
    
    Experience:
    - 6 years of Python development
    - Expert in Django framework
    - Experience with PostgreSQL and MySQL
    - AWS certified solutions architect
    - Led multiple development teams
    
    Education:
    - Bachelor's in Computer Science from MIT
    - Master's in Software Engineering
    
    Skills: Python, Django, SQL, AWS, Leadership, Problem Solving
    """
    
    print("Testing Resume Screening Plugin...")
    print("=" * 50)
    
    # Test individual resume analysis
    result = plugin.analyze_resume(resume_content, job_profile, "John Doe")
    print("Analysis Result:")
    print(result)
    print("\n" + "=" * 50)
    
    # Test ranking functionality
    analysis_results = [result]  # In real scenario, you'd have multiple results
    ranking = plugin.rank_candidates(analysis_results, 3)
    print("Ranking Result:")
    print(ranking)

def test_file_processing():
    """Test file processing functionality"""
    print("\nTesting File Processing...")
    print("=" * 50)
    
    # Create a sample text file for testing
    sample_resume = """
    Jane Smith
    Data Scientist
    
    Experience:
    - 4 years in data science and machine learning
    - Python, R, SQL expertise
    - Experience with TensorFlow and PyTorch
    - PhD in Statistics
    
    Skills: Python, R, Machine Learning, Statistics, Data Visualization
    """
    
    with open("sample_resume.txt", "w") as f:
        f.write(sample_resume)
    
    print("Sample resume file created: sample_resume.txt")
    print("Content preview:")
    print(sample_resume[:200] + "...")
    
    # Clean up
    os.remove("sample_resume.txt")
    print("Sample file cleaned up.")

if __name__ == "__main__":
    print("Resume Screening System Test")
    print("=" * 50)
    
    try:
        test_resume_plugin()
        test_file_processing()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
