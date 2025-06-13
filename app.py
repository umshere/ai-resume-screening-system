import asyncio
import streamlit as st
import pandas as pd
import io
import PyPDF2
import docx
from typing import List, Dict
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

async def main_screening(job_profile, resumes, num_agents, max_interactions=10):
    """Main screening process"""
    expert_agents, expert_agents_names, mas = await run_resume_screening(job_profile, resumes, num_agents)
    
    with st.sidebar:
        st.title("🤖 Expert Screening Agents")
        agent_placeholders = {name: st.empty() for name in expert_agents_names}
        agent_status = {name: "⏳ Initializing..." for name in expert_agents_names}
        
        for agent_name in expert_agents_names:
            agent_placeholders[agent_name].markdown(
                f'<div class="agent-status">👤 <strong>{agent_name}</strong><br>{agent_status[agent_name]}</div>', 
                unsafe_allow_html=True
            )
            await asyncio.sleep(1)

    selection_function = mas.create_selection_function(expert_agents_names)
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
    
    with st.spinner("🔍 Screening resumes..."):
        while not is_complete and interactions < max_interactions:
            # Update agent status
            current_agent = expert_agents_names[interactions % len(expert_agents_names)]
            agent_status[current_agent] = f"🔍 Working on analysis... (Round {interactions + 1})"
            agent_placeholders[current_agent].markdown(
                f'<div class="agent-status">👤 <strong>{current_agent}</strong><br>{agent_status[current_agent]}</div>', 
                unsafe_allow_html=True
            )
            
            status_text.text(f"Step {interactions + 1}/{max_interactions}: {current_agent} is analyzing...")
            progress_bar.progress((interactions + 1) / max_interactions)
            
            await group.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=screening_input))

            async for response in group.invoke_stream():
                # Check if the response contains termination keyword
                if termination_keyword.lower() in response.content.lower():
                    is_complete = True
                    break

            interactions += 1
            await asyncio.sleep(1)
    
    # Update final status
    for agent_name in expert_agents_names:
        agent_status[agent_name] = "✅ Analysis Complete"
        agent_placeholders[agent_name].markdown(
            f'<div class="agent-status">👤 <strong>{agent_name}</strong><br>{agent_status[agent_name]}</div>', 
            unsafe_allow_html=True
        )
    
    progress_bar.progress(1.0)
    status_text.text("✅ Resume screening completed!")
# Streamlit UI for Resume Screening
def app():
    st.title("📋 AI Resume Screening & Matching System 📋")
    st.subheader("Intelligent resume screening with AI expert agents")
    
    # Initialize session state
    if 'screening_results' not in st.session_state:
        st.session_state.screening_results = None
    if 'running' not in st.session_state:
        st.session_state.running = False
    
    # Create two main columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Job Profile")
        
        # Job profile input options
        job_input_method = st.radio(
            "How would you like to provide the job profile?",
            ["📝 Direct Text Input", "🔗 URL/Link"],
            horizontal=True
        )
        
        job_profile = ""
        if job_input_method == "📝 Direct Text Input":
            job_profile = st.text_area(
                "Enter the job description:",
                height=300,
                placeholder="Paste the complete job description here including requirements, skills, experience, etc.",
                help="Provide detailed job requirements for accurate matching"
            )
        else:
            job_url = st.text_input(
                "Enter job posting URL:",
                placeholder="https://example.com/job-posting",
                help="We'll extract the job description from this URL"
            )
            if job_url:
                st.info("URL processing will be implemented to extract job details")
                # TODO: Implement URL processing
                job_profile = "URL processing feature coming soon. Please use direct text input for now."
    
    with col2:
        st.markdown("### 📄 Resumes")
        
        # Resume upload
        uploaded_files = st.file_uploader(
            "Upload resume files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Support for PDF, DOCX, and TXT files. You can upload multiple resumes at once."
        )
        
        resumes = []
        if uploaded_files:
            with st.spinner("📖 Processing uploaded resumes..."):
                resumes = process_resume_files(uploaded_files)
            
            if resumes:
                st.success(f"✅ Successfully processed {len(resumes)} resume(s)")
                with st.expander("📋 Preview processed resumes"):
                    for i, resume in enumerate(resumes):
                        st.markdown(f"**{i+1}. {resume['filename']}**")
                        st.text(resume['content'][:200] + "..." if len(resume['content']) > 200 else resume['content'])
                        st.divider()
    
    # Agent configuration
    st.markdown("### ⚙️ Screening Configuration")
    col_config1, col_config2 = st.columns([1, 1])
    
    with col_config1:
        num_agents = st.slider(
            "Number of expert agents",
            min_value=2,
            max_value=6,
            value=4,
            help="More agents provide more detailed analysis but take longer"
        )
    
    with col_config2:
        analysis_depth = st.selectbox(
            "Analysis depth",
            ["Quick Overview", "Standard Analysis", "Deep Dive"],
            index=1,
            help="Choose the level of analysis detail"
        )
    
    # Start screening button
    st.markdown("### 🚀 Start Screening")
    
    can_start = job_profile.strip() and resumes
    if not can_start:
        if not job_profile.strip():
            st.warning("⚠️ Please provide a job profile")
        if not resumes:
            st.warning("⚠️ Please upload at least one resume")
    
    if st.button(
        '🔍 Start Resume Screening',
        disabled=not can_start or st.session_state.running,
        type="primary",
        use_container_width=True
    ):
        if can_start:
            st.session_state.running = True
            with st.container():
                st.markdown("---")
                st.markdown("### 📊 Screening Progress")
                
                # Run the screening process
                try:
                    screening_results = asyncio.run(
                        main_screening(job_profile, resumes, num_agents)
                    )
                    st.session_state.screening_results = screening_results
                    st.session_state.running = False
                    
                    # Display results
                    display_screening_results(screening_results, resumes)
                    
                except Exception as e:
                    st.error(f"❌ An error occurred during screening: {str(e)}")
                    st.session_state.running = False
    
    # Display previous results if available
    if st.session_state.screening_results and not st.session_state.running:
        st.markdown("---")
        st.markdown("### 📊 Latest Screening Results")
        display_screening_results(st.session_state.screening_results, resumes)

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