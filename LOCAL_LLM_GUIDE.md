# 🏠 Local LLM Integration Guide

## Overview

Your AI Resume Screening System now supports local LLM integration! This means you can run the entire system using your own AI models running locally, with **zero API costs** and **complete privacy**.

## ✅ What's Already Working

✅ **Local LLM Server Detected**: Your server at `http://localhost:1234` is running  
✅ **Available Models**: 
- `gemma-3-4b-it-qat` (recommended for resume screening)
- `dia-1.6b` (lightweight option)
- `text-embedding-nomic-embed-text-v1.5` (for embeddings)

## 🚀 Quick Start

### 1. Configure Your Environment

Copy the example configuration and customize:
```bash
cp .env.example .env
# Edit .env file with local LLM settings
```

Or manually add to your `.env` file:
```env
AI_SERVICE=local
LOCAL_LLM_BASE_URL=http://localhost:1234/v1
LOCAL_LLM_MODEL=gemma-3-4b-it-qat
LOCAL_LLM_MODEL_ORCHESTRATOR=gemma-3-4b-it-qat
```

### 2. Start the Resume Screening System

```bash
streamlit run app.py
```

The system will automatically:
- ✅ Detect your local LLM server
- ✅ Use the `gemma-3-4b-it-qat` model for analysis
- ✅ Create specialized AI agents for resume screening
- ✅ Process resumes completely offline

## 🎯 Benefits of Local LLM

### 💰 **Zero Cost**
- No API fees
- No usage limits
- No monthly subscriptions

### 🔒 **Complete Privacy**
- Resume data never leaves your machine
- No data sent to external services
- Full GDPR/compliance friendly

### ⚡ **Performance**
- No network latency
- Consistent response times
- Works offline

### 🎛️ **Full Control**
- Choose your preferred models
- Adjust parameters freely
- No rate limits

## 🔧 Advanced Configuration

### Custom Models
To use a different model, update your `.env`:
```env
LOCAL_LLM_MODEL=your-preferred-model-name
```

### Custom Server URL
If your LLM server runs on a different port:
```env
LOCAL_LLM_BASE_URL=http://localhost:8080/v1
```

### Performance Tuning
The system automatically optimizes for:
- **Multi-agent processing**: Each resume screening agent runs independently
- **Efficient prompting**: Optimized prompts for local models
- **Error handling**: Graceful fallbacks for network issues

## 🧪 Testing Your Setup

Test the integration:
```bash
python test_local_llm_simple.py
```

Or test the full system:
```bash
python test_ai_config.py
```

## 🎯 Recommended Models for Resume Screening

### **Gemma 3 4B** (Currently Active)
- **Best for**: Balanced performance and speed
- **Memory**: ~3GB RAM
- **Speed**: Fast response times

### **Llama 3.1 8B** (Alternative)
- **Best for**: Higher quality analysis
- **Memory**: ~6GB RAM
- **Speed**: Slower but more detailed

### **Mistral 7B** (Alternative)
- **Best for**: Technical resume analysis
- **Memory**: ~5GB RAM
- **Speed**: Good balance

## 🚀 Next Steps

1. **Start using the system** with your current local setup
2. **Try processing some test resumes** to see the AI agents in action
3. **Experiment with different models** if needed
4. **Scale up** by adding more powerful models for better analysis

## 💡 Tips for Best Results

- **Use specific job descriptions**: The more detailed, the better the matching
- **Process resumes in batches**: 5-10 at a time for optimal performance
- **Monitor your system resources**: Ensure adequate RAM for your chosen model
- **Keep your models updated**: Newer versions often provide better results

## 🔄 Switching Back to Cloud Services

You can always switch back to cloud services by changing your `.env`:
```env
AI_SERVICE=gemini  # or openai, azure
GEMINI_API_KEY=your-api-key
```

---

**🎉 Congratulations!** You now have a completely self-hosted, zero-cost AI resume screening system running on your local machine.
