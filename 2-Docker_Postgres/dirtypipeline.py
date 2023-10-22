## This script loads data with wget, unzips it and ingest it into Our Postgres container
## Command : python dirtypipeline.py --user=root --password=root --host=localhost --port=5432 --db=ny_taxi --table_name=taxi_yellow --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
import pandas as pd
from sqlalchemy import create_engine, text
import argparse
from time import time
import requests
def main(params): 

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = "Taxi_data/Yellow_taxi.csv.gz"
    
    response = requests.get(url)
    with open(csv_name, 'wb') as file:
        file.write(response.content)

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

    t_start = time()
    df = pd.read_csv(csv_name,compression='gzip')
    df = df.head(1000)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df.to_sql(name=table_name, con=engine,index=False, if_exists="replace")
    t_end = time()

    print("Inserted table, took %.3f seconds" % (t_end - t_start))


if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Ingest CSV to PG')

    parser.add_argument("--user", help= 'user name for postgress')
    parser.add_argument("--password", help= 'password for postgress')
    parser.add_argument("--host", help= 'host for postgress')
    parser.add_argument("--port", help= 'port for postgress')
    parser.add_argument("--db", help= 'database name for postgress')
    parser.add_argument("--table_name", help= 'table name for postgress')
    parser.add_argument("--url", help= 'url of the csv file')

    args = parser.parse_args()

    main(args)





