# Fake Store Automated ETL Pipeline
A lightweight data engineering project demonstrating automated extraction, transformation, and reporting using GitHub Actions, Python, and Power BI. *ETL* stands for *Extract*, *Transform*, and *Load*. 

![](fake_store_etl_introduction.jpg)

_Image credit: freepik_

## Introduction

This project simulates a small production-style ETL workflow that collects product data from the Fake Store API, prepares it for analysis, and publishes a clean dataset used by a Power BI report. The pipeline runs automatically in the cloud so that the dataset and dashboard stay up to date without manual intervention. The Python and other scripts were run in Visual Studio Code.

## Overview

The goal of the project is to show an end-to-end workflow that brings together:

* Scheduled automation

* Data extraction and cleaning

* Reliable fallback behaviour when an API fails

* Cloud-hosted data outputs

* Live reporting connected to a GitHub-based dataset

## What I Built

- A Python + Prefect ETL pipeline that:
  - Calls the **Fake Store API** for product data.
  - Falls back to a **local JSON snapshot** if the API is unavailable.
  - Cleans and enriches the data (e.g. calculates `price_with_vat`).
  - Outputs both **Parquet** (for local analytics) and **CSV** (for the web).

- A **GitHub Actions** workflow that:
  - Runs the ETL on a schedule in the cloud.
  - Updates `public/products.csv` with the latest curated dataset.
  - Writes a simple `public/last_updated.txt` file so I can show when the pipeline last ran.

- A **Power BI dashboard** that:
  - Connects directly to the GitHub-hosted CSV using a Web URL.
  - Refreshes to pick up new pipeline runs.
  - Includes a “Last Updated (UTC)” card based on `last_updated.txt`, so viewers can see when the data was last processed.


## High-Level Architecture

```text
Fake Store API (or snapshot)
          ↓
    Python + Prefect
  (extract / transform / load)
          ↓
 data/curated/products.parquet      → used locally
 public/products.csv                → used by Power BI
 public/last_updated.txt            → shows last pipeline run
          ↓
   Power BI (Web connector)
   Live dashboard & KPIs
```

## Project Structure

```text
fake-store-pipeline/
│
├── pipelines/
│   ├── extract.py       # API + fallback snapshot logic
│   ├── transform.py     # cleaning, types, derived metrics
│   └── load.py          # writes Parquet + CSV
│
├── flows.py             # Prefect flow orchestration
├── sample_data/
│   └── products_seed.json   # snapshot used if API fails
│
├── public/
│   ├── products.csv         # latest curated dataset
│   └── last_updated.txt     # timestamp written by GitHub Actions
│
├── .github/workflows/
│   └── etl.yml          # GitHub Actions workflow (scheduled ETL)
│
├── requirements.txt
└── README.md

```

## ETL Behaviour

### 1. Extract:

* Tries to call https://fakestoreapi.com/products.

* If the API responds with an error (e.g. 403, 500, timeout), the pipeline loads sample_data/products_seed.json instead.

* The raw payload is stored under data/raw/ with a timestamped filename.
  

### 2. Transform:

* Normalises the JSON into a flat table (using pandas.json_normalize).

* Standardises column names to snake_case.

* Casts prices and ratings to numeric types.

* Adds a simple derived metric: price_with_vat (20% VAT).

* Drops duplicate products and resets the index.


### 3. Load:

* Writes the curated table to data/curated/products.parquet for efficient local analysis.

* Writes a CSV copy to public/products.csv.

* GitHub Actions later commits that CSV and an updated public/last_updated.txt back to the repository.


## Cloud Automation (GitHub Actions)

The workflow defined in .github/workflows/etl.yml runs the Prefect flow on a schedule.

At a high level, it:

1. Checks out the repository.

2. Sets up Python and installs dependencies from requirements.txt.

3. Runs flows.py to execute the ETL.

4. Copies the latest CSV into public/products.csv.

5. Writes the current UTC time into public/last_updated.txt.

6. Commits and pushes any changes.

This means the repository always contains a fresh, ready-to-use CSV that external tools (like Power BI) can consume over HTTP.

Here is the Python code for the ETL process. Full Python script available upon request.

```python
# flows.py showing functions and code for ETL pipeline

from prefect import flow, task
from pipelines.extract import extract_products
from pipelines.transform import normalize_products
from pipelines.load import to_parquet_and_csv  


@task
def extract_t():
    return extract_products()

@task
def transform_t(raw_path):
    return normalize_products(raw_path)

@task
def load_t(df):
    return to_parquet_and_csv(df)


@flow(name="fake-store-etl")
def run_pipeline():
    raw_path = extract_t()
    df = transform_t(raw_path)
    parquet_path, csv_path = load_t(df)
    print(f"ETL complete → {parquet_path} and {csv_path}")


if __name__ == "__main__":
    run_pipeline()
```

This is a screenshot of a successful run of the code and functions in the terminal:

![](https://github.com/iprincewill3/fake-store-pipeline/blob/main/terminal_run_successfully_completed.png)

## Power BI Dashboard

I created two versions of the report:

* One connected to the local Parquet file (for fast, offline exploration).

* The other one connected to the GitHub CSV using the Web connector.

The GitHub-connected report reads from:

https://raw.githubusercontent.com/iprincewill3/fake-store-pipeline/main/public/products.csv

![](https://github.com/iprincewill3/fake-store-pipeline/blob/main/fake_store_etl_dashboard.png)

The dashboard includes:

* KPIs such as total revenue and number of products.

* Revenue and ratings broken down by category.

* A scatter plot of price vs rating.

* A table of top products.

* A “Last Updated (UTC)” card that reflects the contents of public/last_updated.txt, so stakeholders can see when the pipeline was last refreshed.

This combination shows both the engineering side (automated data feed) and the analytics side (turning it into a clear visual story). Here is a link to the [interactive dashboard](https://app.powerbi.com/view?r=eyJrIjoiMjQ4MmFlOWQtOWQxNS00Zjc5LWI3NzgtZjM0YzMyMGI2NWZhIiwidCI6ImQwMWNmNTVlLTI2MDMtNGExMC04ZjY0LWVkOWY1OWM5NmVkZSJ9).

## What This Project Demonstrates

From a skills perspective, this project demonstrates:

* Working with APIs and handling upstream failures gracefully.

* Building a small but realistic ETL pipeline in Python.

* Using Prefect to orchestrate tasks.

* Using GitHub Actions to run pipelines in the cloud on a schedule.

* Producing analytics-ready data in Parquet and CSV formats.

* Connecting Power BI to a live, GitHub-hosted dataset.

From a business/stakeholder perspective, it shows how to:

* Turn raw product data into something that can answer questions like:

  - “Which categories drive the most revenue?”

  - “How do price and rating relate?”

  - “When was this data last updated?”

* Build a setup where the dashboard does not depend on someone “pulling a file manually” each time.


## Notes

* This is a portfolio project built around the public Fake Store API.

* The API is occasionally unstable, which is why the pipeline includes a snapshot fallback.

* The focus is on the overall flow and automation rather than modelling a production-grade dataset.


