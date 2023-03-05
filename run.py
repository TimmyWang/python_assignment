from fastapi import FastAPI

from database import create_tables
from routes.financials import route as financial_route
from routes.statistics import route as stats_route



# When running 'docker-compose up' command, 
# MySQL container is responsible for creating database while
# FastAPI container is responsible for creating tables in the database.
# It takes some time for the database to be ready.
# Therefore, this 'create_tables' function will try to connect to the DB 10 times,
# and wait for 15 seconds to try connecting again if the previous attempt fails. 
create_tables(try_times=10, wait_seconds=15)

app = FastAPI()

app.include_router(financial_route, prefix="/api/financial_data")

app.include_router(stats_route, prefix="/api/statistics")

















