"""
Billion Transformation Tracker
Track your journey from manual operations to 80% automation

Weekly scorecard for AI Agency Operators
"""

# ============================================================================
# SETUP & IMPORTS
# ============================================================================

# Install required packages (run once)
# !pip install polars duckdb plotly kaleido

import polars as pl
import duckdb
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = "billion_tracker.db"
TABLE_NAME = "transformation_metrics"

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize DuckDB database with schema"""
    con = duckdb.connect(DB_PATH)
    
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            week_number INTEGER PRIMARY KEY,
            submission_date DATE,
            
            -- Time tracking (hours)
            total_hours FLOAT,
            automated_hours FLOAT,
            manual_hours FLOAT,
            
            -- Client metrics
            active_clients INTEGER,
            
            -- Revenue (stored as ratio to baseline for privacy)
            revenue_ratio FLOAT,
            
            -- Subscription transition
            recurring_revenue_pct FLOAT,
            
            -- Qualitative tracking
            automated_this_week TEXT,
            biggest_bottleneck TEXT,
            
            -- Calculated fields (stored for historical accuracy)
            automation_index FLOAT,
            time_saved_vs_baseline FLOAT,
            revenue_efficiency_multiple FLOAT,
            client_capacity_score FLOAT
        )
    """)
    
    con.close()
    print("✅ Database initialized successfully")

# ============================================================================
# WEEKLY DATA ENTRY
# ============================================================================

