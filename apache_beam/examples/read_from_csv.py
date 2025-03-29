import apache_beam as beam
import sqlite3
import uuid

# Input CSV file
input_file = '../Input_files/supermarket_sales.csv'

# Define column lists for different tables
cols_customer = ['customer_id', 'customer_type', 'gender', 'rating']
cols_product = ['product_id', 'product_line', 'unit_price']
cols_sales_fact = [
    'invoice_id', 'customer_id', 'product_id', 'branch_cd', 'city', 'quantity', 'date', 'time', 'payment',
    'cogs', 'tax', 'total', 'gross_income', 'gross_margin'
]

# SQLite database and table names
db_file = "../db/supermarketsalesDB"
table_product = "product"
table_customer = "customer"
table_fact = "sales_fact"

class WriteToSQLite(beam.DoFn):
    """Apache Beam DoFn to write data into SQLite tables."""
    def setup(self):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    
    def process(self, element, table_name):
        """Insert a dictionary element into the specified SQLite table."""
        columns = ', '.join(element.keys())
        placeholders = ', '.join(['?'] * len(element))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, tuple(element.values()))
            self.conn.commit()
            print(str(element)+f" added succesfully in table {table_name}")
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
    
    def teardown(self):
        self.conn.close()

class SplitColumns(beam.DoFn):
    """Apache Beam DoFn to split the input data into three separate tables."""
    def process(self, element, *args, **kwargs):
        element_dict = element._asdict()
        
        # Generate UUIDs for missing customer and product IDs
        # product_uuid = str(uuid.uuid4())
        # customer_uuid = str(uuid.uuid4())
        product_uuid = int(abs(hash(str(uuid.uuid4())))%10**10)
        customer_uuid = int(abs(hash(str(uuid.uuid4())))%10**10)
        
        # Yield transformed records for the customer table
        yield beam.pvalue.TaggedOutput(
            "cols_customer", 
            {col: element_dict.get(col, customer_uuid) if col == "customer_id" else element_dict.get(col) for col in cols_customer}
        )

        # Yield transformed records for the product table
        yield beam.pvalue.TaggedOutput(
            "cols_product", 
            {col: element_dict.get(col, product_uuid) if col == "product_id" else element_dict.get(col) for col in cols_product}
        )

        # Yield transformed records for the sales fact table
        yield beam.pvalue.TaggedOutput(
            "cols_sales_fact",
            {
                col: (
                    customer_uuid if col == "customer_id" and not element_dict.get(col) else
                    product_uuid if col == "product_id" and not element_dict.get(col) else
                    element_dict.get(col)
                ) for col in cols_sales_fact
            }
        )

# Apache Beam pipeline
with beam.Pipeline() as pipeline:
    content = (
        pipeline
        | 'Read CSV file' >> beam.io.ReadFromCsv(input_file)
        | 'Split columns' >> beam.ParDo(SplitColumns()).with_outputs("cols_customer", "cols_product", "cols_sales_fact")
    )

    # Extract individual PCollections
    pcollection_customer = content['cols_customer']
    pcollection_product = content['cols_product']
    pcollection_sales_fact = content['cols_sales_fact']

    # Write data to respective SQLite tables
    pcollection_customer | 'Write to SQLite (Customer)' >> beam.ParDo(WriteToSQLite(), table_name=table_customer)
    pcollection_product | 'Write to SQLite (Product)' >> beam.ParDo(WriteToSQLite(), table_name=table_product)
    pcollection_sales_fact | 'Write to SQLite (Sales Fact)' >> beam.ParDo(WriteToSQLite(), table_name=table_fact)
