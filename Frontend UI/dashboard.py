import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from collections import Counter
from itertools import combinations
import os
from sklearn.ensemble import IsolationForest

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Retail Intel Pro | Strategic Decision Suite",
    page_icon="🏙️",
    layout="wide",
)

# --- PREMIUM CUSTOM STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Outfit:wght@300;600;800&display=swap');
    
    :root {
        --primary: #3b82f6;
        --accent: #8b5cf6;
        --bg-deep: #020617;
        --card-bg: rgba(255, 255, 255, 0.03);
    }

    * { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Outfit', sans-serif; font-weight: 800; letter-spacing: -1px; }
    
    .stApp {
        background: radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.1) 0%, transparent 40%),
                    radial-gradient(circle at 100% 100%, rgba(139, 92, 246, 0.1) 0%, transparent 40%),
                    #020617;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 40px;
        margin-bottom: 30px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    
    /* Hero Landing */
    .hero-container {
        position: relative;
        text-align: left;
        padding: 100px 60px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(0,0,0,0) 100%);
        border-radius: 48px;
        margin-bottom: 80px;
        border: 1px solid rgba(255,255,255,0.05);
        overflow: hidden;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
        z-index: 0;
    }
    
    .hero-title {
        font-size: 5.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        line-height: 1;
        z-index: 1;
        position: relative;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #94a3b8;
        max-width: 650px;
        margin-bottom: 40px;
        line-height: 1.6;
        z-index: 1;
        position: relative;
    }

    /* Status Indicator */
    .live-dot {
        height: 10px;
        width: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 16px; padding: 10px 0; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        color: #94a3b8;
        padding: 0 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 15px 30px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INTELLIGENCE ENGINE ---
@st.cache_data
def load_data():
    paths = ['data/Sample - Superstore.csv', '../data/Sample - Superstore.csv']
    df = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p, encoding='windows-1252')
            break
    if df is None: return None
    
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%Y-%m')
    
    # AI Inventory Simulation
    np.random.seed(42)
    df['Stock_Level'] = np.random.randint(20, 400, size=len(df))
    
    # 🌐 Strategic Omnichannel Simulation
    channel_map = {
        'Second Class': 'Online App',
        'Standard Class': 'In-Store',
        'First Class': 'Web Portal',
        'Same Day': 'Express Online'
    }
    df['Channel'] = df['Ship Mode'].map(channel_map)
    return df

df = load_data()

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "🌐 Landing Page"

def set_page(page):
    st.session_state.page = page

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://ui-avatars.com/api/?name=Retail+Pro&background=3b82f6&color=fff&size=128&rounded=true", width=80)
    st.title("RetailIntel Suite")
    
    page = st.radio(
        "Navigation", 
        ["🌐 Landing Page", "🧠 Intelligence Command"],
        index=0 if st.session_state.page == "🌐 Landing Page" else 1,
        key="navigation_radio",
        on_change=lambda: st.session_state.update({"page": st.session_state.navigation_radio})
    )
    st.markdown("---")
    
    # AI Dynamic Insights in Sidebar
    if st.session_state.page == "🧠 Intelligence Command" and df is not None:
        st.markdown("### 🧠 Live Insights")
        total_rev = df['Sales'].sum()
        st.metric("Global Revenue", f"${total_rev/1000000:.2f}M")
        if total_rev > 2000000:
            st.success("✨ Global Target Met")
        else:
            st.warning("⚠️ Below Global Target")
        
    st.info("Enterprise Analytics Platform v3.0")

if df is None:
    st.error("Data Source Not Found. Please ensure 'Sample - Superstore.csv' is in the data folder.")
    st.stop()

