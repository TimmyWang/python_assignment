import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config.api import ALPHAVANTAGE as ALPHA
from config.db import DB_URL_EXTERNAL
from database.models import FinancialData
from utils.external_data_validation import APIDataValidation



def get_data(endpoint, params):
	'''
	To retrieve data from AlphaVantage API.
	'''
	response = requests.get(endpoint, params=params)
	if response.status_code != 200:
		return [], False

	return response.json(), True


def validate_data(data):
	'''
	To validate data retrieved from AlphaVantage API to see if there's any change in the format.
	'''
	validation = APIDataValidation(data)
	validation.is_dict(key_chain=[])
	validation.has_length(key_chain=['Meta Data','2. Symbol'])
	validation.is_valid_time_series(key_chain=['Time Series (Daily)'])

	return validation.get_error_msg()


def process_data(data, latest_n_days):
	'''
	To process raw data to fit the table schema.
	'''
	symbol = data['Meta Data']['2. Symbol']
	main_data = data['Time Series (Daily)']
	main_data = sorted([[date, daily_data]for date, daily_data in main_data.items()], key=lambda x: x[0], reverse=True)
	main_data = main_data[:latest_n_days]
	
	def process_daily_data(symbol, date, daily_data):
		return{
			'symbol': symbol, 
			'date':date, 
			'open_price':float(daily_data['1. open']), 
			'close_price':float(daily_data['4. close']), 
			'volume': int(daily_data['6. volume'])
		}

	return [process_daily_data(symbol, date, daily_data) for date, daily_data in main_data]


def insert_data(data, db_engine):
	'''
	To insert processed data into database.
	If a record already exists -> update
	If a record does not exist -> insert
	'''
	inserted, updated = 0, 0
	with Session(db_engine) as session:
		for daily_data in data:
			record = session.query(FinancialData).filter(FinancialData.symbol==daily_data['symbol'], FinancialData.date==daily_data['date']).first()
			if not record:
				data_obj = FinancialData(**daily_data)
				session.add(data_obj)
				inserted += 1
			else:
				record.open_price = daily_data['open_price']
				record.close_price = daily_data['close_price']
				record.volume = daily_data['volume']
				updated += 1
		session.commit()
	return inserted, updated


def main(stocks, latest_n_days):
	'''
	Executes the pipeline including:
	1. Data fetching
	2. Data Validation
	3. Data process
	4. Data insertion or update 
	'''
	for stock in stocks:
		
		print('---'*10)
		print(f'symbol processed: {stock}')

		# Get data from api
		params = ALPHA.PARAMS | {'symbol': stock}
		raw_data, success = get_data(endpoint=ALPHA.ENDPOINT, params=params)
		if not success or 'Error Message' in raw_data:
			print('Failed to fetch data from API')
			continue

		# Validate data
		error_msg = validate_data(raw_data)
		if error_msg:
			print('The schema of the API data has changed. Revise process_data function before proceeding.')
			for msg in error_msg:
				print(msg)
			continue

		# Process data
		processed_data = process_data(raw_data, latest_n_days=latest_n_days)
		
		# Insert data
		engine = create_engine(DB_URL_EXTERNAL, echo=False)
		inserted, updated = insert_data(data=processed_data, db_engine=engine)
		print(f'inserted: {inserted}, updated: {updated}')

	print('---'*10)


if __name__ == "__main__":
	
	stocks = ['IBM','AAPL']
	
	latest_n_days = 14
	
	main(stocks=stocks, latest_n_days=latest_n_days)
	










