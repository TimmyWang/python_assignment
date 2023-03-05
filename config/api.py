from config import ALPHAVANTAGE_API_KEY



class ALPHAVANTAGE:
	
	ENDPOINT = 'https://www.alphavantage.co/query'
	
	PARAMS = {
		'function': 'TIME_SERIES_DAILY_ADJUSTED',
		'outputsize': 'compact',
		'apikey': ALPHAVANTAGE_API_KEY,
		'symbol': None # will be replaced with real symbol case by case when sending requests later
	}