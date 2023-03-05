# Project Description

### Goal

1. Get data from [AlphaVantage](https://www.alphavantage.co/documentation/) API and insert processed data into local database.
2. Build 2 APIs that retrieve above-mentioned data in different ways.

### Tech Stack

- Backend: python (FastAPI)
- Database: MySQL
- Container: Docker

### Prerequisites

Make sure you have installed following tools in your computer:

- Python (recommended version 3.10)
- Docker

## Steps to Run the Services

### 1. Create `.env` file to store API key and DB password

```
ALPHAVANTAGE_API_KEY=YOUR_API_KEY
MYSQL_ROOT_PASSWORD=YOUR_DB_PASSWORD
```

### 2. Start the DB and the API containers

Later we will fetch external data and store it in DB (goal 1), so we have to **start the database** and **create the table** first.
Run the following command:

```
docker-compose up
```

You should then see on the terminal:

```
fastapi_1  | INFO:     Application startup complete.
```

### 3. Fetch external data and save it in DB (goal 1)

Run the commands:

```
pip install -r requirements.txt
```

```
python get_raw_data.py
```

Note: You should see messages showing the result after executing `python get_raw_data.py`

### 4. Test API endpoint 1 (goal 2)

endpoint:

```
http://localhost:5000/api/financial_data/
```

Sample request:

```
curl -X GET 'http://localhost:5000/api/financial_data/?start_date=2023-01-01&end_date=2023-03-31&symbol=IBM&limit=3&page=2'
```

| Parameter  | Required | Format           | Note                              |
| ---------- | -------- | ---------------- | --------------------------------- |
| start_date | No       | YYYY-MM-DD       |                                   |
| end_date   | No       | YYYY-MM-DD       |                                   |
| symbol     | No       | 20 charaters max | stock symbol                      |
| limit      | No       | positive integer | number of records for single page |
| page       | No       | positive integer | current page index                |

Response can be:

1. You provide parameters correctly and get some data back:

```
{
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-02-13",
            "open_price": 136,
            "close_price": 137.35,
            "volume": 4403015
        },
        ...
    ],
    "pagination": {
        "count": 28,
        "page": 1,
        "limit": 5,
        "pages": 6
    },
    "info": {
        "error": ""
    }
}
```

2. You provide parameters correctly and get empty data back (There is no data based on your query):

```
{
    "data": [],
    "pagination": {
        "count": 0,
        "page": 1,
        "limit": 5,
        "pages": 0
    },
    "info": {
        "error": ""
    }
}
```

3. You provide parameters incorrectly and get some error messages:

```
{
    "data": [],
    "pagination": {},
    "info": {
        "error": {
            "symbol": [
                "cannot exceed 20 characters"
            ],
            "end_date": [
                "not a valid date string (YYYY-MM-DD)"
            ]
        }
    }
}
```

### 5. Test API endpoint 2 (goal 2)

endpoint:

```
http://localhost:5000/api/statistics/
```

Sample request:

```
curl -X GET 'http://localhost:5000/api/statistics/?start_date=2023-01-01&end_date=2023-03-31&symbol=IBM'
```

| Parameter  | Required | Format           | Note         |
| ---------- | -------- | ---------------- | ------------ |
| start_date | Yes      | YYYY-MM-DD       |              |
| end_date   | Yes      | YYYY-MM-DD       |              |
| symbol     | Yes      | 20 charaters max | stock symbol |

Response can be:

1. You provide parameters correctly and get some data back:

```
{
    "data": {
        "start_date": "2023-02-13",
        "end_date": "2023-02-21",
        "symbol": "IBM",
        "average_daily_open_price": 135.39,
        "average_daily_close_price": 135.25,
        "average_daily_volume": 3466846
    },
    "info": {
        "error": ""
    }
}
```

2. You provide parameters correctly and get empty data back (There is no data based on your query):

```
{
    "data": {},
    "info": {
        "error": "",
        "note": "No data found under the conditions given"
    }
}
```

3. You provide parameters incorrectly and get some error messages:

```
{
    "data": {},
    "info": {
        "error": {
            "symbol": [
                "cannot exceed 20 characters"
            ],
            "start_date": [
                "missing parameter",
                "not a valid date string (YYYY-MM-DD)"
            ],
            "end_date": [
                "not a valid date string (YYYY-MM-DD)"
            ]
        }
    }
}
```

## Others

### Repository structure

```
python_assignment/
├── config
│    ├── __init__.py (A)
├── database
│    ├── __init__.py (B)
│    ├── model.py (C)
├── routes
│    ├── financials.py (D)
│    ├── statistics.py (E)
├── utils
│    ├── external_data_validation.py (F)
│    ├── input_validation.py (G)
│    ├── help_func.py
├── Dockerfile (H)
├── docker-compose.yml (I)
├── README.md
├── requirements.txt
├── get_raw_data.py (J)
├── run.py (K)
└── .env (L)

```

- A: storing variables used in other files
- B: setting up database
- C: defining table in ORM
- D: building up the endpoint 1
- E: building up the endpoint 2
- F: validating data from AlphaVantage API
- G: validating parameters for endpoints 1 and 2
- H: building FastAPI service image
- I: starting FastAPI and MySQL DB services
- J: fetching data from AlphaVantage API and save it in DB
- K: running FastAPI service
- L: storing confidential data (**YOU SHOULD CREATE YOUR OWN .ENV FILE**)

### Library choices

| Library                | Description                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| fastapi                | used to build APIs. it's easy to set up and has built-in interface for testing (http://localhost:5000/docs)    |
| uvicorn                | an ASGI web server implementation for Python                                                                   |
| sqlalchemy             | Object-Relational Mapping (ORM) framework that allows developers to construct SQL queries in a python-like way |
| mysql-connector-python | provides a Python interface for connecting to and interacting with MySQL databases                             |
| python-dotenv          | used to load environment variables (e.g. API KEY) in python code                                               |
| requests               | used to make http requests in python code                                                                      |

### How to store API KEY

| Stage       | Options                                                                                                                                                                         |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Development | API KEYs can be stored with other confidential information in `.env` file.                                                                                                      |
| Production  | Especially when working on a project with a big team, you might want to consider using API secret management services to ensure that only authorized users can access the keys. |

### Database migration

SQLAlchemy includes a built-in migration system called "Alembic" that makes it easy to perform database migrations.

More information on the [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
