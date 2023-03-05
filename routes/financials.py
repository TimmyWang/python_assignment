from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from database.models import FinancialData
from utils.input_validation import Constraint as ct, InputValidation
from utils.helper_func import get_pages
from config.db import SYMBOL_MAX_LENGTH



route = APIRouter()


@route.get("/")
def get_raw_data(symbol="", start_date="1900-01-01", end_date="2999-12-31", limit=5, page=1, db:Session=Depends(get_db)):

	# Validate request parameters
	validation = InputValidation()
	validation.add(name='symbol', value=symbol, constraints=[ct.Length(SYMBOL_MAX_LENGTH)])
	validation.add(name='start_date', value=start_date, constraints=[ct.DateString()])
	validation.add(name='end_date', value=end_date, constraints=[ct.DateString()])
	validation.add(name='limit', value=limit, constraints=[ct.PositiveInteger()])
	validation.add(name='page', value=page, constraints=[ct.PositiveInteger()])
	error_msg = validation.get_error_msg()

	# It there is any error message, returns it and gets out of the function
	if error_msg:
		return {"data":[], "pagination":{}, "info":{"error":error_msg}}

	# If all parameters are valid, use them to query data in DB and return it at the end
	query = \
		db.query(
			FinancialData.symbol,
			FinancialData.date,
			FinancialData.open_price,
			FinancialData.close_price,
			FinancialData.volume
		).filter(
			True if not symbol else FinancialData.symbol==symbol,
			FinancialData.date>=start_date,
			FinancialData.date<=end_date
		)

	count = query.count()
	limit = int(limit)
	page  = int(page)
	pages = get_pages(count, limit)
	
	data       = query.offset(limit*(page-1)).limit(limit).all()
	pagination = {"count":count, "page":page, "limit":limit, "pages":pages}
	info       = {"error":""}
	
	return {"data":data, "pagination":pagination, "info":info}














