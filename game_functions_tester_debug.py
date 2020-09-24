""" A repository of functions dealing with game play for Durak, including AI algorithm. """

from random import randint
from card import *

# Support functions:

def reveal_wild(deck):
	'''Select the wild suit at the beginning of the game.'''
	val = deck[0]
	wild = val.suit()
	return wild

def decide_turn():
	'''A flip of a coin to see who goes first.'''
	flip = randint(1, 10000)
	if flip % 2 == 0:
		return True
	else:
		return False

def draw_cards(hand, deck):
	'''Replenishes cards between turns. Must be called for each character.'''
	while len(deck) > 0 and len(hand) < 6:
		hand.append(deck.pop(0))
	return (hand, deck)

def can_flash(attacking_hand, defending_hand, table, num, deck, wild):
	'''Determines if it's possible to flash back. Returns True or False.'''
	same_rank, with_lower_wilds = [], []
	for index, item in enumerate(attacking_hand):
		if item.rank() == table[-1].rank():
			same_rank.append(attacking_hand[index])	

	if len(same_rank) > 0:
		for index, item in enumerate(same_rank):
			if item.suit() == wild and item.rank() < 9:
				with_lower_wilds.append(same_rank[index])
			if item.suit() != wild:
				with_lower_wilds.append(same_rank[index])
		
		# Makes sure the other player has enough cards to beat the flash.
		if len(with_lower_wilds) > 0:
			if len(defending_hand) >= (num + 1):
				return True
			else:
				return False
		
		# If the deck is gone, checks to make sure the other player has enough cards.
		elif len(deck) == 0:
			if len(defending_hand) >= (num + 1):
				return True
			else:
				return False
	else:
		return False


def able_to_attack (hand, table, deck, wild):
	'''Checks for available attacks. Returns True or False.'''
	possible = []
	rank_list = []

	# If no cards have been played, attacking is always possible.
	if len(table) == 0:
		return True

	# If cards have been played, only matching ranks can be played.
	else:

		# If early in the game, low wilds are okay.
		if len(deck) > 15:
			for item in table:
				rank_list.append(item.rank())

			for card in hand:
				if card.rank() in rank_list:
					if card.suit() != wild:
						possible.append(card)
					if card.suit() == wild and card.rank() < 8:
						possible.append(card)
			if len(possible) > 0:
				return True
			return False
		
		# If in the middle of the game, middle wilds are okay.
		elif 5 < len(deck) <= 15:
			for item in table:
				rank_list.append(item.rank())
			for card in hand:
				if card.rank() in rank_list:
					if card.suit() != wild:
						possible.append(card)
					if card.suit() == wild and card.rank() < 11:
						possible.append(card)
			if len(possible) > 0:
				return True
			return False
		
		# Or at the end, any card can be played.
		else:
			for item in table:
				rank_list.append(item.rank())
			for card in hand:
				if card.rank() in rank_list:
					possible.append(card)
			if len(possible) > 0:
				return True
			return False

def is_game_over(hand_a, hand_b, deck):
	'''Checks to see if the game has ended. Returns True or False.'''
	condition_01 = [len(deck) == 0, len(hand_a) == 0]
	condition_02 = [len(deck) == 0, len(hand_b) == 0]
	if all(condition_01) == True:
		return True
	if all(condition_02) == True:
		return True
	return False

def first_deal():
	'''Sets up the deck and the wild suit, and deals out the cards.'''
	players_hand = []
	comp_hand = []
	d = new_deck()
	deck = permute(d)
	
	# Dealing
	for item in deck[:12:2]:
		comp_hand.append(item)
	for item in deck[1:12:2]:
		players_hand.append(item)
	del (deck[:12])

	# Reveal wild, then move it to the end of the deck.
	wild = reveal_wild(deck)
	deck.append(deck.pop(0))
	return (deck, players_hand, comp_hand, wild)


def conclude_turn(hand_a, hand_b, deck, table, discard_pile, hand_a_play_list):
	'''Distribute cards to both players and clear the table.'''
	hand_a, deck = draw_cards(hand_a, deck)			
	hand_b, deck = draw_cards(hand_b, deck)	
	hand_a_play_list.append('True')
	discard_pile += table
	table = []
	return (hand_a, hand_b, deck, table, discard_pile, hand_a_play_list)

def forfeit_turn(hand_a, hand_b, deck, table, hand_a_play_list):
	'''If a player can't play, the cards are eaten, the other player draws.'''
	for item in table:
		hand_a.append(item)
	hand_b, deck = draw_cards(hand_b, deck)
	hand_a_play_list.append('False')
	table = []
	return (hand_a, hand_b, deck, table, hand_a_play_list)

def flash_back(hand, table):
	'''Selects a flashable card and returns it.'''
	print ('running def flash_back')
	rank_list = list(filter(lambda x: x.rank()==table[-1].rank(), hand))
	min_rank_list = []
	print ('rank list: ' + str(rank_list))
	
	# Sorting by rank.
	while rank_list:
		minimum = rank_list[0]  # Arbitrary number in list 
		for card in rank_list: 
			if card < minimum:
				minimum = card
		min_rank_list.append(minimum)
		rank_list.remove(minimum)
	print ('min_rank_list: ' + str(min_rank_list))

	table.append(min_rank_list[0])
	hand.remove(min_rank_list[0])
	return (hand, table)

