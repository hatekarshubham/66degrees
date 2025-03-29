CREATE OR REPLACE  TABLE `elevated-codex-431815-v2.66degrees.bq_product` (
    product_id INT64 NOT NULL,
    product_line STRING,
    unit_price FLOAT64,
    create_ts TIMESTAMP NOT NULL,
    last_updt_ts TIMESTAMP NOT NULL,
    PRIMARY KEY (product_id) NOT ENFORCED,
);
