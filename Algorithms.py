from random import random


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

	def __init__(self, input: Input, populationSize: int = 100):
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

		initialPopulation = self.initialisePopulation()



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

			teacherTimeslotAllocations = []

			for teacher in range(self.numTeachers): #Add an empty array for each Teacher
				teacherAllocation = []
				teacherTimeslotAllocations.append(teacherAllocation)





		return population


		"""
			random.sample() returns a new shuffled list. The original list remains unchanged.
		"""



"""
	CAT SWARM OPTIMIZATION ALGORITHM
"""

class CatSwarmAlgorithm(TimetableAlgorithm):
	TRACING = 0
	SEEKING = 1
	mode_index = 0

	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor for the Cat Swarm Optimization Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm

			Note that this class has the same class variables specified in the __init__() constructor
			of the superclass TimetableAlgorithm

		"""
		# Call super constructor
		super().__init__(input, populationSize)



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
		global_best_cat = []
		# mixing ratio, initialised to 4% in paper for hybrid CS
		MR = 0.04


		for i in range(0, iteration_counter):
			for current_cat in initialCats:
				# set current cat equal to the first cat
				# calculate fitness of current_cat
				current_cat_fitness = self.evaluateFitness(current_cat)

				# is current_cat's fitness smaller or equal to global_fitness_fitness (think this is a tyop)?
				if current_cat_fitness <= global_best_fitness:
					global_best_fitness =current_cat_fitness
					global_best_cat = current_cat

				# choose a random value between 0 and 1
				random_value = random.random()
				# is random number > MR
				if random_value > MR:
					# current_cat[self.mode_index] = self.SEEKING
					self.seek(current_cat)
				else:
					# current_cat[self.mode_index] = self.TRACING
					self.trace(current_cat)


		# Execute local search refining procedure in order to improve the quality of resultant time timetable regarding teachers gaps
		return  global_best_cat



	def intialiseCats(self):
		# initialise n cats (paper says 30, we may need to change)
		# revisiting the logic later, using the outline from the GA for now
		# paper representation seems similar to ours so adopting it shouldn't be too involved
		population = []  # list of individual cats -> size will be self.populationSize after we add all the cats

		for i in range(self.populationSize):  # Create cat i

			newIndividual = []  # Cat i
			# individual may have an additional entry at the end: one of 0 or 1 to indicate tracing or seeking mode
			# also needs an entry for velocity, may not need to keep track of seeking/tracing if it's not used later
			# might consider using parallel arrays

			mode_index = 56

			# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome

			teacherTimeslotAllocations = []

			for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
				teacherAllocation = []
				teacherTimeslotAllocations.append(teacherAllocation)

		return population

	def evaluateFitness(self, current_cat):
		# change later
		return 1

	def seek(self, current_cat):
		# add code for seeking
		1==1

	def trace(self, current_cat):
		# add code for tracing
		1==1