def new_flash_back(hand, table, deck, wild):
	'''Testing a new flash_back function that first checks for non wilds.'''
	print ('new flash back...')
	first, not_playable, not_wild, playable = [], [], [], []
	
	# First check for matching ranks:
	for item in hand:
		if item.rank() == table[-1].rank():
			first.append(item)
		else:
			not_playable.append(item)
	
	print ('first: ' + str(first))
	print ('not_playable: ' + str(not_playable))
	
	# Then check game progress:

	# If it's early in the game, use low wilds:
	if len(deck) > 15:
		print ("len(deck) > 15")
		for item in first:
			if item.suit() == wild and item.rank() < 9:
				playable.append(item)
			elif item.suit() == wild and item.rank() >= 9:
				not_playable.append(item)
			else:
				not_wild.append(item)

			print ('playable: ' + str(playable))
			print ('not_playable: ' + str(not_playable))
			print ('not_wild : ' + str (not_wild))

		if len(not_wild) > 0:
			print ('len(not_wild) > 0')
			table.append(not_wild.pop(0))
			hand = playable + not_playable + not_wild
			return (hand, table)
		elif len(playable) > 0:
			print ('len(playable) > 0')
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		else:
			print ('nope')
			return (hand, table)

	# If it's later in the game, use middle wilds:
	elif 5 < len(deck) <= 15:
		print ('5 < len(deck) <= 15')
		for item in first:
			if item.suit() == wild and item.rank() < 11:
				playable.append(item)
			elif item.suit() == wild and item.rank() >= 11:
				not_playable.append(item)
			else:
				not_wild.append(item)

			print ('playable: ' + str(playable))
			print ('not_playable: ' + str(not_playable))
			print ('not_wild : ' + str (not_wild))

		if len(not_wild) > 0:
			print ('len(not_wild) > 0')
			table.append(not_wild.pop(0))
			hand = playable + not_playable + not_wild
			return (hand, table)
		elif len(playable) > 0:
			print ('len(playable) > 0')
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		else:
			print ('nope')
			return (hand, table)

	# Or if the game is almost over, use any wild:
	else:
		print ('len(deck) < 5')
		if len(first) > 0:
			table.append(first.pop(0))
			hand = first + not_playable
			return (hand, table)





# Main game:

def durak_main():
	'''A function to make Durak play Durak by itself.'''	
	# Setting up the game:
	table, player_play_list, comp_play_list, discard_pile = [], [], [], []
	deck, players_hand, comp_hand, wild = first_deal()
	attacking = decide_turn()
	print ("Decide turn: " + str(attacking))
	game_over = False
	wild_card = deck[-1]
	turn = 1
	cutoff = 75
	print ("\n\nTurn: " + str(turn))	
	print ("Players_hand: " + str(players_hand))
	print ("Comps_hand:   " + str(comp_hand))
	print ("Wild: " + str(deck[-1]))
	print ("Deck: " + str(deck))


	# Important debugging variables:
	prompt_turn = "\n\nTurn: "
	prompt_comp_hand = "Comp hand:   "
	prompt_play_hand = "Player hand: "
	prompt_table     = "Table:       "
	prompt_wild      = "Wild: "
	prompt_deck      = "\nDeck:\n" 


	# Main loop
	while not game_over:
		# The "player" is attacking.
		if attacking == True:

			# Make sure the game hasn't ended, or something hasn't gone wrong...
			if is_game_over (players_hand, comp_hand, deck) == True or turn > cutoff:
				game_over = True
				continue

			# If a card is not able to be played, the turn ends. Play will take place automatically on a new turn.
			if able_to_attack(players_hand, table, deck, wild) == False:
				print ("Player concludes turn.")
				print (prompt_play_hand + str(players_hand))
				print (prompt_table + str(table))
				players_hand, comp_hand, deck, table, discard_pile, player_play_list = conclude_turn(players_hand, comp_hand, deck, table, discard_pile, player_play_list)						
				turn += 1
				print (prompt_turn + str(turn))
				print (prompt_deck + str(deck))
				print (prompt_play_hand + str(players_hand))
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_wild + str(wild_card))
				attacking = False
				continue

			if turn >= 30 and len(table) > 0:
				print ("Yikes, let's get this game over already...")
				print ("Player concludes turn.")
				print (prompt_play_hand + str(players_hand))
				print (prompt_table + str(table))
				players_hand, comp_hand, deck, table, discard_pile, player_play_list = conclude_turn(players_hand, comp_hand, deck, table, discard_pile, player_play_list)						
				turn += 1
				print (prompt_turn + str(turn))
				print (prompt_deck + str(deck))
				print (prompt_play_hand + str(players_hand))
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_wild + str(wild_card))
				attacking = False
				continue

			else:
				# If a card can be played, then one is:
				players_hand, table = test_comp_attack(players_hand, table, deck, wild)
				print ("\nPlayer attacks...")
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_play_hand + str(players_hand))
				print (prompt_table + str(table))

				# ...and if that play ended the game....
				if is_game_over(players_hand, comp_hand, deck) == True:
					print ("\n\nPlayer wins.")
					game_over = True
					continue

				else:
					#Otherwise, the computer gets a chance to defend:
					new_table = []
					for card in table:
						new_table.append(card)
					print ("Comp tries to defend.")
					comp_hand, table = comp_defend(comp_hand, players_hand, table, deck, wild, 1, comp_play_list)
				
					# If the computer doesn't play:
					if len(new_table) == len(table):
						print ("Forfeits.")
						print (prompt_comp_hand + str(comp_hand))
						print (prompt_table + str(table))
						comp_hand, players_hand, deck, table, comp_play_list = forfeit_turn(comp_hand, players_hand, deck, table, comp_play_list)
						turn += 1
						print (prompt_turn + str(turn))
						print (prompt_deck + str(deck))
						print (prompt_play_hand + str(players_hand))
						print (prompt_comp_hand + str(comp_hand))
						print (prompt_wild + str(wild_card))
						attacking = True
						continue

					# If the computer does play, and ends the game:
					if is_game_over(players_hand, comp_hand, deck) == True:
						print ("\n\nComp wins.")
						game_over = True
						continue

					# If the play occurs without flashing, we return for the player to continue attacking:
					if table[-1].rank() != table[-2].rank():
						print ("Beats card.")
						print (prompt_comp_hand + str(comp_hand))
						print (prompt_table + str(table))
						attacking = True
						continue

					# Double checking that the card was really a flash and not just beaten by a high wild.
					if table[-1].suit() == wild and table[-1].rank() >= 9:
						print ("Beats card.")
						print (prompt_comp_hand + str(comp_hand))
						print (prompt_table + str(table))
						attacking = True
						continue

					else:
						# Or if the play is flashed back:   **  FLASH 1 of 3  **
						new_table = []
						for card in table:
							new_table.append(card)
						print ("Comp FLASH BACK 1")
						print (prompt_table + str(table))
						print ("Player tries to defend...")
						players_hand, table = test_comp_defend(players_hand, comp_hand, table, deck, wild, 2, player_play_list)

						# If the player didn't play during the flash, her turn ends:
						if len(new_table) == len(table):
							print ("Forfeits.")
							print (prompt_play_hand + str(players_hand))
							print (prompt_table + str(table))
							players_hand, comp_hand, deck, table, player_play_list = forfeit_turn(players_hand, comp_hand, deck, table, player_play_list)
							print (prompt_turn + str(turn))
							print (prompt_deck + str(deck))
							print (prompt_play_hand + str(players_hand))
							print (prompt_comp_hand + str(comp_hand))
							print (prompt_wild + str(wild_card))
							attacking = False
							continue

						# ...and if she did and that ended the game....
						if is_game_over(players_hand, comp_hand, deck) == True:
							print ("\n\nPlayer wins.")
							game_over = True
							continue			

						# If she didn't flash back and just beat the cards:
						if len(table)%2 == 0:
							print ("Beats card.")
							print (prompt_play_hand + str(players_hand))
							print (prompt_table + str(table))
							attacking = False
							continue

						else:
							# Otherwise, if she did flash...
							new_table = []
							for card in table:
								new_table.append(card)
							print ("Player FLASH BACK 2")
							print (prompt_table + str(table))
							print ("Comp tries to defend..")
							comp_hand, table = comp_defend(comp_hand, players_hand, table, deck, wild, 3, comp_play_list)

							# If the computer didn't play during the flash:
							if len(new_table) == len(table):
								print ("Forfeits.")
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_table + str(table))
								comp_hand, players_hand, deck, table, comp_play_list = forfeit_turn(comp_hand, players_hand, deck, table, comp_play_list)
								turn += 1
								print (prompt_turn + str(turn))
								print (prompt_deck + str(deck))
								print (prompt_play_hand + str(players_hand))
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_wild + str(wild_card))
								attacking = True
								continue

							# Or if it did and that ended the game....
							if is_game_over(players_hand, comp_hand, deck) == True:
								print ("Comp wins.")
								game_over = True
								continue			

							# If the computer didn't flash back, but beat the cards, we return to continue the turn:
							if table[-1].rank() != table[-2].rank():
								print ("Beats card.")
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_table + str(table))
								attacking = True
								continue

							# Double checking that this isn't a flash.
							if table[-1].suit() == wild and table[-1].rank() >= 9:
								print ("Beats card.")
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_table + str(table))
								attacking = True
								continue

							else:
								# Or if the computer did flash a final time:     **   FLASH 3 of 3   **
								new_table = []
								for card in table:
									new_table.append(card)
								print ("Comp FLASH BACK 3...")
								print (prompt_table + str(table))
								print ("Player tries to defend...")
								players_hand, table = test_comp_defend(players_hand, comp_hand, table, deck, wild, 4, player_play_list)

								#If the player can't beat the final flash, her turn is lost
								if len(new_table) == len(table):
									print ("Forfeits.")
									print (prompt_play_hand + str(players_hand))
									print (prompt_table + str(table))
									players_hand, comp_hand, deck, table, player_play_list = forfeit_turn(players_hand, comp_hand, deck, table, player_play_list)
									turn += 1
									print (prompt_turn + str(turn))
									print (prompt_deck + str(deck))
									print (prompt_play_hand + str(players_hand))
									print (prompt_comp_hand + str(comp_hand))
									print (prompt_wild + str(wild_card))
									attacking = False
									continue

								# ...and if she did and that ended the game....
								if is_game_over(players_hand, comp_hand, deck) == True:
									print ("\n\nPlayer wins.")
									game_over = True
									continue			
	
								#Or if she just beat the card, we continue to finish the turn.
								else:
									print ("Beats card.")
									print (prompt_play_hand + str(players_hand))
									print (prompt_table + str(table))
									attacking = False
									continue

		# Now it's the computer's turn to attack!
		if attacking == False:
			if is_game_over (players_hand, comp_hand, deck) == True or turn > cutoff:
				game_over = True
				continue
			
			# If a card is not able to be played, the turn ends. Play will take place automatically on a new turn.
			if able_to_attack(comp_hand, table, deck, wild) == False:
				print ("Comp concludes turn.")
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_table + str(table))
				comp_hand, players_hand, deck, table, discard_pile, comp_play_list = conclude_turn(comp_hand, players_hand, deck, table, discard_pile, comp_play_list)
				turn += 1
				print (prompt_turn + str(turn))
				print (prompt_deck + str(deck))
				print (prompt_play_hand + str(players_hand))
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_wild + str(wild_card))
				attacking = True
				continue

			if turn >= 30 and len(table) > 0:
				print ("Yikes, let's get this game over already...")
				print ("Comp concludes turn.")
				print (prompt_play_hand + str(players_hand))
				print (prompt_table + str(table))
				comp_hand, players_hand, deck, table, discard_pile, player_play_list = conclude_turn(comp_hand, players_hand, deck, table, discard_pile, player_play_list)						
				turn += 1
				print (prompt_turn + str(turn))
				print (prompt_deck + str(deck))
				print (prompt_play_hand + str(players_hand))
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_wild + str(wild_card))
				attacking = False
				continue

			else:
			# If a card can be played, then one is:
				comp_hand, table = comp_attack(comp_hand, table, deck, wild)
				print ("\nComp attacks...")
				print (prompt_play_hand + str(players_hand))
				print (prompt_comp_hand + str(comp_hand))
				print (prompt_table + str(table))

				# ...and if that play ended the game....
				if is_game_over(players_hand, comp_hand, deck) == True:
					print ("\n\nComp wins.")
					game_over = True
					continue

				#Otherwise, the player gets a chance to defend:
				else:
					new_table = []
					for card in table:
						new_table.append(card)
					print ("Player tries to defend...")
					players_hand, table = test_comp_defend(players_hand, comp_hand, table, deck, wild, 1, player_play_list)

					# If the player doesn't play:
					if len(new_table) == len(table):
						print ("Forfeits.")
						print (prompt_play_hand + str(players_hand))
						print (prompt_table + str(table))
						players_hand, comp_hand, deck, table, player_play_list = forfeit_turn(players_hand, comp_hand, deck, table, player_play_list)
						turn += 1
						print (prompt_turn + str(turn))
						print (prompt_deck + str(deck))
						print (prompt_play_hand + str(players_hand))	
						print (prompt_comp_hand + str(comp_hand))
						print (prompt_wild + str(wild_card))
						attacking = False
						continue

					# If the player does play, and ends the game:
					if is_game_over(players_hand, comp_hand, deck) == True:
						print ("\n\nPlayer wins.")
						game_over = True
						continue

					# If the play occurs without flashing, we return for the computer to continue attacking:
					if table[-1].rank() != table[-2].rank():
						print ("Beats card.")
						print (prompt_play_hand + str(players_hand))
						print (prompt_table + str(table))
						attacking = False
						continue

					# Double checking that this wasn't a flash...
					if table[-1].suit() == wild and table[-1].rank() >= 9:
						print ("Beats card.")
						print (prompt_play_hand + str(players_hand))
						print (prompt_table + str(table))
						attacking = True
						continue

					else:
					# Or if the play is flashed back:   **  FLASH 1 of 3  **
						new_table = []
						for card in table:
							new_table.append(card)
						print ("Player FLASH BACK 1...")
						print (prompt_table + str(table))
						print ("Comp tries to defend...")
						comp_hand, table = comp_defend(comp_hand, players_hand, table, deck, wild, 2, comp_play_list)

						# If the computer didn't play during the flash, it's turn ends:
						if len(new_table) == len(table):
							print ("Forfeits turn.")
							print (prompt_comp_hand + str(comp_hand))
							print (prompt_table + str(table))
							comp_hand, players_hand, deck, table, comp_play_list = forfeit_turn(comp_hand, players_hand, deck, table, comp_play_list)
							turn += 1
							print (prompt_turn + str(turn))
							print (prompt_deck + str(deck))
							print (prompt_play_hand + str(players_hand))	
							print (prompt_comp_hand + str(comp_hand))
							print (prompt_wild + str(wild_card))
							attacking = True
							continue

						# ...and if that play ended the game....
						if is_game_over(players_hand, comp_hand, deck) == True:
							print ("\n\nComp wins.")
							game_over = True
							continue

						# If it didn't flash back and just beat the cards:
						if len(table)%2 == 0:
							print ("Beats card.")
							print (prompt_comp_hand + str(comp_hand))
							print (prompt_table + str(table))
							attacking = True
							continue

						else:
						# Otherwise, if the computer flashed again:    ** Flash 2 of 3
							new_table = []
							for card in table:
								new_table.append(card)
							print ("Comp FLASH BACK 2...")
							print (prompt_table + str(table))
							print ("Player tries to defend...")
							players_hand, table = test_comp_defend(players_hand, comp_hand, table, deck, wild, 3, player_play_list)

							# If the player didn't play during the flash:
							if len(new_table) == len(table):
								print ("Forfeits.")
								print (prompt_play_hand + str(players_hand))
								print (prompt_table + str(table))
								players_hand, comp_hand, deck, table, player_play_list = forfeit_turn(players_hand, comp_hand, deck, table, player_play_list)
								turn += 1
								print (prompt_turn + str(turn))
								print (prompt_deck + str(deck))
								print (prompt_play_hand + str(players_hand))	
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_wild + str(wild))
								attacking = False
								continue

							# If the player does play, and ends the game:
							if is_game_over(players_hand, comp_hand, deck) == True:
								print ("\n\nPlayer wins.")
								game_over = True
								continue
			

							# If she didn't flash back, but beat the cards, we return to continue the turn:
							if table[-1].rank() != table[-2].rank:
								print ("Beats card: ")
								print (prompt_play_hand + str(players_hand))
								print (prompt_table + str(table))
								attacking = False
								continue

							# If she didn't flash back, but beat the cards, we return to continue the turn:
							if table[-1].suit() == wild and table[-1].rank() >= 9:
								print ("Beats card.")
								print (prompt_comp_hand + str(comp_hand))
								print (prompt_table + str(table))
								attacking = True
								continue

							else:
							# Or if the player did flash a final time:     **   FLASH 3 of 3   **
								new_table = []
								for card in table:
									new_table.append(card)
								print ("Player FLASH BACK 3...")
								print (prompt_table + str(table))
								print ("Comp tries to defend...")
								comp_hand, table = comp_defend(comp_hand, players_hand, table, deck, wild, 4, comp_play_list)

								#If the comp can't beat the final flash, its turn is lost
								if len(new_table) == len(table):
									print ("Forfeits.")
									print (prompt_comp_hand + str(comp_hand))
									print (prompt_table + str(table))
									comp_hand, players_hand, deck, table, comp_play_list = forfeit_turn(comp_hand, players_hand, deck, table, comp_play_list)
									turn += 1
									print (prompt_turn + str(turn))
									print (prompt_deck + str(deck))
									print (prompt_play_hand + str(players_hand))	
									print (prompt_comp_hand + str(comp_hand))
									print (prompt_wild + str(wild_card))
									attacking = True
									continue

								# ...and if it did and that ended the game....
								if is_game_over(players_hand, comp_hand, deck) == True:
									print ("\n\nComp wins.")
									game_over = True
									continue
									
								else:
								#Or if it just beat the card, we continue to finish the turn.
									print ("Beats card...")
									print (prompt_comp_hand + str(comp_hand))
									print (prompt_table + str(table))
									attacking = True
									continue
	
	# After the game is over (playing = False), the winners are announced:
	all_cards = len(deck) + len(discard_pile) + len(comp_hand) + len(players_hand) + len(table)
	print ('Total cards:    ' + str(all_cards))
	print (prompt_comp_hand + str(comp_hand))
	print (prompt_play_hand + str(players_hand))
	print ("Game concluded in: " + str(turn) + " turns....\n")
	return (players_hand, comp_hand, turn, table, discard_pile)

