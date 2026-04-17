CREATE DATABASE superstore_db;        ---- created database

----view data
select top 10 * from [dbo].[Sample - Superstore];       

---view categories
select category
from [dbo].[Sample - Superstore];                    

-- clean view
select distinct category
from [dbo].[Sample - Superstore];

-- null check
SELECT *
FROM [dbo].[Sample - Superstore]
WHERE Sales IS NULL 
   OR Profit IS NULL 
   OR Order_Date IS NULL;

-- null count
SELECT 
    COUNT(*) AS total_rows,
    COUNT(Sales) AS sales_not_null,
    COUNT(Profit) AS profit_not_null
FROM [dbo].[Sample - Superstore];

-- duplicate check
SELECT Order_ID, COUNT(*) AS count_orders
FROM [dbo].[Sample - Superstore]
GROUP BY Order_ID
HAVING COUNT(*) > 1;


-- datatype issue check
SELECT TOP 10 Order_Date, Ship_Date
FROM [dbo].[Sample - Superstore];

-- get output as float (datatype is varchar already we have to change it)
SELECT *
FROM [dbo].[Sample - Superstore]
WHERE TRY_CAST(Sales AS FLOAT) < 0 
   OR TRY_CAST(Profit AS FLOAT) < 0;


-- check negative values
SELECT *
FROM [dbo].[Sample - Superstore]
WHERE TRY_CAST(Sales AS FLOAT) < 0;


-- will check which row has problem
SELECT *
FROM [dbo].[Sample - Superstore]
WHERE TRY_CAST(Sales AS FLOAT) IS NULL
   OR TRY_CAST(Profit AS FLOAT) IS NULL;

-- column datatype change
ALTER TABLE [dbo].[Sample - Superstore]
ALTER COLUMN Sales FLOAT;

ALTER TABLE [dbo].[Sample - Superstore]
ALTER COLUMN Profit FLOAT;