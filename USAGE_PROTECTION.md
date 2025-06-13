# 🛡️ Usage Protection Guide

## Overview

Your AI Resume Screening System now includes comprehensive **usage protection** to safeguard against unexpected API costs when published to the external world. This system automatically monitors and limits usage while providing detailed analytics.

## 🔒 Protection Features

### Cost Controls

- **Daily spending limits** - Default: $2/day
- **Session limits** - Default: 20 resumes per session
- **Real-time cost tracking** - Live monitoring of API usage
- **Automatic resets** - Daily limits reset at midnight
- **Emergency shutdown** - Quick disable capability

### Smart Monitoring

- **Usage analytics** - Detailed statistics and trends
- **Cost estimation** - Preview costs before processing
- **Progress tracking** - Visual budget consumption
- **Alert system** - Warnings when approaching limits

### Deployment Safety

- **Rate limiting** - Prevent abuse from high traffic
- **File size limits** - Control upload sizes
- **Session timeouts** - Automatic cleanup
- **Usage logging** - Track all activity

## 📊 Usage Dashboard

When you run the app, you'll see a **"Usage & Cost Monitoring"** section that displays:

```
Daily Cost    Today's Resumes    Budget Remaining    Avg Resumes/Day
$2.45         8 of 20 max        $7.55              12.3 over 5 days
of $2.00

Progress: ████████░░ 24% of daily budget used
```

## 💰 Cost Estimates

### Per Resume Costs:

- **Gemini (Recommended)**: ~$0.03 per resume
- **OpenAI**: ~$0.10 per resume
- **Azure OpenAI**: ~$0.10 per resume

### Example Scenarios:

- **Demo/Portfolio**: 10 resumes/day = $0.30/day = ~$9/month
- **Small Business**: 50 resumes/day = $1.50/day = ~$45/month
- **High Volume**: 200 resumes/day = $6/day = ~$180/month

## 🚀 Configuration

### Environment Variables

Create or update your `.env` file with protection settings:

```env
# Usage Protection Settings
MAX_DAILY_COST=10.0
MAX_RESUMES_PER_SESSION=20
COST_PER_RESUME_GEMINI=0.03
COST_PER_RESUME_OPENAI=0.10
COST_PER_RESUME_AZURE=0.10

# Alert Settings
ENABLE_COST_ALERTS=true
ALERT_THRESHOLD=8.0

# Emergency Controls
EMERGENCY_SHUTDOWN=false
MAINTENANCE_MESSAGE="System temporarily unavailable"

# Your AI Service
AI_SERVICE=gemini
GEMINI_API_KEY=your-actual-api-key
```

### Quick Setup

Run the protection setup script:

```bash
chmod +x setup_protection.sh
./setup_protection.sh
```

This automatically:

- ✅ Creates protected `.env` configuration
- ✅ Sets up usage tracking
- ✅ Creates log directories
- ✅ Tests the configuration

## 🎯 Deployment Modes

### 1. Demo Mode (Recommended)

**Perfect for portfolios and demonstrations**

```env
MAX_DAILY_COST=10.0
MAX_RESUMES_PER_SESSION=10
ENABLE_COST_ALERTS=true
```

- Low cost ($2/day max)
- Professional presentation
- Full protection

### 2. Business Mode

**For production use with customers**

```env
MAX_DAILY_COST=50.0
MAX_RESUMES_PER_SESSION=100
ENABLE_RATE_LIMITING=true
```

- Higher limits for business use
- Rate limiting for security
- Usage analytics for billing

### 3. Free Tier Mode

**Offer limited free usage**

```env
MAX_DAILY_COST=5.0
MAX_RESUMES_PER_SESSION=5
FREE_TIER_LIMIT=3
```

- Very low cost
- Limited free usage per user
- Upgrade prompts

## 🚨 Safety Features

### Automatic Protections

1. **Cost Monitoring**: Real-time tracking prevents overspending
2. **Usage Limits**: Session and daily limits prevent abuse
3. **Alert System**: Warnings before reaching limits
4. **Emergency Stop**: Quick shutdown capability
5. **Daily Reset**: Fresh limits every day

### Manual Controls

