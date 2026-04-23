# Retail-Data-Analytics-Project

Omnichannel Retail Sales and Inventory Analytics Dashboard using SQL, Python, and Power BI

# Retail Data Analytics Project

## Overview

This project focuses on cleaning and analyzing retail sales data using SQL Server, with further plans for dashboarding in Power BI.

## Dataset

* Source: Sample Superstore dataset
* Total Rows: ~10,000
* Domain: Retail / Sales

## Data Cleaning Steps

* Checked for NULL values (none found)
* Verified duplicate records (valid multi-product orders)
* Fixed data type issues (converted Sales & Profit from text to FLOAT)
* Validated data consistency

## SQL Business Analysis

Performed SQL-based analysis to extract key business insights:

* Total Revenue and Profit calculation
* Category-wise performance analysis
* Region-wise sales distribution
* Top-performing products identification
* Monthly sales trend analysis
* Identification of loss-making products

## Tools Used

* SQL Server (SSMS)
* GitHub (Version Control)
* Power BI (Upcoming)
* Python (Upcoming)

## Project Structure

* `data/` → Raw dataset
* `sql/` → SQL queries for cleaning & analysis
* `dashboard/` → (Upcoming Power BI dashboards)
* `python/` → (Upcoming analysis)

## Status

✔ Data Cleaning Completed
✔ SQL Analysis Completed
🚀 Dashboarding (Power BI) Next

## Key Learning

* Handling real-world dirty data
* Data type correction in SQL
* Writing structured queries for business analysis

* ## Business Insights

### 1. Overall Performance

The total revenue generated is approximately 2.29 million, with a total profit of around 286K. The business is profitable, maintaining a moderate profit margin of around 12–13%.

### 2. Category Performance

The Technology category is one of the top-performing categories, contributing significantly to overall revenue. This indicates strong demand for technology-related products.

### 3. Top Performing Products

The product "Canon imageCLASS 2200 Advanced Copier" generates exceptionally high revenue (~484K), making it one of the most valuable products in the dataset.

### 4. Revenue Concentration

A small number of products contribute a large portion of total revenue. This suggests a dependency on a few high-performing products, which presents both an opportunity and a risk.

### 5. Product Performance Variation

There is a noticeable variation in product performance. While some products generate high revenue, others contribute significantly less, indicating an imbalance in the product portfolio.

### 6. Business Recommendation

* Focus on promoting top-performing products
* Improve performance of low-revenue products
* Optimize pricing and cost strategies to increase profit margins

