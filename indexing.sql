-- Index on the fact_sales_transactions table for metadata_id
CREATE INDEX idx_fact_metadata_id ON master.sales_warehousing.fact_sales_transactions (metadata_id);

-- Index on the fact_sales_transactions table for location_id
CREATE INDEX idx_fact_location_id ON master.sales_warehousing.fact_sales_transactions (location_id);

-- Index on the fact_sales_transactions table for time_id
CREATE INDEX idx_fact_time_id ON master.sales_warehousing.fact_sales_transactions (time_id);

-- Index on the fact_sales_transactions table for customer_id
CREATE INDEX idx_fact_customer_id ON master.sales_warehousing.fact_sales_transactions (customer_id);

-- Index on the dim_metadata_transactions table for transaction_category
CREATE INDEX idx_dim_meta_transaction_category ON master.sales_warehousing.dim_metadata_transactions (transaction_category);

-- Index on the dim_metadata_transactions table for transaction_description
CREATE INDEX idx_dim_meta_transaction_description ON master.sales_warehousing.dim_metadata_transactions (transaction_description);

-- Index on the dim_location table for location_name
CREATE INDEX idx_dim_location_name ON master.sales_warehousing.dim_location (location_name);

-- Index on the dim_time table for year and month
CREATE INDEX idx_dim_time_year_month ON master.sales_warehousing.dim_time (year, month);

-- Index on the dim_customer table for is_known_customer
CREATE INDEX idx_dim_customer_known ON master.sales_warehousing.dim_customer (is_known_customer);
