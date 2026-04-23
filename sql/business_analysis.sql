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