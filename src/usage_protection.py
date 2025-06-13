import os
import streamlit as st
from datetime import datetime, timedelta
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsageTracker:
    """Enhanced usage tracking to protect against excessive costs"""
    
    def __init__(self):
        self.usage_file = "usage_tracking.json"
        self.max_daily_cost = float(os.getenv("MAX_DAILY_COST", "2.0"))
        self.max_resumes_per_session = int(os.getenv("MAX_RESUMES_PER_SESSION", "20"))
        self.alert_threshold = float(os.getenv("ALERT_THRESHOLD", "1.5"))
        self.emergency_shutdown = os.getenv("EMERGENCY_SHUTDOWN", "false").lower() == "true"
        
        # Cost per resume based on AI service
        ai_service = os.getenv("AI_SERVICE", "gemini").lower()
        cost_mapping = {
            "gemini": float(os.getenv("COST_PER_RESUME_GEMINI", "0.03")),
            "openai": float(os.getenv("COST_PER_RESUME_OPENAI", "0.10")),
            "azure": float(os.getenv("COST_PER_RESUME_AZURE", "0.10")),
            "local": float(os.getenv("COST_PER_RESUME_LOCAL", "0.00"))
        }
        self.cost_per_resume = cost_mapping.get(ai_service, 0.05)
        
    def load_usage(self):
        """Load usage data with error handling"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    
                # Ensure all required fields exist
                default_data = {
                    "daily_cost": 0,
                    "last_reset": str(datetime.now().date()),
                    "session_count": 0,
                    "total_resumes_processed": 0,
                    "peak_daily_cost": 0,
                    "first_use_date": str(datetime.now().date())
                }
                
                # Merge with defaults
                for key, value in default_data.items():
                    if key not in data:
                        data[key] = value
                        
                return data
        except Exception as e:
            logger.error(f"Error loading usage data: {e}")
            
        # Return default data if file doesn't exist or error
        return {
            "daily_cost": 0,
            "last_reset": str(datetime.now().date()),
            "session_count": 0,
            "total_resumes_processed": 0,
            "peak_daily_cost": 0,
            "first_use_date": str(datetime.now().date())
        }
    
    def save_usage(self, data):
        """Save usage data with error handling"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.usage_file) if os.path.dirname(self.usage_file) else ".", exist_ok=True)
            
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            # Log usage for monitoring
            if os.getenv("ENABLE_USAGE_LOGGING", "true").lower() == "true":
                log_entry = f"{datetime.now().isoformat()} - Daily cost: ${data['daily_cost']:.2f}, Session count: {data['session_count']}"
                logger.info(log_entry)
                
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")
    
    def check_limits(self, num_resumes=1):
        """Enhanced limit checking with detailed feedback"""
        
        # Check emergency shutdown
        if self.emergency_shutdown:
            return False, "🚨 System temporarily disabled for maintenance"
            
        usage = self.load_usage()
        today = str(datetime.now().date())
        
        # Reset daily counter if new day
        if usage.get("last_reset") != today:
            usage["daily_cost"] = 0
            usage["last_reset"] = today
            usage["session_count"] = 0
            self.save_usage(usage)
        
        estimated_cost = num_resumes * self.cost_per_resume
        
        # Check daily cost limit
        if usage["daily_cost"] + estimated_cost > self.max_daily_cost:
            remaining = self.max_daily_cost - usage["daily_cost"]
            max_resumes = int(remaining / self.cost_per_resume)
            return False, f"💰 Daily cost limit (${self.max_daily_cost}) would be exceeded. You can process up to {max_resumes} more resume(s) today."
        
        # Check session limits
        if usage["session_count"] + num_resumes > self.max_resumes_per_session:
            remaining = self.max_resumes_per_session - usage["session_count"]
            return False, f"📊 Session limit ({self.max_resumes_per_session} resumes) would be exceeded. You can process {remaining} more resume(s) in this session."
        
        # Check if approaching limits (warning)
        if usage["daily_cost"] + estimated_cost > self.alert_threshold:
            warning_msg = f"⚠️ Approaching daily limit: ${usage['daily_cost'] + estimated_cost:.2f} of ${self.max_daily_cost}"
            st.warning(warning_msg)
        
        return True, f"✅ Within limits - Estimated cost: ${estimated_cost:.2f}"
    
    def record_usage(self, num_resumes=1, actual_cost=None):
        """Record API usage with enhanced tracking"""
        usage = self.load_usage()
        
        # Use actual cost if provided, otherwise estimate
        cost = actual_cost if actual_cost is not None else (num_resumes * self.cost_per_resume)
        
        usage["daily_cost"] += cost
        usage["session_count"] += num_resumes
        usage["total_resumes_processed"] += num_resumes
        
        # Track peak usage
        if usage["daily_cost"] > usage.get("peak_daily_cost", 0):
            usage["peak_daily_cost"] = usage["daily_cost"]
        
        self.save_usage(usage)
        
        # Send alert if threshold reached
        if (usage["daily_cost"] >= self.alert_threshold and 
            os.getenv("ENABLE_COST_ALERTS", "true").lower() == "true"):
            self.send_cost_alert(usage)
        
        return usage
    
    def send_cost_alert(self, usage):
        """Send cost alert (placeholder for email/webhook)"""
        alert_msg = f"🚨 Cost Alert: Daily usage ${usage['daily_cost']:.2f} exceeded threshold ${self.alert_threshold}"
        logger.warning(alert_msg)
        
        # In production, you could send email or webhook here
        # self.send_email_alert(alert_msg)
        # self.send_webhook_alert(alert_msg)
        
    def get_usage_analytics(self):
        """Get detailed usage analytics"""
        usage = self.load_usage()
        
        analytics = {
            "today": {
                "cost": usage["daily_cost"],
                "resumes": usage["session_count"],
                "remaining_budget": self.max_daily_cost - usage["daily_cost"]
            },
            "totals": {
                "resumes_processed": usage.get("total_resumes_processed", 0),
                "peak_daily_cost": usage.get("peak_daily_cost", 0),
                "days_active": self.get_days_since_first_use(usage.get("first_use_date"))
            },
            "limits": {
                "daily_cost_limit": self.max_daily_cost,
                "session_limit": self.max_resumes_per_session,
                "cost_per_resume": self.cost_per_resume
            }
        }
        
        return analytics
    
    def get_days_since_first_use(self, first_use_date):
        """Calculate days since first use"""
        try:
            if first_use_date:
                first_date = datetime.strptime(first_use_date, "%Y-%m-%d").date()
                return (datetime.now().date() - first_date).days + 1
        except:
            pass
        return 1