# AI Attack and Defense

# Support functions for attacking.

def att_table_empty(hand, table, deck, wild):
	'''How the comp should attack if no cards have yet been played.'''
	print ('attack - table empty')
	wilds, not_wilds = [], []
	# Separate wilds and non-wilds:
	for card in hand:
		if card.suit() == wild:
			wilds.append(card)
	for card in hand:
		if card.suit() != wild:
			not_wilds.append(card)
	
	if len(deck) > 5:
		# If non-wilds are available, play the lowest. If not, play the lowest wild.
		if len(not_wilds) > 0:
			print ('len(non_wilds)>0')
			not_wilds.sort()
			table.append(not_wilds.pop(0))
			hand = wilds + not_wilds
			return (hand, table)
	
		# If nothing, play anything.
		else:
			print ('playing anything...')
			hand.sort()
			table.append(hand.pop(0))
			return (hand, table)

	else:
		if len(wilds) > 3:
			wilds.sort()
			table.append(wilds.pop(0))
			hand = wilds + not_wilds
			return (hand, table)
		else:
			hand.sort()
			table.append(hand.pop(0))
			return (hand, table)


def att_table_not_empty(hand, table, deck, wild):
	''' How the comp should attack if cards have been played.'''
	rank_list, playable, not_playable = [], [], []
	print ("att_table_not_empty")
	# Find the ranks of all cards on the table.
	for item in table:
		rank_list.append(item.rank())

	# Make lists of matching ranks depending on progress in game:
	
	# If it's early in the game:
	if len(deck) > 15:
		print ("len(deck) > 15")

		for card in hand:
			if card.rank() in rank_list:
				if card.suit() != wild:
					playable.append(card)
			if card.rank() in rank_list:
				if card.suit() == wild and card.rank()>8:
					not_playable.append(card)
			if card.rank() in rank_list:
				if card.suit() == wild and card.rank()<=8:
					playable.append(card)
			if card.rank() not in rank_list:
				not_playable.append(card)

		print ("playable: " + str(playable))
		print ('not playable: ' + str(not_playable))
		if len(playable) > 0:
			playable.sort()
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		return (hand, table)

	# If it's later in the game:
	elif 5 < len(deck) <= 15:
		print ('5<len(deck)<=15')
		for card in hand:
			if card.rank() in rank_list:
				if card.suit() != wild:
					playable.append(card)
			if card.rank() in rank_list:
				if card.suit() == wild and card.rank()>11:
					not_playable.append(card)
			if card.rank() in rank_list:
				if card.suit() == wild and card.rank()<=11:
					playable.append(card)
			if card.rank() not in rank_list:
				not_playable.append(card)
		print ("playable: " + str(playable))
		print ('not playable: ' + str(not_playable))
		if len(playable) > 0:
			playable.sort()
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		return (hand, table)
	
	# If it's the end of the game:
	else:
		print ('len(deck) < 5')
		for card in hand:
			if card.rank() in rank_list:
				playable.append(card)
			else:
				not_playable.append(card)
		print ("playable: " + str(playable))
		print ('not playable: ' + str(not_playable))
		if len(playable) > 0:
			playable.sort()
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		return (hand, table)