```python
# Emergency shutdown
EMERGENCY_SHUTDOWN=true

# Maintenance mode
MAINTENANCE_MESSAGE="Upgrading system - back soon!"

# Reset usage (if needed)
python3 -c "from src.usage_protection import reset_daily_usage; reset_daily_usage()"
```

## 📈 Monitoring & Analytics

### Usage Tracking

- Daily cost consumption
- Resumes processed
- Peak usage periods
- Cost efficiency trends

### Log Files

- Usage events logged to `logs/usage.log`
- Cost tracking and alerts
- Performance metrics
- Error monitoring

### Analytics Dashboard

```python
from src.usage_protection import UsageTracker
tracker = UsageTracker()
analytics = tracker.get_usage_analytics()
print(f"Total resumes processed: {analytics['totals']['resumes_processed']}")
```

## 🔧 Customization

### Adjust Costs for Your AI Service

```env
# Gemini (most cost-effective)
AI_SERVICE=gemini
COST_PER_RESUME_GEMINI=0.03

# OpenAI (higher cost, latest models)
AI_SERVICE=openai
COST_PER_RESUME_OPENAI=0.10

# Azure OpenAI (enterprise)
AI_SERVICE=azure
COST_PER_RESUME_AZURE=0.10
```

### Custom Budget Limits

```env
# Conservative (demo/portfolio)
MAX_DAILY_COST=5.0

# Standard (small business)
MAX_DAILY_COST=25.0

# High volume (enterprise)
MAX_DAILY_COST=100.0
```

### Rate Limiting (for public deployments)

```env
ENABLE_RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=10
MAX_FILE_SIZE_MB=10
SESSION_TIMEOUT_MINUTES=30
```

## 🎉 Benefits

### For Portfolio/Demo Use:

- ✅ **Controlled costs** - Never exceed your budget
- ✅ **Professional presentation** - Show real, working AI
- ✅ **User-friendly** - Clear usage information
- ✅ **Scalable** - Easy to increase limits later

### For Business Use:

- ✅ **Cost management** - Predictable expenses
- ✅ **Usage analytics** - Understand customer patterns
- ✅ **Revenue optimization** - Track costs vs. pricing
- ✅ **Abuse prevention** - Rate limiting and controls

## 🚀 Getting Started

### 1. Setup Protection

```bash
./setup_protection.sh
```

### 2. Configure Your Budget

Edit `.env` file with your preferred limits

### 3. Test Locally

```bash
streamlit run app.py
```

### 4. Deploy with Confidence

```bash
./deploy.sh
```

### 5. Monitor Usage

Check the usage dashboard and logs regularly

## 💡 Pro Tips

### Cost Optimization:

- Use **Gemini** for best cost/performance ratio
- Start with **conservative limits** and increase as needed
- Monitor **peak usage** times for planning
- Consider **free tier** options for user acquisition

### Safety Best Practices:

- Set **alert thresholds** below your daily limit
- Enable **email notifications** for high usage
- Regular **usage reviews** and limit adjustments
- Keep **emergency shutdown** option ready

### Revenue Strategies:

- **Freemium model**: 3 free resumes, then paid
- **Subscription tiers**: Different limits for different plans
- **Pay-per-use**: Charge $2-5 per resume (99% profit margin!)
- **Enterprise**: Custom pricing for high-volume users

## 🔍 Troubleshooting

### Common Issues:

**"Daily limit reached"**

- Wait until midnight for automatic reset
- Increase `MAX_DAILY_COST` in `.env`
- Use manual reset: `reset_daily_usage()`

**"Session limit exceeded"**

- Process smaller batches of resumes
- Increase `MAX_RESUMES_PER_SESSION`
- Clear browser session and try again

**"Usage tracking error"**

- Check file permissions on `usage_tracking.json`
- Ensure `logs/` directory exists
- Verify Python write permissions

## 📞 Support

For usage protection questions:

1. Check the usage dashboard for current status
2. Review `logs/usage.log` for detailed activity
3. Test configuration with `./setup_protection.sh`
4. Adjust limits in `.env` file as needed

---

**🛡️ With usage protection enabled, you can confidently publish your AI Resume Screening System knowing your costs are controlled and monitored!**
