# FEMA ETL Pipeline

A structured, production-style ETL (Extract → Transform → Load) pipeline that ingests FEMA Public Assistance project data into a local PostgreSQL database.

---

## 🚀 Overview

This project pulls data from the FEMA Open API:

https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails

It then:

1. **Extracts** paginated data from the API
2. **Transforms** it into a curated schema
3. **Loads** it into a PostgreSQL database

The pipeline is designed with **separation of concerns**, making it scalable, maintainable, and easy to extend.

---

## 🧱 Project Structure

```
api_etl/
│
├── conf/
│   ├── settings.py        # Configuration (env, API, DB)
│   └── conf.py            # Logging setup
│
├── api/
│   └── fema_client.py     # Extract layer (API calls)
│
├── services/
│   ├── fema_transform.py  # Data transformation logic
│   └── fema_service.py    # Business logic (ETL coordination)
│
├── db/
│   ├── postgres.py        # DB connection + DB creation
│   └── repositories.py    # Table creation + inserts
│
├── utils/
│   └── http.py            # HTTP requests with retries
│
├── pipelines/
│   └── fema_pipeline.py   # Orchestration layer
│
├── app.py                 # Entry point
├── env/.env               # Environment variables
└── logs/                  # Log files
```

---

## ⚙️ Setup

### 1. Clone repository

```
git clone <your-repo-url>
cd api_etl
```

---

### 2. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

Required packages:

* requests
* psycopg2
* python-dotenv

---

### 4. Configure environment

Create `env/.env`:

```
# API
API_TIMEOUT=10
API_MAX_RETRIES=3
API_BACKOFF_FACTOR=0.5
FEMA_API_BASE=https://www.fema.gov/api/open/v2
FEMA_PAGE_LIMIT=1000

# PostgreSQL
PG_HOST=localhost
PG_PORT=5432
PG_DB=fema
PG_USER=postgres
PG_PASSWORD=postgres
```

---

## ▶️ Running the Pipeline

```
python app.py
```

---

## 🧠 How It Works

### 🔌 Extract (API Layer)

* Fetches FEMA data using `limit` and `offset`
* Implements pagination
* Includes retry logic with exponential backoff

---

### 🔄 Transform (Service Layer)

* Converts raw JSON into structured records
* Selects only **important columns**
* Cleans data (e.g., date parsing, numeric conversion)

---

### 🗄️ Load (Database Layer)

* Automatically creates:

  * Database (if missing)
  * Table schema
* Inserts data in batches
* Logs number of inserted rows

---

### 🔁 Pipeline (Orchestration)

Coordinates the entire flow:

```
fetch → transform → insert
```

---

## 🧱 Database Schema

```
fema_projects
```

| Column           | Type      | Description        |
| ---------------- | --------- | ------------------ |
| id               | SERIAL    | Primary key        |
| disaster_number  | INTEGER   | FEMA disaster ID   |
| project_number   | TEXT      | Project identifier |
| state            | TEXT      | State              |
| county           | TEXT      | County             |
| incident_type    | TEXT      | Disaster type      |
| declaration_date | DATE      | Declaration date   |
| applicant_name   | TEXT      | Applicant          |
| project_title    | TEXT      | Project name       |
| federal_share    | NUMERIC   | Federal funding    |
| total_obligated  | NUMERIC   | Total funding      |
| created_at       | TIMESTAMP | Insert timestamp   |

---

## ⚠️ Pagination Safety

To prevent infinite loops or runaway ingestion:

* Uses **offset-based pagination**
* Includes a **maximum offset limit**
* Stops when:

  * No data is returned
  * Last page is reached
  * Offset exceeds safety threshold

---

## 📊 Example Queries

### Total records

```
SELECT COUNT(*) FROM fema_projects;
```

---

### Total funding by state

```
SELECT state, SUM(federal_share)
FROM fema_projects
GROUP BY state
ORDER BY SUM(federal_share) DESC;
```

---

### Top 10 largest projects

```
SELECT project_title, federal_share
FROM fema_projects
ORDER BY federal_share DESC
LIMIT 10;
```

---

## 🧠 Design Principles

* **Separation of concerns**
* **Config-driven (via .env)**
* **Idempotent database setup**
* **Batch processing**
* **Resilient API handling**

---

## 🚀 Future Improvements

* Bulk inserts using PostgreSQL `COPY` (performance)
* Incremental loading (only new data)
* Schema validation (Pydantic)
* Dockerized setup
* Scheduling (Airflow / cron)

---

## 🐛 Troubleshooting

### No data in table

* Ensure you are connected to the correct database:

  ```
  SELECT current_database();
  ```

---

### Pipeline runs forever

* Check `MAX_OFFSET` in `fema_client.py`

---

### API errors

* Verify internet connection
* Increase retry settings in `.env`

---

## 📌 Summary

This project demonstrates how to build a **real-world ETL pipeline** with:

* Clean architecture
* Reliable data ingestion
* Scalable design

---

## 👨‍💻 Author

O Oloye
