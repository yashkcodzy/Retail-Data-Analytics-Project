import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import combinations
from collections import Counter
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Retail Intelligence Pro | Enterprise Edition",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM GLASSMORPHISM STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { 
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    .stMetric {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    
    .stPlotlyChart {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .sidebar .sidebar-content {
        background: #0F172A;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px 8px 0px 0px;
        color: #94A3B8;
        padding: 0px 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: white !important;
    }
    
    h1, h2, h3 { color: #F8FAFC; letter-spacing: -1px; }
    
    .badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-high { background: #10B981; color: white; }
    .badge-mid { background: #F59E0B; color: white; }
    .badge-low { background: #EF4444; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING & FEATURE ENGINEERING ---
@st.cache_data
def load_data():
    path = 'data/Sample - Superstore.csv'
    try:
        df = pd.read_csv(path, encoding='windows-1252')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
        df['Year'] = df['Order Date'].dt.year
        df['DayOfYear'] = df['Order Date'].dt.dayofyear
        
        # Mock Inventory Data for Demonstration
        # In a real app, this would come from an inventory DB
        df['Stock_Level'] = np.random.randint(10, 200, size=len(df)) 
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR: GLOBAL CONTROLS ---
    with st.sidebar:
        st.title("🏙️ Strategic Ops")
        st.markdown("---")
        
        selected_year = st.multiselect("Select Years", sorted(df['Year'].unique(), reverse=True), default=df['Year'].unique())
        selected_region = st.multiselect("Select Regions", sorted(df['Region'].unique()), default=df['Region'].unique())
        
        st.markdown("---")
        st.subheader("💡 Simulator")
        sim_discount = st.slider("Target Discount Rate (%)", 0, 50, 15) / 100
        
        st.markdown("---")
        st.info("💡 **Pro Tip:** Use the tabs to switch between different business perspectives.")

    # Filter Data
    filtered_df = df[(df['Year'].isin(selected_year)) & (df['Region'].isin(selected_region))]

    # --- TOP LEVEL ANALYTICS ---
    total_rev = filtered_df['Sales'].sum()
    total_prof = filtered_df['Profit'].sum()
    avg_curr_discount = filtered_df['Discount'].mean()
    sim_profit = total_prof + (total_rev * (avg_curr_discount - sim_discount))
    margin = (total_prof / total_rev) * 100 if total_rev > 0 else 0

    st.title("🏙️ Retail Intelligence Pro")
    st.markdown("### Strategic Business Decision Suite")
    
    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Revenue", f"${total_rev/1000000:.2f}M", help="Total sales across selected filters")
    k2.metric("Projected Profit", f"${sim_profit/1000:.1f}K", delta=f"{(sim_profit - total_prof)/1000:.1f}K", help="Simulated profit based on discount target")
    k3.metric("Operating Margin", f"{margin:.1f}%", help="Efficiency of current sales")
    k4.metric("Avg Discount", f"{avg_curr_discount*100:.1f}%", help="Current average discount rate")

    # --- MAIN INTELLIGENCE TABS ---
    t_cust, t_sales, t_inv, t_profit = st.tabs([
        "👥 Customer Value", 
        "📈 Growth Dynamics", 
        "📦 Inventory Intel", 
        "💰 Profit Matrix"
    ])

    # T1: CUSTOMER VALUE (RFM + CLV + CHURN)
    with t_cust:
        st.subheader("Advanced Customer Segmentation")
        col_c1, col_c2 = st.columns([1, 1])
        
        # RFM + CLV Logic
        curr_date = df['Order Date'].max()
        rfm = filtered_df.groupby('Customer ID').agg({
            'Order Date': lambda x: (curr_date - x.max()).days,
            'Order ID': 'count',
            'Sales': 'sum'
        }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})
        
        # Simple CLV Prediction: (Avg Order Value * Frequency) * Retention Factor
        rfm['CLV_Pred'] = (rfm['Monetary'] / rfm['Frequency']) * rfm['Frequency'] * 1.5 
        rfm['Churn_Risk'] = rfm['Recency'].apply(lambda x: "High" if x > 365 else "Medium" if x > 180 else "Low")
        
        # Scoring
        for col in ['Recency', 'Frequency', 'Monetary']:
            try: rfm[f'{col[0]}_Score'] = pd.qcut(rfm[col].rank(method='first'), 4, labels=[1,2,3,4])
            except: rfm[f'{col[0]}_Score'] = 1
        
        rfm['Segment'] = rfm.apply(lambda x: 'Champions' if (int(x['R_Score'])+int(x['F_Score'])+int(x['M_Score'])) >= 10 else 
                                  ('Loyal' if (int(x['R_Score'])+int(x['F_Score'])+int(x['M_Score'])) >= 7 else 
                                   ('At Risk' if (int(x['R_Score'])+int(x['F_Score'])+int(x['M_Score'])) >= 5 else 'Lost')), axis=1)
        
        with col_c1:
            st.plotly_chart(px.pie(rfm, names='Segment', hole=0.5, template='plotly_dark', 
                                   color_discrete_sequence=px.colors.qualitative.Pastel), use_container_width=True)
        
        with col_c2:
            st.plotly_chart(px.histogram(rfm, x='Churn_Risk', color='Churn_Risk', title="Churn Risk Distribution",
                                        template='plotly_dark', color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}), 
                            use_container_width=True)
            
        st.markdown("#### 💎 Top 5 High-Value Customers (Predicted CLV)")
        st.dataframe(rfm.sort_values('CLV_Pred', ascending=False).head(5)[['Monetary', 'Frequency', 'CLV_Pred', 'Segment']], use_container_width=True)

    # T2: GROWTH DYNAMICS (Forecasting + Sunburst)
    with t_sales:
        st.subheader("Revenue Forecasting & Hierarchy")
        
        # Sunburst for Hierarchy
        fig_sun = px.sunburst(filtered_df, path=['Category', 'Sub-Category', 'Region'], values='Sales',
                              template='plotly_dark', title="Sales Hierarchy (Double-Click to Drill Down)")
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # Trend Analysis
        trend_df = filtered_df.groupby('Month')[['Sales']].sum().reset_index()
        z = np.polyfit(range(len(trend_df)), trend_df['Sales'], 1)
        p = np.poly1d(z)
        trend_df['Trend'] = p(range(len(trend_df)))
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Sales'], name='Actual Revenue', line=dict(color='#3B82F6', width=3)))
        fig_trend.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Trend'], name='Forecast Projection', line=dict(color='rgba(255,255,255,0.5)', dash='dash')))
        fig_trend.update_layout(template='plotly_dark', title="Long-term Growth Trend", hovermode="x unified")
        st.plotly_chart(fig_trend, use_container_width=True)

    # T3: INVENTORY INTEL (Stockout Risk)
    with t_inv:
        st.subheader("Inventory Stockout Risk Analysis")
        
        # Calculate daily velocity
        inv_df = filtered_df.groupby('Sub-Category').agg({
            'Quantity': 'sum',
            'Stock_Level': 'first' # In real data, this would be current stock
        }).reset_index()
        
        # Avg Daily Sales (Simple heuristic: total quantity / 365 days)
        inv_df['Daily_Velocity'] = inv_df['Quantity'] / (365 * len(selected_year) if len(selected_year) > 0 else 365)
        inv_df['Days_to_Stockout'] = inv_df['Stock_Level'] / inv_df['Daily_Velocity']
        
        st.info("🚨 **Alert:** Products with 'Days to Stockout' < 10 require immediate reordering.")
        
        fig_inv = px.bar(inv_df.sort_values('Days_to_Stockout'), x='Days_to_Stockout', y='Sub-Category', 
                         color='Days_to_Stockout', color_continuous_scale='RdYlGn_r',
                         template='plotly_dark', title="Estimated Days until Stockout")
        st.plotly_chart(fig_inv, use_container_width=True)
        
        col_i1, col_i2 = st.columns(2)
        col_i1.warning("**High Risk (Stockout < 15 Days)**")
        col_i1.table(inv_df[inv_df['Days_to_Stockout'] < 15][['Sub-Category', 'Days_to_Stockout']])
        
        col_i2.success("**Healthy (Stockout > 60 Days)**")
        col_i2.table(inv_df[inv_df['Days_to_Stockout'] > 60][['Sub-Category', 'Days_to_Stockout']])

    # T4: PROFIT MATRIX (Pareto + MBA)
    with t_profit:
        st.subheader("Profitability & Association Strategy")
        
        # Market Basket
        basket = filtered_df.groupby('Order ID')['Sub-Category'].apply(list)
        pairs = Counter()
        for items in basket:
            items = sorted(list(set(items)))
            if len(items) > 1: pairs.update(combinations(items, 2))
        
        pdf = pd.DataFrame(pairs.most_common(5), columns=['Pair', 'Freq'])
        pdf['Pair'] = pdf['Pair'].apply(lambda x: f"{x[0]} + {x[1]}")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### Product Pairing (Market Basket)")
            st.plotly_chart(px.bar(pdf, x='Freq', y='Pair', orientation='h', template='plotly_dark', color='Freq'), use_container_width=True)
            
        with col_p2:
            st.markdown("#### Pareto (80/20) Revenue Concentration")
            ps = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).reset_index()
            ps['Cum%'] = 100 * ps['Sales'].cumsum() / ps['Sales'].sum()
            st.plotly_chart(px.line(ps[:50], x=ps.index[:50], y='Cum%', template='plotly_dark'), use_container_width=True)

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("<center>Developed by Strategic Intelligence Unit | 2026</center>", unsafe_allow_html=True)

else:
    st.error("⚠️ Data Source Not Found. Please ensure 'Sample - Superstore.csv' is in the project data folder.")
