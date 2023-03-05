import os
from dotenv import load_dotenv


# loading environment variables
load_dotenv()

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

MYSQL_ROOT_PASSWORD  = os.environ.get("MYSQL_ROOT_PASSWORD")




