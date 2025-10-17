"""
Billion Transformation Tracker - Example Usage
Copy this notebook and customize with YOUR metrics each week
"""

# Import the tracker functions
# (Make sure billion_tracker.py is in the same directory or install as package)
from billion_tracker import *

# ============================================================================
# WEEK 1 - BASELINE SUBMISSION (EXAMPLE)
# ============================================================================

"""
📝 Week 1 Instructions:
- Track EVERY hour you work this week
- Be honest about what's automated vs manual
- This becomes your baseline for measuring progress
- For revenue_ratio, use 1.0 (this is your 100% baseline)
"""

submit_weekly_metrics(
    week_number=1,
    
    # Time tracking (hours this week)
    total_hours_worked=55.0,  # Example: Working 55 hours/week
    automated_hours=8.0,       # Example: Only 8 hours automated
    
    # Client metrics
    active_clients=3,          # Example: Serving 3 clients
    
    # Revenue (use 1.0 for Week 1 baseline)
    revenue_ratio_to_baseline=1.0,  # Always 1.0 for Week 1
    
    # Subscription transition
    recurring_revenue_percentage=10.0,  # Example: Only 10% recurring
    
    # Qualitative
    what_i_automated_this_week="Email filtering with labels, automated meeting notes with Otter.ai",
    biggest_bottleneck_now="Manual client onboarding taking 4+ hours per client"
)

# ============================================================================
# WEEK 2 SUBMISSION (EXAMPLE)
# ============================================================================

"""
📝 Week 2 Instructions:
- Installed AIAgencyOS
- Built first N8N workflow
- For revenue_ratio: If revenue is same as Week 1, use 1.0
                     If revenue is 10% higher, use 1.1
                     If revenue is 20% lower, use 0.8
"""

submit_weekly_metrics(
    week_number=2,
    
    # Time tracking
    total_hours_worked=52.0,  # Saved 3 hours!
    automated_hours=15.0,     # Automated more tasks
    
    # Client metrics
    active_clients=3,
    
    # Revenue ratio (relative to Week 1)
    revenue_ratio_to_baseline=1.05,  # Example: 5% revenue increase
    
    # Subscription transition
    recurring_revenue_percentage=10.0,  # No change yet
    
    # Qualitative
    what_i_automated_this_week="AIAgencyOS setup complete, first N8N workflow (contact form → database → email notification)",
    biggest_bottleneck_now="Still manually cleaning client data before onboarding"
)

# ============================================================================
# WEEK 3 SUBMISSION (EXAMPLE)
# ============================================================================

submit_weekly_metrics(
    week_number=3,
    
    total_hours_worked=48.0,  # Saved 7 hours from baseline!
    automated_hours=22.0,     # Data cleaning automated
    
    active_clients=4,         # Took on new client!
    
    revenue_ratio_to_baseline=1.15,  # 15% revenue increase
    
    recurring_revenue_percentage=15.0,  # Started talking subscriptions
    
    what_i_automated_this_week="Data cleaning pipeline with Polars, automated ETL to Supabase, client onboarding form",
    biggest_bottleneck_now="Creating personalized outreach emails manually"
)

# ============================================================================
# VIEW YOUR PROGRESS
# ============================================================================

# Print progress table
print_progress_table()

# Generate visualizations
create_visualizations()

# Get full transformation report
generate_transformation_report()

# ============================================================================
# WEEKLY WORKFLOW (COPY THIS FOR EACH WEEK)
# ============================================================================

"""
🔄 YOUR WEEKLY ROUTINE:

1. At start of week: Review last week's bottleneck
2. Throughout week: Track your hours (use provided spreadsheet)
3. End of week: Submit metrics using submit_weekly_metrics()
4. Review your dashboard: print_progress_table() and create_visualizations()
5. Share in community: Post your "automated this week" win!

💡 TIPS:

- Be honest with yourself about automated vs manual hours
- For "automated_hours": Only count tasks that run WITHOUT you
- For "revenue_ratio": 
  * Week 1 revenue = $10K → use 1.0
  * Week 5 revenue = $12K → use 1.2
  * Week 8 revenue = $15K → use 1.5
  * Week 10 revenue = $9K → use 0.9
  
- For "recurring_revenue_percentage":
  * Calculate: (Monthly Recurring Revenue / Total Monthly Revenue) × 100
  
- For "what_i_automated_this_week":
  * Be specific! "Automated lead enrichment" not just "made workflow"
  
- For "biggest_bottleneck_now":
  * Be honest! This helps you focus next week
  * This is what the community can help you solve

🎯 TARGETS BY WEEK 12:

✅ Automation Index: 80%+
✅ Time Saved: 50%+ reduction
✅ Revenue Efficiency: 1.5x+ baseline
✅ Client Capacity: 1.5x+ baseline  
✅ Recurring Revenue: 50%+

📊 SHARE YOUR PROGRESS:

Export your charts and share in community:
- create_visualizations() → Screenshot → Post to WhatsApp
- Weekly check-in: "This week I automated: [X], Time saved: [Y]"
- Celebrate wins with the cohort! 🎉
"""

# ============================================================================
# TEMPLATE FOR YOUR WEEKLY SUBMISSION
# ============================================================================

"""
# 📋 WEEK X SUBMISSION TEMPLATE
# Copy this template and fill in YOUR numbers each week

submit_weekly_metrics(
    week_number=X,  # Change this each week (4, 5, 6, ...)
    
    # ⏰ TIME TRACKING
    # How many hours did you work this week?
    total_hours_worked=__,  # Your total hours
    
    # Of those hours, how many were fully automated (running without you)?
    automated_hours=__,  # Hours of automated work
    
    # 👥 CLIENT METRICS
    # How many active clients are you serving?
    active_clients=__,  # Number of clients
    
    # 💰 REVENUE (PRIVACY-PRESERVING)
    # What's your revenue this week compared to Week 1?
    # Week 1 = 1.0, if revenue doubled = 2.0, if down 20% = 0.8
    revenue_ratio_to_baseline=__,  # Ratio (e.g., 1.2)
    
    # 📈 SUBSCRIPTION TRANSITION
    # What % of your revenue is recurring/subscription-based?
    recurring_revenue_percentage=__,  # 0-100
    
    # 📝 QUALITATIVE TRACKING
    # What specific automation(s) did you implement this week?
    what_i_automated_this_week="",  # Be specific!
    
    # What's your biggest bottleneck preventing more automation?
    biggest_bottleneck_now=""  # Be honest!
)

# After submitting, view your progress:
print_progress_table()
create_visualizations()
generate_transformation_report()
"""