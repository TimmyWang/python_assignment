# def format_date_string(date_string):
# 	year, month, day = date_string.split('-')
# 	return f'{year}-{int(month):02d}-{int(day):02d}'


def get_boundary_dates(data):
	'''Get the earliest and the latest date given a query result'''
	dates = sorted([record.date for record in data])
	return str(dates[0]), str(dates[-1])


def calculate_avg(data, decimal=2):
	'''Calculate average given an array of numbers'''
	result = sum(data)/len(data)
	if decimal > 0:
		return round(result,decimal)
	return int(result)


def get_pages(count, limit):
	'''Calculate total pages given data count and page size'''
	return (count // limit) + (1 if count % limit else 0)