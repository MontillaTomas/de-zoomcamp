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

df2 = pipeline.dataset(dataset_type="default").rides.df()
df2.info()

with pipeline.sql_client() as client:
    res = client.execute_sql(
        """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
    )
    print(res)
