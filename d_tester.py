import game_functions_tester_bare as bare
import game_functions_tester_brief as brief
import game_functions_tester_debug as debug
import sys

# Support functions

def game_test_runner(number, type_of_test):
	val = number
	player_wins, comp_wins, turn_list, table_list, discard_list = [], [], [], [], []

	while val > 0:
		player, comp, turn, table, discard_pile = type_of_test.durak_main()
		total = len(player) + len(comp) + len(table) + len(discard_pile)
		
		# if total != 52:
		# 	print ("Whoops, somethin' done gone wrong :(")
		# 	val = 0
		# 	continue

		# if len(player) and len(comp) != 0:
		# 	print ("Somehow both lost!")
		# 	val = 0
		# 	continue

		# if len(player) and len(comp) == 0:
		# 	print ("Somehow both won!")
		# 	val = 0
		# 	continue

		if turn > 70:
			print ("Oh no, this game went on WAY too long....")	
			val = 0
			continue

		if len(player) == 0:
			player_wins.append(1)
		else:
			player_wins.append(0)
		
		if len(comp) == 0:
			comp_wins.append(1)
		else:
			comp_wins.append(0)
		
		turn_list.append(turn)
		discard_list.append(total)
		val -= 1
		continue

	if len(player_wins) > 0:
		print ("     Trials : " + str(number))
		print ("Player wins : " + str(sum(player_wins)))
	if len(comp_wins) > 0:
		print ("  Comp wins : " + str(sum(comp_wins)))
	if len(player_wins) and len(comp_wins) > 0:
		print (" Stalemates : " + str(number-(sum(comp_wins) + sum(player_wins))))
	if len(turn_list) > 0:
		print ("   Max Turn : " + str(max(turn_list)))
		print ("   Min Turn : " + str(min(turn_list)))
		print ("       Mean : " + str((sum(turn_list))/len(turn_list)))
	if len(discard_list) > 0:
		print ("Discard min : " + str(min(discard_list)))
	return

def bulk_run(type_of_test):
	while True:
		prompt = input("\nHow many...? ")

		try:
			int_prompt = int(prompt)
		except ValueError:
			print ("Whoops!")
			continue

		if int_prompt == 0:
			return

		else:
			game_test_runner(int_prompt, type_of_test)

# Main loop
print ("\nDurak Debug Test")

while True:
	prompt = input("(1) Normal - One run\n(2) Verbose - One run\n(3) Normal - Bulk run\n(4) Verbose - Bulk run\n(0) Exit\n=> ")

	try:
		int_prompt = int(prompt)
	except ValueError:
		print ("Whoops! Try again...")
		continue

	if int_prompt == 0:
		sys.exit()

	if int_prompt == 1:
		brief.durak_main()
		continue

	if int_prompt == 2:
		debug.durak_main()
		continue

	if int_prompt == 3:
		bulk_run(bare)
		continue

	if int_prompt == 4:
		bulk_run(debug)

	else:
		print ('No entiendo!')
		continue




# while True:
# 	prompt = input("\nStart new test? (y) or (n): ")

# 	if prompt == 'n':
# 		sys.exit()

# 	if prompt == 'y':
# 		prompt2 = input("\n(1) One game at a time\n(2) Bulk run\n==> ")

# 		if int(prompt2) == 1:
# 			prompt4 = input("\n(1) Normal Test\n(2) Debug(Verbose)\n ==>  ")

# 			if prompt4 == 'n':
# 				sys.exit()
	
# 			if int(prompt4) == 1:
# 				brief.durak_main()
# 				continue

# 			if int(prompt4) == 2:
# 				debug.durak_main()
# 				continue

# 		if int(prompt2) == 2:
# 			prompt3 = input("\nSelect number of tests: ")
# 			int_prompt3 = int(prompt3)
# 			game_test_runner(int_prompt3)
# 			continue				
	

