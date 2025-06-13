# 💰 API Cost Analysis for AI Resume Screening System

## Current Cost Estimates (as of June 2025)

### Google Gemini (Recommended)

- **Cost per resume**: ~$0.01-0.05
- **100 resumes**: ~$1-5
- **1000 resumes**: ~$10-50
- **Free tier**: 15 requests/minute, generous daily limits

### OpenAI GPT-4o-mini

- **Cost per resume**: ~$0.05-0.15
- **100 resumes**: ~$5-15
- **1000 resumes**: ~$50-150

### Azure OpenAI

- **Cost per resume**: ~$0.05-0.15
- **100 resumes**: ~$5-15
- **1000 resumes**: ~$50-150

## Usage Scenarios

### Demo/Portfolio Use

- **10 resumes/day**: $0.10-0.50/day with Gemini
- **Monthly cost**: ~$3-15
- **Perfect for**: Showcasing to potential employers/clients

### Small Business Use

- **50 resumes/day**: $0.50-2.50/day with Gemini
- **Monthly cost**: ~$15-75
- **Revenue potential**: $5-10 per screening = $250-500/day

### Enterprise Use

- **500 resumes/day**: $5-25/day with Gemini
- **Monthly cost**: ~$150-750
- **Revenue potential**: $2-5 per screening = $1000-2500/day

## Cost Control Strategies

### 1. Free Tier Strategy

```python
# Offer limited free screenings per user
FREE_SCREENINGS_PER_USER = 3
PREMIUM_PRICE_PER_SCREENING = 2.00
```

### 2. Subscription Model

```python
# Monthly subscription with included screenings
BASIC_PLAN = {"price": 29, "screenings": 100}
PRO_PLAN = {"price": 99, "screenings": 500}
ENTERPRISE_PLAN = {"price": 299, "screenings": 2000}
```

### 3. Usage Monitoring

```python
# Track and limit usage
def track_usage(user_id, cost):
    if daily_cost > BUDGET_LIMIT:
        send_alert()
        disable_service_temporarily()
```

## Revenue Potential

### Market Rates

- **Manual screening**: $10-50 per resume (HR consultant)
- **Your AI service**: $2-10 per resume (80% cost savings)
- **Value proposition**: Faster, consistent, unbiased analysis

### Break-even Analysis

- **Gemini cost**: $0.03 per resume
- **Your price**: $3 per resume
- **Profit margin**: 99%
- **Break-even**: ~10 resumes to cover monthly hosting

## Recommendation for Publishing

### For Portfolio/Demo

✅ **Use your API key** with Gemini

- Low cost ($10-30/month max)
- Full control
- Professional demonstration

### For Business

🚀 **Hybrid approach**:

1. **Free tier**: 3 resumes per user (your API key)
2. **Paid tier**: Users provide API key OR pay per screening
3. **Enterprise**: Custom pricing with your infrastructure

### Implementation

```python
# In your app
if user.plan == "free" and user.usage >= 3:
    show_upgrade_options()
elif user.plan == "premium":
    use_user_api_key()
else:
    use_your_api_key()
```

## Bottom Line

- **Demo use**: ~$10-30/month (very manageable)
- **Business potential**: High profit margins
- **Risk**: Low (can disable anytime)
- **Control**: Full monitoring and limits available