# --- PAGE 1: LANDING PAGE ---
if st.session_state.page == "🌐 Landing Page":
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <div style="background:rgba(59, 130, 246, 0.1); color:#3b82f6; padding:8px 20px; border-radius:30px; display:inline-block; font-weight:700; font-size:0.85rem; margin-bottom:30px; border:1px solid rgba(59, 130, 246, 0.2);">
                <span class="live-dot"></span> SYSTEM ONLINE | ENTERPRISE VERSION 4.2
            </div>
            <h1 class="hero-title">Retail Intelligence<br>Pro Suite</h1>
            <p class="hero-subtitle">
                The definitive strategic decision-support suite for high-end retail ecosystems. 
                Synchronize your omnichannel data, predict inventory velocity, and optimize profit margins with neural-driven insights.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    st.markdown("### 💎 Strategic Intelligence Modules")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="glass-card">
                <div style="font-size:2.5rem; margin-bottom:20px;">🌐</div>
                <h3 style="color:#fff">Omnichannel Orchestration</h3>
                <p style="color:#94a3b8; font-size:1.1rem;">Unified visibility across Web, App, and Physical stores. Real-time synchronization of global retail performance.</p>
                <div style="margin-top:20px; color:#3b82f6; font-weight:600; cursor:pointer;">Explore Neural Mapping →</div>
            </div>
            <div class="glass-card">
                <div style="font-size:2.5rem; margin-bottom:20px;">🧠</div>
                <h3 style="color:#fff">Predictive Inventory Engine</h3>
                <p style="color:#94a3b8; font-size:1.1rem;">Automated restock intelligence and supply velocity forecasting using advanced regression models.</p>
                <div style="margin-top:20px; color:#10b981; font-weight:600; cursor:pointer;">Audit Supply Chain →</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="glass-card">
                <div style="font-size:2.5rem; margin-bottom:20px;">👥</div>
                <h3 style="color:#fff">Customer Value Intelligence</h3>
                <p style="color:#94a3b8; font-size:1.1rem;">AI-driven RFM segmentation and Lifetime Value (CLV) projections for hyper-personalized growth.</p>
                <div style="margin-top:20px; color:#8b5cf6; font-weight:600; cursor:pointer;">View Segment Reports →</div>
            </div>
            <div class="glass-card">
                <div style="font-size:2.5rem; margin-bottom:20px;">💰</div>
                <h3 style="color:#fff">Profit Optimization Matrix</h3>
                <p style="color:#94a3b8; font-size:1.1rem;">Dynamic What-If simulators and Market Basket bundling strategies to maximize operational margins.</p>
                <div style="margin-top:20px; color:#f59e0b; font-weight:600; cursor:pointer;">Optimize Margins →</div>
            </div>
        """, unsafe_allow_html=True)

    # Launch CTA
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 LAUNCH INTELLIGENCE COMMAND", use_container_width=True, type="primary"):
            st.session_state.page = "🧠 Intelligence Command"
            st.rerun()

# --- PAGE 2: INTELLIGENCE COMMAND ---
else:
    st.title("🧠 Intelligence Command Center")
    st.markdown("#### Strategic Executive Dashboard")
    
    # Global Filters
    f_year = st.sidebar.multiselect("Select Year", sorted(df['Year'].unique(), reverse=True), default=df['Year'].unique()[:2])
    f_region = st.sidebar.multiselect("Select Region", sorted(df['Region'].unique()), default=df['Region'].unique())
    f_channel = st.sidebar.multiselect("Select Channel", sorted(df['Channel'].unique()), default=df['Channel'].unique())
    
    mask = df['Year'].isin(f_year) & df['Region'].isin(f_region) & df['Channel'].isin(f_channel)
    f_df = df[mask]
    
    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    rev = f_df['Sales'].sum()
    prof = f_df['Profit'].sum()
    disc = f_df['Discount'].mean() * 100
    m1.metric("Gross Revenue", f"${rev/1000000:.2f}M")
    m2.metric("Net Profit", f"${prof/1000:.1f}K")
    m3.metric("Avg Discount", f"{disc:.1f}%")
    m4.metric("Market Margin", f"{(prof/rev*100):.1f}%")

    # Modules
    tab_cust, tab_omni, tab_inv, tab_growth, tab_profit, tab_ai, tab_sim = st.tabs([
        "👥 Customer Value", "🌐 Omnichannel", "📦 Inventory", "📈 Growth Dynamics", "💰 Profit Optimization", "🧠 AI Anomalies", "🧠 Tactical Simulator"
    ])
    
    # 1. Customer Value
    with tab_cust:
        st.subheader("Customer Intelligence Suite")
        col_c1, col_c2 = st.columns([1, 1])
        
        # RFM Logic
        max_d = df['Order Date'].max()
        rfm = f_df.groupby('Customer ID').agg({
            'Order Date': lambda x: (max_d - x.max()).days,
            'Order ID': 'count',
            'Sales': 'sum'
        }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})
        
        # AI Segment
        rfm['Score'] = rfm.rank(method='first').sum(axis=1)
        rfm['Segment'] = pd.qcut(rfm['Score'].rank(method='first'), 4, labels=['Lost', 'At Risk', 'Loyal', 'Champions'])
        
        with col_c1:
            fig_rfm = px.pie(rfm, names='Segment', hole=0.6, title="Value Segmentation", template='plotly_dark',
                            color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#10b981'])
            st.plotly_chart(fig_rfm, use_container_width=True)
        
        with col_c2:
            st.markdown("#### 💎 Top Predictive CLV Profiles")
            rfm['CLV'] = rfm['Monetary'] * 1.5
            st.dataframe(rfm.sort_values('CLV', ascending=False).head(10)[['Monetary', 'Frequency', 'CLV', 'Segment']], use_container_width=True)

    # 2. Omnichannel Intelligence
    with tab_omni:
        st.subheader("Omnichannel Performance Analytics")
        col_o1, col_o2 = st.columns([1, 1])
        
        with col_o1:
            fig_chan = px.pie(f_df, values='Sales', names='Channel', hole=0.5,
                             title="Revenue Share by Channel", template='plotly_dark',
                             color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_chan, use_container_width=True)
            
        with col_o2:
            chan_perf = f_df.groupby('Channel').agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
            fig_perf = px.bar(chan_perf, x='Channel', y=['Sales', 'Profit'], barmode='group',
                             title="Revenue vs Profitability by Channel", template='plotly_dark',
                             color_discrete_map={'Sales': '#3b82f6', 'Profit': '#10b981'})
            st.plotly_chart(fig_perf, use_container_width=True)
            
        st.markdown("#### 🚀 Channel Velocity Matrix")
        chan_metrics = f_df.groupby('Channel').agg({
            'Order ID': 'nunique',
            'Sales': 'mean',
            'Profit': 'mean'
        }).rename(columns={'Order ID': 'Order Volume', 'Sales': 'Avg Order Value', 'Profit': 'Avg Margin'})
        st.table(chan_metrics.style.background_gradient(cmap='Blues'))

    # 2. Inventory
    with tab_inv:
        st.subheader("Inventory Velocity & Restock Engine")
        inv_df = f_df.groupby('Sub-Category').agg({'Quantity': 'sum', 'Stock_Level': 'first'}).reset_index()
        inv_df['Velocity'] = inv_df['Quantity'] / (365 * len(f_year) if f_year else 365)
        inv_df['Days_Left'] = inv_df['Stock_Level'] / inv_df['Velocity'].replace(0, 0.01)
        
        st.warning("🚨 **Restock Alerts**: Products with < 15 Days supply remaining.")
        fig_inv = px.bar(inv_df.sort_values('Days_Left'), x='Days_Left', y='Sub-Category', color='Days_Left',
                         color_continuous_scale='RdYlGn_r', template='plotly_dark', title="Days of Supply Remaining")
        st.plotly_chart(fig_inv, use_container_width=True)

    # 3. Growth
    with tab_growth:
        st.subheader("Strategic Forecaster & Hierarchy Audit")
        
        # Sunburst
        fig_sun = px.sunburst(f_df, path=['Category', 'Sub-Category', 'Region'], values='Sales',
                             template='plotly_dark', title="Sales Hierarchy (Click to Drill Down)")
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # Forecast
        trend = f_df.groupby('Month')['Sales'].sum().reset_index()
        X = np.array(range(len(trend))).reshape(-1, 1)
        y = trend['Sales'].values
        model = LinearRegression().fit(X, y)
        trend['Forecast'] = model.predict(X)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=trend['Month'], y=trend['Sales'], name='Actual Revenue', line=dict(color='#3b82f6', width=3)))
        fig_trend.add_trace(go.Scatter(x=trend['Month'], y=trend['Forecast'], name='AI Trend', line=dict(dash='dash', color='gray')))
        fig_trend.update_layout(template='plotly_dark', title="Long-term Growth Forecast")
        st.plotly_chart(fig_trend, use_container_width=True)

    # 4. Profit Optimization
    with tab_profit:
        st.subheader("Optimization Matrix")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("#### ⚖️ What-If Simulator")
            target_d = st.slider("Target Discount Rate (%)", 0, 40, 15) / 100
            sim_p = prof + (rev * ( (disc/100) - target_d ))
            st.markdown(f"**Projected Profit Impact:**")
            st.title(f"${sim_p/1000:.1f}K")
            st.progress(min(max(sim_p/prof, 0.0), 1.0))
            
        with col_p2:
            st.markdown("#### 🧺 Market Basket Analysis")
            basket = f_df.groupby('Order ID')['Sub-Category'].apply(list)
            pairs = Counter()
            for items in basket:
                items = sorted(list(set(items)))
                if len(items) > 1: pairs.update(combinations(items, 2))
            
            top_pairs = pd.DataFrame(pairs.most_common(5), columns=['Pair', 'Freq'])
            top_pairs['Pair'] = top_pairs['Pair'].apply(lambda x: f"{x[0]} + {x[1]}")
            st.table(top_pairs)

        st.markdown("---")
        st.markdown("#### 🎯 Pareto 80/20 Concentration")
        prod_sales = f_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).reset_index()
        prod_sales['Cum%'] = 100 * prod_sales['Sales'].cumsum() / prod_sales['Sales'].sum()
        fig_pareto = px.line(prod_sales.head(100), x=prod_sales.index[:100], y='Cum%', title="Cumulative Sales Concentration", template='plotly_dark')
        st.plotly_chart(fig_pareto, use_container_width=True)

    # 5. AI Anomalies
    with tab_ai:
        st.subheader("AI Anomaly & Fraud Detection")
        st.write("Detecting unusual patterns in Sales, Profit, and Discounts using Isolation Forest (Outlier Analysis).")
        
        # Prepare features for anomaly detection
        features = ['Sales', 'Profit', 'Discount']
        X_iso = f_df[features].copy()
        
        # Simple Isolation Forest
        iso = IsolationForest(contamination=0.03, random_state=42)
        f_df['Anomaly'] = iso.fit_predict(X_iso)
        f_df['Anomaly_Label'] = f_df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})
        
        anomalies = f_df[f_df['Anomaly'] == -1]
        
        col_a1, col_a2 = st.columns([2, 1])
        
        with col_a1:
            fig_anom = px.scatter(f_df, x='Sales', y='Profit', color='Anomaly_Label', 
                                 hover_data=['Customer Name', 'Product Name', 'Discount'],
                                 color_discrete_map={'Normal': 'rgba(59, 130, 246, 0.4)', 'Anomaly': '#ef4444'},
                                 title="Sales vs Profit Anomaly Map", template='plotly_dark')
            st.plotly_chart(fig_anom, use_container_width=True)
            
        with col_a2:
            st.markdown("#### 🚨 Intelligence Alert")
            st.metric("Detected Anomalies", len(anomalies), delta=f"{len(anomalies)/len(f_df)*100:.1f}% of total", delta_color="inverse")
            st.info("These transactions show high discount/low profit ratios or extreme sales volume. Recommended for manual audit.")
            
        st.markdown("#### Detailed Anomaly Audit Trail")
        st.dataframe(anomalies[['Order Date', 'Customer Name', 'Product Name', 'Sales', 'Profit', 'Discount']].sort_values('Sales', ascending=False), use_container_width=True)

    # 6. Tactical Simulator
    with tab_sim:
        st.subheader("Neural Tactical Simulator")
        col_s1, col_s2 = st.columns([1, 2])
        
        with col_s1:
            st.markdown("#### Simulation Variables")
            s_price = st.slider("Price Adjustment (%)", -20, 20, 0)
            s_vol = st.slider("Volume Variance (%)", -30, 50, 0)
            s_cost = st.slider("Operational Cost (%)", -10, 20, 0)
            
        with col_s2:
            orig_rev = f_df['Sales'].sum()
            orig_prof = f_df['Profit'].sum()
            
            sim_rev = orig_rev * (1 + s_price/100) * (1 + s_vol/100)
            sim_prof = sim_rev * (orig_prof/orig_rev) * (1 - s_cost/100)
            
            diff = ((sim_prof - orig_prof) / orig_prof * 100) if orig_prof != 0 else 0
            
            c1, c2 = st.columns(2)
            c1.metric("Simulated Profit", f"${sim_prof/1000:.1f}K", delta=f"{diff:.1f}%")
            c2.metric("Simulated Revenue", f"${sim_rev/1000000:.2f}M")
            
            sim_data = pd.DataFrame({
                'Metric': ['Current', 'Simulated'],
                'Profit': [orig_prof/1000, sim_prof/1000]
            })
            st.plotly_chart(px.bar(sim_data, x='Metric', y='Profit', color='Metric', 
                                 color_discrete_map={'Current': '#3b82f6', 'Simulated': '#10b981'},
                                 template='plotly_dark'), use_container_width=True)

    st.markdown("---")
    st.markdown("<center>Retail Intelligence Pro | Enterprise Strategic Suite | © 2026 | Powered by Advanced AI</center>", unsafe_allow_html=True)
