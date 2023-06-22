## Data Engineering Project 2 / NIFTY 50 Stock Market Data

This project will leverage the historical stock data of 50 NIFTY (National Stock Exchange) India. It will help us to see the pattern and can be beneficial to predict the future stock progress. We would analyze the whole stock data individually and also collectively. 

## 1. Description of the Problem:

In the field of investment banking and hedge funds, quantitative analysts (or 'quants') often use historical stock market data to develop complex financial models. These models serve to predict future movements of stock prices and are employed to guide investment strategies.

Suppose a quant at a hedge fund is using the NIFTY 50 stock datasets to build a predictive model for algorithmic trading. The model employs a time-series analysis approach based on historical price trends, trading volumes, and other relevant stock market indicators.

However, in March 2020, the global stock market saw unprecedented volatility due to the outbreak of the COVID-19 pandemic. In real-world situations like these, relying solely on past stock market data for modeling can lead to significant forecasting errors. This is because the historical data in the dataset does not account for unforeseen external shocks like pandemics, geopolitical events, or abrupt regulatory changes.

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/bfa8eaec-3fad-47d4-8c34-1d66ab50996e">


In the context of the NIFTY 50 datasets, for example, the market behaviors during the pandemic period were quite different from historical trends. A trading algorithm relying heavily on past data might make flawed predictions and lead to substantial financial losses for the hedge fund.

Another issue could arise for international investors who use these datasets. The NIFTY 50 data is denominated in Indian Rupees, so fluctuations in exchange rates between the Rupee and other currencies can affect investment returns. If the investor fails to factor in these currency risks while analyzing the datasets, it could lead to inaccurate assessments of potential profits or losses.

These scenarios highlight the importance of supplementing historical data analysis with an understanding of current market conditions, world events, and other relevant factors to make informed and prudent investment decisions.


## 2. Objective:

The datasets containing the price history and trading volumes of the fifty stocks in the NIFTY 50 index from the National Stock Exchange (NSE) India are of great value for a multitude of applications. They can be used by investors, analysts, and economists for financial analysis. This can range from performing time-series analysis to predict future prices, analyzing performance over time, assessing risk, and identifying investment opportunities. Additionally, it serves as an excellent resource for educational purposes, allowing students to understand stock market behavior, volatility, trends, and the impact of market events on prices.

Furthermore, these datasets can be utilized for algorithmic trading, enabling high-frequency traders and algorithm developers to backtest trading strategies, build predictive models, and optimize algorithms. For researchers, the data aids in understanding the impact of economic events on the Indian stock market and how individual stocks correlate with the overall market.

Each stock dataset, split into .csv files, includes fields like date, open, high, low, close, and volume, whereas the metadata file provides information about the stock symbol, industry, listing date, and market cap. Despite its immense utility, the data should be used with an understanding of its limitations, such as it reflects historical market conditions, does not account for corporate actions, external events, exchange rate fluctuations, and regulatory changes, which might impact the stock prices significantly. Finally, it's crucial to use this dataset responsibly and ensure compliance with all applicable laws and regulations.

## 3. Technologies:

The choosen technologies is variative and depends on the case and condition. There are some option for certain case and in this case, I am using this option since it's the easiest.

- Dockerfile
- Docker Compose
- VM GCP
- Airflow / Prefect
- GCS (Google Cloud Storage)
- Bigquery
- Spark
- Google Data Studio

## 4. Data Architecture:
<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/90760468-bdb7-4997-a624-e46f4da061cc">

## 5. Data Description:

The data is the price history and trading volumes of the fifty stocks in the index NIFTY 50 from NSE (National Stock Exchange) India. All datasets are at a day-level with pricing and trading values split across .cvs files for each stock along with a metadata file with some macro-information about the stocks itself. The data spans from 1st January, 2000 to 30th April, 2021.

These data was collected from kaggle : https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data

## 6. Set Up the Environment

You gonna need some tools:

1. Google Cloud Platform
2. Terraform

### 6.1 Google Cloud Platform:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/5424e67f-d94a-45fa-8ab9-ac706aeddfad">

In this chapter, we will set up several things you need to set up your firest google cloud platform accout before ready to be used

