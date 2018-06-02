import random

class D(object):
	@classmethod
	def roll(self, sides, index=False):
		if (index):
			return(random.randint(0, sides-1))
		else:
			return(random.randint(1, sides))
