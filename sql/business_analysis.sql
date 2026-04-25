--Total Revenue

SELECT SUM(Sales) AS total_revenue
FROM [dbo].[Sample - Superstore];

--Total Profit

SELECT SUM(Profit) AS total_profit
FROM [dbo].[Sample - Superstore];

--Category Wise Performance

SELECT Category,
       SUM(Sales) AS revenue,
       SUM(Profit) AS profit
FROM [dbo].[Sample - Superstore]
GROUP BY Category
ORDER BY revenue DESC;


--Region Analysis

SELECT Region,
       SUM(Sales) AS revenue,
       SUM(Profit) AS profit
FROM [dbo].[Sample - Superstore]
GROUP BY Region
ORDER BY revenue DESC;


-- Top 10 Products

SELECT TOP 10 Product_Name,
       SUM(Sales) AS revenue
FROM [dbo].[Sample - Superstore]
GROUP BY Product_Name
ORDER BY revenue DESC;


-- Time Analysis

SELECT YEAR(Order_Date) AS year,
       SUM(Sales) AS revenue
FROM [dbo].[Sample - Superstore]
GROUP BY YEAR(Order_Date)
ORDER BY year;


-- SUB-CATEGORY ANALYSIS

SELECT Sub_Category,
       SUM(Sales) AS revenue
FROM [dbo].[Sample - Superstore]
GROUP BY Sub_Category
ORDER BY revenue DESC;


-- LOSS MAKING PRODUCTS

SELECT Product_Name,
       SUM(Profit) AS total_profit
FROM [dbo].[Sample - Superstore]
GROUP BY Product_Name
HAVING SUM(Profit) < 0
ORDER BY total_profit;


-- SEGMENT ANALYSIS

SELECT Segment,
       SUM(Sales) AS revenue
FROM [dbo].[Sample - Superstore]
GROUP BY Segment;


-- MONTHLY TREND

SELECT 
    MONTH(Order_Date) AS month,
    SUM(Sales) AS revenue
FROM [dbo].[Sample - Superstore]
GROUP BY MONTH(Order_Date)
ORDER BY month;

-- 

create database omni_channel_db;
select * from [dbo].[DA Project-1 dataset (Omni Channel)];

-- change datatype from nvarchar to float
ALTER TABLE [dbo].[DA Project-1 dataset (Omni Channel)]
ALTER COLUMN Sales FLOAT;

ALTER TABLE [dbo].[DA Project-1 dataset (Omni Channel)]
ALTER COLUMN Profit FLOAT;

--Total orders
SELECT COUNT(DISTINCT Order_ID) AS total_orders
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- tota revenue
SELECT SUM(Sales) AS total_revenue
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- total profit
SELECT SUM(Profit) AS total_profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

-- average order value
SELECT 
    SUM(Sales) / COUNT(DISTINCT Order_ID) AS avg_order_value
FROM [dbo].[DA Project-1 dataset (Omni Channel)];

--category analysis
SELECT 
    Category,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Category
ORDER BY revenue DESC;

-- sub category analysis
SELECT 
    Sub_Category,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Sub_Category
ORDER BY revenue DESC;

-- gographical analysis
SELECT 
    Region,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Region
ORDER BY revenue DESC;

--time bases analysis 
SELECT 
    YEAR(Order_Date) AS order_year,
    SUM(Sales) AS revenue
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY YEAR(Order_Date)
ORDER BY order_year;

-- discount impact
SELECT 
    Discount,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Discount
ORDER BY Discount;

--profit margin by category
SELECT 
    Category,
    SUM(Profit) / SUM(Sales) * 100 AS profit_margin_percent
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Category
ORDER BY profit_margin_percent DESC;

-- channel analysis
SELECT 
    Ship_Mode,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM [dbo].[DA Project-1 dataset (Omni Channel)]
GROUP BY Ship_Mode
ORDER BY revenue DESC;



-- 
