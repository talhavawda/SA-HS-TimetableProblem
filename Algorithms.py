import random


class Input:
	"""
		A class to represent the problem instance (i.e. the variables obtained from the Sample Input textfile)
	"""

	def __init__(self, teachingTable, numTeachers: int, numGr7Classes: int, numGr8Classes: int, numGr9Classes: int):
		"""
			Constructor

			:param teachingTable:	A 2D list/array indicating the teacher to Class-Subject allocations
			The rows are the classes and the columns are the subjects, and the value at [i, j] is the TeacherID of
			the teacher who teaches Subject j to Class i

			:param numTeachers		The number of teachers teaching the Grade 7 to 9's
			:param numGr7Classes	The number of classes in Grade 7
			:param numGr8Classes	The number of classes in Grade 8
			:param numGr9Classes	The number of classes in Grade 9

		"""
		self.teachingTable = teachingTable
		self.numTeachers = numTeachers
		self.numGr7Classes = numGr7Classes
		self.numGr8Classes = numGr8Classes
		self.numGr9Classes = numGr9Classes
		self.totalnumClasses = self.numGr7Classes + self.numGr8Classes + self.numGr9Classes



	def print(self):
		"""
			Displays (to the Console) the values of this input instance

			- Displays the Number of classes in each Grade, the number of teachers, and the
			  Teacher Class-Subject Allocation Table (i.e. the teacher that teaches Class i Subject j)

			:return: None
		"""

		print("Number of classes in Grade 7: \t\t\t\t", self.numGr7Classes)
		print("Number of classes in Grade 8: \t\t\t\t", self.numGr8Classes)
		print("Number of classes in Grade 9: \t\t\t\t", self.numGr9Classes)
		print("\nNumber of teachers teaching in Grades 7-9:\t", self.numTeachers)



		print("\n\nTeacher Class-Subject Allocation Table:\n")

		# Print Column Headings (Subjects)

		print("Subjects ->", end="\t\t\t\t")
		headerStr = "-----------------------"


		# Subjects are represented as digits from 0 to 8 but will display as 1 to 9
		for subject in range(1, 10):
			print(subject, end="\t")
			headerStr += "----"

		print("\nClasses:")
		print(headerStr)

		classNames = []

		for i in range(self.numGr7Classes):
			className = "Grade 7 - Class " + str(i + 1)
			classNames.append(className)

		for i in range(self.numGr8Classes):
			className = "Grade 8 - Class " + str(i + 1)
			classNames.append(className)

		for i in range(self.numGr9Classes):
			className = "Grade 9 - Class " + str(i + 1)
			classNames.append(className)

		for Class in range(self.totalnumClasses):
			print(classNames[Class], end="\t|\t")  # Row Heading
			for Teacher in self.teachingTable[Class]:
				print(Teacher+1, end="\t") # TeacherID's are represented as digits from 0 to numTeachers-1 but will display as 1 to numTeachers
			print()

		print(headerStr + "\n")



