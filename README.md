Retail-Data-Analytics-Project
Omnichannel Retail Sales and Inventory Analytics Dashboard using SQL, Python, and Power BI

Retail-Data-Analytics-Project
Omnichannel Retail Sales and Inventory Analytics Dashboard using SQL, Python, and Power BI

Overview
This project focuses on cleaning and analyzing retail sales data using SQL Server, followed by building an interactive dashboard in Power BI to derive business insights.

Dataset
Source: Cleaned Omni-channel Retail Dataset
Total Orders: ~5000+
Domain: Retail / Sales
Data Cleaning Steps
Checked for NULL values
Verified duplicate records
Fixed data type issues (converted Sales & Profit from text to FLOAT in SQL)
Validated data consistency after import
SQL Business Analysis
Performed SQL-based analysis to extract key business insights:

Total Orders, Revenue, and Profit calculation
Average Order Value (AOV)
Category and Sub-Category analysis
Geographic (Region-wise) performance
Time-based sales trends
Discount impact on revenue and profit
Profit margin analysis
Channel (Ship Mode) performance analysis
Tools Used
SQL Server (SSMS)
GitHub (Version Control)
Power BI (In Progress)
Python (Optional)
Project Structure
data/ → Raw & cleaned datasets
sql/ → SQL queries (cleaning + analysis)
dashboard/ → Power BI dashboards
python/ → (Optional analysis)
Status
✔ Data Cleaning Completed ✔ SQL Analysis Completed 🚀 Power BI Dashboard In Progress

Key Learning
Handling real-world data issues during SQL import
Data type conversion and debugging in SQL
Writing analytical SQL queries for business insights
Translating raw data into meaningful insights
Business Insights
1. Overall Performance (Based on overall aggregation)
The total revenue generated is approximately 2.29 million, with a total profit of around 286K from 5009 orders. The business maintains a healthy profit margin of approximately 17%, indicating efficient operations and stable profitability.

2. Customer Behavior (Based on Average Order Value analysis)
The average order value is approximately 458, indicating moderate customer spending per order. This suggests an opportunity to increase revenue by improving basket size through cross-selling and upselling strategies.

3. Category Performance (Based on category-wise analysis)
The Technology category generates revenue of approximately 501K, making it one of the top-performing categories. This indicates strong customer demand for technology-related products and highlights it as a key revenue driver.

4. Top Product Contribution (Based on product-level revenue analysis)
The product Canon imageCLASS 2200 Advanced Copier generates revenue of approximately 484K, making it one of the highest contributing products. This indicates a strong dependency on specific high-value products.

5. High Revenue Concentration (Based on revenue distribution analysis)
A significant portion of revenue is concentrated among a few key contributors, with values such as 835K, 706K, 678K, and 484K. This indicates that a small number of segments/products contribute heavily to total revenue, following a Pareto-like distribution.

6. Sub-Category / Segment Variation (Based on revenue spread)
Revenue values such as 223K, 206K, and 94K indicate variation in performance across different sub-categories or segments. This highlights an imbalance where some segments perform significantly better than others.

7. Profitability Analysis (Based on profit margin calculation)
The overall profit margin is approximately 17.03%, indicating efficient pricing and cost management. However, further optimization in low-performing areas can improve profitability.

8. Business Risk Insight (Based on revenue dependency)
The high dependency on a few high-performing products or segments presents a potential risk. If these key contributors underperform, it could significantly impact overall business performance.

9. Business Recommendations
Focus on expanding high-performing categories like Technology
Reduce dependency on a few top products by diversifying revenue streams
Improve performance of low-revenue segments
Optimize pricing and discount strategies to further enhance profit margins
Increase average order value through bundling and targeted promotions
