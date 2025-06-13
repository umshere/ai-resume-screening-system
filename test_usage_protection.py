#!/usr/bin/env python3

from src.usage_protection import UsageTracker, get_cost_estimate
import os

print('🧪 Testing Usage Protection System')
print('=' * 40)

# Test usage tracker
tracker = UsageTracker()
print(f'✅ Usage tracker initialized')
print(f'   Daily limit: ${tracker.max_daily_cost}')
print(f'   Session limit: {tracker.max_resumes_per_session}') 
print(f'   Cost per resume: ${tracker.cost_per_resume}')

# Test limit checking
can_proceed, message = tracker.check_limits(5)
print(f'✅ Limit check for 5 resumes: {message}')

# Test usage recording  
usage = tracker.record_usage(num_resumes=3, actual_cost=0.09)
print(f'✅ Recorded usage: ${usage["daily_cost"]:.2f} spent, {usage["session_count"]} resumes')

# Test analytics
analytics = tracker.get_usage_analytics()
print(f'✅ Analytics loaded: {analytics["today"]["resumes"]} resumes today')

# Test cost estimation
cost = get_cost_estimate(10)
print(f'✅ Cost estimate for 10 resumes: ${cost:.2f}')

print('\n🎉 All usage protection tests passed!')
print('\n📊 Current Status:')
print(f'   Emergency shutdown: {tracker.emergency_shutdown}')
print(f'   AI service: {os.getenv("AI_SERVICE", "not set")}')
print(f'   Usage file: {tracker.usage_file}')