class TimetableAlgorithm:
	"""
		The abstract class to represent an algorithm used to solve our Timetable Problem

		A specific algorithm that we use sublcasses this class and implements its functions.
		An instance of the subclass will be used to solve the Timetabling Problem on a given input
	"""

	"""CLASS CONSTANTS"""
	SUBJECTS = [
				"Home Language", "First Additional Language", "Mathematics", "Natural Science", "Social Science",
				"Technology", "Economic and Management Science", "Life Orientation", "Arts and Culture"
				]

	# Using List Comprehension to define the Lesson and Timeslot numbers
	# In the code, we are representing the number of Lessons and Timeslots from 0-54 as indexes begin at 0 (Mathematically, its from 1-55)
	# So Day numbers will be represented from 0-4 and to get the day number of a timeslot, use floor(timeslot // 5)

	LESSONS = [lesson for lesson in range(0, 55)]
	TIMESLOTS = [timeslot for timeslot in range(0, 55)] # The permutation of all the timeslots in increasing order
	TIMESLOTS_SET = set(TIMESLOTS) # Representing the Timeslots as a set | Will be used to compare to a generated timeslot to determine if it is a valid permutation




	# Indicates the Subject index of a lesson - index is the lesson number, and value is the Subject index at that lesson
	# Use the SUBJECTS constant to get the Subject name at that Subject index
	LESSON_SUBJECTS = 	[
							0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
							2, 2, 2, 2, 2, 2, 2, 2, 2,
							3, 3, 3, 3, 3, 3,
							4, 4, 4, 4, 4, 4,
							5, 5, 5, 5,
							6, 6, 6, 6,
							7, 7, 7, 7,
							8, 8, 8, 8
						]




	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor

			:param input:	An object of type Input containing the teachingTable, numTeachers, numGr7Classes, numGr8Classes,
			 numGr9Classes, totalNumClasses variables of this problem instance

			The teachingTable is a 2D list/array indicating the teacher to Class-Subject allocations
			The rows are the classes and the columns are the subjects, and the value at [i, j] is the TeacherID of
			the teacher who teachers Subject j to Class i

			:param populationSize	the size of the population to use for the Algorithm

		"""

		self.teachingTable = input.teachingTable
		self.numTeachers = input.numTeachers
		self.numGr7Classes = input.numGr7Classes
		self.numGr8Classes = input.numGr8Classes
		self.numGr9Classes = input.numGr9Classes
		self.totalNumClasses = input.totalnumClasses
		self.populationSize = populationSize


	def solveTimetable(self):
		"""
			Solve the Timetable Problem using this algorithm
			This function can call helper functions defined in the subclass that it can use to solve


			A solution in the Solution Space for this Problem is a 2D-array/list of integer values indicating the
			Timeslot that a specific Class has a specific Lesson
			The rows are the classes and the columns are the lessons, and the value at [i, j] in this 2D array/list
			is the Timeslot number that Class i has Lesson j in the week
			It can also be viewed as a list of sublists with each sublist being a row in the table -
			each sublist (of size 55) representing (the timeslot to lesson allocations of) a Class,
			and sublist i is a permutation of the integers 0-54 (as all 55 lessons must be allocated to timeslots, and to unique timeslots)
			For sublist i, the value at index j is the timeslot that Class i has Lesson j

			Thus we can view a solution as a list of permutations of the set {0, 1, ..., 54}


			:return:	The optimal feasible solution after the termination criteria has been met, and its associated value (as a tuple, in that order)
		"""

"""
	GENETIC ALGORITHM