def comp_attack(hand, table, deck, wild):
	'''The main function dealing with computer attacking.'''
	# If not cards, draw some!
	if len(hand) == 0:
		print ("hand = 0, drawing")
		hand, deck = draw_cards(hand, deck)

	# First off, if the table is empty:
	elif len(table) == 0:
		print ("table = 0")
		# Play the lowest non-wild:
		hand, table = att_table_empty(hand, table, deck, wild)
		return (hand, table)

	# Second, if the table is NOT empty:
	else:
		print ('table not empty')		
		# Return the lowest card of matching rank:	
		hand, table = att_table_not_empty(hand, table, deck, wild)
		return (hand, table)
	
# Functions for Defense

def def_card_processing (hand, table, holding ,val, sorted_playable, wild):
	'''Adds potential plays to holding, removes from hand.'''
	new_hand = []
	print ('sorted_playable_not_zero')
	if len(sorted_playable) > 0:
		holding.append(sorted_playable.pop(0))

		if len(holding) == 0:
			print ("holding 0, returning")
			return (hand, table, holding)
		else:
			for item in hand:
				if item._id != holding[-1]._id:
					new_hand.append(item)
			print ('after append: ')
			print ('holding: ' + str(holding))
			print ('new_hand: ' + str(new_hand))
			hand = new_hand

			if is_card_beatable(table, holding, wild, val) == True:
				return (hand, table, holding)
			else:
				hand.append(holding.pop(-1))
				return (hand, table, holding)
	else:
		return (hand, table, holding)


