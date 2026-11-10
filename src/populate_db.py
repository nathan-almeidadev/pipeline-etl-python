from db import DB
import pandas as pd
import os

db = DB(host="localhost", port=5432, database='db_etl_viacep', user='postgres', password='viacep_etl')

for file in os.listdir("./data/02-silver_validated"):
    df = pd.read_parquet(f'./data/02-silver_validated/{file}')

    db.create_table(
        file.replace(".parquet", ""), 
        df.columns.tolist()
    )

    db.insert_data(
        file.replace(".parquet", ""),
        df
    )

db.close()