"""



class GeneticAlgorithm(TimetableAlgorithm):

	def __init__(self, input: Input, populationSize: int = 10):
		"""
			Constructor for the Genetic Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm
			Popuzlation Size is assigned a default value of 100

			Note that this class has the same class variables specified in the __init__() constructor
			of the superclass TimetableAlgorithm

		"""

		# Call super constructor
		super().__init__(input, populationSize)


	def solveTimetable(self):
		"""
			Implementing this abstract function defined in the superclass

			Solve the Timetable Problem using this Genetic algorithm

			See the docstring of solveTimetable() in the superclass for a description of a solution (chromosome)

			A gene is an integer value that represents a timeslot
			Thus the Gene  Pool is all values in the range [0 ,54]

			We can think of a  super-gene in a chromosome as a permutation list of the set {0, 1, ..., 54}
			It is useful to think of a super-gene, as a constraint of our problem is that each row (sub-list) in the solution table
			is a list representing a permutation of the numbers 0-54
			The number of super-genes (sublists) in a chromosome for a problem instance is input.totalNumClasses

			:return:	The optimal feasible solution after the termination criteria has been met, and its associated fitness value (as a tuple, in that order)
		"""

		# initialise Population
		initialPopulation = self.initialisePopulation()

		# Set benchmark fitness to the individual at 0
		bestIndividual = initialPopulation[0]
		bestFitness = self.calculate_fitness(bestIndividual)

		# Continue updating for a 1000 iterations if the best representation has not been changed
		iterationsSinceLastUpdate = 0
		print("METHODS NOT IMPLEMENTED YET - MIGHT THROW AN ERROR SOMEWHERE")
		while iterationsSinceLastUpdate < 1000:
			foundBetterSoln = False
			# calculate the fitness of the population and update the best fitness if necessary
			for individual in initialPopulation:
				individualFitness = self.calculate_fitness(individual)
				if individualFitness > bestFitness:
					bestIndividual = individual
					bestFitness = individualFitness
					foundBetterSoln = True
			if foundBetterSoln:
				iterationsSinceLastUpdate = 0
			else:
				iterationsSinceLastUpdate += 1

			updatedPopulation = []

			for i in range(len(initialPopulation)):
				# Select parents
				parent1, parent2 = self.selection(population=initialPopulation)
				# produce a child from 2 parents
				child = self.crossover(parent1, parent2)
				# Probability for operators
				probability = random.random()
				# if probability is less than 0.1 then conduct mutation on child
				if probability < 0.1:
					# mutation on child
					child = self.mutation(child)
				# add child to new population
				updatedPopulation.append(child)

			initialPopulation = updatedPopulation







	"""Helper Functions for solveTimetable()"""

	def initialisePopulation(self):
		"""
			Initialises the population (generates the initial population) for the Genetic Algorithm

			Size of population is self.populationSize

			[DEPRECATED]The chromosomes are randomly generated by repeatedly generating shuffled lists of the TIMESLOTS list
			The chromosomes are built by doing each value in the chromosome table, ensuring teachers dont have clashes
			(i.e. repeatedly selecting a random value of the available remaining timeslots for that class
			(timeslot for a Class-Lesson) till that teacher doesnt have a clash)

			:return:	The initial population for this Problem to be used by the Genetic Algorithm
		"""

		population = []  # list of individual chromosomes -> size will be self.populationSize after we add all the chromosomes

		for i in range(self.populationSize): # Create chromosome individual i

			newIndividual =[] # Chromosome i

			# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome

			teacherTimeslotAllocations = self.getEmptyTeacherAllocation()

			assigned = 0
			while assigned != self.totalNumClasses:
				# generate shuffled list for a class
				allocation = list(range(55))
				random.shuffle(allocation)
				# is the class allocation a valid one wrt teacher times
				isValid = True
				for slot in range(len(allocation)):
					# get subject index
					subject = self.LESSON_SUBJECTS[slot]
					teacher = self.teachingTable[assigned][subject]
					# check if list is okay to add i.e no clashes for teachers
					subjectTeachersAllocation = teacherTimeslotAllocations[teacher]
					if allocation[slot] in subjectTeachersAllocation:  # teacher is busy
						# not a valid allocation
						isValid = False
						# print('Suggested allocation is not permitted - clash of time')
						break

				if isValid:
					assigned = assigned + 1
					newIndividual.append(allocation)
					print('individual', i, ' class', assigned, '\n', newIndividual)
					for j in range(len(allocation)):
						subject = self.LESSON_SUBJECTS[j]
						teacher = self.teachingTable[assigned-1][subject]
						teacherTimeslotAllocations[teacher].append(allocation[j])
			population.append(newIndividual)





		return population


		"""
			random.sample() returns a new shuffled list. The original list remains unchanged.
		"""
	def getEmptyTeacherAllocation(self) -> [[]]:
		teacherTimeslotAllocations = []
		for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
			teacherAllocation = []
			teacherTimeslotAllocations.append(teacherAllocation)
		return teacherTimeslotAllocations

	def mutation(self, chromosome):
			# TODO: Mutation
			return chromosome


	def crossover(self, chromosome1, chromosome2):
			# TODO: Crossover
			return chromosome1


	def selection(self, population):
		# TODO: Selection
		parent1 = population[0] # population[random.randint(0, len(population))]
		parent2 = population[1] # population[random.randint(0, len(population))]
		return parent1, parent2



	def calculate_fitness(self, chromosome):
		# TODO: GA fitness
		# return fitness of chromosome
		# +5 for every correct allocation.
		# +3 for a double period [done]
		# -2 for more than 2 periods on a subject in a day
		# -2 for two single periods on the same day for a subject
		# -2 for each time a teacher teaches for more than 4 periods consecutively [done]
		fitness = 0
		# for each subject evaluate the allocation (class and teacher wise)
		# empty teacher allocation array
		teacherAllocation = self.getEmptyTeacherAllocation()
		# take the individuals distibution and assign to relevant teachers
		for i in range(len(chromosome)):
			for j in range(len(chromosome[i])):
				sub = self.LESSON_SUBJECTS[j]
				teacher = self.teachingTable[i][sub]
				teacherAllocation[teacher].append(chromosome[i][j])
		# check to see if any teacher works more than 4periods at once
		for teacher in teacherAllocation:
			workingPeriods = teacher
			# sort in order [0, 54]
			workingPeriods.sort()
			consecutive = 0
			for i in range(len(workingPeriods)-1):
				if workingPeriods[i]+1 == workingPeriods[i+1]:
					consecutive += 1
				else:
					consecutive = 0
				if consecutive == 4:
					fitness -= 2
					consecutive = 0

		# reward double periods
		# for each class in the chromosome
		for i in range(len(chromosome)):
			# for each slot in the class
			for j in range(len(chromosome[i])-1):
				# for each slot after j
				for k in range(j+1, len(chromosome[i]) - 1):
					# get subject being held at j
					subject1 = self.LESSON_SUBJECTS[j]
					# get subject being held at k
					subject2 = self.LESSON_SUBJECTS[k]
					# check if they are the same subject
					if subject1 == subject2:
						# check if they are consecutive
						if chromosome[i][j]+1 == chromosome[i][k]:
							fitness += 3
					else:
						break
		print('Individual fitness = ', fitness)
		return fitness



"""
	CAT SWARM OPTIMIZATION ALGORITHM
