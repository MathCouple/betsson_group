
-- Base scenarios to categories X 
SELECT
    m.transaction_category,
    m.transaction_description,
    SUM(f.quantity) AS total_sales_quantity,
    SUM(f.quantity * f.price) AS total_sales_revenue
FROM master.sales_warehousing.fact_sales_transactions f
JOIN master.sales_warehousing.dim_metadata_transactions m
    ON f.metadata_id = m.metadata_id
GROUP BY m.transaction_category, m.transaction_description
ORDER BY total_sales_revenue DESC;

