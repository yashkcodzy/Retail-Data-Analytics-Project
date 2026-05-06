import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import combinations
from collections import Counter

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ultimate Retail Strategy Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM THEME STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    .stMetric {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stPlotlyChart {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #334155;
    }
    .css-1kyx0rg { background-color: #1E293B; }
    h1, h2, h3 { color: #F8FAFC; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    path = r'C:\Users\Varsha\Downloads\Retail-Data-Analytics-Project-main\Retail-Data-Analytics-Project-main\data\Sample - Superstore.csv'
    try:
        df = pd.read_csv(path, encoding='windows-1252')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
        df['Year'] = df['Order Date'].dt.year
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR: WHAT-IF SIMULATOR ---
    st.sidebar.title("🧪 Strategic Controls")
    
    selected_year = st.sidebar.multiselect("Select Years", sorted(df['Year'].unique(), reverse=True), default=df['Year'].unique())
    selected_region = st.sidebar.multiselect("Select Regions", sorted(df['Region'].unique()), default=df['Region'].unique())
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📉 Profit Simulator")
    sim_discount = st.sidebar.slider("Simulate Avg Discount (%)", 0, 50, 15) / 100
    
    # Filter Data
    filtered_df = df[(df['Year'].isin(selected_year)) & (df['Region'].isin(selected_region))]

    # --- TOP KPI CALCULATIONS ---
    total_rev = filtered_df['Sales'].sum()
    total_prof = filtered_df['Profit'].sum()
    avg_curr_discount = filtered_df['Discount'].mean()
    sim_profit = total_prof + (total_rev * (avg_curr_discount - sim_discount))
    margin = (total_prof / total_rev) * 100 if total_rev > 0 else 0

    st.title("🏆 Ultimate Retail Strategy Suite")
    
    # --- DYNAMIC NARRATIVE ---
    status = "🟢 Healthy" if margin > 15 else "🟡 Stable" if margin > 5 else "🔴 Critical"
    st.markdown(f"> **Executive Summary:** The business is in a **{status}** state. Current profit is **${total_prof/1000:.1f}K** with a **{margin:.1f}%** margin. Adjusting discounts in the sidebar will update the **Projected Profit** below.")

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Revenue", f"${total_rev/1000000:.2f}M")
    k2.metric("Projected Profit", f"${sim_profit/1000:.1f}K", delta=f"{(sim_profit - total_prof)/1000:.1f}K (Simulated)")
    k3.metric("Profit Margin", f"{margin:.1f}%")
    k4.metric("Avg Discount", f"{avg_curr_discount*100:.1f}%")

    # --- MAIN TABS ---
    t_cust, t_sales, t_profit, t_geo = st.tabs(["👥 Customer Intelligence", "📈 Sales & Trends", "💰 Profit Optimization", "🌍 Geo-Insights"])

    # T1: CUSTOMER INTELLIGENCE (RFM)
    with t_cust:
        st.subheader("RFM Segmentation (Customer Value Mapping)")
        
        # RFM Logic
        curr_date = df['Order Date'].max()
        rfm = filtered_df.groupby('Customer ID').agg({
            'Order Date': lambda x: (curr_date - x.max()).days,
            'Order ID': 'count',
            'Sales': 'sum'
        }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})
        
        # Scoring (Handling small datasets)
        for col in ['Recency', 'Frequency', 'Monetary']:
            try:
                rfm[f'{col[0]}_Score'] = pd.qcut(rfm[col].rank(method='first'), 4, labels=[1,2,3,4])
            except:
                rfm[f'{col[0]}_Score'] = 1
        
        def segment(row):
            score = int(row['R_Score']) + int(row['F_Score']) + int(row['M_Score'])
            if score >= 10: return 'Champions'
            if score >= 7: return 'Loyal'
            if score >= 5: return 'At Risk'
            return 'Lost'
        
        rfm['Segment'] = rfm.apply(segment, axis=1)
        
        c1, c2 = st.columns(2)
        fig_rfm = px.pie(rfm, names='Segment', hole=0.5, template='plotly_dark', title="Customer Segments")
        c1.plotly_chart(fig_rfm, use_container_width=True)
        
        fig_val = px.scatter(rfm, x='Frequency', y='Monetary', color='Segment', size='Monetary', template='plotly_dark', title="Value Mapping")
        c2.plotly_chart(fig_val, use_container_width=True)

    # T2: SALES & TRENDS (Forecasting + Market Basket)
    with t_sales:
        st.subheader("Sales Forecasting & Trends")
        trend_df = filtered_df.groupby('Month')[['Sales']].sum().reset_index()
        
        # Forecasting
        z = np.polyfit(range(len(trend_df)), trend_df['Sales'], 1)
        p = np.poly1d(z)
        trend_df['Trend'] = p(range(len(trend_df)))
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Sales'], name='Actual Sales', line=dict(color='#3B82F6')))
        fig_trend.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Trend'], name='Trend Line', line=dict(color='white', dash='dash')))
        fig_trend.update_layout(template='plotly_dark', title="Revenue Forecast")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.subheader("Market Basket Analysis (Top Pairs)")
        basket = filtered_df.groupby('Order ID')['Sub-Category'].apply(list)
        pairs = Counter()
        for items in basket:
            items = sorted(list(set(items)))
            if len(items) > 1:
                pairs.update(combinations(items, 2))
        
        pdf = pd.DataFrame(pairs.most_common(5), columns=['Pair', 'Freq'])
        pdf['Pair'] = pdf['Pair'].apply(lambda x: f"{x[0]} + {x[1]}")
        st.plotly_chart(px.bar(pdf, x='Freq', y='Pair', orientation='h', template='plotly_dark'), use_container_width=True)

    # T3: PROFIT OPTIMIZATION (Simulator + Pareto + Strategic Tables)
    with t_profit:
        st.subheader("Strategic Profit Analysis")
        
        # Pareto
        ps = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).reset_index()
        ps['Cum%'] = 100 * ps['Sales'].cumsum() / ps['Sales'].sum()
        st.plotly_chart(px.line(ps[:50], x=ps.index[:50], y='Cum%', title="Pareto 80/20 Rule", template='plotly_dark'), use_container_width=True)
        
        # Strategic Insight Tables
        st.markdown("### 🔍 High-Action Insight Tables")
        col_t1, col_t2 = st.columns(2)
        
        top_drivers = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)
        col_t1.info("**Top Revenue Drivers**")
        col_t1.table(top_drivers)
        
        worst_profit = filtered_df.groupby('Product Name')['Profit'].sum().sort_values(ascending=True).head(5)
        col_t2.error("**Most Unprofitable (Immediate Action)**")
        col_t2.table(worst_profit)

    # T4: GEO-INSIGHTS
    with t_geo:
        st.subheader("Regional Performance Map")
        sdf = filtered_df.groupby('State')['Sales'].sum().reset_index()
        fig_map = px.choropleth(sdf, locations='State', locationmode="USA-states", color='Sales', scope="usa", template='plotly_dark')
        st.plotly_chart(fig_map, use_container_width=True)

else:
    st.error("Could not load data.")
