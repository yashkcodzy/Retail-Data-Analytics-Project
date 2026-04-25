-- DATABASE 
-- 
CREATE DATABASE omni_channel_db;

-- VIEW DATA

SELECT * 
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- 
-- DATA TYPE FIX
-- 
ALTER TABLE [dbo].[DA Project-1 dataset (Omni Channel)]
ALTER COLUMN Sales FLOAT;

ALTER TABLE [dbo].[DA Project-1 dataset (Omni Channel)]
ALTER COLUMN Profit FLOAT;

-- BASIC METRICS

-- Total Orders
SELECT COUNT(DISTINCT Order_ID) AS total_orders
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- Total Revenue
SELECT SUM(Sales) AS total_revenue
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- Total Profit
SELECT SUM(Profit) AS total_profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- Average Order Value
SELECT 
    SUM(Sales) / COUNT(DISTINCT Order_ID) AS avg_order_value
FROM [dbo].[DA Project-1 dataset (Omni Channel)];


-- CATEGORY ANALYSIS

SELECT 
    Category,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Category
ORDER BY revenue DESC;

-- SUB-CATEGORY ANALYSIS

SELECT 
    Sub_Category,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Sub_Category
ORDER BY revenue DESC;


-- GEOGRAPHIC ANALYSIS

SELECT 
    Region,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Region
ORDER BY revenue DESC;


-- TIME-BASED ANALYSIS 

SELECT 
    FORMAT(Order_Date, 'yyyy-MM') AS month,
    SUM(Sales) AS revenue
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY FORMAT(Order_Date, 'yyyy-MM')
ORDER BY month;


-- DISCOUNT IMPACT 

SELECT 
    Discount,
    COUNT(*) AS total_orders,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Discount
ORDER BY Discount;


-- PROFIT MARGIN 

SELECT 
    Category,
    SUM(Profit) / NULLIF(SUM(Sales), 0) * 100 AS profit_margin_percent
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Category
ORDER BY profit_margin_percent DESC;


-- CHANNEL ANALYSIS

SELECT 
    Ship_Mode,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Ship_Mode
ORDER BY revenue DESC;


-- SEGMENT ANALYSIS 

SELECT 
    Segment,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Segment
ORDER BY revenue DESC;
