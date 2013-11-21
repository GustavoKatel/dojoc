# Author: Gustavo Brito (GustavoKatel)

class DojoCTest:

	def __init__(self, unit, params, return_val):
		self.unit = unit
		self.params = params
		self.return_val = return_val
	
	def test(self, val):
		return val==str(self.return_val)

	def getTestFunc(self):
		fn = self.unit+"("
		for i in range(len(self.params)):
			if type(self.params[i]) is str:
				quote = "\""
				if len(self.params[i])==1:
					quote = "'"
				fn = fn + quote+self.params[i]+quote
			else:
				fn = fn + str(self.params[i])
			if i<len(self.params)-1:
				fn = fn+","
		fn = fn + ")"
		return fn

	def toString(self):
		s = str(self.params) + " = " + str(self.return_val)
		s = s.replace("[", "").replace("]", "")
		return s

	def getReturnVal(self):
		return self.return_val
