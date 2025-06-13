# AI Multi-Agent Resume Screening System Changelog

<a name="0.3.1-alpha"></a>

# 0.3.1-alpha (2025-06-12)

_Smart Progress Tracking & Bug Fixes_

## 🐛 Critical Bug Fixes

### Dynamic Progress Calculation

- **Fixed hardcoded max_interactions** - Now dynamically calculated based on agent count
- **Improved progress tracking** - Shows "Round X/Y" instead of confusing "Step X/10"
- **Agent-aware progress display** - Shows current agent and total agent count in status
- **Optimized interaction cycles** - Prevents unnecessary extended processing

### Variable Scope Fixes

- **Fixed "name 'resumes' is not defined" error** in `display_screening_results` function
- **Corrected variable scope** by using `resumes_to_screen` instead of undefined `resumes`
- **Enhanced error handling** with proper variable references throughout the application

## 🔧 Technical Improvements

### Smart Agent Orchestration

- **Dynamic max_interactions calculation**: `max(num_agents * 2, 4)` ensures optimal rounds
- **Progress calculation logic**: Each agent gets at least 2 rounds, minimum 4 total
- **Better user feedback**: Clear indication of which agent is working and progress status

### Example Enhanced Progress Display

```
Main Status:
Round 2/4 | Experience_Evaluation_Agent | 2 agents total | Initial Analysis
🎯 Evaluating work experience relevance for 3 candidate(s)

Sidebar Agent Card:
👤 Skills_Analysis_Agent
🔧 Technical Skills & Expertise
🔍 Cross-referencing skill requirements with candidate experience

Previous Simple Format:
For 2 agents: "Round 1/4: Skills_Analysis_Agent is analyzing... (2 agents total)"
```

---

<a name="0.3.0-alpha"></a>

# 0.3.0-alpha (2025-06-12)

_Multi-AI Service Support & Enhanced Reliability_

## 🎉 Major Features Added

### Multi-AI Service Support

- **Added Google Gemini API support** alongside existing Azure OpenAI
- **Flexible AI service selector** in `.env` file with clear setup instructions
- **Automatic service detection and initialization** based on available credentials
- **Consistent agent interface** across all AI services

### Enhanced Configuration System

- **AI_SERVICE environment variable** to choose between `azure`, `openai`, and `gemini`
- **Robust error handling** for missing or invalid API keys
- **Optional Bing Search integration** - system works without it
- **Clear setup instructions** with copy-paste ready examples

## 🔧 Technical Improvements

### Smart Agent Orchestration

- **Dynamic round calculation** based on agent count (2× rounds per agent, minimum 4)
- **Intelligent progress tracking** with "Round X/Y" format showing actual progress
- **Agent-aware status updates** displaying current agent and total agent count
- **Optimized interaction cycles** preventing unnecessary extended processing

### Gemini Integration

- **GeminiWrapper class** providing OpenAI-compatible interface
- **GeminiAgent and GeminiChatGroup classes** for proper agent management
- **Streaming support** with `invoke_stream` method compatibility
- **Response format conversion** maintaining existing code compatibility

### Error Handling & Resilience

- **Graceful credential validation** with helpful error messages
- **Optional dependency handling** for Bing Search API
- **Safe fallback responses** for blocked or failed API calls
- **Proper environment variable loading** across all entry points

## 🐛 Critical Bug Fixes

### Authentication Issues

- **Fixed Azure OpenAI credential loading** from `.env` file
- **Added proper dotenv loading** in `app.py`, `main.py`, and `mas.py`
- **Resolved "missing credentials" errors** with specific troubleshooting guidance

### Agent Management

- **Fixed "'str' object has no attribute 'name'" error** by using proper agent objects
- **Fixed "name 'resumes' is not defined" error** by correcting variable scope in display function
- **Implemented dynamic max_interactions** based on agent count instead of hardcoded value
- **Added missing `invoke_stream` method** to GeminiChatGroup class
- **Ensured consistent agent creation** patterns across all services

### Progress Tracking Improvements

- **Enhanced progress display** with "Round X/Y" format instead of confusing "Step X/10"
- **Agent-aware status messages** showing current agent and total count
- **Dynamic interaction limits** preventing unnecessary extended processing
- **Improved user feedback** with contextual progress information

## 📝 Configuration Updates

### New Environment Variables

```bash
# AI Service Selection (choose one)
AI_SERVICE=gemini  # Options: azure, openai, gemini

# Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MODEL_ORCHESTRATOR=gemini-1.5-flash

# Optional Bing Search
BING_API_KEY=your-bing-api-key-here  # Optional feature
```

