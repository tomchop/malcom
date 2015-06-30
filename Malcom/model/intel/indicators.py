from Malcom.model.intel.entities import Indicator


class Attribute(dict):  # this should be replaced by openioc
	
	types = ['regex', 'string']

	def __init__(self, type, value):
		if type not in Attribute.types:
			raise ValueError("'type' can be {}".format(Attribute.types))
		self.type = _type
		self.value = value

	def check_regex():
		pass
	
	def check_string():
		pass

	def match(string):
		f = self.__getattr__("check_{}".format(self.type))
		
		if not f:
			raise ValueError("No matching function for {}".format(self.type))
		
		f(string)


class Email(Indicator):
	"""docstring for Email"""
	def __init__(self):
		super(Email, self).__init__()
		
		