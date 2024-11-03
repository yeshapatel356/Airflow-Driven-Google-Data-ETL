# Airflow-Driven-Google-Data-ETL
This project utilizes Apache Airflow to automate the process of extracting, transforming, and loading (ETL) restaurant data from Google Places. It allows users to search for restaurants based on location and retrieves details, reviews, and sentiment analysis for positive reviews.

## Technologies and Tools:

* Apache Airflow: Orchestrates the ETL pipeline, providing task scheduling, dependency management, and workflow visualization.
* Google Cloud Platform (GCP): Leverages GCP services for data extraction, transformation, and storage.
* Python: Programming language for data processing and manipulation.

## Requirements:

* Python 3.x
* Airflow
* Google Maps API Key (store in Airflow Variables or .dotenv file)
* pandas
* TextBlob
* requests

## Setup

### 1. Install required libraries:
```Bash```
> ```pip install airflow pandas textblob requests```

### 2. Create an Airflow environment (optional):
```Bash```
> ```python -m venv .venv```
>``` source .venv/bin/activate```

### 3. Create Google Maps API Key
Obtain a Google Maps API Key from Google Cloud Console and store it in one of the following locations:
Airflow Variables: Set a variable named ```GOOGLE_API_KEY``` with your API key.
```.dotenv``` file: Create a file named ```.dotenv``` in the project root directory and add the line ```GOOGLE_API_KEY=your_api_key```

## Running the Script:

### 1. Initialize the Airflow environment (if using a virtual environment):
```Bash```
>```source .venv/bin/activate```

### 2. Start Airflow
```Bash```
>```airflow standalone```

### 3. Trigger the DAG Manually in the Airflow UI
Access the Airflow UI at ```http://localhost:8080```, find your DAG, and trigger it manually

## Explanation of Scripts:

```google_etl.py```: This script defines functions for interacting with Google Places API for restaurant search, details retrieval, and review extraction.
```analyze_reviews.py```: This script analyzes reviews loaded from a CSV file and extracts dishes mentioned in positive reviews.


## Airflow DAG:

```google_etl_dag.py```: Defines the Airflow DAG that orchestrates the Google Places ETL process. It includes tasks for:
Running the Google Places ETL script.
Analyzing reviews for positive sentiment and extracting dish mentions.

## Output:

```positive_dishes_per_restaurant.csv```: This CSV file (generated after review analysis) stores information about restaurants and the unique dishes mentioned in their positive reviews.<br>
```restaurant_reviews.csv``` (temporary): This CSV file stores the raw restaurant data and reviews retrieved from Google Places (used for review analysis).