Rapidly build tabular datasets in the following formats:
- SQL Tables (Generate code for SQL CREATE and INSERT queries)
- CSV 
- JSON

Supports: PostgreSQL, MySQL, MS SQL, SQLite

Input parameters:
- **table_name**  - This is the name of the table to be created
- **num_rows** - The number of rows to insert into the table
- **column_defs** - A dictionary object with key value pairs.
- **path** - The path to the directory and file name where you want to export the sql
queries or dataset for the specified format.

**column_defs** is a dictionary object of the form:
```
{column_name: {"col_type": type, ...}}
```
The definitions of the parameters for **colum_defs** is given below.

- col_type: int, float, varchar, bool
- varchar_length: int (required for MySQL and MS SQL)
- is_primary_key: bool - True if this field is the primary key
- is_name: bool - True if values for this column should come from the names collection
- is_email: bool - True if this column is an email. Note that you must have at least one column with is_name = True 
to use is_email.
- is_date: bool - True if this column is a date. Default format is YYYY-mm-dd
- is_timestamp: bool - True if this column is a timestamp. Default format is YYYY-mm-dd HH:MM:SS
- is_country: bool - True of this column is a country code. Codes are ISO Alpha-2.
- is_state: bool - True if this column is a US state abbreviation. 
- is_address: bool - True if this column is a street address.
- bounds: tuple(lowerbnd, upperbnd) - Forces lowerbnd <= column values <= upperbnd
- fixed_collection: tuple(elem1, elem2, ..., elemn) - Forces column values to be elements of this tuple
- fixed_map: tuple(column_name, {key: value}) - Forces values for this column to be associated to the value of another 
column
- is_nullable: bool - True if this column can have null values
- proportion_null: float - The approximate proportion of expected null values in this column. Note that is_nullable 
must be true to use proportion_null

Note that using is_primary_key assumes the column you're defining is an integer
based column starting at 1.

If you're planning on running queries on a MySQL or MS SQL Server machine then you
need to specify the length of each varchar field using the varchar_length parameter.

In this example we're generating SQL code to create a table which tracks orders placed for
an imaginary online store. We'll create a table with the following columns:
- id - the primary key for this table
- name - the name associated to the user who placed this order
- order_ts - the timestamp associated with this order
- product_id - the id for the product ordered
- price - the cost of the product being ordered. Since we want every row with a given product_id to have the same cost we 
use a fixed map to implement this column 

```
from datamaker.SQLTableGenerator import SQLTableGen


table_name = "Example"
num_rows = 500
column_defs = {
    "id": {"col_type": "int", "is_primary_key": True},
    "name": {"col_type": "varchar", "is_name": True},
    "order_ts": {"col_type": "varchar", "is_timestamp": True},
    "product_id": {"col_type": "int", "bounds": (1, 5)},
    "price": {"col_type": "float", "fixed_map": ("product_id", {1: 5.99, 2: 10.99, 3: 0.99, 4: 99.99, 5: 20})},
}
output_path = "example.sql"

gen = SQLTableGen(table_name, num_rows, column_defs, output_path)

gen.build_sql_doc()
```

Future improvements:
- Add support for sequential fields
