from random import randint

class Card(object):
	"""A class for all playing cards used in Durak. Creates a unique number
	that can be calculated to find a suit (an int between 0 and 4) and a
	rank (an int between 0 and 12) to classify the individual cards."""
	
	def __init__(self, n):
		if n in range(0, 52):
			self._id = n
		else:
			raise Exception("Card numbers are from 0 to 51 !!!")
		# self.clubs = 0
		# self.diamonds = 1
		# self.hearts = 2
		# self.spades = 3

	def __repr__(self):
		# An integer between 0 and 51
		# return str(self._id)

		#A number/letter for rank and a symbol for suit:
		suit_sym = {0: '\u2663', 1: '\u2666', 2: '\u2665', 3: '\u2660'}
		rank_sym = {
			0: ' 2', 1: ' 3', 2: ' 4', 3: ' 5', 4: ' 6', 5: ' 7', 6: ' 8', 7: ' 9',
			8 : '10', 9: ' J', 10: ' Q', 11: ' K', 12: ' A'
			}
		return rank_sym[self.rank()] + suit_sym[self.suit()]
	
	# def __iter__(self):
	# 	return self._id

			# yield int(self.id%13)

	# def __eq__(self, other):
	# 	return self._id == other._id
	
	# def __lt__(self, other):
	# 	return self._id < other._id

	
	def __eq__(self, other):
		return self._id%13 == other._id%13
	

	def __lt__(self, other):
		return self._id%13 < other._id%13
	
	# # For suits
	# def __gt__(self, other):
	# 	return self._id//13 > other._id//13

	def rank(self):
		# Return an integer between 0 (2) and 12(Ace)
		return self._id % 13

	def suit (self):
		# Return a suit number: 0 = clubs, 1 = diamonds, 2 = hearts, 3 = spades
		return self._id // 13


def new_deck():
	# Create a list of 52 card objects. An entire deck without duplicates.
	return [Card(i) for i in range (52)]

def permute(sequence):
	# Shuffle a list. For shuffling the deck
	for i in range(0, len(sequence) - 1):
		r = randint(i, len(sequence)-1)
		sequence[i], sequence[r] = sequence[r], sequence[i]
	return sequence