def add_usage_monitoring():
    """Add enhanced usage monitoring to your app"""
    tracker = UsageTracker()
    
    # Check for emergency shutdown first
    if tracker.emergency_shutdown:
        st.error("🚨 System temporarily disabled for maintenance")
        st.info(os.getenv("MAINTENANCE_MESSAGE", "Please try again later."))
        return False
    
    # Get number of resumes to process
    num_resumes = len(st.session_state.get('resumes', []))
    
    if num_resumes == 0:
        return True  # No cost if no resumes
    
    # Check limits before processing
    can_proceed, message = tracker.check_limits(num_resumes)
    
    if not can_proceed:
        st.error(f"🚫 {message}")
        
        # Show helpful information
        analytics = tracker.get_usage_analytics()
        remaining_budget = analytics["today"]["remaining_budget"]
        
        with st.expander("💡 Cost Management Options", expanded=True):
            st.markdown(f"""
            **Current Status:**
            - Daily budget used: ${analytics['today']['cost']:.2f} of ${analytics['limits']['daily_cost_limit']}
            - Remaining budget: ${remaining_budget:.2f}
            - Resumes processed today: {analytics['today']['resumes']}
            
            **Options:**
            1. **Wait until tomorrow** - Limits reset at midnight
            2. **Process fewer resumes** - Upload smaller batches
            3. **Use your own API key** - Configure in settings for unlimited use
            """)
            
            if remaining_budget > 0:
                max_resumes = int(remaining_budget / analytics['limits']['cost_per_resume'])
                st.success(f"✅ You can still process up to {max_resumes} more resume(s) today!")
        
        return False
    
    # Show cost preview
    estimated_cost = num_resumes * tracker.cost_per_resume
    st.info(f"💰 Estimated cost for {num_resumes} resume(s): ${estimated_cost:.2f}")
    
    return True

def show_usage_stats():
    """Display enhanced current usage stats"""
    tracker = UsageTracker()
    analytics = tracker.get_usage_analytics()
    
    # Current day stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Daily Cost", 
            f"${analytics['today']['cost']:.2f}", 
            f"of ${analytics['limits']['daily_cost_limit']}"
        )
    
    with col2:
        st.metric(
            "Today's Resumes", 
            analytics['today']['resumes'],
            f"of {analytics['limits']['session_limit']} max"
        )
    
    with col3:
        remaining = analytics['today']['remaining_budget']
        st.metric(
            "Budget Remaining", 
            f"${remaining:.2f}",
            delta=f"${remaining - analytics['limits']['daily_cost_limit']:.2f}" if remaining < analytics['limits']['daily_cost_limit'] else None
        )
    
    with col4:
        efficiency = analytics['totals']['resumes_processed'] / max(analytics['totals']['days_active'], 1)
        st.metric(
            "Avg Resumes/Day", 
            f"{efficiency:.1f}",
            f"over {analytics['totals']['days_active']} days"
        )
    
    # Progress bar for daily budget
    progress = min(analytics['today']['cost'] / analytics['limits']['daily_cost_limit'], 1.0)
    st.progress(progress)
    
    if progress > 0.8:
        st.warning("⚠️ Approaching daily budget limit")
    elif progress > 0.5:
        st.info("📊 Moderate usage today")
    else:
        st.success("✅ Well within budget")
    
    # Total statistics
    st.markdown("### 📈 Usage Statistics")
    st.markdown(f"""
    **All-Time Statistics:**
    - Total resumes processed: {analytics['totals']['resumes_processed']:,}
    - Peak daily cost: ${analytics['totals']['peak_daily_cost']:.2f}
    - Days active: {analytics['totals']['days_active']}
    - Current AI service: {os.getenv('AI_SERVICE', 'gemini').upper()}
    - Cost per resume: ${analytics['limits']['cost_per_resume']:.3f}
    
    **Budget Settings:**
    - Daily limit: ${analytics['limits']['daily_cost_limit']}
    - Session limit: {analytics['limits']['session_limit']} resumes
    - Auto-reset: Daily at midnight
    """)

def get_cost_estimate(num_resumes):
    """Get cost estimate for processing resumes"""
    tracker = UsageTracker()
    return num_resumes * tracker.cost_per_resume

def reset_daily_usage():
    """Manual reset of daily usage (admin function)"""
    tracker = UsageTracker()
    usage = tracker.load_usage()
    usage["daily_cost"] = 0
    usage["session_count"] = 0
    usage["last_reset"] = str(datetime.now().date())
    tracker.save_usage(usage)
    return True
