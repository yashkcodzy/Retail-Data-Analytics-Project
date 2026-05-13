from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Retail Intelligence Pro API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Sample - Superstore.csv")

def load_data():
    if not os.path.exists(DATA_PATH):
        # Fallback to local data dir if not in parent
        DATA_PATH_LOCAL = os.path.join(os.path.dirname(__file__), "data/Sample - Superstore.csv")
        if os.path.exists(DATA_PATH_LOCAL):
            df = pd.read_csv(DATA_PATH_LOCAL, encoding='windows-1252')
        else:
            raise FileNotFoundError(f"Data file not found")
    else:
        df = pd.read_csv(DATA_PATH, encoding='windows-1252')
    
    # Simulate Grocery Items if not in data (fallback)
    if 'Grocery' not in df['Category'].unique():
        grocery_data = pd.DataFrame([
            {'Order ID': 'G-001', 'Order Date': pd.Timestamp('2026-05-01'), 'Category': 'Grocery', 'Sub-Category': 'Flour', 'Product Name': 'Premium Flour', 'Sales': 1200, 'Profit': 300, 'Ship Mode': 'Standard Class', 'Customer ID': 'C-1', 'Discount': 0, 'Quantity': 50},
            {'Order ID': 'G-002', 'Order Date': pd.Timestamp('2026-05-02'), 'Category': 'Grocery', 'Sub-Category': 'Flour', 'Product Name': 'Organic Flour', 'Sales': 800, 'Profit': 200, 'Ship Mode': 'First Class', 'Customer ID': 'C-2', 'Discount': 0, 'Quantity': 30}
        ])
        df = pd.concat([df, grocery_data], ignore_index=True)

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    
    channel_map = {
        'Second Class': 'Online App',
        'Standard Class': 'In-Store',
        'First Class': 'Web Portal',
        'Same Day': 'Express Online'
    }
    df['Channel'] = df['Ship Mode'].map(channel_map).fillna('Other')
    return df

@app.get("/api/summary")
def get_summary():
    df = load_data()
    return {
        "total_sales": float(df['Sales'].sum()),
        "total_profit": float(df['Profit'].sum()),
        "total_orders": int(df['Order ID'].nunique()),
        "avg_discount": float(df['Discount'].mean())
    }

@app.get("/api/analytics/full")
def get_full_analytics():
    df = load_data()
    
    # 1. Trends
    df['Month'] = df['Order Date'].dt.strftime('%Y-%m')
    trends = df.groupby('Month')['Sales'].sum().sort_index().reset_index().to_dict(orient='records')
    
    # 2. Categories
    cats = df.groupby('Category')['Sales'].sum().to_dict()
    
    # 3. Omnichannel
    omni = df.groupby('Channel').agg({'Sales':'sum', 'Profit':'sum'}).reset_index().to_dict(orient='records')
    
    # 4. Inventory
    np.random.seed(42)
    df['Stock'] = np.random.randint(20, 500, size=len(df))
    inv = df.groupby('Sub-Category').agg({'Quantity': 'sum', 'Stock': 'first'}).reset_index()
    inv['Days_Left'] = (inv['Stock'] / (inv['Quantity'] / 365).replace(0, 0.01)).round(0)
    inv_data = inv.to_dict(orient='records')
    
    # 5. RFM
    max_d = df['Order Date'].max()
    rfm = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (max_d - x.max()).days,
        'Order ID': 'count',
        'Sales': 'sum'
    }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})
    rfm['Segment'] = pd.qcut(rfm['Monetary'].rank(method='first'), 4, labels=['Bronze', 'Silver', 'Gold', 'Platinum'])
    rfm_data = {
        "segments": rfm['Segment'].value_counts().to_dict(),
        "top": rfm.sort_values('Monetary', ascending=False).head(8).reset_index().to_dict(orient='records')
    }
    
    # 6. Anomalies
    iso = IsolationForest(contamination=0.01, random_state=42)
    df['anom'] = iso.fit_predict(df[['Sales', 'Profit']].fillna(0))
    anoms = df[df['anom'] == -1].head(10)[['Order Date', 'Customer Name', 'Sales', 'Profit']].to_dict(orient='records')

    # 7. Advanced AI Forecast (Next 6 Months)
    last_month = df['Order Date'].max()
    future_dates = [last_month + pd.DateOffset(months=i) for i in range(1, 7)]
    base_sales = df['Sales'].mean() * 30
    forecast = []
    for i, date in enumerate(future_dates):
        # Simulate growth + seasonality
        seasonality = 1 + 0.2 * np.sin(2 * np.pi * (date.month / 12))
        growth = 1 + (0.05 * i)
        pred = float(base_sales * growth * seasonality)
        forecast.append({"Month": date.strftime('%Y-%m'), "Predicted_Sales": pred})

    return {
        "trends": trends,
        "categories": cats,
        "omnichannel": omni,
        "inventory": inv_data,
        "rfm": rfm_data,
        "anomalies": anoms,
        "forecast": forecast
    }

class ProductItem(BaseModel):
    order_id: str
    category: str
    sub_category: str
    product_name: str
    sales: float
    profit: float
    quantity: int
    region: str = "East"

@app.post("/api/products/add")
def add_product(item: ProductItem):
    try:
        new_row = {
            'Row ID': 99999, # Dummy ID
            'Order ID': item.order_id,
            'Order Date': datetime.now().strftime('%m/%d/%Y'),
            'Ship Date': datetime.now().strftime('%m/%d/%Y'),
            'Ship Mode': 'Standard Class',
            'Customer ID': 'USR-NEW',
            'Customer Name': 'Dashboard User',
            'Segment': 'Consumer',
            'Country': 'United States',
            'City': 'New York',
            'State': 'New York',
            'Postal Code': 10001,
            'Region': item.region,
            'Product ID': f"NEW-{item.sub_category[:3].upper()}",
            'Category': item.category,
            'Sub-Category': item.sub_category,
            'Product Name': item.product_name,
            'Sales': item.sales,
            'Quantity': item.quantity,
            'Discount': 0,
            'Profit': item.profit
        }
        
        # Append to CSV
        df_new = pd.DataFrame([new_row])
        df_new.to_csv(DATA_PATH, mode='a', header=False, index=False)
        
        return {"status": "success", "message": f"Added {item.product_name} to system."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