"""

class CatSwarmAlgorithm(TimetableAlgorithm):

	# mode_index = 0

	class CAT:
		IDLE = 0 # I think seeking is an idle mode, will possibly take this out
		SEEKING = 1
		TRACING = 2

		def __init__(self):
			self.state = 0
			"""
			0 for when the cat is idle 1 in seek mode and 2 for trace mode 
			"""
			self.location = 0
			"""
				current position in the solution space, changes when cat given permission to seek
			"""
			self.solution = [[]]
			"""current solution the cat possesses
			"""
			self.velocity = 0.0

		def setState(self, newState: int):
			"""
					setter for state
			"""
			self.state = newState

		def setLocation(self, newlocation: int):
			"""
					setter for location
			"""
			self.location = newlocation

		def setVelocity(self, newVelocity: int):
			"""
					setter for location
			"""
			self.velocity = newVelocity

		def setSolution(self, newSolution: [[]]):
			"""
					setter for solution
			"""
			self.solution = newSolution

		def getState(self):
			return self.state

		def getSolution(self):
			return  self.solution

	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor for the Cat Swarm Optimization Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm

			Note that this class has the same class variables specified in the __init__() constructor
			of the superclass TimetableAlgorithm

		"""
		# Call super constructor
		super().__init__(input, populationSize)
		self.global_best_cat = self.CAT()

	def solveTimetable(self):
		"""
			Implementing this abstract function defined in the superclass

			Solve the Timetable Problem using this Cat Swarm Optimization algorithm
			This function can call helper functions defined in the subclass that it can use to solve

			:return:	The optimal feasible solution after the termination criteria has been met, and its associated value (as a tuple, in that order)
		"""
		# I'm going to write out the steps here to help myself a bit

		# execute initialisation procedure to initialise cats
		initialCats = self.intialiseCats()

		#set global best fitness to worst possible
		global_best_fitness = 1000000 # may need to change once we determine objective function, place holder value for now

		# paper uses 5000 iterations
		iteration_counter = 5000
		# mixing ratio, initialised to 4% in paper for hybrid CS
		MR = 0.04


		for i in range(0, iteration_counter):
			for current_cat in initialCats:
				# set current cat equal to the first cat
				# calculate fitness of current_cat
				current_cat_fitness = self.evaluateFitness(current_cat)

				# is current_cat's fitness smaller or equal to global_fitness_fitness (think this is a tyop)?
				if current_cat_fitness >= global_best_fitness: # assuming out fitness function wants to minimise
					global_best_fitness =current_cat_fitness
					global_best_cat = current_cat

				# choose a random value between 0 and 1
				random_value = random.random()
				# is random number > MR
				if random_value > MR:
					# current_cat[self.mode_index] = self.SEEKING
					current_cat.setState(self.CAT.SEEKING)
					#self.seek(current_cat)
				else:
					# current_cat[self.mode_index] = self.TRACING
					current_cat.setState(self.CAT.TRACING)
					#self.trace(current_cat)
				self.seek(cat for cat in initialCats if cat.getState() == self.CAT.SEEKING)
				self.trace(cat for cat in initialCats if cat.getState() == self.CAT.TRACING)
		# Execute local search refining procedure in order to improve the quality of resultant time timetable regarding teachers gaps
		return  global_best_cat



	def intialiseCats(self):
		# initialise n cats (paper says 30, we may need to change)
		# revisiting the logic later
		CATS = []  # list of individual cats -> size will be self.populationSize after we add all the cats

		for i in range(self.populationSize):  # Create cat i

			teacherClassAlloc = list(range(1,56))


			new_allocation = [[0 for i in range(self.totalNumClasses)]for j in range(56)] #cat i
			for j in range(len(new_allocation[0])):
				random.shuffle(teacherClassAlloc)
				for i in range(len(new_allocation)):
					new_allocation[j][i] = teacherClassAlloc[i]
					
			new_cat = self.CAT()
			new_cat.setSolution(new_allocation)
			CATS.append(new_allocation)

			# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome

			teacherTimeslotAllocations = []

			for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
				teacherAllocation = []
				teacherTimeslotAllocations.append(teacherAllocation)


		return CATS

	def evaluateFitness(self, current_cat):
		# change later
		pass

	def seek(self, cats ):
		# add code for seeking
		# values from the paper after experimentation
		SPC = True
		SMP = 2
		CDC = 0.1
		SRD = 0.1
		j = 0 # default initialisation
		candidate_positions = [self.CAT]
		for cat in cats:
			best_fitness = self.evaluateFitness(cat)
			if SPC == True:
				j = SMP -1
				candidate_positions.append( cat)
			else :
				j = SMP
			cat_copies = []
			for i in range(0,j):
				cat_copies.append(cat.getSolution)
			tc = CDC * 	len(self.TIMESLOTS) # nr of timeslots we will "replace"/change
			sm = SRD * len(self.totalNumClasses) # total nr of swaps
			for cat_copy in cat_copies:
				self.Change_Random(cat_copy, tc) # insert tc random timeslots from global_best_cat to cat_copy
				for i in range(0, sm):
					cat_copy = self.Single_Swap(cat_copy)
					if (self.Valid(cat_copy)): # if statement is not necessary if single swap only returns valid swaps
						new_fitness_value = self.evaluateFitness(cat_copy)
						if (new_fitness_value<= best_fitness):
							best_fitness = new_fitness_value
							candidate_positions.append( cat_copy)
			flag = True
			old_fitness = self.evaluateFitness(candidate_positions[0])
			for i in  range(len(candidate_positions)-1):
				fitness = self.evaluateFitness(candidate_positions[i])
				if (fitness != old_fitness): # a cat having a better than initial fitness had been found
					# TODO: calculate the selection probability for each candidate position;
					#  based it's difference from global best cat
					pass
				else:
					# TODO: set selecting probability of each cat = 1
					pass
			# pick a random position from the candidate positions the one to move to
			random_pos = self.CAT
			cat.setSolution(random_pos.getSolution())



	def trace(self, cats):
		# add code for tracing
		for cat in cats:
			c1 = 1 # i can't find where they set this value???
			similarity =  self.Similarity(cat)
			distance = self.totalNumClasses * len(self.TIMESLOTS) - similarity
			rand_number = random.random()
			cs = rand_number* c1 * distance # number of cells to be swapped
			self.Single_Swap(cat)
		pass

	def Similarity(self, cat):
		similarity = 0
		for i in range(cat):
			for j in range (cat[i]):
				if cat[i][j] == self.global_best_cat[i][j]:
					similarity+=1
		return similarity

	def Single_Swap(self, current_cat):
		randClass = random.randint(0,self.totalNumClasses)
		randCell1 = random.randint(0,56)
		randCell2 = random.randint(0,56)

		inCol1 = False
		inCol2 = False
		for i in range(self.totalNumClasses):
			if current_cat[i][randCell1] == current_cat[randClass][randCell2]:
				inCol1 = True
				break

		for i in range(self.totalNumClasses):
			if current_cat[i][randCell2] == current_cat[randClass][randCell1]:
				inCol2 = True
				break

		if (current_cat[randClass][randCell1] != current_cat[randClass][randCell2]) and (not inCol1) and (not inCol2):
			tempCat = current_cat[randClass][randCell1]
			current_cat[randClass][randCell1] = current_cat[randClass][randCell2]
			current_cat[randClass][randCell2] = tempCat

		return current_cat

		pass

	def Change_Random(self, current_cat, tc):
		# insert tc random timeslots from global_best_cat to cat_copy
		pass

	def Valid(self, current_cat):
		# check whether current cat is valid
		return  False