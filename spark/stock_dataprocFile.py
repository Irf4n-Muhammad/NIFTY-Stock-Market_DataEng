#!/usr/bin/env python
# coding: utf-8

import argparse
from pyspark.sql import SparkSession
from google.cloud import storage

parser = argparse.ArgumentParser()

parser.add_argument('--source_dir', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

source_dir = args.source_dir
output = args.output

spark = SparkSession.builder \
        .master('local[*]') \
        .appName('test') \
        .getOrCreate()
print("First step workin")

spark.conf.set('temporaryGcsBucket', 'dataproc-staging-us-central1-766808300065-xikpviop')

# Connect to GCS
client = storage.Client()

# Assuming the format of source_dir is 'gs://bucket/path/'
bucket_name, prefix = source_dir[5:].split('/', 1)
bucket = client.get_bucket(bucket_name)

print("Second step workin")

# List all files in the source directory
blobs = bucket.list_blobs(prefix=prefix)
first_run = True
stock_metadata = None

print("Third step workin")

for blob in blobs:
    if blob.name.endswith('.parquet'):
        print(f"{blob.name} is working now")
        df_stock = spark.read.parquet(f'gs://{bucket_name}/{blob.name}')
        if 'stock_metadata.parquet' in blob.name:
            df_stock = df_stock.withColumnRenamed("Company Name", "CompanyName")
            df_stock = df_stock.withColumnRenamed("ISIN Code", "ISINCode")
            stock_metadata = df_stock
        elif first_run:
            df_stock = df_stock.withColumnRenamed("Prev Close", "PrevClose")
            df_stock = df_stock.withColumnRenamed("Deliverable Volume", "DeliverableVolume")
            df_stock = df_stock.withColumnRenamed("%Deliverable", "PercentDeliverable")
            stock_col = df_stock
            first_run = False
        else:
            # Before union, ensure the column is renamed in stock_col as well
            stock_col = stock_col.withColumnRenamed("ISIN Code", "ISINCode")
            stock_col = stock_col.withColumnRenamed("Prev Close", "PrevClose")
            stock_col = stock_col.withColumnRenamed("Deliverable Volume", "DeliverableVolume")
            stock_col = stock_col.withColumnRenamed("%Deliverble", "PercentDeliverable")
            stock_col = stock_col.withColumnRenamed("Company Name", "CompanyName")
            stock_col = stock_col.union(df_stock)
        print(f"{blob.name} was done")

stock_col.printSchema()
stock_metadata.printSchema()
# Union with stock_metadata
# Union with stock_metadata
if stock_metadata is not None:
    stock_col = stock_col.join(stock_metadata, stock_col.Symbol == stock_metadata.Symbol)

# Drop duplicate Symbol column
stock_col = stock_col.drop(stock_metadata.Symbol)
stock_col = stock_col.drop(stock_metadata.Series)

stock_col.printSchema()

print("metadata was done")

stock_col.createOrReplaceTempView('stock_table')

final_result = spark.sql("""
WITH stock_sql_year AS (
    SELECT *,
        row_number() over(PARTITION BY `Symbol` ORDER BY `Date`) AS Row_number,
        YEAR(`Date`) AS Year
    FROM stock_table
)


SELECT 
    Row_number,
    Year,
    CAST(`Symbol` AS STRING) AS Symbol,
    CAST(`CompanyName` AS STRING) AS CompanyName,
    CAST(`Industry` AS STRING) AS Industry,
    CAST(`ISINCode` AS STRING) AS ISINCode,
    CAST(`Series` AS STRING) AS Series,
    CAST(`PrevClose` AS FLOAT) AS PrevClose,
    CAST(`Open` AS FLOAT) AS Open,
    CAST(`High` AS FLOAT) AS High,
    CAST(`Low` AS FLOAT) AS Low,
    CAST(`Last` AS FLOAT) AS Last,
    CAST(`Close` AS FLOAT) AS Close,
    CAST(`VWAP` AS FLOAT) AS VWAP,
    CAST(`Volume` AS INT) AS Volume,
    CAST(`Turnover` AS FLOAT) AS Turnover,
    CAST(`Trades` AS FLOAT) AS Trades,
    CAST(`DeliverableVolume` AS FLOAT) AS DeliverableVolume,
    CAST(`PercentDeliverable` AS FLOAT) AS PercentDeliverable
FROM stock_sql_year
""")

print("Printing final_result schema:")
final_result.printSchema()

print("it's almost done")

final_result.write.format('bigquery') \
        .option('table', output) \
        .save()


