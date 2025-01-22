# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1

> Answer

First, we need to run the container with the `python:3.12.8` image in an interactive mode and use the entrypoint `bash`:

```bash
docker run -it --entrypoint bash python:3.12.8
```

Then, we can check the version of `pip`:

```bash
pip --version
```

The output will be:

```bash
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

Therefore, the correct answer is:

- 24.3.1

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

If there are more than one answers, select only one of them

> Answer

- db:5432

The `hostname` is the name of the database service in the `docker-compose.yaml` file, which is `db`. The `port` is the port that the database service is exposed on, which is `5432`.

##  Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from October 2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether
you want to use Jupyter or a python script.

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles 

Answers:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202

> Answer

To calculate the number of trips for each segment, we can use the following SQL queries:

```sql
SELECT COUNT(*)
FROM green_taxi_trips
WHERE trip_distance <= 1.0; -- 104838

SELECT COUNT(*)
FROM green_taxi_trips
WHERE trip_distance > 1.0 AND trip_distance <= 3.0; -- 199013

SELECT COUNT(*)
FROM green_taxi_trips
WHERE trip_distance > 3.0 AND trip_distance <= 7.0; -- 109645

SELECT COUNT(*)
FROM green_taxi_trips
WHERE trip_distance > 7.0 AND trip_distance <= 10.0; -- 27688

SELECT COUNT(*)
FROM green_taxi_trips
WHERE trip_distance > 10.0; -- 35202
```

Therefore, the correct answer is:

- 104,838;  199,013;  109,645;  27,688;  35,202

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31

> Answer

To find the pick up day with the longest trip distance we can use the following SQL query:

```sql
SELECT  lpep_pickup_datetime::DATE AS date, 
        MAX(trip_distance) AS max_trip_distance
FROM green_taxi_trips
GROUP BY lpep_pickup_datetime::DATE
ORDER BY max_trip_distance DESC
LIMIT 1;
```

The output will be:

| date       | max_trip_distance |
|------------|-------------------|
| 2019-10-31 | 515.89            |

Therefore, the correct answer is:

- 2019-10-31

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

> Answer

To find the top pickup locations with over 13,000 in `total_amount` for 2019-10-18, we can use the following SQL query:

```sql
SELECT z."Zone", SUM(total_amount) AS total_amount_sum
FROM green_taxi_trips gtt
JOIN zones z ON gtt."PULocationID" = z."LocationID"
WHERE gtt.lpep_pickup_datetime::DATE = '2019-10-18'
GROUP BY z."Zone"
HAVING SUM(total_amount) > 13000.0
ORDER BY total_amount DESC;
```

The output will be:

| Zone                | total_amount_sum   |
|---------------------|--------------------|
| East Harlem North   | 18686.679999999724 |
| East Harlem South   | 16797.259999999802 |
| Morningside Heights | 13029.789999999914 |

Therefore, the correct answer is:

- East Harlem North, East Harlem South, Morningside Heights

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone
named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

> Answer

To find the drop off zone that had the largest tip for the passengers picked up in October 2019 in the zone named "East Harlem North", we can use the following SQL query:

```sql
SELECT zdo."Zone" AS dropoff_zone, MAX(gtt.tip_amount) AS max_tip_amount
FROM green_taxi_trips gtt
JOIN zones zpu ON gtt."PULocationID" = zpu."LocationID"
JOIN zones zdo ON gtt."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'East Harlem North'
GROUP BY zdo."Zone"
ORDER BY max_tip_amount DESC
LIMIT 1;
```

The output will be:

| dropoff_zone  | max_tip_amount |
|---------------|----------------|
| JFK Airport	  | 87.3           |  

Therefore, the correct answer is:

- JFK Airport

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](../../../01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

> Answer

The correct sequence of commands for the Terraform workflow is:

- terraform init, terraform apply -auto-approve, terraform destroy