LOAD DATA OVERWRITE hatvalues-sandbox.jaffle_shop.customers
  (
    ID INT64,
    FIRST_NAME STRING,
    LAST_NAME STRING
  )
  CLUSTER BY ID
  OPTIONS(
    description="customer sample table"
  )
  FROM FILES(
    skip_leading_rows=1,
    format='CSV',
    uris = ['gs://hatvalues-dbt-store/bq-load/customers.csv']
  );

LOAD DATA OVERWRITE hatvalues-sandbox.jaffle_shop.orders
  (
    ID INT64,
    USER_ID INT64,
    ORDER_DATE DATE,
    STATUS STRING,
    _etl_loaded_at DATETIME
  )
  CLUSTER BY ID
  OPTIONS(
    description="order sample table"
  )
  FROM FILES(
    skip_leading_rows=1,
    format='CSV',
    uris = ['gs://hatvalues-dbt-store/bq-load/orders.csv']
  );

LOAD DATA OVERWRITE hatvalues-sandbox.stripe.payments
  (
  id INT64,
  orderid INT64,
  paymentmethod STRING,
  status STRING,
  amount INT64,
  created DATE,
  _batched_at DATETIME
  )
  CLUSTER BY id
  OPTIONS(
    description="payments sample table"
  )
  FROM FILES(
    skip_leading_rows=1,
    format='CSV',
    uris = ['gs://hatvalues-dbt-store/bq-load/payments.csv']
  );