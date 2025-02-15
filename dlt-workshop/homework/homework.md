# **Workshop "Data Ingestion with dlt": Homework**

## **Question 1: dlt Version**

1. **Install dlt**:

```
!pip install dlt[duckdb]
```

2. **Check** the version:

```
!dlt --version
```

> Answer

- dlt 1.6.1

## **Question 2: Define & Run the Pipeline (NYC Taxi API)**

Use dlt to extract all pages of data from the API.

Steps:

1️⃣ Use the `@dlt.resource` decorator to define the API source.

2️⃣ Implement automatic pagination using dlt's built-in REST client.

3️⃣ Load the extracted data into DuckDB for querying.

```py
import dlt
import duckdb
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(base_page=1, total_path=None),
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline", destination="duckdb", dataset_name="ny_taxi_data"
)

load_info = pipeline.run(ny_taxi, write_disposition="replace")

conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")
df = conn.sql("DESCRIBE").df()

print(df)
```

How many tables were created?

* 2
* 4
* 6
* 8

> Answer

Output:

```
           database        schema  ...                                       column_types temporary
0  ny_taxi_pipeline  ny_taxi_data  ...  [VARCHAR, VARCHAR, BIGINT, TIMESTAMP WITH TIME...     False
1  ny_taxi_pipeline  ny_taxi_data  ...  [BIGINT, BIGINT, VARCHAR, VARCHAR, TIMESTAMP W...     False
2  ny_taxi_pipeline  ny_taxi_data  ...  [BIGINT, BIGINT, TIMESTAMP WITH TIME ZONE, VAR...     False
3  ny_taxi_pipeline  ny_taxi_data  ...  [DOUBLE, DOUBLE, DOUBLE, BIGINT, VARCHAR, DOUB...     False

[4 rows x 6 columns]
```

- 4

## **Question 3: Explore the loaded data**

Inspect the table `ride`:

```py
df = pipeline.dataset(dataset_type="default").rides.df()
df.info()
```

What is the total number of records extracted?

* 2500
* 5000
* 7500
* 10000

> Answer

Output:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10000 entries, 0 to 9999
Data columns (total 18 columns):
 #   Column                  Non-Null Count  Dtype
---  ------                  --------------  -----
 0   end_lat                 10000 non-null  float64
 1   end_lon                 10000 non-null  float64
 2   fare_amt                10000 non-null  float64
 3   passenger_count         10000 non-null  int64
 4   payment_type            10000 non-null  object
 5   start_lat               10000 non-null  float64
 6   start_lon               10000 non-null  float64
 7   tip_amt                 10000 non-null  float64
 8   tolls_amt               10000 non-null  float64
 9   total_amt               10000 non-null  float64
 10  trip_distance           10000 non-null  float64
 11  trip_dropoff_date_time  10000 non-null  datetime64[us, UTC]
 12  trip_pickup_date_time   10000 non-null  datetime64[us, UTC]
 13  surcharge               10000 non-null  float64
 14  vendor_name             10000 non-null  object
 15  _dlt_load_id            10000 non-null  object
 16  _dlt_id                 10000 non-null  object
 17  store_and_forward       135 non-null    float64
dtypes: datetime64[us, UTC](2), float64(11), int64(1), object(4)
memory usage: 1.4+ MB
```

- 10000

## **Question 4: Trip Duration Analysis**

Run the SQL query below to:

* Calculate the average trip duration in minutes.

```py
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )
    # Prints column values of the first row
    print(res)
```

What is the average trip duration?

* 12.3049
* 22.3049
* 32.3049
* 42.3049

> Answer

Output: 

```
[(12.3049,)]
```

- 12.3049