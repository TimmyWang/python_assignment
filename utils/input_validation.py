from datetime import datetime



class Constraint:
	'''Contains classes to verify GET request parameters sent to FastAPI endpoints'''
	
	class Required:
		'''To check if the parameter is empty'''
		
		def __init__(self):
			pass

		def verify(self, value):
			if len(value) == 0:
				return False, "missing parameter"
			return True, ""

	class DateString:
		'''To check if the parameter is a vaid date string'''

		def __init__(self, ds_format='%Y-%m-%d'):
			self.ds_format = ds_format

		def verify(self, value):
			try:
				datetime.strptime(value, self.ds_format)
				return True, ""
			except:
				return False, "not a valid date string (YYYY-MM-DD)"

	class PositiveInteger:
		'''To check if the parameter is a positive integer'''
		
		def __init__(self):
			pass

		def verify(self, value):
			try:
				integer = int(value)
			except:
				return False, "not a positive integer"
			if integer <= 0:
				return False, "not a positive integer"
			return True, ""

	class Length:

		def __init__(self, max_length):
			self.max_length = max_length

		def verify(self, value):
			if len(value) > self.max_length:
				return False, f"cannot exceed {self.max_length} characters"
			return True, ""


class InputValidation:
	'''
	To validate request parameters:
	1. Create an object: X = InputValidation()
	2. Add constraints you wnat to check: X.add(parameter_name, parameter_value, constraint_list=[Constraint.Required(),...])
	3. Check if there is any error: error_msg = X.get_error_msg()
	'''
	
	def __init__(self):
		self.error_msg = {}

	def add(self, name, value, constraints):
		error_msg = []
		for constraint in constraints:
			verified_result, msg = constraint.verify(value)
			if not verified_result:
				error_msg.append(msg)
		if error_msg:
			 self.error_msg[name] = error_msg

	def get_error_msg(self):
		return self.error_msg


	
	













