import asyncio
import streamlit as st
import pandas as pd
import io
import PyPDF2
import docx
from typing import List, Dict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from src.mas import Orchestrator, MultiAgent

st.set_page_config(
    page_title="AI Resume Screening & Matching System",
    page_icon="📋",
    layout="wide"
)

# Enhanced CSS for resume screening interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(-45deg, #667eea, #764ba2, #6b73ff, #9a9ce1);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        margin: 0;
        padding: 0;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stFileUploader {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1em;
        border: 2px dashed #667eea;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.9);
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #667eea;
        color: #fff;
        border: none;
        border-radius: 10px;
        font-size: 1em;
        padding: 0.6em 1em;
        margin-top: 1em;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton>button:hover {
        background-color: #764ba2;
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.3);
    }
    .agent-status {
        background: rgba(255,255,255,0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #667eea;
    }
    .matching-score {
        font-size: 2em;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #fff;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def process_resume_files(uploaded_files) -> List[Dict]:
    """Process uploaded resume files and extract text"""
    resumes = []
    for uploaded_file in uploaded_files:
        st.write(f"🔍 Processing: {uploaded_file.name} (Type: {uploaded_file.type})")
        
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = str(uploaded_file.read(), "utf-8")
        else:
            st.warning(f"Unsupported file type: {uploaded_file.type}")
            continue
            
        if text.strip():
            resumes.append({
                "filename": uploaded_file.name,
                "content": text
            })
            st.success(f"✅ Successfully extracted {len(text)} characters from {uploaded_file.name}")
        else:
            st.error(f"❌ Failed to extract text from {uploaded_file.name} - file appears to be empty or corrupted")
    
    st.write(f"📊 Total processed resumes: {len(resumes)}")
    return resumes

async def run_resume_screening(job_profile, resumes, num_agents):
    """Run the resume screening process"""
    # Create screening context
    screening_context = {
        "job_profile": job_profile,
        "resumes": resumes,
        "num_resumes": len(resumes)
    }
    
    orchestrator = Orchestrator(screening_context, num_agents)
    dynamic_agents = orchestrator.run()

    mas = MultiAgent()
    expert_agents = mas.create_agents(dynamic_agents)
    expert_agents_names = [agent.name for agent in expert_agents]

    return expert_agents, expert_agents_names, mas

async def main_screening(job_profile, resumes, num_agents, max_interactions=None):
    """Main screening process"""
    expert_agents, expert_agents_names, mas = await run_resume_screening(job_profile, resumes, num_agents)
    
    # Set max_interactions based on number of agents if not specified
    if max_interactions is None:
        max_interactions = max(num_agents * 2, 4)  # At least 2 rounds per agent, minimum 4
    
    with st.sidebar:
        st.title("🤖 Expert Screening Agents")
        agent_placeholders = {name: st.empty() for name in expert_agents_names}
        agent_status = {name: "⏳ Initializing..." for name in expert_agents_names}
        
        # Define agent specializations for better user understanding
        agent_specializations = {
            "Skills_Analysis_Agent": "🔧 Technical Skills & Expertise",
            "Experience_Evaluation_Agent": "📈 Work Experience & Career",
            "Education_Assessment_Agent": "🎓 Educational Background",
            "Cultural_Fit_Agent": "🤝 Team & Cultural Alignment",
            "Leadership_Assessment_Agent": "👑 Leadership & Management",
            "Technical_Depth_Agent": "🔬 Deep Technical Analysis"
        }
        
        for agent_name in expert_agents_names:
            specialization = agent_specializations.get(agent_name, "🔍 General Analysis")
            agent_placeholders[agent_name].markdown(
                f'<div class="agent-status">👤 <strong>{agent_name}</strong><br><small>{specialization}</small><br>⏳ Initializing...</div>', 
                unsafe_allow_html=True
            )
            await asyncio.sleep(1)

    selection_function = mas.create_selection_function(expert_agents)
    termination_keyword = 'yes'
    termination_function = mas.create_termination_function(termination_keyword)

    group = mas.create_chat_group(
        expert_agents,
        selection_function,
        termination_function,
        termination_keyword
    )

    interactions: int = 0
    is_complete: bool = False
    
    # Define detailed agent activities based on their roles
    def get_agent_activity(agent_name, round_num, total_resumes):
        """Get detailed activity description for each agent"""
        activities = {
            "Skills_Analysis_Agent": [
                f"🔍 Analyzing technical skills alignment across {total_resumes} resume(s)",
                f"⚙️ Evaluating programming languages and frameworks",
                f"🛠️ Assessing tool proficiency and certifications",
                f"📊 Cross-referencing skill requirements with candidate experience"
            ],
            "Experience_Evaluation_Agent": [
                f"📈 Evaluating work experience relevance for {total_resumes} candidate(s)",
                f"🏢 Analyzing company backgrounds and industry experience",
                f"📅 Assessing career progression and tenure patterns",
                f"🎯 Matching role responsibilities with job requirements"
            ],
            "Education_Assessment_Agent": [
                f"🎓 Reviewing educational qualifications for {total_resumes} resume(s)",
                f"🏫 Evaluating degree relevance and institution reputation",
                f"📚 Assessing additional certifications and training",
                f"🧠 Analyzing academic achievements and projects"
            ],
            "Cultural_Fit_Agent": [
                f"🤝 Analyzing cultural alignment indicators across {total_resumes} profile(s)",
                f"💭 Evaluating communication style and collaboration signals",
                f"🌟 Assessing leadership potential and team dynamics",
                f"🎯 Reviewing personality traits and work style indicators"
            ],
            "Leadership_Assessment_Agent": [
                f"👑 Evaluating leadership experience in {total_resumes} candidate(s)",
                f"📊 Analyzing team management and project leadership",
                f"🚀 Assessing strategic thinking and decision-making",
                f"🌟 Reviewing mentoring and development capabilities"
            ],
            "Technical_Depth_Agent": [
                f"🔬 Deep-diving into technical expertise across {total_resumes} resume(s)",
                f"⚡ Analyzing system architecture and design experience",
                f"🧪 Evaluating problem-solving and debugging skills",
                f"🔧 Assessing code quality and best practices knowledge"
            ]
        }
        
        # Get activities for this agent, default to generic if not found
        agent_activities = activities.get(agent_name, [
            f"🔍 Analyzing candidate profiles for {total_resumes} resume(s)",
            f"📊 Evaluating qualifications and requirements",
            f"🎯 Assessing job-candidate alignment",
            f"📈 Generating detailed analysis insights"
        ])
        
        # Return activity based on round number (cycle through activities)
        activity_index = (round_num - 1) % len(agent_activities)
        return agent_activities[activity_index]
    
    # Create screening context
    screening_input = f"""
    Job Profile: {job_profile}
    
    Number of Resumes to Screen: {len(resumes)}
    
    Resumes:
    {chr(10).join([f"{i+1}. {resume['filename']}: {resume['content'][:500]}..." for i, resume in enumerate(resumes)])}
    
    Please analyze each resume against the job profile and provide matching scores with detailed explanations.
    """
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    detailed_status = st.empty()
    
    with st.spinner("🔍 Screening resumes..."):
        while not is_complete and interactions < max_interactions:
            # Update agent status with detailed activity
            current_agent = expert_agents_names[interactions % len(expert_agents_names)]
            current_round = interactions + 1
            
            # Get detailed activity for this agent
            current_activity = get_agent_activity(current_agent, current_round, len(resumes))
            
            agent_status[current_agent] = f"🔍 {current_activity.split(' ', 1)[1]}"  # Remove emoji from activity
            specialization = agent_specializations.get(current_agent, "🔍 General Analysis")
            agent_placeholders[current_agent].markdown(
                f'<div class="agent-status">👤 <strong>{current_agent}</strong><br><small>{specialization}</small><br>🔍 {current_activity.split(" ", 1)[1]}</div>', 
                unsafe_allow_html=True
            )
            
            # Update main status with detailed information
            phase = "Initial Analysis" if current_round <= max_interactions // 2 else "Deep Analysis & Validation"
            status_text.markdown(f"**Round {current_round}/{max_interactions}** | **{current_agent}** | {len(expert_agents)} agents total | *{phase}*")
            detailed_status.info(f"🎯 {current_activity}")
            progress_bar.progress(current_round / max_interactions)
            
            await group.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=screening_input))

            async for response in group.invoke_stream():
                # Check if the response contains termination keyword
                if termination_keyword.lower() in response.content.lower():
                    is_complete = True
                    break

            interactions += 1
            await asyncio.sleep(1)
    
    # Update final status with completion summary
    for agent_name in expert_agents_names:
        agent_status[agent_name] = "✅ Analysis Complete - Ready for results compilation"
        specialization = agent_specializations.get(agent_name, "🔍 General Analysis")
        agent_placeholders[agent_name].markdown(
            f'<div class="agent-status">👤 <strong>{agent_name}</strong><br><small>{specialization}</small><br>✅ Analysis Complete</div>', 
            unsafe_allow_html=True
        )
    
    progress_bar.progress(1.0)
    status_text.markdown("**✅ Resume screening completed!**")
    detailed_status.success(f"🎉 All {len(expert_agents)} agents have completed their analysis of {len(resumes)} resume(s). Compiling final results...")
