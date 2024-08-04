from sqlalchemy import create_engine, text

DATABASE_URL = 'mysql+pymysql://root:Manny5810@localhost:3306/APIProject'

engine = create_engine(DATABASE_URL)

# SQL command to drop the tables
drop_tables_sql = """
DROP TABLE IF EXISTS pricing_strategies, customer_segments, customers, customer_profiles, activities, sales_transactions, competitor_pricing, market_trends, products;
"""

with engine.connect() as connection:
    connection.execute(text(drop_tables_sql))

print("Tables dropped successfully.")
