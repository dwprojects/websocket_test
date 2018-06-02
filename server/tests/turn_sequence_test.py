import sys
sys.path.append("../")

from game import Game
from game import RegisterFullError
from player import Player

def add_to_register(t):
	try:
		card = t.current_player.hand.pop()
		t.add_card_to_register(t.current_player, card)
	except RegisterFullError as e:
		print e





p1 = Player("1", "P1")
p2 = Player("2", "P2")
t = Game("INIT", [p1, p2])

# t0
t.init_game()		# start game

# t1
print "Turn: %s" % t.turn_count
t.play_game()		# first player can play a card
add_to_register(t)	# add card to register
t.end_turn()

# t2
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t3
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t4
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t5
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t6
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t7
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#

# t8 -- register is full
print "Turn: %s" % t.turn_count
t.play_game()		# player draws card
add_to_register(t)	# add card to register
t.end_turn()		#
t.play_game()		#




# load players into game
# flip coin to decides who goes first
# have p1 skip turn
# have p2 draw a card