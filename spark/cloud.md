gcloud dataproc jobs submit pyspark \
 --cluster=cluster-eb63 \
 --region=us-central1 \
 --jars=gs://newbucketaja/spark-3.3-bigquery-0.31.1.jar \
 gs://myproject1-delay-airline/stock_dataprocFile.py \
 -- \
 --source_dir=gs://myproject1-delay-airline/nifty50-stock-market-data/ \
 --output=project2_data.yearly_stock
