from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from pyspark.sql.types import StructType, StructField, StringType, DateType, IntegerType, FloatType

import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

credentials_location = '/home/irfankey/.google/credentials/google_credentials.json'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
    
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
    
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

# Schema for the data
schema = StructType([
    StructField("Date", StringType(), True),  # Temporarily read "Date" as StringType
    StructField("Symbol", StringType(), True),
    StructField("Series", StringType(), True),
    StructField("Prev_Close", FloatType(), True),
    StructField("Open", FloatType(), True),
    StructField("High", FloatType(), True),
    StructField("Low", FloatType(), True),
    StructField("Last", FloatType(), True),
    StructField("Close", FloatType(), True),
    StructField("VWAP", FloatType(), True),
    StructField("Volume", IntegerType(), True),
    StructField("Turnover", FloatType(), True),
    StructField("Trades", FloatType(), True),
    StructField("Deliverable_Volume", FloatType(), True),
    StructField("_Deliverable", FloatType(), True)
])

df_parquet = spark.read \
            .option("header", "true") \
            .schema(schema) \
            .parquet('gs://myproject1-delay-airline/nifty50-stock-market-data/INFRATEL.parquet')

# Convert the "Date" column to the correct type
df_parquet = df_parquet.withColumn("Date", to_date(col("Date"), "your_date_format"))

df_parquet.write.parquet('gs://myproject1-delay-airline/nifty50-stock-market-data/INFRATEL_converted.parquet')
