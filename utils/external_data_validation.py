from datetime import datetime



def is_valid_date(data):
	'''To check if data is a valid date string'''
	try:
		datetime.strptime(data, '%Y-%m-%d')
		return True
	except:
		return False


def is_valid_daily_data(data):
	'''
	To check if data is valid daily data
	This is an adhoc function for ALPHAVANTAGE API
	'''
	if not isinstance(data, dict):
		return False
	for key in ['1. open', '4. close', '6. volume']:
		try:
			float(data[key])
		except:
			return False
	return True


class APIDataValidation:
	'''To check if data fetched from external API is of the format we want'''

	def __init__(self,data):
		self.data = data
		self.error_msg = []

	def _get_dict_value(self, key_chain):
		'''
		To get nested value in a dictionary
		d = {1:{2:{3:4}}}
		self._get_dict_value([]) -> return d
		self._get_dict_value([1]) -> return d[1]
		self._get_dict_value([1,2]) -> return d[1][2]
		self._get_dict_value([1,2,3]) -> return d[1][2][3]
		self._get_dict_value([2]) -> generate error message
		'''
		if not key_chain:
			return self.data
		obj = self.data
		for key in key_chain:
			try:
				obj = obj[key]
			except:
				self.error_msg.append(f'Key chain: {key_chain}; Error: key missing')
				return None
		return obj

	def is_dict(self, key_chain):
		'''To check if the value under a series of keys is a dictionary'''
		obj = self._get_dict_value(key_chain=key_chain)
		if obj is not None and not isinstance(obj, dict):
			self.error_msg.append(f'Key chain: {key_chain}; Error: Value not a dictionary')

	def has_length(self, key_chain):
		'''To check if the value under a series of keys is not empty'''
		obj = self._get_dict_value(key_chain=key_chain)
		if obj is not None and len(obj) == 0:
			self.error_msg.append(f'Key chain: {key_chain}; Error: Value empty')

	def is_valid_time_series(self, key_chain):
		'''
		To check if the value under a series of keys is valid time series data
		This is an adhoc function for ALPHAVANTAGE API
		'''
		obj = self._get_dict_value(key_chain=key_chain)
		if obj is None:
			return
		for date, daily_data in obj.items():
			if not is_valid_date(date):
				self.error_msg.append(f'Key chain: {key_chain}; Error: Value "{date}" not a valid date string (YYYY-MM-DD)')
			if not is_valid_daily_data(daily_data):
				self.error_msg.append(
					f'Key chain: {key_chain+[date]}; ' +
					f'Error: Value "{daily_data}" not a valid dictionary ' +
					f'(containing {{ "1. open": number, "4. close": number, "6. volume": number }})'
				)

	def get_error_msg(self):
		return self.error_msg






		
	
