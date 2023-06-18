## Data Engineering Project 2 / NIFTY 50 Stock Market Data

This project will leverage the historical stock data of 50 NIFTY (National Stock Exchange) India. It will help us to see the pattern and can be beneficial to predict the future stock progress. We would analyze the whole stock data individually and also collectively. 

## 1. Description of the Problem:

In the field of investment banking and hedge funds, quantitative analysts (or 'quants') often use historical stock market data to develop complex financial models. These models serve to predict future movements of stock prices and are employed to guide investment strategies.

Suppose a quant at a hedge fund is using the NIFTY 50 stock datasets to build a predictive model for algorithmic trading. The model employs a time-series analysis approach based on historical price trends, trading volumes, and other relevant stock market indicators.

However, in March 2020, the global stock market saw unprecedented volatility due to the outbreak of the COVID-19 pandemic. In real-world situations like these, relying solely on past stock market data for modeling can lead to significant forecasting errors. This is because the historical data in the dataset does not account for unforeseen external shocks like pandemics, geopolitical events, or abrupt regulatory changes.

![image](https://github.com/Irf4n-Muhammad/Data-Engineering-Project_NIFTY-50-Stock-Market-Data/assets/121205860/bfa8eaec-3fad-47d4-8c34-1d66ab50996e)

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
<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/6f76020a-5b27-4935-9878-af6bd7d388b3">


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

## 8. DBT:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/6104b129-366d-47c2-a3cb-7cda8357ac34">

DBT is the tool that you can transform your data using sql command. It's very simple and you can even create the documentation to track the history of the process and the dependencies of each files. To use DBT, you have two option to run it, either using local database or using dbt cloud. Each of them have their own benefits, but I suggest you to use dbt local since it's free.

Here's the way to set up the DBT:

1. Create the dictionary and clone your github repo
2. Run the dbt install ( pip install dbt-bigquery ), you can change the bigquery with other tools, for more information check the dbt website
3. Set the profiles.yaml to set the information you need for initialization
4. Run ( dbt init ) to initialize
5. Run ( dbt debug ) to check if it's successful
6. Try to run the dbt ( dbt run ), make sure in the same directory where dbt_projects.yaml exist
7. In the model folder, create new dir (staging) and (core)
8. In the staging dir, create new file (schema.yaml and <your-file.sql>)
9. Write your database in the schema.yaml and create the model in your-file.sql
10. Use macros if you need to create function
11. Set the packages if you need that and run ( dbt deps )
12. Run the file using ( dbt run ) and check your bigquery table and see if the table has created

## 9. Google Data Studio:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/5e3bd7a1-eee6-43a8-8912-985be393722e">

It's pretty simple, you can connect your bigquery with google data studio and use the created table to be visualized. Build your dasboard which with the hope, it can answer all the problem solving question clearly.

These are my dashboard:

<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/82b1b5ae-6632-4b11-ae01-bda45ccc8df2">
<img width="700" alt="image" src="https://github.com/Irf4n-Muhammad/Data-Engineering-Project_COVID19-Dataset/assets/121205860/2a61fa8c-7de7-4759-80a5-0c16b90a785a">

From this two data visualization, we could answer our question:

#### 1. What's country has the most confirmed COVID-19 patient?

Answer: (Graph 1) America, with 27.1% confirmed COVID-19 patient in the world are from America.

#### 2. What's the death probability of the COVID-19 patient?

Answer: (Graph 1) We could see from the graph, the increase of the death and confirmed patient has the same pattern. So we could calculate it to be:
Death Ratio = Total death / Confirmed patient x 100 = 43.384.904 / 828.508.482 x 100 = 5.236 %

#### So the death probability of COVID-19 patient is 5.236 %

#### 3. What's region(continent) has the least number of COVID-19 patient?

Answer: (Graph 1) From the map, we could say Africa and Australia has smaller number compared to other continents. However, We still has shortage of data to get the reason why.

#### 4. What are factor that impact the spread of COVID-19 virus?

Answer: (Graph 2) The graph shows us the ratio of the covid-19 patient by the whole population is generally has higher position for small population country. It means that most of the people in small country has higher probability to get infected rather than the big country, even though the number of patients is still less than big country.

#### 5. What's country has the highes probability of getting infected by COVID-19?

Answer: (Graph 2) Qatar position in the first place with 4% probability. It's pretty high comparing to other countries, which the second position only have 2% probability.

Those are the question we can answer from our graph. However, there are so many information we haven't answered yet, so you can dig more information from that graph by yourself.

## Reference Link:

https://w0.peakpx.com/wallpaper/252/11/HD-wallpaper-stock-market-perfect-line-chart-representation-chart-pattern-thumbnail.jpg