def def_card_not_wild(hand, table, wild, holding, val):
	'''If the card to defend against is not wild.'''
	print ('def card not wild: ')
	playable, suit_list, sorted_playable, new_hand = [], [], [], []
	for card in hand:
		if card.suit() == table[-val].suit():
			suit_list.append(card)
	print ("suit_list: " + str(suit_list))
	for item in suit_list:
		if item.rank() > table[-val].rank():
			playable.append(item)
	print ('playable: ' + str(playable))
	
	while playable:
		minimum = playable[0]  # Arbitrary number in list 
		for card in playable: 
			if card < minimum:
				minimum = card
		sorted_playable.append(minimum)
		playable.remove(minimum)
	print ('sorted_playable:' + str(sorted_playable))
	
	if len(sorted_playable) == 0:
		print ('sorting_playable = 0')
		print ('hand :' + str(hand))
		return (hand, table, holding)
	
	else:
		hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
		return (hand, table,holding)
	

def def_use_low_wilds(hand, table, wild, holding, val):
	'''Checking the hand for lower-valued wilds'''
	print ('def use low wilds')
	playable, sorted_playable, new_hand = [], [], []

	for card in hand:
		if card.suit() == wild and card.rank() < 8:
			playable.append(card)

	while playable:
		minimum = playable[0]  # Arbitrary number in list 
		for card in playable: 
			if card < minimum:
				minimum = card
		sorted_playable.append(minimum)
		playable.remove(minimum)
	
	print ('sorted playable: ' + str(sorted_playable))
	
	if len(sorted_playable) == 0:
		return (hand, table, holding)
	else:
		hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
		return (hand, table, holding)


def def_use_middle_wilds(hand, table, wild, holding, val):
	'''Checking the hand for mid-level wilds.'''
	print ('def use middle wilds')
	playable, sorted_playable, new_hand = [], [], []

	for card in hand:
		if card.suit() == wild and card.rank() < 11:
			playable.append(card)

	
	while playable:
		minimum = playable[0]  # Arbitrary number in list 
		for card in playable: 
			if card < minimum:
				minimum = card
		sorted_playable.append(minimum)
		playable.remove(minimum)

	if len(sorted_playable) == 0:
		return (hand, table, holding)

	else:
		hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
		return (hand, table, holding)

def def_use_any_wild(hand, table, wild, holding, val):
	'''Finds any wilds in the hand.'''
	playable, sorted_playable, new_hand = [], [], []

	print ('use any wild...')
	for card in hand:
		if card.suit() == wild:
			playable.append(card)

	while playable:
		minimum = playable[0]  # Arbitrary number in list 
		for card in playable: 
			if card < minimum:
				minimum = card
		sorted_playable.append(minimum)
		playable.remove(minimum)
	
	if len(sorted_playable) == 0:
		return (hand, table, holding)
	else:
		hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
		return (hand, table, holding)

def is_card_beatable(table, holding, wild, val):
	'''Checks if the card on the table can be beaten by the card in hand.'''
	# If the card on the table isn't a wild and the one in holding is:
	if table[-val].suit() != wild and holding[-1].suit() == wild:
		return True
	# If the card on the table is not a wild and the one in holding outranks it:
	elif table[-val].suit() != wild and holding[-1].rank() > table[-val].rank():
		return True
	# If the card on the table IS a wild and the one in holding is too:
	elif table[-val].suit() == wild and holding[-1].suit() == wild:
		# Double check that it outranks the table. If yes, True. Else, False.
		if table[-val].rank() < holding[-1].rank():
			return True
		else:
			return False
	# Otherwise, it isn't beatable.
	else:
		return False