### Dependencies Added

- `google-generativeai==0.8.3` for Gemini API support
- Enhanced `python-dotenv` usage for reliable config loading

## 🧪 Testing & Validation

- **Comprehensive AI service configuration tests** added
- **Live API integration testing** for all supported services
- **Error handling verification** for various failure scenarios
- **Backward compatibility confirmation** for existing setups

## ⚠️ Migration Notes

- **Fully backward compatible** - existing Azure OpenAI setups continue working
- **No breaking changes** to existing configurations
- **Optional migration** to Gemini for cost optimization

<a name="0.2.0-alpha"></a>

# 0.2.0-alpha (2025-06-13)

_Major System Transformation_

- Converted from presentation builder to resume screening and matching system
- Complete redesign of multi-agent architecture for HR and recruitment use cases
- New interactive Streamlit UI optimized for resume screening workflows

_New Features_

- Resume processing support for PDF, DOCX, and TXT formats
- Job profile input via direct text or URL
- Multi-agent screening with specialized expertise areas
- AI-powered matching scores with detailed explanations
- Real-time progress tracking and agent status visualization
- Comprehensive candidate ranking and reporting
- Downloadable CSV reports for screening results

_Technical Changes_

- New ResumeScreeningPlugin for candidate analysis
- Updated orchestrator prompts for resume screening
- Enhanced file processing and text extraction
- Improved error handling and user feedback
- New dependencies: PyPDF2, python-docx, pandas

_Breaking Changes_

- Not backward compatible with presentation builder version
- Environment variables and configuration updated
- Agent prompts completely redesigned
- UI and workflows completely changed for HR use case

<a name="0.1.0-alpha"></a>

# 0.1.0-alpha (Previous)

_Legacy Features (Presentation Builder)_

- Multi-agent presentation creation system
- PowerPoint template support and slide generation
- Web search integration for content research
- Azure OpenAI integration with Semantic Kernel orchestration

<a name="0.4.0-alpha"></a>

# 0.4.0-alpha (2025-06-13)

_Enhanced Agent Monitoring & User Experience_

## 🎉 Major Features Added

### Enhanced Agent Activity Monitoring

- **Agent specialization display** - Each agent shows their specific expertise area
- **Detailed activity descriptions** - Real-time updates of what each agent is analyzing
- **Phase-based progress** - Shows "Initial Analysis" vs "Deep Analysis & Validation"
- **Rich agent cards** - Sidebar displays with agent roles and current activities
- **Activity rotation** - Each agent cycles through different specific tasks per round

### User Experience Improvements

- **Contextual progress updates** - Users see exactly what analysis is happening
- **Agent expertise visibility** - Clear understanding of each agent's role
- **Enhanced status messages** - More informative and engaging progress display
- **Debug information** - Added troubleshooting info for file processing issues

## 🔧 Technical Improvements

### Smart Agent Orchestration

- **Refined activity rotation logic**: Agents now rotate tasks for comprehensive analysis
- **Improved phase tracking**: Distinguishes between initial and deep analysis stages
- **Enhanced agent status updates**: More detailed and contextual information

### UI/UX Enhancements

- **Interactive agent cards**: Displays agent specialization and current tasks
- **Real-time activity feed**: Shows live updates of agent activities and analysis progress
- **Contextual tooltips and help**: In-app guidance for new users and complex features

### Performance Optimizations

- **Reduced response times**: Streamlined processing for faster analysis and feedback
- **Lower resource consumption**: Optimized code and dependencies for efficiency

## 🐛 Critical Bug Fixes

### Agent Activity Monitoring

- **Fixed agent specialization display**: Correctly shows each agent's expertise area
- **Resolved activity description issues**: Accurate real-time updates for agent activities
- **Corrected phase-based progress tracking**: Distinguishes initial analysis and deep analysis

### UI/UX Bugs

- **Fixed layout issues** in agent cards and activity feeds
- **Resolved tooltip display problems**: Contextual help now shows correctly
- **Improved error messages**: More informative and user-friendly

## 📝 Configuration Updates

### New Environment Variables

```bash
# No new environment variables in this release
```

### Dependencies Updated

- `streamlit` to latest version for improved UI components
- `google-generativeai` for enhanced Gemini API features

## 🧪 Testing & Validation

- **Thorough testing of agent activity monitoring features**
- **UI/UX testing with focus on new agent cards and activity feeds**
- **Performance benchmarking** to validate speed and resource usage improvements

## ⚠️ Migration Notes

- **No migration required** - changes are fully compatible with existing setups
- **Optional UI refresh** by clearing browser cache to load new assets
