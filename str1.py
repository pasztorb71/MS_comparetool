class str1(str):
	def __init__(self, s):
		self.s = s

	def is_separate(self, i, length):
		"""
		Azt vizsgálja, hogy...
		:param text:
		:param i:
		:param length:
		:return:
		"""
		if i > 0 and self.s[i - 1:i - 1 + 1].isspace() is False:
			return False
		if len(self.s) > i + length and self.s[i + length:i + length + 1].isspace() is False:
			return False
		return True
