from deck import Deck
from card import Card

class Player(object):
	def __init__(self, _id, handle):
		self._id = _id
		self.handle = handle
		self.deck = None
		self.hand = []
		self.register = []


	def load_deck(self):
		if not (self.deck):
			self.deck = Deck()

		self.deck.build_deck()


	def draw_card(self):
		return(self.deck.draw_card())


	def hand_dict(self):
		return([x.to_dict() for x in self.hand])


	def register_dict(self):
		return([x.to_dict() for x in self.register])


	def to_json(self):
		pass