def submit_weekly_metrics(
    week_number: int,
    
    # Time tracking
    total_hours_worked: float,
    automated_hours: float,
    
    # Client metrics  
    active_clients: int,
    
    # Revenue (enter as ratio to your Week 1 baseline, e.g., 1.0, 1.2, 1.5)
    revenue_ratio_to_baseline: float,
    
    # Subscription transition (percentage, 0-100)
    recurring_revenue_percentage: float,
    
    # Qualitative
    what_i_automated_this_week: str,
    biggest_bottleneck_now: str
):
    """
    Submit your weekly metrics
    
    Privacy Note: Revenue is stored as a ratio to YOUR baseline,
    never as absolute numbers. Only you know what the baseline represents.
    """
    
    con = duckdb.connect(DB_PATH)
    
    # Calculate derived metrics
    manual_hours = total_hours_worked - automated_hours
    automation_index = (automated_hours / total_hours_worked * 100) if total_hours_worked > 0 else 0
    
    # Get baseline metrics from Week 1
    baseline = con.execute(f"""
        SELECT 
            total_hours,
            active_clients,
            revenue_ratio
        FROM {TABLE_NAME}
        WHERE week_number = 1
    """).fetchone()
    
    if baseline and week_number > 1:
        baseline_hours, baseline_clients, baseline_revenue = baseline
        time_saved = baseline_hours - total_hours_worked
        revenue_efficiency_multiple = (revenue_ratio_to_baseline / total_hours_worked) / (baseline_revenue / baseline_hours)
        client_capacity_score = (active_clients / total_hours_worked) / (baseline_clients / baseline_hours)
    else:
        # Week 1 is the baseline
        time_saved = 0
        revenue_efficiency_multiple = 1.0
        client_capacity_score = 1.0
    
    # Insert or update
    con.execute(f"""
        INSERT OR REPLACE INTO {TABLE_NAME} VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, [
        week_number,
        datetime.now().date(),
        total_hours_worked,
        automated_hours,
        manual_hours,
        active_clients,
        revenue_ratio_to_baseline,
        recurring_revenue_percentage,
        what_i_automated_this_week,
        biggest_bottleneck_now,
        automation_index,
        time_saved,
        revenue_efficiency_multiple,
        client_capacity_score
    ])
    
    con.close()
    
    print(f"✅ Week {week_number} metrics submitted successfully!")
    print(f"📊 Automation Index: {automation_index:.1f}%")
    print(f"⏰ Time Saved vs Baseline: {time_saved:.1f} hours/week")
    print(f"📈 Revenue Efficiency Multiple: {revenue_efficiency_multiple:.2f}x")

# ============================================================================
# VISUALIZATION & REPORTING
# ============================================================================

def get_metrics_df():
    """Load all metrics as Polars DataFrame"""
    con = duckdb.connect(DB_PATH)
    
    df = con.execute(f"""
        SELECT * FROM {TABLE_NAME}
        ORDER BY week_number
    """).pl()
    
    con.close()
    return df

def print_progress_table():
    """Display formatted progress table"""
    df = get_metrics_df()
    
    if df.height == 0:
        print("❌ No data yet. Submit your first week's metrics!")
        return
    
    # Select and rename columns for display
    display_df = df.select([
        pl.col("week_number").alias("Week"),
        pl.col("automation_index").round(1).alias("Automation %"),
        pl.col("time_saved_vs_baseline").round(1).alias("Hours Saved"),
        pl.col("revenue_efficiency_multiple").round(2).alias("Rev Efficiency"),
        pl.col("client_capacity_score").round(2).alias("Client Capacity"),
        pl.col("recurring_revenue_pct").round(1).alias("Recurring %")
    ])
    
    print("\n" + "="*80)
    print("📊 YOUR TRANSFORMATION PROGRESS")
    print("="*80)
    print(display_df)
    print("="*80 + "\n")
    
    # Latest week summary
    latest = df.tail(1)
    week_num = latest["week_number"][0]
    
    print(f"📅 Week {week_num} Summary:")
    print(f"   🤖 Automated this week: {latest['automated_this_week'][0]}")
    print(f"   🚧 Biggest bottleneck: {latest['biggest_bottleneck'][0]}")
    print()

def create_visualizations():
    """Generate comprehensive visualizations"""
    df = get_metrics_df()
    
    if df.height == 0:
        print("❌ No data yet. Submit your first week's metrics!")
        return
    
    # Convert to pandas for Plotly (Plotly works better with pandas)
    df_pd = df.to_pandas()
    
    # Create subplot figure with 2x2 grid
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '🤖 Automation Index (Target: 80%)',
            '⏰ Time Liberation Score',
            '📈 Revenue & Client Efficiency',
            '💰 Subscription Transition (Target: 50%)'
        ),
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "scatter"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 1. Automation Index
    fig.add_trace(
        go.Scatter(
            x=df_pd['week_number'],
            y=df_pd['automation_index'],
            mode='lines+markers',
            name='Automation %',
            line=dict(color='#00D9FF', width=3),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    # Target line at 80%
    fig.add_trace(
        go.Scatter(
            x=[df_pd['week_number'].min(), df_pd['week_number'].max()],
            y=[80, 80],
            mode='lines',
            name='Target (80%)',
            line=dict(color='#00FF88', width=2, dash='dash'),
            showlegend=False
        ),
        row=1, col=1
    )
    
    # 2. Time Liberation Score
    fig.add_trace(
        go.Scatter(
            x=df_pd['week_number'],
            y=df_pd['time_saved_vs_baseline'],
            mode='lines+markers',
            name='Hours Saved',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ),
        row=1, col=2
    )
    
    # 3. Efficiency Multiples
    fig.add_trace(
        go.Scatter(
            x=df_pd['week_number'],
            y=df_pd['revenue_efficiency_multiple'],
            mode='lines+markers',
            name='Revenue Efficiency',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=10)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df_pd['week_number'],
            y=df_pd['client_capacity_score'],
            mode='lines+markers',
            name='Client Capacity',
            line=dict(color='#95E1D3', width=3),
            marker=dict(size=10)
        ),
        row=2, col=1
    )
    # Baseline at 1.0x
    fig.add_trace(
        go.Scatter(
            x=[df_pd['week_number'].min(), df_pd['week_number'].max()],
            y=[1.0, 1.0],
            mode='lines',
            name='Baseline (1.0x)',
            line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 4. Subscription Transition
    fig.add_trace(
        go.Scatter(
            x=df_pd['week_number'],
            y=df_pd['recurring_revenue_pct'],
            mode='lines+markers',
            name='Recurring Revenue %',
            line=dict(color='#FFD93D', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(255, 217, 61, 0.2)'
        ),
        row=2, col=2
    )
    # Target line at 50%
    fig.add_trace(
        go.Scatter(
            x=[df_pd['week_number'].min(), df_pd['week_number'].max()],
            y=[50, 50],
            mode='lines',
            name='Target (50%)',
            line=dict(color='#00FF88', width=2, dash='dash'),
            showlegend=False
        ),
        row=2, col=2
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Week", row=1, col=1)
    fig.update_xaxes(title_text="Week", row=1, col=2)
    fig.update_xaxes(title_text="Week", row=2, col=1)
    fig.update_xaxes(title_text="Week", row=2, col=2)
    
    fig.update_yaxes(title_text="%", row=1, col=1)
    fig.update_yaxes(title_text="Hours", row=1, col=2)
    fig.update_yaxes(title_text="Multiple (x)", row=2, col=1)
    fig.update_yaxes(title_text="%", row=2, col=2)
    
    # Update layout
    fig.update_layout(
        title_text="<b>Billion Transformation Dashboard</b>",
        title_font_size=24,
        showlegend=True,
        height=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    fig.show()
    
    # Create hours breakdown chart
    fig_hours = go.Figure()
    
    fig_hours.add_trace(go.Bar(
        x=df_pd['week_number'],
        y=df_pd['automated_hours'],
        name='Automated Hours',
        marker_color='#00D9FF'
    ))
    
    fig_hours.add_trace(go.Bar(
        x=df_pd['week_number'],
        y=df_pd['manual_hours'],
        name='Manual Hours',
        marker_color='#FF6B6B'
    ))
    
    fig_hours.update_layout(
        title='📊 Weekly Hours Breakdown: Automated vs Manual',
        xaxis_title='Week',
        yaxis_title='Hours',
        barmode='stack',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white'
    )
    
    fig_hours.show()

def generate_transformation_report():
    """Generate comprehensive transformation report"""
    df = get_metrics_df()
    
    if df.height == 0:
        print("❌ No data yet. Submit your first week's metrics!")
        return
    
    latest = df.tail(1)
    first = df.head(1)
    
    week_num = latest["week_number"][0]
    
    print("\n" + "="*80)
    print("🎯 TRANSFORMATION REPORT")
    print("="*80)
    print(f"\n📅 Current Week: {week_num}/12")
    print(f"📆 Journey Started: {first['submission_date'][0]}")
    print(f"📆 Latest Update: {latest['submission_date'][0]}")
    
    print("\n" + "-"*80)
    print("📊 KEY METRICS")
    print("-"*80)
    
    # Automation Index
    ai_current = latest["automation_index"][0]
    ai_start = first["automation_index"][0]
    ai_change = ai_current - ai_start
    print(f"\n🤖 Automation Index:")
    print(f"   Week 1: {ai_start:.1f}%")
    print(f"   Week {week_num}: {ai_current:.1f}%")
    print(f"   Change: {ai_change:+.1f}% {'✅' if ai_change > 0 else '⚠️'}")
    print(f"   Target: 80% {'✅ ACHIEVED!' if ai_current >= 80 else f'({80-ai_current:.1f}% to go)'}")
    
    # Time Liberation
    time_saved = latest["time_saved_vs_baseline"][0]
    baseline_hours = first["total_hours"][0]
    time_reduction_pct = (time_saved / baseline_hours * 100) if baseline_hours > 0 else 0
    print(f"\n⏰ Time Liberation Score:")
    print(f"   Hours Saved per Week: {time_saved:.1f} hours")
    print(f"   Time Reduction: {time_reduction_pct:.1f}%")
    print(f"   Target: 50% reduction {'✅ ACHIEVED!' if time_reduction_pct >= 50 else f'({50-time_reduction_pct:.1f}% to go)'}")
    
    # Revenue Efficiency
    rem = latest["revenue_efficiency_multiple"][0]
    print(f"\n📈 Revenue Efficiency Multiple:")
    print(f"   Current: {rem:.2f}x baseline")
    print(f"   Status: {'✅ Growing!' if rem > 1.0 else '⚠️ Below baseline'}")
    
    # Client Capacity
    ccs = latest["client_capacity_score"][0]
    print(f"\n👥 Client Capacity Score:")
    print(f"   Current: {ccs:.2f}x baseline")
    print(f"   You can now serve {ccs:.1f}x more clients per hour worked")
    
    # Subscription Transition
    sti = latest["recurring_revenue_pct"][0]
    print(f"\n💰 Subscription Transition Index:")
    print(f"   Recurring Revenue: {sti:.1f}%")
    print(f"   Target: 50% {'✅ ACHIEVED!' if sti >= 50 else f'({50-sti:.1f}% to go)'}")
    
    # Graduation Readiness
    print("\n" + "-"*80)
    print("🎓 GRADUATION READINESS")
    print("-"*80)
    
    requirements = [
        ("Automation Index ≥ 70%", ai_current >= 70),
        ("Time Liberation ≥ 50%", time_reduction_pct >= 50),
        ("Subscription Revenue ≥ 50%", sti >= 50),
        ("Complete 12 weeks", week_num >= 12)
    ]
    
    for req, met in requirements:
        status = "✅" if met else "⬜"
        print(f"{status} {req}")
    
    ready_to_graduate = all(met for _, met in requirements)
    
    if ready_to_graduate:
        print("\n🎉 CONGRATULATIONS! You're ready to graduate!")
        print("📧 Submit your transformation portfolio to receive your certification.")
    else:
        remaining = sum(1 for _, met in requirements if not met)
        print(f"\n💪 Keep going! {remaining} requirement(s) remaining.")
    
    # Recent wins
    print("\n" + "-"*80)
    print("🏆 RECENT PROGRESS")
    print("-"*80)
    
    if df.height >= 2:
        last_2_weeks = df.tail(2)
        print(f"\n📝 Week {week_num-1}:")
        print(f"   Automated: {last_2_weeks['automated_this_week'][0]}")
        print(f"   Bottleneck: {last_2_weeks['biggest_bottleneck'][0]}")
    
    print(f"\n📝 Week {week_num}:")
    print(f"   Automated: {latest['automated_this_week'][0]}")
    print(f"   Bottleneck: {latest['biggest_bottleneck'][0]}")
    
    print("\n" + "="*80 + "\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Initialize database
    init_database()
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║               🚀 BILLION TRANSFORMATION TRACKER 🚀                     ║
    ║                                                                        ║
    ║            Track Your Journey to 80% Automation in 12 Weeks            ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    
    📋 INSTRUCTIONS:
    
    1️⃣  Submit your weekly metrics using submit_weekly_metrics()
    2️⃣  View your progress table with print_progress_table()
    3️⃣  Generate visualizations with create_visualizations()
    4️⃣  Get full report with generate_transformation_report()
    
    🔒 PRIVACY: Your actual revenue numbers are NEVER stored.
       Only ratios relative to YOUR Week 1 baseline are tracked.
    
    📖 Example usage below ⬇️
    """)