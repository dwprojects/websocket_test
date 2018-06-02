import json

class Card(object):
	def __init__(self, color, level, _id=""):
		self._id = _id
		self.color = color
		self.level = level


	def to_dict(self):
		return(
				{
					"color": self.color,
					"level": self.level
				}
		)


	def to_json(self):
		return(json.dumps(self.to_dict()))