1. Create the new project (you can use the old project, if you think it's fine)
2. Set the VM Instances
3. Set the service account and assign the right roles on it
4. Create the new bucket
5. Create the new dataset (optional, due to you can make it along the process)

### 6.2 Terraform:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/2faa8507-d149-4bc5-889d-9381c84f21be">

The terraform will help us to make the stable and organizable environment for our google cloud and it's very easy to monitor since we only use python file to control. You can even share it to other team member if you work in group, so you all can assure using the same environment set up.

1. Set the main.tf
2. Set the variable.tf
3. Run the terraform through some command :
   1. terraform init = initialize the terraform
   2. terraform validate = check and validate that it's proper update
   3. terraform plan = you can see what's the update and what's new in your environment
   4. terraform apply = run and make the update

## 7. Airflow:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/0b299387-a421-49b7-aa4c-97c7816b37a9">

Airflow is a tool to help the data engineer to monitor the ingesting data process. We can create the workflow by our own using python file and we can edit as like as we want. Here are some sets up to run the Airflow:

1. Prepare the Dockerfile (check the environment that will be used for ingesting the data)
2. Prepare the docker-compose.yaml (fill some specific variable based on your personal data)
3. Prepare .env file
4. Prapare the requirements.txt file
5. Open the virtual machine and connect to the host (you can find it on vs code)
6. Set the port (8080), make sure there is no machine using the same port
7. Run the docker-compose build in directory that has docker-compose.yaml and Dockerfile
8. Run the docker-compose up airflow-init to initialize the airflow
9. Run the docker-compose up, wait until all the image has settled
10. Open the search engine (google, bing, etc) and open the web ( localhost:8080 )
11. Wait until the loading ended
12. Sign in the airflow using the password and username that you set before (in docker-compose.yaml)
13. Choose the DAG file that you want to run
14. Trigger the DAG
15. If all task has dark green color (which means succeed), then please check your gcs bucket or bigquery (only if your DAG file has a task sending the file to the bgquery)
16. If there is an error, then click the square task and click log button to see what's the message giving to you the error information
    There are several thing that I ever experienced that cause an error:
    1. Airflow version is too low - Solution = Set the latest version in your Dockerfile and when you run the docker-compose build
    2. DAG issue - Solution = Since it would be very specific, so please check the log to see what's error there
    3. PORT is occupied - Solution : If you're using the docker, then you can find out what's machine that may use that port and you can delete that image in the docker (you can use docker apps or type the command in the git bash)

## 8. Apache Spark

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/0e5461ea-cd71-4472-9707-ba22cf96488b">

Spark is the best tool to handle large dataset and transform it to be useful and clean data. It will be used to download(extract) and will ingest into the google cloud storage bucket or bigquery using dataproc. 

The general idea about what we gonna do in spark:
So basically we wanna try to transfrom all 50+ data to be one file that cover the essential information that we need. We will merge the whole stocks data, which we have identified has the same number and column name. In case, there is an issue (according to name or data type that probably a bit different (in my case, I found one column that supposed to be date and not integer)). Then, there is one file that is additional informatiion of the entire stocks that we will join that as well using .join. After that we gonna partition by years for each company to see the progress of the stock year by year. 

1. Firstly, set the virtual machines using linux or in my case, I am using google cloud VM.
2. Export the python argument to the terminal to init the pyspark, so it can be connected to the jupyter notebook eventually.
3. Open jupyter notebook and create the new folder.
4. Set the connection into the google cloud platform
5. Import the pyspark and any package you need
6. Create the spark variable using SparkSession.builder
7. Read the file using spark.read
8. Check the schema using .schema or printSchema()
9. Edit the schema if needed to decrease the number of storage and fasthen the sending process
10. Add and renamed the column if you think it will be benefitial
11. Do the join if you need
12. Input registerTempTable("file-nname")
13. Using spark.sql to use the SQL command to your file
14. Send to the bigquery afterwards
15. Convert it to the pyhton script
16. Using argparse package to receive the variable from our python command which will be inserted into our terminal
17. Set up the cluster and run the job
18. If succeed, please check the bigquery to make sure.
19. Your work has done

## 9. Google Data Studio:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/5e3bd7a1-eee6-43a8-8912-985be393722e">

It's pretty simple, you can connect your bigquery with google data studio and use the created table to be visualized. Build your dasboard which with the hope, it can answer all the problem solving question clearly.

These are my dashboard:

<img width="725" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/9f39fa24-adfc-43e8-9c3c-2bda5d5d8006">
<img width="720" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/15c07694-dfa6-497d-b841-104f7ac13a28">


From this two data visualization, we could get many information:
1. The most expensive stocks since 2000 - 2021
2. The progress of stock indicator in every year
3. The industrial category that going up and down in different era
4. Analyze why certain stock was booming and others was not
5. Find the pattern of similar situation that can use to predict the future stocks
6. etc



## Reference Link:

https://w0.peakpx.com/wallpaper/252/11/HD-wallpaper-stock-market-perfect-line-chart-representation-chart-pattern-thumbnail.jpg
