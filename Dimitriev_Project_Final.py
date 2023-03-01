#CISC 851: FINAL PROJECT
#Alan Dimitriev - 20062431


import os
import random
import operator
import copy
import statistics
from statistics import mean


#Spell Name - Mana Cost - Cast Time - Cooldown
spell_data = {'Healing Surge' : [.24, 1.5, 0],
			'Riptide' : [.08, 0, 6],
			'Unleash Life':  [.04, 0, 15],
			'Chain Heal': [.30, 2.5, 0],
			'Healing Wave' : [.15, 2.5, 0],
			'Healing Stream Totem':[.09, 0, 30.0],
			'Healing Rain': [.216, 2, 10.0],
			'Downpour': [.15, 1.5, 15],
			'Wellspring': [.20, 1.5, 20.0]

}


#Initialize population of size pop_size where each member of the population is of length rotation_length
def initialize_population(pop_size, rotation_length):
	spell_list = ['Healing Surge', 'Riptide', 'Unleash Life', 'Chain Heal', 'Healing Wave', 'Healing Stream Totem', 'Healing Rain', 'Downpour', 'Wellspring']
	population = []
	for x in range(pop_size):
		#Randomly select a spell at each index in the rotation
		population.append(random.choices(spell_list, k = rotation_length))

	return population