# Streamlit UI for Resume Screening
def app():
    # Initialize session state variables
    if 'job_profile' not in st.session_state:
        st.session_state.job_profile = ""
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'num_agents' not in st.session_state:
        st.session_state.num_agents = 4
    if 'analysis_depth' not in st.session_state:
        st.session_state.analysis_depth = "Standard Analysis"
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'screening_results' not in st.session_state:
        st.session_state.screening_results = None

    st.title("📋 AI Resume Screening & Matching System 📋")
    st.subheader("Intelligent resume screening with AI expert agents")
    
    # Progress indicator
    progress_steps = ["Job Profile", "Resumes", "Configuration", "Review & Start"]
    completed_steps = []
    
    if st.session_state.job_profile.strip():
        completed_steps.append("Job Profile")
    if st.session_state.resumes:
        completed_steps.append("Resumes")
    if st.session_state.num_agents >= 2:
        completed_steps.append("Configuration")
    
    # Progress bar
    progress_value = len(completed_steps) / len(progress_steps)
    st.progress(progress_value, text=f"Setup Progress: {len(completed_steps)}/{len(progress_steps)} steps completed")
    
    # Progress indicators row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = "✅" if "Job Profile" in completed_steps else "⭕"
        st.markdown(f"**{status} Job Profile**")
    with col2:
        status = "✅" if "Resumes" in completed_steps else "⭕"
        st.markdown(f"**{status} Resumes**")
    with col3:
        status = "✅" if "Configuration" in completed_steps else "⭕"
        st.markdown(f"**{status} Configuration**")
    with col4:
        status = "✅" if len(completed_steps) == 4 else "⭕"
        st.markdown(f"**{status} Ready to Start**")
    
    st.markdown("---")
    
    # Tab-based wizard flow with enhanced titles
    tab_titles = [
        f"📝 Job Profile {'✅' if 'Job Profile' in completed_steps else ''}",
        f"📄 Resumes {'✅' if 'Resumes' in completed_steps else ''}",
        f"⚙️ Configuration {'✅' if 'Configuration' in completed_steps else ''}",
        f"🚀 Review & Start {'✅' if len(completed_steps) == 4 else ''}"
    ]
    
    tab1, tab2, tab3, tab4 = st.tabs(tab_titles)

    with tab1:
        # Job Profile section
        st.markdown("### 📝 Job Profile")
        
        # Job profile input options
        job_input_method = st.radio(
            "How would you like to provide the job profile?",
            ["📝 Direct Text Input", "🔗 URL/Link"],
            horizontal=True
        )
        
        if job_input_method == "📝 Direct Text Input":
            job_profile_input = st.text_area(
                "Enter the job description:",
                value=st.session_state.job_profile,
                height=300,
                placeholder="Example: Senior Software Engineer position requiring 5+ years experience in Python, React, and cloud technologies. Must have experience with microservices architecture...",
                help="💡 Tip: Include specific skills, experience requirements, and qualifications for better matching accuracy"
            )
            
            # Character counter and validation
            char_count = len(job_profile_input)
            if char_count > 0:
                if char_count < 100:
                    st.warning(f"📝 {char_count} characters - Consider adding more details for better analysis")
                else:
                    st.success(f"✅ {char_count} characters - Good job description length!")
            
            st.session_state.job_profile = job_profile_input
        else:
            job_url = st.text_input(
                "Enter job posting URL:",
                placeholder="https://example.com/job-posting",
                help="We'll extract the job description from this URL"
            )
            if job_url:
                st.info("URL processing will be implemented to extract job details")
                # TODO: Implement URL processing
                st.session_state.job_profile = "URL processing feature coming soon. Please use direct text input for now."

        # Show resume status with enhanced styling
        if st.session_state.resumes:
            st.markdown(
                f"""
                <div style="
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 10px 0;
                ">
                    <h4 style="color: #155724; margin: 0;">✅ Resume Upload Complete</h4>
                    <p style="color: #155724; margin: 5px 0 0 0;">
                        {len(st.session_state.resumes)} resume(s) successfully processed. 
                        You can manage them in the 'Resumes' tab.
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="
                    background-color: #fff3cd; 
                    border: 1px solid #ffeaa7; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 10px 0;
                ">
                    <h4 style="color: #856404; margin: 0;">📄 Next Step: Upload Resumes</h4>
                    <p style="color: #856404; margin: 5px 0 0 0;">
                        Navigate to the 'Resumes' tab to upload candidate files for screening.
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )


    with tab2:
        # Resumes section (for detailed file management)
        st.markdown("### 📄 Resumes")
        uploaded_files_tab2 = st.file_uploader( # Changed variable name for clarity
            "Upload resume files here:", # Slightly different label
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Support for PDF, DOCX, and TXT files. You can upload multiple resumes at once.",
            key="resume_uploader_tab2"  # Unique key for this file_uploader
        )
        
        if uploaded_files_tab2:
            with st.spinner("📖 Processing uploaded resumes..."):
                st.info(f"🔍 Processing {len(uploaded_files_tab2)} uploaded file(s)...")
                newly_processed_resumes = process_resume_files(uploaded_files_tab2)
                st.success(f"✅ Successfully processed {len(newly_processed_resumes)} resume(s) from upload")
                
                # Append new resumes to existing ones in session state, avoiding duplicates by filename
                existing_filenames = {r['filename'] for r in st.session_state.resumes}
                added_count = 0
                for res in newly_processed_resumes:
                    if res['filename'] not in existing_filenames:
                        st.session_state.resumes.append(res)
                        existing_filenames.add(res['filename'])
                        added_count += 1
                    else:
                        st.warning(f"⚠️ Skipped duplicate file: {res['filename']}")
                
                if added_count > 0:
                    st.success(f"➕ Added {added_count} new resume(s) to your collection")
            
        if st.session_state.resumes:
            st.success(f"✅ Successfully processed {len(st.session_state.resumes)} resume(s)")
            
            # Debug information
            with st.expander("🔍 Debug Information", expanded=False):
                st.write("**Current resumes in session state:**")
                for i, resume in enumerate(st.session_state.resumes):
                    st.write(f"{i+1}. {resume['filename']} ({len(resume['content'])} chars)")
            
            col_clear, col_space = st.columns([1, 3])
            with col_clear:
                if st.button("🗑️ Clear All Resumes", help="Remove all uploaded files and start over", key="clear_resumes_button"):
                    st.session_state.resumes = []
                    st.rerun()
            
            # Enhanced resume preview with file info
            with st.expander(f"📋 Preview Resumes ({len(st.session_state.resumes)})", expanded=False):
                for i, resume in enumerate(st.session_state.resumes):
                    # File info header
                    file_extension = resume['filename'].split('.')[-1].upper()
                    file_size = f"{len(resume['content'])} chars"
                    
                    col_info, col_remove = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"**📄 {i+1}. {resume['filename']}** (`{file_extension}` • {file_size})")
                    with col_remove:
                        if st.button("❌", key=f"remove_{i}", help=f"Remove {resume['filename']}"):
                            st.session_state.resumes.pop(i)
                            st.rerun()
                    
                    # Content preview
                    preview_text = resume['content'][:300] + "..." if len(resume['content']) > 300 else resume['content']
                    st.text_area(
                        f"Content preview:",
                        value=preview_text,
                        height=100,
                        disabled=True,
                        key=f"preview_{i}"
                    )
                    if i < len(st.session_state.resumes) - 1:
                        st.divider()
            # Clear the uploader after processing to prevent re-processing on rerun if files are not changed by user
            # This is a common pattern but might need adjustment based on desired UX
            # For now, let's rely on session state to manage the list of resumes.

    with tab3:
        # Screening Configuration section
        st.markdown("### ⚙️ Screening Configuration")
        st.markdown("Configure the AI agents and analysis depth for optimal screening results.")
        
        col_config1, col_config2 = st.columns([1, 1])
        
        with col_config1:
            st.markdown("**👥 Expert Agents**")
            num_agents = st.number_input(
                "Number of expert agents",
                min_value=2,
                max_value=6,
                value=st.session_state.num_agents,
                step=1,
                help="💡 More agents provide more detailed analysis but take longer to complete"
            )
            st.session_state.num_agents = num_agents
            
            # Agent explanation
            agent_descriptions = {
                2: "Basic analysis with 2 core agents",
                3: "Balanced analysis with 3 specialized agents", 
                4: "Comprehensive analysis with 4 expert agents (Recommended)",
                5: "Detailed analysis with 5 specialized agents",
                6: "Maximum analysis with 6 expert agents"
            }
            st.info(f"🤖 {agent_descriptions.get(num_agents, 'Custom configuration')}")
            
        with col_config2:
            st.markdown("**🔍 Analysis Depth**")
            analysis_depth = st.selectbox(
                "Analysis depth",
                ["Quick Overview", "Standard Analysis", "Deep Dive"],
                index=["Quick Overview", "Standard Analysis", "Deep Dive"].index(st.session_state.analysis_depth),
                help="Choose the level of detail for resume analysis"
            )
            st.session_state.analysis_depth = analysis_depth
            
            # Depth explanation
            depth_descriptions = {
                "Quick Overview": "⚡ Fast screening with key highlights",
                "Standard Analysis": "⚖️ Balanced analysis with detailed insights", 
                "Deep Dive": "🔬 Comprehensive analysis with detailed explanations"
            }
            st.info(depth_descriptions[analysis_depth])

    with tab4:
        # Review inputs and final Start Screening button
        st.markdown("### 🚀 Review & Start Screening")
        # Ensure job_profile is initialized, e.g., from session_state or set to empty string
        job_profile_tab4 = st.session_state.get('job_profile', "") # Get from session_state or default
        resumes_tab4 = st.session_state.get('resumes', []) # Get from session_state or default

        can_start = job_profile_tab4.strip() and resumes_tab4
        
        # Display a summary of what will be screened
        if job_profile_tab4.strip():
            with st.expander("Review Job Profile", expanded=False):
                st.text_area("Job Profile:", value=job_profile_tab4, height=150, disabled=True, key="review_job_profile")
        else:
            st.warning("⚠️ Please provide a job profile in the 'Job Profile' tab.")

        if resumes_tab4:
            with st.expander(f"Review Resumes ({len(resumes_tab4)})", expanded=False):
                st.write(f"**Total resumes to be screened: {len(resumes_tab4)}**")
                for i, resume in enumerate(resumes_tab4):
                    st.markdown(f"**{i+1}. {resume['filename']}** ({len(resume['content'])} characters)")
                    
                # Debug section
                st.write("---")
                st.write("**Debug Info:**")
                st.write(f"Session state resumes count: {len(st.session_state.get('resumes', []))}")
                st.write(f"Local resumes_tab4 count: {len(resumes_tab4)}")
        else:
            st.warning("⚠️ Please upload at least one resume in the 'Resumes' tab.")

        if st.button(
            '🔍 Start Resume Screening',
            disabled=not can_start or st.session_state.get('running', False),
            type="primary",
            use_container_width=True,
            key="start_screening_button_tab4" # Added key
        ):
            if can_start:
                st.session_state.running = True
                # ... rest of your screening logic ...
                # Ensure job_profile and resumes are correctly passed to main_screening
                # For example, by retrieving them from session_state if they are stored there
                # or by ensuring they are correctly scoped from the tabs.
                
                # Assuming job_profile and resumes are updated in session_state from their respective tabs
                job_profile_to_screen = st.session_state.get('job_profile', "")
                resumes_to_screen = st.session_state.get('resumes', [])

                with st.container():
                    st.markdown("---")
                    st.markdown("### 📊 Screening Progress")
                    
                    try:
                        screening_results = asyncio.run(
                            main_screening(job_profile_to_screen, resumes_to_screen, st.session_state.get('num_agents', 4)) # Ensure num_agents is also available
                        )
                        st.session_state.screening_results = screening_results
                        st.session_state.running = False
                        
                        # Display results
                        display_screening_results(screening_results, resumes_to_screen)
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred during screening: {str(e)}")
                        st.session_state.running = False
    
    # Display previous results if available
    if st.session_state.get('screening_results') and not st.session_state.get('running', False):
        st.markdown("---")
        st.markdown("### 📊 Latest Screening Results")
        display_screening_results(st.session_state.screening_results, st.session_state.get('resumes', []))

def display_screening_results(results, resumes):
    """Display the screening results in an organized format"""
    st.markdown("### 🎯 Matching Results")
    
    # Mock results for demonstration (replace with actual agent results)
    sample_results = []
    for i, resume in enumerate(resumes):
        score = 85 - (i * 5)  # Mock decreasing scores
        sample_results.append({
            "filename": resume["filename"],
            "score": score,
            "explanation": f"Strong match with {score}% compatibility. Candidate shows excellent technical skills and relevant experience.",
            "strengths": ["Technical expertise", "Industry experience", "Education background"],
            "concerns": ["Limited experience in specific domain", "Skill gap in emerging technologies"]
        })
    
    # Sort by score
    sample_results.sort(key=lambda x: x["score"], reverse=True)
    
    for i, result in enumerate(sample_results):
        with st.expander(f"🏆 #{i+1} - {result['filename']} - Score: {result['score']}%", expanded=i < 3):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f'<div class="matching-score">{result["score"]}%</div>', unsafe_allow_html=True)
                
                # Score interpretation
                if result["score"] >= 80:
                    st.success("🎯 Excellent Match")
                elif result["score"] >= 60:
                    st.warning("⚡ Good Match")
                else:
                    st.error("❌ Poor Match")
            
            with col2:
                st.markdown("**📝 Analysis Summary:**")
                st.write(result["explanation"])
                
                st.markdown("**✅ Strengths:**")
                for strength in result["strengths"]:
                    st.write(f"• {strength}")
                
                st.markdown("**⚠️ Areas of Concern:**")
                for concern in result["concerns"]:
                    st.write(f"• {concern}")
    
    # Download report button
    if st.button("📥 Download Detailed Report", type="secondary"):
        # Generate and download report
        report_data = generate_report(sample_results)
        st.download_button(
            label="📄 Download CSV Report",
            data=report_data,
            file_name="resume_screening_report.csv",
            mime="text/csv"
        )

def generate_report(results):
    """Generate a CSV report of the screening results"""
    import io
    output = io.StringIO()
    
    # Create CSV content
    output.write("Rank,Filename,Score,Status,Summary\n")
    for i, result in enumerate(results):
        status = "Excellent" if result["score"] >= 80 else "Good" if result["score"] >= 60 else "Poor"
        output.write(f"{i+1},{result['filename']},{result['score']}%,{status},\"{result['explanation']}\"\n")
    
    return output.getvalue()

if __name__ == "__main__":
    app()