def def_check_wild_cards (hand, table, wild, holding, val, deck, num, play_list):
	'''Handles processing that occurs when (1) the card to beat is a wild, or
	(2) the card is not a wild but couldn't be beaten with other cards, depending
	on progress in the game.'''
	print ("checking wild cards...")
	wild_list = []

	# If it's early in the game:
	if len(deck) > 15:
		print ('len(deck) > 15')
		
		# Let's see how many wilds are in hand:
		for card in hand:
			if card.suit() == wild:
				wild_list.append(card)

		print ('wild_list: ' + str(wild_list))
		# If there's a whole lot, use any wild:
		if len(wild_list) > 5:
			print ('lots of wilds...')
			hand, table, holding = def_use_any_wild(hand, table, wild, holding, val)
			return (hand, table, holding)

		# If there's a bunch, use middle wilds:
		elif len(wild_list) > 3:
			print ('a bunch of wilds')
			hand, table, holding = def_use_middle_wilds(hand, table, wild, holding, val)
			return (hand, table, holding)

		# If there's aren't a bunch of wilds:
		else:
			print ('not many wilds..')
			#And if there aren't a bunch of flashes:
			if num <= 2:
				print ('num <=2')

				# Find any low wilds.
				hand, table, holding = def_use_low_wilds(hand, table, wild, holding, val)
				return (hand, table, holding)		

			# Or if there are a bunch of flashes...
			else:
	
				# Find middle wilds.
				hand, table, holding = def_use_middle_wilds(hand, table, wild, holding, val)
				return (hand, table, holding)	
					
	# Or if it's late in the game:
	elif 5 < len(deck) <= 15:
		print ('elif 5 < len(deck) <= 15')
					
		# And there aren't too many flashes:
		if num <= 2:
			print ('num <= 2')

			# Use middle wilds
			hand, table, holding = def_use_middle_wilds(hand, table, wild, holding, val)
			return (hand, table, holding)	

			# If there are, use any wild.
		else:
			hand, table, holding = def_use_any_wild(hand, table, wild, holding, val)
			return (hand, table, holding)	

	# Or if it's the end of the game, use any wild:
	else:
		print ('else, near end of game...')
		# Use any wild.
		hand, table, holding = def_use_any_wild(hand, table, wild, holding, val)
		return (hand, table, holding)	

def comp_defend (hand, attacking_hand, table, deck, wild, num, play_list):
	'''Main function for handling computer defense. "Num" refers to the number of cards
	being defended against. Play_list is a running tally of whether the computer played or
	forfeited.'''
	
	# Make sure it has cards to play.
	if len(hand) == 0:
		print ('len = 0, drawing')
		hand, deck = draw_cards(hand, deck)

	# If it can flash back, it will flash back.
	if can_flash (hand, attacking_hand, table, num, deck, wild) == True:
		print ("can flash = True")
		hand, table = new_flash_back(hand, table, deck, wild)
		return (hand, table)

	# Otherwise, a loop to find a solution to every card that needs to be beaten:
	holding = []
	val = num # Val will decrease with each pass through the loop.
	loop = 0  # And 'loop' will increase with each pass.

	while val > 0:
		loop += 1
		print ("val = " + str(val))
		print ('holding: ' + str(holding))
		possible = []

		# If the card is not a wild:
		if table[-val].suit() != wild:
			print ('not wild == True')

			#A function to check for plays:
			hand, table, holding = def_card_not_wild(hand, table, wild, holding, val)
			print ('holding: ' + str(holding))
			
			# If there were plays...
			if len(holding) == loop:
				val -= 1
				continue
			
			# If not, check to see if a wild could be used:
			else:

				# Comp checks how long it has been playing:
				if len(play_list) > 5:
					has_been_playing = []
					print ('play list: ' + str(play_list[-5:0]))
					
					for item in play_list[-5:]:
						has_been_playing.append(item)
					
					# And whether it has forfeited 5 times in a row.
					if 'True' in has_been_playing == False:
						print ('True in has been playing == False')
						print ('using any wild...')
						
						# If yes, then look for any wild.
						hand, table, holding = def_use_any_wild(hand, table, wild, holding, val)
						if len(holding) != loop:
							val = 0
							continue
						else:
							val -= 1
							continue
					
					# If it hasn't forfeited 5 times in a row, check for wilds:
					else:
						print ("True in has been playing == True")
						hand, table, holding = def_check_wild_cards(hand, table, wild, holding, val, deck, num, play_list)

						if len(holding) != loop:
							val = 0
							continue
						else:
							val -= 1
							continue
				
				# And if it hasn't been playing that many turns yet, check for wilds:
				else:
					hand, table, holding = def_check_wild_cards(hand, table, wild, holding, val, deck, num, play_list)

					if len(holding) != loop:
						val = 0
						continue
					else:
						val -= 1
						continue
		
		# If the card IS a wild:
		else:
			print ("Card to beat is wild...")
			hand, table, holding = def_check_wild_cards (hand, table, wild, holding, val, deck, num, play_list)

			if len(holding) != loop:
				val = 0
				continue
			else:
				val -= 1
				continue

	# After the selection loop is over, check results:
	print ('check results...')
	print ('holding: ' + str(holding))
	print ('hand: ' + str(hand))
	print ('table: ' + str(table))

	if len(holding) == 0:
		print ('len(holding) == 0')
		return (hand, table)
		
	elif len(holding) == num:
		print ('len(holding) == num')
		print ('holding: ' + str(holding))
		for card in holding:
			table.append(card)
		return (hand, table)
	else:
		print ('len holding != to 0 or num')
		print ('holding: ' + str(holding))
		for card in holding:
			hand.append(card)
		return (hand, table)


# AI TEST FUNCTIONS