#Fitness evaluation function
#Takes an individual population member as input
#Returns fitness score (percent healing) and the 'intron free' version of the rotation
def evaluate_fitness(rotation):

	cast_order = []

	base_mana = 100.0
	#Was originally going to incorporate mana but elected not to, kept implementation incase I ever do want to refine it
	current_mana = 300000000.0


	#Set all cooldowns to 0 to start
	global_cooldown = 0
	riptide_cooldown = 0
	unleashlife_cooldown = 0
	healingstreamtotem_cooldown = 0
	healingrain_cooldown = 0
	downpour_cooldown = 0
	wellspring_cooldown = 0

	total_healing = 0.0
	global_time = 0.0


	#Set all cast variables to false
	chainheal_casted = False
	healingwave_casted = False
	wellspring_casted = False
	downpour_casted = False
	healingrain_casted = False
	healingsurge_casted = False
	finish_cast = False
	cast_time = 0.0
	casted = False
	totem_time = 0.0
	healingrain_time = 0
	unleashlife_buff = False
	riptide_buff = 0.0



	#Sequentially iterate through the input rotation
	for x in range(len(rotation)):

		global_time += 0.5

		#Check if a cast finished at this time
		if finish_cast == True:
			global_cooldown -= 0

			#HEALING SURGE
			if healingsurge_casted == True:
				if unleashlife_buff == True:
					total_healing += (248 + (.35 * 248))
					unleashlife_buff = False
				else:
					total_healing += 248
				healingsurge_casted == False

			#HEALING RAIN
			if healingrain_casted == True:
				healingrain_time = 10.0
				healingrain_casted = False


			#WELLSPRING
			if wellspring_casted == True:
				if unleashlife_buff == True:
					total_healing += (190 + (.35 * 190))
					unleashlife_buff = False
				else:
					total_healing += 190
				wellspring_casted = False

			#CHAIN HEAL
			if chainheal_casted == True:
				if unleashlife_buff == True:
					total_healing += (210 + (.35 * 210))
					unleashlife_buff = False
				else:
					total_healing += 210
				chainheal_casted = False


			#HEALING WAVE
			if healingwave_casted == True:
				if unleashlife_buff == True:
					total_healing += (300 + (.35 * 300))
					unleashlife_buff = False
				else:
					total_healing += 300
				healingwave_casted = False

			#DOWNPOUR
			if downpour_casted == True:
				if unleashlife_buff == True:
					total_healing += (175 + (.35 * 175))
					unleashlife_buff = False
				else:
					total_healing += 175
				downpour_casted = False


			finish_cast = False
		elif casted == False:
			global_cooldown -= .5
		if global_cooldown < 0.0:
			global_cooldown = 0.0

		#Update cooldowns
		riptide_cooldown -= .5
		if riptide_cooldown < 0.0:
			riptide_cooldown = 0.0
		unleashlife_cooldown -= .5
		if unleashlife_cooldown < 0.0:
			unleashlife_cooldown = 0.0
		healingstreamtotem_cooldown -= .5
		if healingstreamtotem_cooldown < 0.0:
			healingstreamtotem_cooldown = 0.0
		healingrain_cooldown -= .5
		if healingrain_cooldown < 0.0:
			healingrain_cooldown = 0.0
		downpour_cooldown -= .5
		if downpour_cooldown < 0.0:
			downpour_cooldown = 0.0
		wellspring_cooldown -= .5
		if wellspring_cooldown < 0.0:
			wellspring_cooldown = 0.0


		#Check if currently casting/if cast finished
		if casted == True:
			cast_time -= 0.5
			if cast_time == 0.0:
				casted = False
				finish_cast = True

			


		#While global cooldown not active, check what the current spell is and if it is valid to cast
		elif global_cooldown <= 0.0:

			#HEALING SURGE
			if rotation[x] == 'Healing Surge':
				#print(f'Cast Healing Surge')
				cost = spell_data['Healing Surge'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Healing Surge', global_time - 0.5))
					current_mana -= cost
					global_cooldown = 1.5
					casted = True
					cast_time = 1
					healingsurge_casted = True

			#RIPTIDE
			if rotation[x] == 'Riptide' and riptide_cooldown <= 0.0:
				#print(f'Cast Riptide')
				cost = spell_data['Riptide'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Riptide', global_time - 0.5))
					current_mana -= cost
					if unleashlife_buff == True:
						total_healing += (170 + (.3 * 170))
					else:
						total_healing += 170
						unleashlife_buff = False
					riptide_buff = 18.0
					global_cooldown = 1.5
					riptide_cooldown = 6.0

			#UNLEASH LIFE
			if rotation[x] == 'Unleash Life' and unleashlife_cooldown <= 0.0:
				#print(f'Cast Unleash Life')
				cost = spell_data['Unleash Life'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Unleash Life', global_time - 0.5))
					current_mana -= cost
					if unleashlife_buff == True:
						total_healing += (190 + (.35 * 190))
						unleashlife_buff = False
					else:
						total_healing += 190
					unleashlife_buff = True
					global_cooldown = 1.5
					unleashlife_cooldown = 15.0

			#CHAIN HEAL
			if rotation[x] == 'Chain Heal':
				#print(f'Cast Chain Heal')
				cost = spell_data['Chain Heal'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Chain Heal', global_time - 0.5))
					current_mana -= cost
					global_cooldown = 1.5
					casted = True
					chainheal_casted = True
					cast_time = 2.0

			#HEALING WAVE
			if rotation[x] == 'Healing Wave':
				#print(f'Cast Healing Wave')
				cost = spell_data['Healing Wave'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Healing Wave', global_time - 0.5))
					current_mana -= cost
					casted = True
					healingwave_casted = True
					cast_time = 2.0
					global_cooldown = 1.5

			#HEALING STREAM TOTEM
			if rotation[x] == 'Healing Stream Totem' and healingstreamtotem_cooldown <= 0.0:
				#print(f'Cast Healing Stream Totem')
				cost = spell_data['Healing Stream Totem'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Healing Stream Totem', global_time - 0.5))
					current_mana -= cost
					totem_time = 15.0
					totem_tick = 2
					global_cooldown = 1.5
					totem_cast = True
					healingstreamtotem_cooldown = spell_data['Healing Stream Totem'][2]
	
			#HEALING RAIN
			if rotation[x] == 'Healing Rain' and healingrain_cooldown <= 0.0:
				#print(f'Cast Healing Rain')
				cost = spell_data['Healing Rain'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Healing Rain', global_time - 0.5))
					current_mana -= cost
					global_cooldown = 1.5
					casted = True
					healingrain_casted = True
					cast_time = 1.5
					healingrain_cooldown = spell_data['Healing Rain'][2]

			#DOWNPOUR
			if rotation[x] == 'Downpour' and downpour_cooldown <= 0.0:
				#print(f'Cast Downpour')
				cost = spell_data['Downpour'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Downpour', global_time - 0.5))
					current_mana -= cost
					global_cooldown = 1.5
					downpour_casted = True
					casted = True
					cast_time = 1.0
					downpour_cooldown = spell_data['Downpour'][2]

			#WELLSPRING
			if rotation[x] == 'Wellspring' and wellspring_cooldown <= 0.0:
				#print(f'Cast Wellspring')
				cost = spell_data['Wellspring'][0] * base_mana
				if cost < current_mana:
					cast_order.append(('Wellspring', global_time - 0.5))
					current_mana -= cost
					global_cooldown = 1.5
					wellspring_casted = True
					casted = True
					cast_time = 1.0
					wellspring_cooldown = spell_data['Wellspring'][2]


		#If riptide buff still has time remaining then add health
		if riptide_buff > 0.0:
			riptide_buff -= 0.5
			total_healing += 3.66666667

		#If healing rain is active then add health
		if healingrain_time > 0.0:
			healingrain_time -= 0.5
			total_healing += 7.95

		#If healing totem is active check if it heals at this time
		if totem_time > 0.0:
			if totem_cast == False:
				totem_time -= 0.5
				totem_tick -= .5
				if totem_tick == 0.0:
					total_healing += 47
					totem_tick = 2.0
			else:
				totem_cast = False

	return total_healing, cast_order




#Function to evalute fitness of entire population
def evaluate_population(population):
	fitness_scores = []

	#Evaluate the fitness for each individual within the population
	for x in population:
		temp_fitness, _ = evaluate_fitness(x)
		fitness_scores.append(temp_fitness)

	return fitness_scores


#Parent Selection Function
#Input: List of population members and their associated fitness in a list
#Output: Index of two winner individuals and index of two loser individuals
def parent_selection(population, fitness):
	num_tournaments = 2
	tournament_size = 3

	#Choose 6 random participants without replacement
	participants = random.sample(range(len(population)), k = tournament_size * num_tournaments)

	#Separate the chosen 6 into two separate tournaments
	tournament_1 = participants[:tournament_size]
	tournament_2 = participants[tournament_size:]

	#Create association list between participant index and respective fitness
	for x in range(tournament_size):
		tournament_1[x] = (tournament_1[x], fitness[tournament_1[x]])
		tournament_2[x] = (tournament_2[x], fitness[tournament_2[x]])

	#Sort the participants
	tournament_1.sort(key=operator.itemgetter(1))
	tournament_2.sort(key=operator.itemgetter(1))

	#Winners have the highest percent healing
	winner1 = tournament_1[-1][0]
	winner2 = tournament_2[-1][0]

	#Losers have the lowest percent healing
	loser1 = tournament_1[0][0]
	loser2 = tournament_2[0][0]

	return winner1, winner2, loser1, loser2





#Perform recombination from two parents
def recombination(parent1, parent2):

	#Generate random number to represent probability
	crossover_check = random.randint(1, 10)
	crossover_type= random.randint(1, 2)

	#If probability is less than or equal to eight perform crossover.
	if crossover_check <= 8:

		if crossover_type == 1:

			#First crossover point is randomly chosen
			crossover_point = random.randint(1, len(parent1) - 2)

			#Split parents based on crossover points
			p1_top = parent1[:crossover_point]
			p1_bot = parent1[crossover_point:]

			p2_top = parent2[:crossover_point]
			p2_bot = parent2[crossover_point:]

			#Recombine sections to create offspring
			offspring1 = p1_top + p2_bot
			offspring2 = p2_top + p1_bot



		if crossover_type == 2:

			#First crossover point is randomly chosen
			crossover_point1 = random.randint(1, len(parent1) - 2)

			#Second crossover point is also randomly chosen
			while True:
				crossover_point2 = random.randint(1, len(parent1) - 2)
				if crossover_point2 != crossover_point1:
					break

			if crossover_point1 < crossover_point2:

				#Split parents based on crossover points
				p1_top = parent1[:crossover_point1]
				p1_mid = parent1[crossover_point1:crossover_point2]
				p1_bot = parent1[crossover_point2:]

				p2_top = parent2[:crossover_point1]
				p2_mid = parent2[crossover_point1:crossover_point2]
				p2_bot = parent2[crossover_point2:]

				#Recombine sections to create offspring
				offspring1 = p1_top + p2_mid + p1_bot
				offspring2 = p2_top + p1_mid + p2_bot

			if crossover_point2 < crossover_point1:

				#Split parents based on crossover points
				p1_top = parent1[:crossover_point2]
				p1_mid = parent1[crossover_point2:crossover_point1]
				p1_bot = parent1[crossover_point1:]

				p2_top = parent2[:crossover_point2]
				p2_mid = parent2[crossover_point2:crossover_point1]
				p2_bot = parent2[crossover_point1:]

				#Recombine sections to create offspring
				offspring1 = p1_top + p2_mid + p1_bot
				offspring2 = p2_top + p1_mid + p2_bot


	#If crossover probability does not occur, return parents
	else:
		offspring1 = parent1
		offspring2 = parent2

	return offspring1, offspring2


#Mutation function
#Input: Two offspring individuals
#Output: Two individuals that may have undergone mutation
def mutation(offspring1, offspring2):
	spell_list = ['Healing Surge', 'Riptide', 'Unleash Life', 'Chain Heal', 'Healing Wave', 'Healing Stream Totem', 'Healing Rain', 'Downpour', 'Wellspring']
	micro_mutation_rate = .5

	off1_micro = random.uniform(0, 1)
	off2_micro = random.uniform(0, 1)

	#Randomly decide if offspring1 is to undergo mutation
	if off1_micro <= micro_mutation_rate:
		#Select a random instruction
		target_allele = random.randint(0, len(offspring1) - 1)
		while True:
			new_allele = random.choice(spell_list)
			if new_allele != offspring1[target_allele]:
				break
		#Replace random spell in rotation with a different spell
		offspring1[target_allele] = new_allele

	#Randomly decide if offspring2 is to undergo mutation
	if off2_micro <= micro_mutation_rate:
		#Select a random instruction
		target_allele = random.randint(0, len(offspring2) - 1)
		while True:
			new_allele = random.choice(spell_list)
			if new_allele != offspring2[target_allele]:
				break
		#Replace random spell in rotation with a different spell
		offspring2[target_allele] = new_allele

	return offspring1, offspring2


#Greedy Algorithm for comparison
#Finds the highest percent healing spell available and uses it
def greedy_algorithm(rotation_length):

	rotation = []

	riptide_val = 302
	healingrain_val = 159
	unleashlife_val = 225
	wellspring_val = 190
	healingsteamtotem_val = 329
	downpour_val = 175
	healingwave_val = 300
	healingsurge_val = 248
	chainheal_val = 210


	riptide_cooldown = 0
	unleashlife_cooldown = 0
	healingstreamtotem_cooldown = 0
	healingrain_cooldown = 0
	downpour_cooldown = 0
	wellspring_cooldown = 0

	global_cooldown = 0

	spell_list = ['Healing Surge', 'Riptide', 'Unleash Life', 'Chain Heal', 'Healing Wave', 'Healing Stream Totem', 'Healing Rain', 'Downpour', 'Wellspring']
	spell_val = [248, 302, 225, 210, 300, 329, 159, 175, 190]
	for x in range(rotation_length):

		global_cooldown -= 0.5

		riptide_cooldown -= .5
		if riptide_cooldown <= 0.0:
			riptide_cooldown = 0.0
			spell_val[1] = 302
		unleashlife_cooldown -= .5
		if unleashlife_cooldown <= 0.0:
			unleashlife_cooldown = 0.0
			spell_val[2] = 225
		healingstreamtotem_cooldown -= .5
		if healingstreamtotem_cooldown <= 0.0:
			healingstreamtotem_cooldown = 0.0
			spell_val[5] = 329
		healingrain_cooldown -= .5
		if healingrain_cooldown <= 0.0:
			healingrain_cooldown = 0.0
			spell_val[6] = 159
		downpour_cooldown -= .5
		if downpour_cooldown <= 0.0:
			downpour_cooldown = 0.0
			spell_val[7] = 175
		wellspring_cooldown -= .5
		if wellspring_cooldown <= 0.0:
			wellspring_cooldown = 0.0
			spell_val[8] = 190

		if global_cooldown <= 0:

			print(spell_val)
			max_value = max(spell_val)
			index = spell_val.index(max_value)

			rotation.append(spell_list[index])

			if spell_list[index] == 'Downpour':
				spell_val[index] = 0
				downpour_cooldown = spell_data['Downpour'][2]

			if spell_list[index] == 'Riptide':
				spell_val[index] = 0
				riptide_cooldown = spell_data['Riptide'][2]

			if spell_list[index] == 'Unleash Life':
				spell_val[index] = 0
				unleashlife_cooldown = spell_data['Unleash Life'][2]

			if spell_list[index] == 'Healing Stream Totem':
				spell_val[index] = 0
				healingstreamtotem_cooldown = spell_data['Healing Stream Totem'][2]

			if spell_list[index] == 'Healing Rain':
				spell_val[index] = 0
				healingrain_cooldown = spell_data['Healing Rain'][2]

			if spell_list[index] == 'Wellspring':
				spell_val[index] = 0
				wellspring_cooldown = spell_data['Wellspring'][2]

			global_cooldown = 1.5

		else:
			rotation.append("")

	return rotation




def main():

	#n defines the number of trials
	n = 5

	#vmax defines how many iterations you wish to run each trial for
	vmax = 50000
	final_rotations = []
	final_fitness = []

	#Defines how long a period of time you want a rotation to cover
	#For example a 5 minute period equates to 300 seconds, which must be doubled
	#to be mapped to 0.5 seconf increments 
	individual_length = 600



	#NOTE: To run the comparative algorithm uncomment this section

	# greedy_output = greedy_algorithm(individual_length)
	# fitness, intron_free = evaluate_fitness(greedy_output)

	# print(fitness)
	# print(intron_free)



	for iteration in range(n):
		population = initialize_population(100, individual_length)

		for i in range(vmax):

			fitness_scores = evaluate_population(population)

			#Print every 100 evaluations
			if i % 1000 == 0:
				print(f'Iteration {iteration} - Maximum fitness {max(fitness_scores)} | Minimum fitness at iteration {i} : {min(fitness_scores)}')

			#If final evaluation, end the loop
			if i == vmax-1:
				break


			#Perform tournament parent selection
			winner1, winner2, loser1, loser2 = parent_selection(population, fitness_scores)

			
			parent1 = copy.deepcopy(population[winner1])
			parent2 = copy.deepcopy(population[winner2])

			#Apply recombination using the two winners of the tournaments
			offspring1, offspring2 = recombination(parent1, parent2) 

			#Apply mutations to offspring
			offspring1, offspring2 = mutation(offspring1, offspring2)

			#Replace two losers from tournament with offspring
			population[loser1] = offspring1
			population[loser2] = offspring2
		

		final_list = list(zip(population, fitness_scores))
		final_list.sort(key=lambda x: x[1], reverse = True)

		best_fitness = final_list[0][1]


		best_programs = []
		for x in range(len(final_list)):
			if final_list[x][1] == best_fitness:
				best_programs.append(x)

		print("-------------")
		print("FINAL PROGRAM")
		print(f'fitness: {final_list[0][1]}')
		print("-------------")
		_, intron_free = evaluate_fitness(final_list[0][0])
		print(intron_free)
		print("-------------")
		print(final_list[0][0])

		final_fitness.append(final_list[0][1])
		final_rotations.append(intron_free)

	for index in range(len(final_rotations)):
		print("------------------")
		print(f'Fitness: {final_fitness[index]}')
		print(final_rotations[index])
		print("------------------")


main()