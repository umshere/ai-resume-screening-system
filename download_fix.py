# Fixed Download Section for app.py

def create_download_section():
    """Create stable download buttons that don't reset the page"""
    if 'screening_results' in st.session_state and st.session_state.screening_results and st.session_state.get('screening_completed', False):
        st.markdown("### 📥 Download Reports")
        
        # Generate stable timestamp for downloads
        if 'download_timestamp' not in st.session_state:
            st.session_state.download_timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        timestamp = st.session_state.download_timestamp
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                report_data = generate_detailed_report(st.session_state.screening_results)
                st.download_button(
                    label="📥 Download CSV Report",
                    data=report_data,
                    file_name=f"resume_screening_report_{timestamp}.csv",
                    mime="text/csv",
                    key="stable_csv_download",
                    help="Download detailed screening results as CSV",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating CSV report: {str(e)}")
        
        with col2:
            try:
                summary_data = generate_summary_report(st.session_state.screening_results)
                st.download_button(
                    label="📄 Download Summary Report", 
                    data=summary_data,
                    file_name=f"resume_screening_summary_{timestamp}.txt",
                    mime="text/plain",
                    key="stable_summary_download",
                    help="Download summary report as text file",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating summary report: {str(e)}")
    else:
        st.info("📥 Download options will appear after screening is completed.")

# Add this function call where the download section should be
# create_download_section()
