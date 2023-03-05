from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from database.models import FinancialData
from utils.input_validation import Constraint as ct, InputValidation
from utils.helper_func import get_boundary_dates, calculate_avg
from config.db import SYMBOL_MAX_LENGTH



route = APIRouter()


@route.get("/")
def get_avg_stats(symbol="", start_date="", end_date="", db:Session=Depends(get_db)):

	# Valiate request parameters
	validation = InputValidation()
	validation.add(name='symbol', value=symbol, constraints=[ct.Required(), ct.Length(SYMBOL_MAX_LENGTH)])
	validation.add(name='start_date', value=start_date, constraints=[ct.Required(), ct.DateString()])
	validation.add(name='end_date', value=end_date, constraints=[ct.Required(), ct.DateString()])
	error_msg = validation.get_error_msg()

	# It there is any error message, returns it and gets out of the function
	if error_msg:
		return {"data":{}, "info":{"error":error_msg}}

	# If all parameters are valid, use them to query data in DB
	data = db\
		.query(
			FinancialData.open_price,
			FinancialData.close_price,
			FinancialData.volume,
			FinancialData.date)\
		.filter(
			FinancialData.symbol==symbol,
			FinancialData.date>=start_date,
			FinancialData.date<=end_date
		)\
		.all()

	count = len(data)

	# If no data retrieved from DB, returns note informing the user 
	# (There is no pagination in this route, so returning some info is better. 
	# Otherwise, user will get {'data':[], "info":{'error':""}}, which is weird...)
	if count == 0:
		return {"data":{}, "info":{"error":"", "note":"No data found under the conditions given"}}

	# If data is not empty, process and return it to the user
	start_date, end_date = get_boundary_dates(data)

	data = {
        "start_date": start_date,
        "end_date": end_date,
        "symbol": symbol,
        "average_daily_open_price": calculate_avg([record.open_price for record in data],2),
        "average_daily_close_price": calculate_avg([record.close_price for record in data],2),
        "average_daily_volume": calculate_avg([record.volume for record in data],0)
    }

	return {"data":data, "info":{'error':""}}











