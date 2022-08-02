![Long-term trend and PPI](imgs/janus_green_3.png)
# Introduction 
Janus is a statistical contract pricing model that draws on Coyote's data to forecast the average cost of moving freight on a lane. There are several layers of time-series modeling that work in tandem to produce a forecast: **inflation adjustment**, **long-term price trend modeling**, and **seasonal modeling**. Below is a brief description of Janus’s data sources, each modeling layer, and the model’s load sampling process. Finally, we provide a step-by-step walkthrough of how the model generates a cost forecast for a given lane. 

The model was designed and is maintained primarily by the DataScience team. Contact info: cole.freeman@coyote.com, monica.stettler@coyote.com.

## Data Sources
Janus uses two primary sets of data. First, it consumes Coyote load data from 2010 onward to model long term price trends. This includes 5.9 million loads. Second, Janus uses 4.3 million data points from 2015 onward to model seasonality on lanes. For both load sources, we have only included truckload data for vans. We exclude loads with accessorials or special qualities (hazmat, multi-stops, team loads, drop trailers, etc.) from consideration. Janus models cost-per-mile. Janus updates its long-term trend model on a weekly basis. For recent data, however, data can change; we therefore refresh the last six months to a year of data every day.

## Inflation Adjustment
The first step in preparing data is to adjust costs for inflation. We use the Producer Price Index (PPI) for freight and trucking, which is produced by the U.S. Bureau of Labor Statistics (BLS) ([FRED data here](https://fred.stlouisfed.org/series/PCU484121484121)). A PPI removes cost fluctuations caused by changes in the purchasing power of the US dollar. It is used as a deflator of economic series in economic analysis and forecasting tasks, and it works by translating historical prices into inflation-free dollars. For example, constant-dollar gross domestic product data are estimated using deflators based on PPI data ([BLS PPI FAQ](https://www.bls.gov/ppi/faqs/questions-and-answers.htm#1)). Historical values for the freight and long-haul trucking industry’s PPI is plotted on the right side of the chart below.

![Long-term trend and PPI](imgs/trend_and_ppi.png)

## Long-term Price Trends
Janus takes the inflation-free values from 2010 to today to model the long-term trend of costs for all lanes. The model produced in this step captures two basic patterns: (1) the high-level cycles of inflation and deflation that drive cost variance across all lanes; and (2) the slow linear growth of costs that drive markets upward over time. On the left side of the chart below, we give a picture of how the inflation-free average for CPM fluctuates over the past decade. Actual values are shown with the red line and the values produced by our model are shown in black. The difference between the two lines is filled in light red.

## Seasonal Curves
Janus models seasonality by fitting a curve to the changing average costs across a lane over the course of one year. While there will be variation from year to year, we are interested in capturing average movement from one day to the next. Janus uses weighted averages, where the weight for each load represents its physical proximity to the lane we want a cost forecast for. Seasonality curves are unique to each lane. Below is an example of a seasonal curve from Chicago, IL to Miami, FL where costs drop during the summer months and rise in the winter months. 

![Seasonality curve](imgs/seasonality.png)
## Load Sampling
### Radial expansion
The model currently gathers load cost data based on the city-to-city origin/destination pair. It will pull in loads moved within a configurable radius if the exact city-to-city lane lacks enough data to produce a forecast. For example, if there is not enough price data between Milwaukee and Green Bay, the model can add data from nearby cities within X miles of the lane’s origin and destination. 

### Corridor search
Janus also has the capability to search by corridors. It will first seek city-to-city matches, and only pull in data from the corridor if it has not found enough loads to make a forecast for the lane.

### Hybrid sampling
We can also search out loads through a hybrid method of radial and cluster search. This expands radially within a cluster, and once it reaches those boundaries begins searching outside the cluster radially until a given number of loads are found.

### Donut sampling
This method is related to the radial expansion method, but we give Janus an array of partitions. It will look out in layers, moving first from 0 radius to *n_1* miles out, then from from *n1* miles to *n2* miles out, etc. The effect is searching loads out in donut-like layers.

## Modeling Steps
For each request to produce a cost forecast on a city-to-city lane, Janus takes the following actions:
1.	It samples historical loads, searching for freight moved since January 2015. It records and weights each load by its physical proximity to the searched city origin/destination pair.
2.	The model then separates the data into 12-month periods (one 12-month period represents one season). The costs in each season are transformed into a percent-change value off that period’s average. Janus then averages these percentage-off-average values across all periods in our sample data. The result is a seasonality curve, which gives us a picture of how costs fluctuate over the course of a year on average.
3.	Janus then takes price data from the three most recent months to get a fix on where current costs are for the 12-month season we are currently in. For this step, current cost data is not adjusted for inflation, thus incorporating inflation back into the price prediction. The model uses the least-squares method to fit the recent loads on the seasonality curve produced in Step 2. This estimate represents the average cost for the season we are currently on. 
4.	Next, the model uses our current cost estimate for the 12-month period we are on in conjunction with our long-term price trend model to forecast how prices will vary across future time periods. 
5.	Lastly, Janus makes cost predictions on a per-month basis moving forward across the contract period. It returns an average cost for the contract period, as well as a confidence interval in which we are x% confident the mean lies.

## Backtesting
Janus is capable of performing backtest. When instantiating the class, pass the Janus init method a datetime string (i.e. "2018-09-01) which will be interpreted as the "today" date for the test. Internally, Janus will remove all data after that date and generate a newly fit long-term trend model using only data up to that point. A user can then request Janus to give a forecast, which it will do from that date forward just as it does for forecasts into the future from today's date.

If doing multiple backtests, it is suggested that you reinstantiate Janus for each backtest date. This ensures that you are working with the correct data.

# Getting Started

To run the application locally, we must first set up our Python environment. We can do this in a number of ways. We have the file *env.yml* that contains the necessary packages to run both the data prepare job and launch the API in a Conda environment. We also have *requirements.txt* that can be used with pipenv or other virtual environments to generate a working environment for the project.

If using Conda, open a terminal the project directory on your local machine and make sure you can run Conda commands there. Use the following command to generate the environment:
```
>> conda env create -f env.yml
```

Then we can check that our environment has been properly created:
```
>> conda env list
```

We should see **janus** listed in the active conda environments. We then activate our newly created environment with the following command:
```
>> conda activate janus
```

## Project preparation and data generation
Once your environment is created and activated, and you are on a server that can connect with Coyote's on-prem SQL servers, run the data prepare routine to build the data files needed to launch the application and set up the necessary directories for the API. With the **janus** environment active, run the prepare job with the following command:
```
>> python prepare.py
```
Logging is configured so that we can check on the status of this job and recognize any errors that may come up. The main problem that may arise is with SQL connectivity. We want to make sure that any machine running these jobs is on Coyote's network, and thus has access to our on-prem servers. If the data prepare job runs properly, we should see that the data/ directory has several parquet files. These are used by the Janus model and API to provide cost estimates to client requests.

## Launching the API
Once your data files are ready, you are ready to launch the application. We use uvicorn to host the API. 

```
>> uvicorn src.app.main:app --host 0.0.0.0 --port 8080
```

## Running Unit Tests

First we want to make sure that the shell script that runs our unit tests and coverage report are executable. On a bash shell, run:
```
>> git update-index --chmod=+x tests/unit/run.sh
```
then to execute the unit tests, run:

```
>> sh tests/unit/run.sh
```

## Running the Application in a Docker Container

Login to Azure:
```
>> az login 
```
Then:
```
>> az acr login -n coyoteleftacr
```
Then to build the Docker image, use the following command:
```
>> docker build -t janus -f Dockerfile.baseimage .
```
Then we build the image forthe API:
```
>> docker build -t janusapi -f Dockerfile.api .
```
Next we run our Docker file with the following command:
```
>> docker run -d -p 8080:8080 janusapi
```


OLD Docker commands to run application:
```
>> docker build -t janus .
>> docker run -d -p 5000:5000 janus
```
The first command builds the image of your project. This will be used to build the container itself with the proper environment. The second command launches your (detached) container from the image you've just built, and maps port 5000 on your local machine to port 5000 in the container's directory.

Get the name of your container:
 ```
 >> docker ps
...CONTAINER ID   IMAGE       COMMAND                  CREATED          STATUS         PORTS                    NAMES
...3f1b1e2f1f20   janus   "/bin/sh -c ./entry-…"   10 seconds ago   Up 8 seconds   0.0.0.0:5000->5000/tcp   upbeat_beaver
```
** Note that the name of your image and your container are different. 
Stop running your container:
```
>>> docker stop [container_name]
```
To completely clean your containers and images from the directory:
```
>>> docker system prune -a
```

# CosmosDB Emulator
To start the CosmosDB emulator, use:
```
>> "C:\Program Files\Azure Cosmos DB Emulator\Microsoft.Azure.Cosmos.Emulator.exe" /AllowNetworkAccess /Key=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
```


```
>> docker run -p 8081:8081 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254  -m 3g --cpus=2.0 --name=test-linux-emulator -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 -e AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=true -e AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=172.23.112.1 -it mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
```
# TODO:
- Make sure that we have enough data for the prediction! Sometimes, we may be basing our prediction fit on just a few points, producing unreliable costs.
- Flagship cities per state could be established, and the model run on each one weekly and results recorded. When they are searched, that stored value can be retrieved quickly. When a nearby value is searched, we can use these flagships to set relative prices in the absence of better values (This is a method close to what Kevin Shaw described...his pricing algorithm). We can call it the Shaw method. :) 
- Add in notes from talking to Pricing Team guys
- Check in with Andrew Arbour's big lane table 