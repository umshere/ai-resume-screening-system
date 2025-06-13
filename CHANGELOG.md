# AI Multi-Agent Resume Screening System Changelog

<a name="0.2.0-alpha"></a>
# 0.2.0-alpha (2025-06-13)

*Major System Transformation*
* Converted from presentation builder to resume screening and matching system
* Complete redesign of multi-agent architecture for HR and recruitment use cases
* New interactive Streamlit UI optimized for resume screening workflows

*New Features*
* Resume processing support for PDF, DOCX, and TXT formats
* Job profile input via direct text or URL
* Multi-agent screening with specialized expertise areas
* AI-powered matching scores with detailed explanations
* Real-time progress tracking and agent status visualization
* Comprehensive candidate ranking and reporting
* Downloadable CSV reports for screening results

*Technical Changes*
* New ResumeScreeningPlugin for candidate analysis
* Updated orchestrator prompts for resume screening
* Enhanced file processing and text extraction
* Improved error handling and user feedback
* New dependencies: PyPDF2, python-docx, pandas

*Breaking Changes*
* Not backward compatible with presentation builder version
* Environment variables and configuration updated
* Agent prompts completely redesigned
* UI and workflows completely changed for HR use case

<a name="0.1.0-alpha"></a>
# 0.1.0-alpha (Previous)

*Legacy Features (Presentation Builder)*
* Multi-agent presentation creation system
* PowerPoint template support and slide generation
* Web search integration for content research
* Azure OpenAI integration with Semantic Kernel orchestration
