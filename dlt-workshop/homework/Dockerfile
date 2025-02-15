FROM python:3.12.0-slim

WORKDIR /app

RUN pip install pandas dlt[duckdb] 

COPY data_ingestion.py .

CMD [ "python", "data_ingestion.py" ]