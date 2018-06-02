import random
import json

from card import Card
from d import D

class Deck(object):
	def __init__(self):
		self.cards = []


	def build_deck(self):
		deck_1 = [self.random_card("primary") for i in range(0,40)]
		deck_2 = [self.random_card("secondary") for i in range(0,20)]

		self.cards = deck_1 + deck_2
		self.shuffle()

					 
	def shuffle(self):
		random.shuffle(self.cards)


	def draw_card(self):
		if (self.cards):
			return(self.cards.pop())


	def random_card(self, tier):
		primary_colors = ["C", "M", "Y", "K"]
		secondary_colors = ["W", "P"]

		if (tier == "primary"):
			color = primary_colors[D.roll(4, index=True)]
		else:
			color = secondary_colors[D.roll(2, index=True)]

		if (color == "W"):
			level = D.roll(5)
		else:
			level = D.roll(4)

		return(Card(color, level))


	def cards_dict(self):
		return([card.to_dict() for card in self.cards])


	def to_json(self):
		return(json.dumps(self.cards_dict()))
