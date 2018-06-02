import json

from deck import Deck
from sequence import Sequence
from register import Register
from d import D

class Game(object):
	def __init__(self, state, players):
		self.state = state
		self.players = players
		self.current_player = None
		self.turn_count = 0


	def init_game(self):
		"""
		Load player decks
		Flip coin to determine which player goes first
		"""
		if (self.state == "INIT"):
			for player in self.players:
				player.load_deck()
				for i in range(0,7):
					player.hand.append(player.draw_card())

			self.current_player = self.players[D.roll(2, index=True)]

			for player in self.players:
				self.print_hand(player)

			self.update_gamestate("FIRST_TURN")
			self.update_turncount()
		else:
			pass


	def play_game(self):
		if (self.state == "FIRST_TURN"):
			print "%s's turn" % self.current_player.handle
		elif (self.state == "DRAW_TURN"):
			draw_card = self.current_player.draw_card()
			self.current_player.hand.append(draw_card)
			self.print_hand(self.current_player)
			self.update_gamestate("PLAY_TURN")
		elif (self.state == "PLAY_TURN"):
			# present available options to player
			pass
		else:
			pass


	def end_game(self):
		pass


	def pause_game(self):
		pass


	def update_gamestate(self, state):
		# have all possible states
		states = ["INIT", "FIRST_TURN", "DRAW_TURN", "PLAY_TURN"]
		if (state in states):
			self.state = state
		else:
			pass


	def end_turn(self):
		# check if self.current_player's hand is greater than 7
		if not (self.enforce_hand_limit(self.current_player)):
			print "%s ends turn" % self.current_player.handle
			self.current_player = self.next_player()
			self.update_gamestate("DRAW_TURN")
			self.update_turncount()
		else:
			print "Player must discard card"


	def add_card_to_register(self, player, card):
		# find card from player's hand
		# add to sequence
		# remove from player's hand
		if (len(player.register) < 4):
			player.register.append(card)
			print "\n%s register: %s " % (player.handle, str(player.register_dict()))
		else:
			# raise register limit error
			raise RegisterFullError("\n%s register is full\n" % player.handle)


	def enforce_hand_limit(self, player):
		if (len(player.hand) > 7):
			return(True)
		else:
			return(False)


	def discard_card(self, player, card):
		# if card exists in player's hand, discard it
		pass


	def next_player(self):
		return([x for x in self.players if x._id != self.current_player._id][0])


	def update_turncount(self):
		self.turn_count += 1


	def print_hand(self, player):
		print "\n%s hand: %s\n\n" % (player.handle, player.hand_dict())


	def number_of_cards_in_hand(self, player):
		pass


	def number_of_cards_in_deck(self, player):
		pass


	def number_of_cards_in_discard(self, player):
		pass


	def number_of_cards_in_sequence(self, player):
		pass



class RegisterFullError(Exception):
	pass