# 🚀 Deployment Guide

This guide covers multiple deployment options for the AI Resume Screening System, from simple cloud deployments to enterprise-grade solutions.

## 📋 Quick Deployment Options

### 🌟 **Option 1: Streamlit Community Cloud (Recommended - Free)**

**Perfect for**: Demos, portfolios, small teams  
**Cost**: Free  
**Setup Time**: 5 minutes

#### Steps:

1. **Push to GitHub**:

   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**:

   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add environment variables in the **Secrets** section:
     ```toml
     AI_SERVICE = "gemini"
     GEMINI_API_KEY = "your-actual-api-key-here"
     ```

3. **Go Live**: Your app will be available at `https://your-app-name.streamlit.app`

---

### 🐳 **Option 2: Docker Deployment (Any Cloud)**

**Perfect for**: Production environments, custom domains  
**Cost**: Variable based on hosting provider  
**Setup Time**: 15 minutes

#### Steps:

1. **Build the Docker image**:

   ```bash
   docker build -t ai-resume-screening .
   ```

2. **Test locally**:

   ```bash
   docker run -p 8501:8501 --env-file .env ai-resume-screening
   ```

3. **Deploy to cloud** (choose one):
   - **Google Cloud Run**: `gcloud run deploy`
   - **AWS ECS**: Use AWS console or CLI
   - **Azure Container Instances**: `az container create`
   - **DigitalOcean App Platform**: Connect GitHub repo

---

### ⚡ **Option 3: Railway (Easiest Cloud Deploy)**

**Perfect for**: Quick production deployments  
**Cost**: $5+/month (free tier available)  
**Setup Time**: 3 minutes

#### Steps:

1. **Connect to Railway**:

   - Visit [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway auto-detects Python/Streamlit

2. **Set Environment Variables**:

   ```bash
   AI_SERVICE=gemini
   GEMINI_API_KEY=your-actual-key
   PORT=8501
   ```

3. **Deploy**: Automatic deployment on every push

---

### 🎨 **Option 4: Render (Great for Demos)**

**Perfect for**: Portfolio projects, client demos  
**Cost**: Free tier available  
**Setup Time**: 5 minutes

#### Steps:

1. **Create new Web Service** on [render.com](https://render.com)
2. **Connect GitHub repository**
3. **Configuration**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. **Add Environment Variables** in Render dashboard

---

## 🔧 Environment Configuration

### Required Environment Variables

For **any deployment**, you need to set these environment variables:

```bash
# Choose your AI service
AI_SERVICE=gemini  # or "azure" or "openai"

# For Gemini (Recommended - Most Cost Effective)
GEMINI_API_KEY=your-actual-api-key-here

# For Azure OpenAI
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-key

# For OpenAI Direct
OPENAI_API_KEY=your-openai-key
```

### 🌟 **Recommended: Google Gemini Setup**

1. **Get Free API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **No Credit Card Required**: Generous free tier
3. **Best Performance/Cost**: Optimized for production use

---

## 🚀 Production Deployment Checklist

### Before Going Live:

- [ ] **Test locally**: `streamlit run app.py`
- [ ] **Verify AI service**: `python test_ai_config.py`
- [ ] **Check environment variables**: All API keys set correctly
- [ ] **Test file uploads**: Ensure resume processing works
- [ ] **Security review**: No API keys in code/logs
- [ ] **Performance test**: Try with multiple resumes

### Security Best Practices:

- [ ] **Never commit `.env` files** with real API keys
- [ ] **Use environment variables** in production
- [ ] **Enable HTTPS** for production deployments
- [ ] **Set upload limits** to prevent abuse
- [ ] **Monitor API usage** to avoid unexpected costs

---

## 🔍 Monitoring & Maintenance

### Health Checks:

Most platforms support health checks. Use this endpoint:

```
GET /_stcore/health
```

### Logging:

Monitor these logs for issues:

- Application startup
- AI API calls
- File processing errors
- User interactions

### Cost Monitoring:

**Gemini**: Check usage at [Google AI Studio](https://aistudio.google.com)  
**Azure OpenAI**: Monitor in Azure Portal  
**OpenAI**: Check usage at [OpenAI Platform](https://platform.openai.com/usage)

---

## 🎯 Recommended Deployment Strategy

### For Different Use Cases:

1. **Personal Portfolio/Demo**:

   - Use **Streamlit Community Cloud** (free)
   - Gemini API for cost-effectiveness

2. **Small Team/Startup**:

   - Use **Railway** or **Render** ($5-20/month)
   - Gemini API with usage monitoring

3. **Enterprise**:

   - Use **Docker** on your cloud platform
   - Azure OpenAI for compliance
   - Custom domain and SSL

4. **Development/Testing**:
   - Use **Docker Compose** locally
   - Switch between AI services easily

---

## ⚠️ Troubleshooting Common Issues

### "Missing credentials" error:

- Check environment variables are set correctly
- Verify API key format (no extra spaces)

### "Port already in use":

- Change port: `streamlit run app.py --server.port 8502`

### "File upload fails":

- Check upload size limits in deployment platform
- Verify file processing permissions

### "AI API calls fail":

- Verify API key is active and has quota
- Check internet connectivity from deployment platform

---

## 🎉 Success Metrics

After deployment, your app should:

- ✅ Load within 10 seconds
- ✅ Process resumes without errors
- ✅ Display AI-generated screening results
- ✅ Handle multiple concurrent users
- ✅ Stay within AI API cost limits

---

## 📞 Need Help?

- **Documentation**: Check README.md for detailed setup
- **Testing**: Run `python test_comprehensive.py`
- **AI Issues**: Verify with `python test_ai_config.py`

Your AI Resume Screening System is ready for the world! 🌍
