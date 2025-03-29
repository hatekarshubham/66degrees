 create or replace view  `elevated-codex-431815-v2.66degrees.bq_supermarket_sales_report`
 as
 select
    fact.invoice_id ,
    fact.branch ,
    fact.city ,
    fact.customer_id ,
    coalesce(cust.customer_type,"NOT/AVAIL") customer_type,
    coalesce(cust.gender,"NOT/AVAIL") gender,
    coalesce(cust.rating,-1.0) rating,
    fact.product_id ,
    coalesce(prdt.product_line,"NOT/AVAIL") product_line,
    coalesce(prdt.unit_price,-1.0) unit_price,
    fact.quantity ,
    fact.tax ,
    fact.total ,
    fact.date ,
    fact.time ,
    fact.payment ,
    fact.cogs ,
    fact.gross_margin_percentage ,
    fact.gross_income ,
current_timestamp() create_ts  ,
current_timestamp() last_updt_ts
from `elevated-codex-431815-v2.66degrees.bq_supermarket_sales_fact` fact
left outer join
`elevated-codex-431815-v2.66degrees.bq_customer` cust
on fact.customer_id = cust.customer_id
left outer join
`elevated-codex-431815-v2.66degrees.bq_product` prdt
on fact.product_id = prdt.product_id;