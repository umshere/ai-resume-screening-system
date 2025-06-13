# AI Multi-Agent Resume Screening & Matching System

Create comprehensive resume screening and matching reports effortlessly with the power of AI. This project leverages multiple AI agents to collaboratively analyze job profiles and resumes, providing detailed matching scores and explanations.

In this repository, we demonstrate how to use **Semantic Kernel** to orchestrate Multi-Agent systems using **Azure OpenAI** models. We use a swarm agent architecture with **o1-mini** as the orchestrator and **gpt-4o-mini** model as the LLM for the task-oriented agents.

**Semantic Kernel** is utilized for agent orchestration, enabling seamless coordination and communication between different AI agents. By leveraging Semantic Kernel, the system efficiently manages task delegation, context sharing, and workflow automation, ensuring that each agent contributes effectively to the resume screening and matching process.

This repository is designed for **learning purposes**, offering insights into the development and integration of multi-agent systems for automated resume screening and candidate matching.

The diagram below shows how the orchestrator creates the agents and the expert agents collaborate with each other to accomplish the goal:

![MAS](images/mas-orchestrator-deck-builder.png)

The **Expert agents** are dynamically created and have a level of autonomy to accomplish their tasks. Each one will be responsible for a specific aspect of resume screening (skills analysis, experience evaluation, cultural fit assessment, etc.).

## Features

This project framework provides the following features:

* **Dynamic Agent Creation**: Automatically generates AI agents tailored to specific resume screening tasks.
* **Collaborative AI**: Multiple AI agents work together to create comprehensive matching reports.
* **Streamlit Integration**: User-friendly web interface for seamless interaction with drag-and-drop functionality.
* **Job Profile Processing**: Accept job descriptions via URL or direct text input.
* **Resume Processing**: Upload multiple resumes via drag-and-drop or file upload.
* **Intelligent Matching**: AI-powered matching algorithms that analyze skills, experience, and cultural fit.
* **Detailed Reports**: Generate comprehensive matching reports with scores and explanations.
* **Interactive UI**: Real-time progress tracking showing which agents are working and current status.
* **Export Functionality**: Generate and download matching reports in various formats.

## Demo
The system provides an interactive web interface where users can:
1. Input job profiles via text or URL
2. Upload multiple resumes (PDF, DOCX, TXT)
3. Configure expert agents for analysis
4. Monitor real-time screening progress
5. View detailed matching reports with scores and explanations
6. Download comprehensive screening reports

## How It Works

### Multi-Agent Architecture
1. **Orchestrator Agent**: Creates specialized expert agents based on job requirements
2. **Skills Analysis Agent**: Evaluates technical and soft skills alignment
3. **Experience Evaluation Agent**: Assesses work experience relevance and depth
4. **Education Assessment Agent**: Reviews educational background and certifications
5. **Cultural Fit Agent**: Analyzes personality traits and team compatibility
6. **Report Compilation Agent**: Synthesizes all evaluations into final scores

### Screening Process
1. Job profile is analyzed to identify key requirements
2. Resumes are processed and text is extracted
3. Expert agents collaborate to evaluate each candidate
4. Matching scores are calculated with detailed explanations
5. Candidates are ranked and comprehensive reports are generated

## Getting Started

### Prerequisites

- Python 3.10+
- Azure OpenAI API Key
- Bing API Key (optional, for web search capabilities)

### Installation

1. Clone the repository:
    ```sh
    git clone [repository clone url]
    cd TFaimultiagentprsntnbuildr
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
    
    Or using Poetry:
    ```sh
    poetry install
    ```

4. Set up environment variables:
    ```sh
    cp .env.example .env
    # Edit .env file with your API keys and configuration
    ```

### Configuration

Edit the `.env` file with your configuration:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_MODEL=gpt-4o-mini
AZURE_OPENAI_MODEL_ORCHESTRATOR=o1-mini

# Bing Search Configuration (optional)
BING_API_KEY=your_bing_api_key

# Template Configuration
TEMPLATE_DIR_PROMPTS=src/prompts
TEMPLATE_SYSTEM_ORCHESTRATOR=orchestrator.jinja
TEMPLATE_SELECTION=selection.jinja
TEMPLATE_TERMINATION=termination.jinja
```

### Usage

1. **Run the application**:
    ```sh
    streamlit run app.py
    ```
    
    Or using the main entry point:
    ```sh
    python main.py
    ```

2. **Access the web interface**:
    Open your browser and go to `http://localhost:8501`

3. **Use the system**:
    - Enter or paste a job description
    - Upload resume files (PDF, DOCX, or TXT)
    - Configure the number of expert agents
    - Click "Start Resume Screening"
    - Monitor the progress and view results

### Testing

Run the test script to verify the system:
```sh
python test_system.py
```

3. Set up your environment variables:
    - Copy  to  and fill in your API keys and other configurations.
    - You can use the [.env.sample](.env.sample) file to adjust your own environment variables. Rename the file to `.env` and change each one with your own data.

### Quickstart

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your browser and navigate to `http://localhost:8501`.

3. Enter a theme for your presentation and let the AI agents do the rest!

## Demo

A demo app is included to show how to use the project.

To run the demo, follow these steps:

1. Ensure all prerequisites are met.
2. Follow the Quickstart guide to run the Streamlit app.
3. Interact with the AI agents and generate a presentation.

## Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Jinja Documentation](https://jinja.palletsprojects.com/)

## Contributing

This project welcomes contributions and suggestions. Please open a PR and it will be analyzed as soon as possible.

## License

This project is licensed under the MIT License. See the  file for details.
