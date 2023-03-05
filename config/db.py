from config import MYSQL_ROOT_PASSWORD



# connect string for entity OUTSIDE the container network (get_raw_data.py in this case)
DB_URL_EXTERNAL = f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@localhost:3306/ctw"

# connect string for entity INSIDE the container network (FastAPI service in this case)
DB_URL_INTERNAL = f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@mysql/ctw"

SYMBOL_MAX_LENGTH = 20