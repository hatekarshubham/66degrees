CREATE OR REPLACE  TABLE `elevated-codex-431815-v2.66degrees.bq_customer` (
    customer_id INT64 NOT NULL,
    customer_type STRING,
    gender STRING,
    rating FLOAT64,
    create_ts TIMESTAMP NOT NULL,
    last_updt_ts TIMESTAMP NOT NULL,
    PRIMARY KEY (customer_id) NOT ENFORCED,
);