def def_test_use_any_wild(hand, table, wild, holding, val):
	'''Test function. Finds any wild.'''
	playable, sorted_playable, new_hand = [], [], []
	print ('test use any wild')
	
	# If the card is a wild, only a higher wild can beat it.
	if table[-val].suit() == wild:
		for card in hand:
			if card.suit() == wild and card.rank() > table[-val].rank():
				playable.append(card)

		while playable:
			minimum = playable[0]
			for card in playable:
				if card < minimum:
					minimum = card
			sorted_playable.append(minimum)
			playable.remove(minimum)

		if len(sorted_playable) == 0:
			return (hand, table, holding)
		else:
			# Or if there is a play, call the function that handles card swapping.
			hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
			return (hand, table, holding)

	# If it's not wild, any wild will do:
	else:
		for card in hand:
			if card.suit() == wild:
				playable.append(card)
		print ('playable: ' + str(playable))
	
		# Sorting the cards.
		while playable:
			minimum = playable[0]  # Arbitrary number in list 
			for card in playable: 
				if card < minimum:
					minimum = card
			sorted_playable.append(minimum)
			playable.remove(minimum)
	
		print ('sorted_playable: ' + str(sorted_playable))
		
		# If nothing to play, return.
		if len(sorted_playable) == 0:
			return (hand, table, holding)
		else:
			print ('else...')
			# Or if there is a play, call the function that handles card swapping.
			hand, table, holding = def_card_processing(hand, table, holding ,val, sorted_playable, wild)
			return (hand, table, holding)


def def_test_card_processing (hand, table, holding ,val, playable, wild):
	'''Test card processing.'''
	sorted_playable, new_hand = [], []
	print ('def test card processing')
	if len(playable) > 0:
		print ('playable greater than 0')
		while playable:
			minimum = playable[0]  # Arbitrary number in list 
			for card in playable: 
				if card < minimum:
					minimum = card
			sorted_playable.append(minimum)
			playable.remove(minimum)
		holding.append(sorted_playable.pop(0))

		print ('holding after sort: ' + str(holding))
		if len(holding) == 0:
			return (hand, table, holding)
		else:
			# Double check for duplicates.
			for item in hand:
				if item._id != holding[-1]._id:
					new_hand.append(item)
			hand = new_hand

			#Check if the card is going to beat the one on the table.
			if is_card_beatable(table, holding, wild, val) == True:
				return (hand, table, holding)
			else:
				hand.append(holding.pop(-1))
				return (hand, table, holding)
	else:
		return (hand, table, holding)

def test_comp_defend (hand, attacking_hand, table, deck, wild, num, play_list):
	'''A test version of comp attack. Plays anything playable.'''

	# First, make sure the comp has cards to play with!
	if len(hand) == 0:
		hand, deck = draw_cards(hand, deck)

	# Then, if it can flash back, it will flash back...
	if test_can_flash (hand, attacking_hand, table, num, deck, wild) == True:
		print ('can flash == True')
		hand, table = new_flash_back(hand, table, deck, wild)
		return (hand, table)

	# Otherwise, a loop to find a solution to every card that needs to be beaten:
	holding = []
	val = num # Val will decrease with each pass through the loop.
	loop = 0  # And 'loop' will increase with each pass.

	while val > 0:
		loop += 1
		possible = []
		print ("val: " + str(val))
		print ("holding: " + str(holding))

		# If the card is NOT a wild:
		if table[-val].suit() != wild:
			print ('card not wild...')
			suit_list, playable = [], []
			for card in hand:
				if card.suit() == table[-val].suit():
					suit_list.append(card)
			for item in suit_list:
				if item.rank() > table[-val].rank():
					playable.append(item)
			print ('suit_list: ' + str(suit_list))
			print ('playable: ' + str(playable))

			if len(playable) > 0:
				hand, table, holding = def_test_card_processing (hand, table, holding ,val, playable, wild)
			
				# If there were plays:
				if len(holding) == loop:
					val -= 1
					continue
			
				# If not, check to see if a wild could be used:
				else:
					print ('could a wild be used?')
					hand, table, holding = def_test_use_any_wild(hand, table, wild, holding, val)
					if len(holding) != loop:
						val = 0
						continue
					else:
						val -= 1
						continue
			# If not, check to see if a wild could be used:
			else:
				print ('could a wild be used # 2?')
				hand, table, holding = def_test_use_any_wild(hand, table, wild, holding, val)
				if len(holding) != loop:
					val = 0
					continue
				else:
					val -= 1
					continue
					
		# If the card IS a wild:
		else:
			print ('card is wild...')
			hand, table, holding = def_test_use_any_wild(hand, table, wild, holding, val)
			if len(holding) != loop:
				val = 0
				continue
			else:
				val -= 1
				continue

	# After the selection loop is over, check results:
	print ('checking results...')
	print ('holding: ' + str(holding))
	if len(holding) == 0:
		return (hand, table)	
	elif len(holding) == num:
		for card in holding:
			table.append(card)
		return (hand, table)
	else:
		for card in holding:
			hand.append(card)
		return (hand, table)


def test_can_flash(attacking_hand, defending_hand, table, num, deck, wild):
	'''Determines if it's possible to flash back. Returns True or False.'''
	same_rank = []
	for item in attacking_hand:
		if item.rank() == table[-1].rank():
			same_rank.append(item)	

	if len(same_rank) > 0:
		if len(defending_hand) >= (num + 1):
			return True
	return False

def test_comp_attack(hand, table, deck, wild):
	'''A test function for attack. Plays anything playable.'''
	print ('test comp attack')
	# If no cards, draw some!
	if len(hand) == 0:
		hand, deck = draw_cards(hand, deck)

	# First off, if the table is empty:
	if len(table) == 0:
		print ('table empty')
		
		# Play the lowest card.
		hand, table = att_table_empty(hand, table, deck, wild)
		return (hand, table)

	# Second, if the table is NOT empty:
	else:
		print ('table not empty')
		rank_list, playable, not_playable = [], [], []

		for item in table:
			rank_list.append(item.rank())
		
		for card in hand:
			if card.rank() in rank_list:
				playable.append(card)
			else:
				not_playable.append(card)
		
		if len(playable) > 0:
			playable.sort()
			table.append(playable.pop(0))
			hand = playable + not_playable
			return (hand, table)
		return (hand, table)



