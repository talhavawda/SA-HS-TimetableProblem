import copy
import random
import datetime
import time
import math
import typing
import copy
import bisect


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
				print(Teacher + 1,
					  end="\t")  # TeacherID's are represented as digits from 0 to numTeachers-1 but will display as 1 to numTeachers
			print()

		print(headerStr + "\n")



seedVal = 0 # global variable | used by weightedSampler()

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

	NUM_SUBJECTS = 9
	NUM_LESSONS = 55
	NUM_TIMESLOTS = 55

	LESSONS = [lesson for lesson in range(0, 55)]
	TIMESLOTS = [timeslot for timeslot in range(0, 55)]  # The permutation of all the timeslots in increasing order
	TIMESLOTS_SET = set(
		TIMESLOTS)  # Representing the Timeslots as a set | Will be used to compare to a generated timeslot to determine if it is a valid permutation

	# Indicates the Subject index of a lesson - index is the lesson number, and value is the Subject index at that lesson
	# Use the SUBJECTS constant to get the Subject name at that Subject index
	LESSON_SUBJECTS = [
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

	#Indicates the (lower and upper) bounds of the lesson numbers of a subject. Indexes are the subject indexes/numbers
	SUBJECT_LESSON_BOUNDS = [
		[0, 9],
		[10, 17],
		[18, 26],
		[27, 32],
		[33, 38],
		[39, 42],
		[43, 46],
		[47, 50],
		[51, 43]
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

	def getObjectiveValue(self, solution):
		"""
			Abstract Function to be implemented by subclasses

			:return: The objective function's value of this candidate solution
		"""


	def getEmptyTeacherTimeslotAllocations(self) -> [[]]:
		teacherTimeslotAllocations = []
		for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
			teacherAllocation = []
			teacherTimeslotAllocations.append(teacherAllocation)
		return teacherTimeslotAllocations


	def getTeacherTimeslotAllocations(self, chromosome):
		teacherTimeslotAllocations = self.getEmptyTeacherTimeslotAllocations()
		# take the individuals distribution and assign to relevant teachers
		for Class in range(self.totalNumClasses):
			for Lesson in range(self.NUM_LESSONS):
				Subject = self.LESSON_SUBJECTS[Lesson]
				Teacher = self.teachingTable[Class][Subject]
				timeslot = chromosome[Class][Lesson]
				teacherTimeslotAllocations[Teacher].append(timeslot)

		return teacherTimeslotAllocations


	def printTeacherAllocation(self, teacherTimeslotAllocations):
		print("\nTeacher-Timeslot Allocations:\n")

		for teacher in range(self.numTeachers):
			teacherAllocation = teacherTimeslotAllocations[teacher]
			teacherAllocation.sort()

			print("Teacher", teacher+1,  end="\t|\t") # Row Heading | teacher+1 cos we start displaying from 1

			for timeslot in teacherAllocation:
				print(timeslot+1, end="\t") # Timeslot's are represented as digits from 0 to 54 but will display as 1 to 55

			print()

		print("----------------------------------------------------------\n")

	def printSolution(self, solution):
		"""
			Display a possible/candidate solution (i.e. an individual/chromosome)

			:param solution: A candidate solution in the solution space
			:return: None
		"""
		print("\n\nSOLUTION:\nClass-Lesson Timeslot Allocation Table:\n")

		# Print Column Headings (Subjects)

		print("Lessons ->", end="\t\t\t\t")
		headerStr = "-----------------------"

		# Lessons are represented as digits from 0 to 54 but will display as 1 to 55
		for lesson in range(1, 56):
			print(lesson, end="\t")
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

		for Class in range(self.totalNumClasses):
			print(classNames[Class], end="\t|\t")  # Row Heading
			classAllocation = solution[Class]
			for Lesson in self.LESSONS:
				Timeslot = classAllocation[Lesson]
				print(Timeslot + 1,end="\t")  # Timeslot's are represented as digits from 0 to 54 but will display as 1 to 55
			print()

		print(headerStr + "\n")

		solutionValue = self.getObjectiveValue(solution)
		print("\nSolution Value (Fitness):", solutionValue)
		print("----------------------------------------------------------\n")


	def convertToTimetable(self, solution):
		"""
			Convert a solution to a master timetable (2D Array)
			-> Make the columns the timeslots and values the lessons (i.e. swap them around)
			The rows are still the classes

			:param solution: Candidate feasible solution in the solution space
			:return:

		"""

		masterTimetable = []

		for Class in range(self.totalNumClasses):

			classTimeslotsAllocation = solution[Class]

			classLessonsAllocation = []

			for timeslot in range(self.NUM_TIMESLOTS):
				lesson = classTimeslotsAllocation.index(timeslot) # get the lesson that occurs at this timeslot
				classLessonsAllocation.append(lesson)

			masterTimetable.append(classLessonsAllocation)


		return masterTimetable


	def printMasterTimetable(self, masterTimetable):
		"""
			Display master timetable of solution
			:param masterTimetable:
			:return: None
		"""
		print("\nMaster Timetable (Class-Timeslot Lesson Allocations):\n")

		# Print Column Headings (Timeslots)

		print("Timeslots ->", end="\t\t\t")
		headerStr = "-----------------------"

		# Timeslots are represented as digits from 0 to 54 but will display as 1 to 55
		for timeslot in range(1, 56):
			print(timeslot, end="\t")
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

		for Class in range(self.totalNumClasses):
			print(classNames[Class], end="\t|\t")  # Row Heading
			classAllocation = masterTimetable[Class]
			for Timeslot in self.TIMESLOTS:
				Lesson = classAllocation[Timeslot]
				print(Lesson + 1,
					  end="\t")  # Timeslot's are represented as digits from 0 to 54 but will display as 1 to 55
			print()

		print(headerStr + "\n")



	def printClassTimetables(self, masterTimetable):
		"""
			Print the Class  timetables of the given master timetable of the feasible solution solution
			:param solution:
			:return: None
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

			:return:	The optimal feasible solution after the termination criteria has been met, the generation it was found in, and its associated score / fitness value (as a tuple, in that order)
		"""

		# initialise Population
		# start = datetime.datetime.now()
		start = time.time()

		initialPopulation = self.initialisePopulation()

		# end = datetime.datetime.now()
		end = time.time()

		timeTaken = end - start
		print("\tTime taken to initialise population:", timeTaken, "seconds")

		# Set benchmark fitness to the individual at 0
		bestIndividual = initialPopulation[0]
		fitnessBestIndiv = self.calculateFitness(bestIndividual)
		generationOfBestSoln = 0
		generations = 0

		# Continue generating up to 1000 new generations of populations if the best representation/solution has not been improved
		iterationsSinceLastUpdate = 0

		population = initialPopulation

		print("\tFinding optimal solution...")

		print("\t\tGeneration:\t", end="")

		while iterationsSinceLastUpdate < 100:
			generations += 1
			print(generations, end=", ")

			foundBetterSoln = False

			# calculate the fitness of the population and update the best fitness if necessary
			for individual in population:
				individualFitness = self.calculateFitness(individual)
				if individualFitness > fitnessBestIndiv:
					bestIndividual = copy.deepcopy(individual) # store a copy of this individual as the best | cant just assign as a pointer will be assigned
					fitnessBestIndiv = individualFitness
					foundBetterSoln = True
					generationOfBestSoln = generations

			if foundBetterSoln:
				iterationsSinceLastUpdate = 0
			else:
				iterationsSinceLastUpdate += 1


			# Generate new population
			newPopulation = []

			for i in range(self.populationSize):

				child = []  # Declare the child chromosome; either generated from Recombination or taken directly from current population

				probRecombination = random.random()  # A random floating value in the range [0.0, 1.0)

				recombinationRate = 0.9

				if probRecombination < recombinationRate:
					# Do Recombination (Crossover)

					# Select 2 parents
					parents = self.selection(2, population) # Select 2 parents for recombination

					# produce a child from 2 parents
					child = self.recombination(parents[0], parents[1])

				else:
					# Select a random individual from the current generation and place it directly in the new population
					parent = self.selection(1, population) # Select a random individual from the current generation
					child = parent[0]  # select() returns a list so get the first element from it
				
				
				probMutation = random.random()  # A random floating value in the range [0.0, 1.0)
				mutationRate = 0.1
				
				if probMutation < mutationRate:
					# Do Mutation on child
					child = self.mutation(child)
					
				# add child to new population
				newPopulation.append(child)

			population = newPopulation

		#print('Solution found in generation', generationOfBestSoln, ' with a fitness of ', fitnessBestIndiv)
		#self.printSolution(bestIndividual)


		print()
		
		return bestIndividual, generationOfBestSoln, fitnessBestIndiv


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

		print("\n\tInitialising Population ","(",self.populationSize, " individuals):\n", sep="")

		population = []  # list of individual chromosomes -> size will be self.populationSize after we add all the chromosomes

		for i in range(self.populationSize):  # Create chromosome individual i

			"""
				Chromosome i is a 2D-array / a list of sub-lists with the number of rows (sublists being seld.totalNumClasses)
				and the number of columns (size of a sublist)  being 55 (representing the lessons)
			"""
			newIndividual = []  # Chromosome i

			# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome
			teacherTimeslotAllocations = self.getEmptyTeacherTimeslotAllocations()

			currentClass = 0

			while currentClass < self.totalNumClasses:  # Create timeslot allocation for each class j in chromosome i

				# generate an lesson-timeslot allocation  for class j

				# classAllocation = list(range(55))
				# random.shuffle(classAllocation)

				classAllocation = random.sample(self.TIMESLOTS, self.NUM_TIMESLOTS)  # random.sample(list, size) returns a new shuffled list. The original list remains unchanged.

				"""
					Determine if this class allocation a valid one with respect to teacher times
					(i.e. there are (currently) no timeslot conflicts for any teacher when adding this allocation- 
					Hard Constraint 3: A teacher can only teach one lesson in a specific timeslot)
				"""
				isValidAllocation = True

				for lesson in range(self.NUM_LESSONS):  # For each of the 55 lessons that we allocated a timeslot

					timeslot = classAllocation[lesson]  # the timeslot allocated to this lesson

					subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
					teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson

					# check if this teacher is not already teaching in this timeslot

					teacherAllocation = teacherTimeslotAllocations[teacher]

					if timeslot in teacherAllocation:  # teacher is already allocated to this timeslot - i.e. there is a clash
						#print("Lesson\t", lesson)
						#print("Timeslot\t", timeslot)
						#print("Subject\t", self.LESSON_SUBJECTS[lesson])
						#print("This teachers allocation: \t", teacherAllocation)
						#print("Teacher\t", teacher)
						#print("All teachers", teacherTimeslotAllocations)


						# Find another teacher that teaches this class (a subject) to swap with
						swapFound = False

						for otherSubject in range(self.NUM_SUBJECTS):
							if otherSubject != subject:
								#print("\tChecking subject", otherSubject)
								# Get teacher that teaches this other subject to this class
								otherTeacher = self.teachingTable[currentClass][otherSubject]
								otherTeacherAllocation = teacherTimeslotAllocations[otherTeacher]
								#print("\t\tOther teacher: \t", otherTeacher)
								#print("\t\tOther teacher's allocation: \t", otherTeacherAllocation)

								if timeslot not in otherTeacherAllocation:  # the other teacher is free in this current timeslot
									# See if this current teacher is free in any of the timeslots that this other teacher teaches this class

									otherSubjectLessonBounds = self.SUBJECT_LESSON_BOUNDS[otherSubject]
									otherSubjectLowerLessonBound = otherSubjectLessonBounds[0]
									otherSubjectUpperLessonBound = otherSubjectLessonBounds[1]

									for otherLesson in range(otherSubjectLowerLessonBound, otherSubjectUpperLessonBound+1):
										otherTimeslot = classAllocation[otherLesson]  # the timeslot allocated to this other lesson

										if otherTimeslot not in teacherAllocation:  # the current teacher is free in this other timeslot
											swapFound = True
											#print("swap found")
											# we can swap timeslots
											temp = copy.deepcopy(classAllocation[lesson])
											classAllocation[lesson] = copy.deepcopy(classAllocation[otherLesson])
											classAllocation[otherLesson] = temp

											break  # stop the search as we've found another lesson to swap with


						"""
						# ALTERNATIVE way to to the above, going lesson by lesson (takes a bit longer)
						subjectLessonBounds = self.SUBJECT_LESSON_BOUNDS[subject]
						subjectLowerLessonBound = subjectLessonBounds[0]
						subjectUpperLessonBound = subjectLessonBounds[1]

						for otherLesson in range(self.NUM_LESSONS):  # For each of the 55 lessons
							if otherLesson < subjectLowerLessonBound or otherLesson > subjectUpperLessonBound: # For lessons of different subjects (as lessons of same subject taught by same teacher)
								otherTimeslot = classAllocation[otherLesson]  # the timeslot allocated to this other lesson

								if otherTimeslot not in teacherAllocation: # the current teacher is free in this other timeslot
									otherSubject = self.LESSON_SUBJECTS[otherLesson]  # get the index/number of the subject that this other lesson is
									otherTeacher = self.teachingTable[currentClass][otherSubject]  # teacher that teaches this other lesson
									otherTeacherAllocation = teacherTimeslotAllocations[otherTeacher]

									if timeslot not in otherTeacherAllocation: # the other teacher is free in this current timeslot
										swapFound = True
										print("swap found")
										# we can swap timeslots
										temp = copy.deepcopy(classAllocation[lesson])
										classAllocation[lesson] = copy.deepcopy(classAllocation[otherLesson])
										classAllocation[otherLesson] = temp
										break # stop the search as we've found another lesson to swap with
						"""

						if swapFound == False: # if we did not find another lesson to swap with (since there is a clash), then this cannot be a valid allocation
							isValidAllocation = False


				"""
					If this lesson-timeslot allocation for this class is valid, then add it in its place to the chromosome
					and add to the teacher allocations
					Then increment the class number to move on to the next class
					
					If this allocation is invalid (the condition below is False) then the loop will run again for the 
					same class, generating a different initial allocation to work with
				"""
				if isValidAllocation:

					newIndividual.append(classAllocation)

					for lesson in self.LESSONS:  # ALT: for lesson in range(len(self.LESSONS))
						subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
						teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson
						teacherTimeslotAllocations[teacher].append(classAllocation[lesson])  # add this timeslot to this teacher's allocated timeslots

					#print('Individual', i + 1, ' Class', currentClass + 1, "allocated")
					currentClass = currentClass + 1
				#else:
					#print("\tInvalid allocation", 'Individual', i + 1, ' Class', currentClass + 1)

			population.append(newIndividual)
			#self.printSolution(newIndividual)

		return population







	def weightedSampler(self, seq, weights):
		"""
			Return a random-sample function that picks from seq weighted by (the corresponding) weights.

			Code Acknowledgement: Artificial Intelligence: A Modern Approach (https://github.com/aimacode/aima-python)
		"""

		totals = []

		# random.seed(datetime.now())

		global seedVal
		random.seed(seedVal)
		seedVal += 42345876

		for w in weights:
			totals.append(w + totals[-1] if totals else w)

		return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]



	def selection(self, n, population):
		"""
			Select and return n parents from the population

			Selection Strategy - Roulette Selection (Fitness Proportionate Selection)
				- 	The parents are selected at random with the chance/probability of a chromosome being selected is proportional to its fitness
					-	Fitter individuals have a higher chance of being selected (for 'mating' and passing on their genes to child chromosomes)
					-	This ensures a reasonable spread of both good and bad chromosomes (with good/fit chromosomes being favoured)
				- 	This Selection Strategy was used as we want a mixture of both good and bad chromosomes
					-	If we only pick the fittest parents from the current population (Elitism Selection) then we
						lose chromosomes that are unfit but have part of the solution in them.
						It also leads to a loss of diversity and premature convergence (which is undesirable for Genetic Algorithms)
							-	Loss of Diversity is where the population consists of chromosomes of similar genes,
							which can lead to having a local optimal solution, but not being able to reach the global optimal solution

			:param population: the population to select n parents from
			:return:
		"""

		# fitnesses[i] is the fitness value of the chromosome population[i]
		fitnesses = [self.calculateFitness(chromosome) for chromosome in population]


		"""
			weightedSampler() does the Roulette Selection
			It returns a function that picks a random sample that picks from population weighted by the fitnesses
		"""
		sampler = self.weightedSampler(population, fitnesses)


		return [sampler() for i in range(n)]


	def mutation(self, chromosome):
		"""
			Do Mutation on a chromosome
			:param chromosome:
			:return: Mutated chromosome
		"""
		mutatedChromosome = []

		teacherAllocation = self.getTeacherTimeslotAllocations(chromosome)
		for Class in range(self.totalNumClasses):

			# get the period timeslots allocation of class i
			classAllocation = copy.deepcopy(chromosome[Class])

			isMutated = False

			while not isMutated:

				# get a random lesson period
				lesson1 = random.randint(0, 54) # random integer in range [0, 54]
				# get a second random period
				lesson2 = random.randint(0, 54)  # random integer in range [0, 54]

				#get the timeslots of these lessons
				timeslot1 = classAllocation[lesson1]
				timeslot2 = classAllocation[lesson2]

				# get the 2 relevant subjects
				subject1 = self.LESSON_SUBJECTS[lesson1]
				subject2 = self.LESSON_SUBJECTS[lesson2]

				# get the teachers teaching these lessons
				teacher1 = self.teachingTable[Class][subject1]
				teacher2 = self.teachingTable[Class][subject2]

				# get the teacher allocations of those subjects
				teacherAlloc1 = teacherAllocation[teacher1]
				teacherAlloc2 = teacherAllocation[teacher2]

				# If there's no clash
				if timeslot1 not in teacherAlloc2 and timeslot2 not in teacherAlloc1:

					# updating the timeslot allocations
					classAllocation[lesson1] = timeslot2
					classAllocation[lesson2] = timeslot1

					# update teacher allocations
					teacherAlloc1.remove(timeslot1)
					teacherAlloc1.append(timeslot2)
					teacherAlloc2.remove(timeslot2)
					teacherAlloc1.append(timeslot1)

					isMutated = True

				if isMutated:
					break

			# The loop will run and the mutated class will be added to the new chromosome

			mutatedChromosome.append(classAllocation)
			#print(mutatedChromosome)

		return mutatedChromosome

	def recombination(self, parent1, parent2):
		"""
			Doing Recombination (Crossover) on 2 parent chromosomes to produce a child chromosome
			:param chromosome1:
			:param chromosome2:
			:return: Child chromosome
		"""

		child = []

		"""
			Each parent chromosome is a 2D list and Crossover splits the parents in terms of the outer list (i.e. the classes)
				-> The Crossover point is a class boundary to stop copying at from the beginning of the first parent and where to s
					start copying from in the second parent to its end
					
			We are selecting the Grade boundaries as the crossover point possibilities to minimise teacher timeslot clashes
			Thus the boundaries are either: between Grade 7 and Grade 8, or between Grade 8 and Grade 9
			
			However there still may be some clashes once we start copying from parent2
			so we keep track of teacher allocations, and do mutation where necessary to resolve the clashes
		"""

		# Crossover point possibilities
		crossoverPointChoices = (self.numGr7Classes, self.numGr7Classes + self.numGr8Classes)

		# Select a crossover point
		crossoverPoint = random.choice(crossoverPointChoices)

		# copy from beginning of parent1 to crossover point, and from parent 2 from the crossover point to the end of parent 2

		# Simpler way of combining using the slice operator but cant use it to easily check for clashes
		#child = parent1[:crossoverPoint] + parent2[crossoverPoint:]


		# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome
		teacherTimeslotAllocations = self.getEmptyTeacherTimeslotAllocations()

		currentClass = 0


		for i in range(0, crossoverPoint): # copy from beginning of parent1 to crossover point
			# Copy from parent 1

			# All these classes wont have clashes as they're being taken from the same parent
			# So we just adding to the teacher allocations

			classI = parent1[i]
			child.append(classI)

			for lesson in self.LESSONS:
				subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
				teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson
				teacherTimeslotAllocations[teacher].append(classI[lesson])  # add this timeslot to this teacher's allocated timeslots

			currentClass += 1


		for i in range(crossoverPoint, self.totalNumClasses): # Copy from parent 2 from the crossover point to the end of parent 2
			# Copy from parent 2

			classI = parent2[i]

			"""
				Find and fix any conflicts/clashes that arise due to Hard Constraint 3 -
				Hard Constraint 3: A teacher can only teach one lesson in a specific timeslot)
			"""

			for lesson in range(self.NUM_LESSONS):  # For each of the 55 lessons that we allocated a timeslot

				timeslot = classI[lesson]  # the timeslot allocated to this lesson

				subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
				teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson

				# check if this teacher is not already teaching in this timeslot

				teacherAllocation = teacherTimeslotAllocations[teacher]

				if timeslot in teacherAllocation:  # teacher is already allocated to this timeslot - i.e. there is a clash
					# Find another teacher that teaches this class (a subject) to swap with
					swapFound = False

					for otherSubject in range(self.NUM_SUBJECTS):
						if otherSubject != subject:
							# Get teacher that teaches this other subject to this class
							otherTeacher = self.teachingTable[currentClass][otherSubject]
							otherTeacherAllocation = teacherTimeslotAllocations[otherTeacher]

							if timeslot not in otherTeacherAllocation:  # the other teacher is free in this current timeslot
								# See if this current teacher is free in any of the timeslots that this other teacher teaches this class

								otherSubjectLessonBounds = self.SUBJECT_LESSON_BOUNDS[otherSubject]
								otherSubjectLowerLessonBound = otherSubjectLessonBounds[0]
								otherSubjectUpperLessonBound = otherSubjectLessonBounds[1]

								for otherLesson in range(otherSubjectLowerLessonBound, otherSubjectUpperLessonBound + 1):
									otherTimeslot = classI[otherLesson]  # the timeslot allocated to this other lesson

									if otherTimeslot not in teacherAllocation:  # the current teacher is free in this other timeslot
										swapFound = True
										# print("swap found")
										# we can swap timeslots
										temp = copy.deepcopy(classI[lesson])
										classI[lesson] = copy.deepcopy(classI[otherLesson])
										classI[otherLesson] = temp

										break  # stop the search as we've found another lesson to swap with

			child.append(classI)

			for lesson in self.LESSONS:  # ALT: for lesson in range(len(self.LESSONS))
				subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
				teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson
				teacherTimeslotAllocations[teacher].append(classI[lesson])  # add this timeslot to this teacher's allocated timeslots

			currentClass += 1


		return child




	def calculateFitness(self, chromosome):
		"""
			Calculates and returns the fitness of the chromosome
			:param chromosome: A chromosome in the population
			:return: Fitness of the chromosome
		"""

		"""
			HARD CONSTRAINTS
				Since we have enforced all the Hard Constraints when creating the chromosomes (feasible solutions),
				add +1 point for every Timeslot allocation in the chromosome 
				Also multiply this by the number of a teachers (so that larger and harder inputs dont get negatively affected)
				-> thus add total number of classes * 55 (number of lessons/timeslots) * num teachers
			
			SOFT CONSTRAINTS
				SC1:    (Reward)    +20 points for each time a class has a double-lesson period of the same subject on the same day   
				SC2:    (Penalty)   -10 for points for each time a class has more than 2 lesson periods of a subject being taught to it on the same a day
				SC3:    (Penalty)   -5 point for for each time a class has two single-lesson periods of the same subject on the same day
				SC4.1:  (Penalty)   -10 points for each time a teacher teaches for more than 4 periods consecutively
				SC4.2:	(Reward)    +10 points for each different day that a teacher teaches


		"""


		# Score constant values for the Soft Constraints
		SC1 = +20
		SC2 = -10
		SC3 = -5
		SC4_1 = -10
		SC4_2 = +10



		fitness = 0

		# Hard Constraints met -> +1 point for each allocation
		fitness += self.totalNumClasses * self.NUM_LESSONS * self.numTeachers

		# for each subject evaluate the allocation (class and teacher wise)


		# SC1 - Reward double periods (of the same subject)

		# for each class i in the chromosome
		for i in range(self.totalNumClasses):

			# for each lesson j
			for j in range(self.NUM_LESSONS - 1): # -1 as we comparing current lesson to the one after it so we have to stop one before the end

				# Check if lesson j and the following lesson (j+1) are both lessons of the same subject
				if self.LESSON_SUBJECTS[j] == self.LESSON_SUBJECTS[j+1]:

					# Get the timeslots of both lessons
					timeslot1 = chromosome[i][j]  # Timeslot of class i having lesson j
					timeslot2 = chromosome[i][j+1] # Timeslot of class i having lesson j+1

					# If timeslot2 is the next (or previous) timeslot after timeslot1, then these 2 lessons form a double period
					if timeslot2 == timeslot1+1 or timeslot2 == timeslot1-1:
						fitness += SC1
						#print("SC1", i+1, j+1, "\t", timeslot1+1, timeslot2+1)




		# SC2 - Penalise more than 2 periods of a subject on the same day
		# SC3 - Penalize two separate single-lesson periods on the same day

		for i in range(self.totalNumClasses):
			Class = chromosome[i]


			"""
				A 2D list representing the timeslots (and also number of times) a subject is being taught (number of lesson periods) 
				on a specific day. Rows are subjects. Columns are days. Value at [row][col] is a list indicating the timeslots that that subject's lessons
				occur on that day
				Thus values in the 2D array are initialised as an empty list
			"""
			subjectsAllocation = [[[] for day in range(5)] for subject in range(self.NUM_SUBJECTS)]

			for j in range(self.NUM_LESSONS):

				subject = self.LESSON_SUBJECTS[j]  # get subject number of this lesson

				timeslot = chromosome[i][j]
				dayOfTimeslot = timeslot // 11 # integer division by 11 -> 11 lessons in a day; first day (Monday) is day 0; thus Friday is 4

				subjectsAllocation[subject][dayOfTimeslot].append(timeslot)

				if len(subjectsAllocation[subject][dayOfTimeslot]) > 2: # If the number of timeslots (thus number of lessons periods) is greater than 2 than penalise
					fitness += SC2
					#print("SC2", i+1, j+1, "\t", subject, "\t", subjectsAllocation[subject][dayOfTimeslot])

				if len(subjectsAllocation[subject][dayOfTimeslot]) == 2: # If this is the second lesson period for ths subject on this day
					earlierLessonTimeslot = subjectsAllocation[subject][dayOfTimeslot][0]

					if timeslot != earlierLessonTimeslot+1 and timeslot != earlierLessonTimeslot-1: # If they were not double lesson periods
						fitness += SC3
						#print("SC3", i+1, j+1, "\t", earlierLessonTimeslot+1, "\t", timeslot+1)


			"""
			# Shah's old code for SC2 & SC3
			subjectsAllocation = []  # a list where the indexes are the timeslots and the values are the subjects at that timeslot, for this class

			for timeslot in range(self.NUM_TIMESLOTS):
				lesson = Class.index(timeslot)  # get the lesson that is being taught at this timeslot from the chromosome
				subject = self.LESSON_SUBJECTS[lesson]  # get subject number of this lesson
				subjectsAllocation.append(subject)

			for s in range(self.NUM_TIMESLOTS - 2):
				# 3 consec periods of the same subject
				if subjectsAllocation[s] == subjectsAllocation[s + 1] and subjectsAllocation[s] == \
						subjectsAllocation[s + 2]:
					fitness += SC3 # Since SC3 is a negative value, a decrement will actually happen
				else:
					continue
			counter = 0
			
			
						for timeslot in range(self.NUM_TIMESLOTS):
				subject = subjectsAllocation[timeslot]
				for t in range(timeslot + 2, 11):
					if subject == subjectsAllocation[t]:
						fitness += SC3
			"""


		# SC4.1 - Penalise for a teacher teaching for more than 4 periods consecutively
		# SC4.2 - Reward a teacher for each different day that they teach on

		# teacher allocation array
		teacherAllocation = self.getTeacherTimeslotAllocations(chromosome)

		for teacherTimeslots in teacherAllocation: # For each teacher (their timeslot allocations)

			# sort timeslots in order
			teacherTimeslots.sort()

			consecutiveTeaching = 0

			teachingDays = [] # The days this teacher teaches on

			for i in range(len(teacherTimeslots)):

				timeslot = teacherTimeslots[i]

				dayOfTimeslot = timeslot // 11  # integer division by 11 -> 11 lessons in a day; first day (Monday) is day 0; thus Friday is 4

				if dayOfTimeslot not in teachingDays:
					teachingDays.append(dayOfTimeslot)
					fitness += SC4_2

				if i < len(teacherTimeslots) -1 : # we want to stop at the second last timeslot as we comparing each timeslot to the next
					nextTimeslot = teacherTimeslots[i+1]

					if nextTimeslot == timeslot + 1:
						consecutiveTeaching += 1
						if consecutiveTeaching > 4:
							fitness += SC4_1
							consecutive = 0
					else:
						consecutiveTeaching = 0








		#print('Individual fitness = ', fitness)

		return fitness


	def getObjectiveValue(self, solution):
		return self.calculateFitness(solution)




"""
	CAT SWARM OPTIMIZATION ALGORITHM
"""


class CatSwarmAlgorithm(TimetableAlgorithm):


	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor for the Cat Swarm Optimization Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm

			Note that this class has the same class variables specified in the __init__() constructor
			of the superclass TimetableAlgorithm

		"""
		# Call super constructor
		super().__init__(input, populationSize)

		# set best cat
		self.global_best_cat = self.CAT()

	class CAT:

		SEEKING = 1
		TRACING = 2


		def __init__(self):
			self.state = 0
			"""
			0 for when the cat is idle 1 in seek mode and 2 for trace mode 
			"""

			"""
				current position in the solution space, changes when cat given permission to seek
			"""
			self.solution = []


		def setState(self, newState: int):
			"""
					setter for state
			"""
			self.state = newState


		def setSolution(self, newSolution: []):
			"""
					setter for solution

			"""
			self.solution = newSolution

		def getState(self):
			"""
					getter for state
			"""
			return self.state

		def getSolution(self):
			"""
					getter for solution
			"""
			return self.solution

	def solveTimetable(self):
		"""
			Implementing this abstract function defined in the superclass

			Solve the Timetable Problem using this Cat Swarm Optimization algorithm
			This function can call helper functions defined in the subclass that it can use to solve

			:return:	The optimal feasible solution after the termination criteria has been met, and its associated value (as a tuple, in that order)
		"""
		start = time.time()
		# execute initialisation procedure to initialise cats
		initialCats = self.initialiseCats
		end = time.time()
		timeTaken = end - start
		print("initialization done")

		# set global best fitness to worst possible
		global_best_fitness = 0 # We are maximising our fitness value so set to very low value

		# paper uses 5000 iterations
		iteration_counter = 50
		# mixing ratio, initialised to 4% in paper for hybrid CS, seeking/trace ratio
		MR = 0.04

		for i in range(0, iteration_counter):
			for current_cat in initialCats:
				# set current cat equal to the first cat
				# calculate fitness of current_cat
				current_cat_fitness = current_cat.getSolution()
				current_cat_fitness = self.calculateFitness(current_cat_fitness)


				if current_cat_fitness > global_best_fitness:
					global_best_fitness = current_cat_fitness
					self.global_best_cat = current_cat

				# choose a random value between 0 and 1
				random_value = random.random()
				# is random number > MR

				if random_value > MR:
					current_cat.setState(self.CAT.SEEKING)
				else:
					current_cat.setState(self.CAT.TRACING)

				# put the "behaviour" of the cats here as it's not clear where it should go, and in the
				# original CSO algorithm, we move all the cats at once

				seeking_cats = []

				for cat in initialCats:
					if cat.getState() == self.CAT.SEEKING:
						seeking_cats.append(cat)
				self.seek(seeking_cats)
				tracing_cats = []

				for cat in initialCats:
					if cat.getState() == self.CAT.TRACING:
						tracing_cats.append(cat)
				self.trace(tracing_cats)
		# Execute local search refining procedure in order to improve the quality of resultant time timetable ; don't
		# think we do this outside of evaluation(and the paper doesn't say how)
		self.getObjectiveValue(self.global_best_cat.getSolution())
		return self.global_best_cat.getSolution()

	@property
	def initialiseCats(self):
		"""
			Initialises the population (generates the initial population) for the Genetic Algorithm

			Size of population is self.populationSize

			[DEPRECATED]The chromosomes are randomly generated by repeatedly generating shuffled lists of the TIMESLOTS list

			The chromosomes are built by doing each value in the chromosome table, ensuring teachers dont have clashes
			(i.e. repeatedly selecting a random value of the available remaining timeslots for that class
			(timeslot for a Class-Lesson) till that teacher doesnt have a clash)

			:return:	The initial population for this Problem to be used by the Genetic Algorithm
		"""
		print('\n Begin Initialization:\n')
		CATS = []  # list of individual chromosomes -> size will be self.populationSize after we add all the chromosomes

		for i in range(self.populationSize):  # Create chromosome individual i

			"""
				Chromosome i is a 2D-array / a list of sub-lists with the number of rows (sublists being seld.totalNumClasses)
				and the number of columns (size of a sublist)  being 55 (representing the lessons)
			"""
			newcat = self.CAT()  # Chromosome i
			catsolution = newcat.getSolution()

			# Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome
			teacherTimeslotAllocations = self.getEmptyTeacherTimeslotAllocations()

			currentClass = 0

			while currentClass < self.totalNumClasses:  # Create timeslot allocation for each class j in chromosome i

				# generate an lesson-timeslot allocation  for class j

				# classAllocation = list(range(55))
				# random.shuffle(classAllocation)

				classAllocation = random.sample(self.TIMESLOTS,
												self.NUM_TIMESLOTS)  # random.sample(list, size) returns a new shuffled list. The original list remains unchanged.

				"""
					Determine if this class allocation a valid one with respect to teacher times
					(i.e. there are (currently) no timeslot conflicts for any teacher when adding this allocation- 
					Hard Constraint 3: A teacher can only teach one lesson in a specific timeslot)
				"""
				isValidAllocation = True

				for lesson in range(self.NUM_LESSONS):  # For each of the 55 lessons that we allocated a timeslot

					timeslot = classAllocation[lesson]  # the timeslot allocated to this lesson

					subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
					teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson

					# check if this teacher is not already teaching in this timeslot

					teacherAllocation = teacherTimeslotAllocations[teacher]

					if timeslot in teacherAllocation:  # teacher is already allocated to this timeslot - i.e. there is a clash
						# print("Lesson\t", lesson)
						# print("Timeslot\t", timeslot)
						# print("Subject\t", self.LESSON_SUBJECTS[lesson])
						# print("This teachers allocation: \t", teacherAllocation)
						# print("Teacher\t", teacher)
						# print("All teachers", teacherTimeslotAllocations)

						# Find another teacher that teaches this class (a subject) to swap with
						swapFound = False

						for otherSubject in range(self.NUM_SUBJECTS):
							if otherSubject != subject:
								# print("\tChecking subject", otherSubject)
								# Get teacher that teaches this other subject to this class
								otherTeacher = self.teachingTable[currentClass][otherSubject]
								otherTeacherAllocation = teacherTimeslotAllocations[otherTeacher]
								# print("\t\tOther teacher: \t", otherTeacher)
								# print("\t\tOther teacher's allocation: \t", otherTeacherAllocation)

								if timeslot not in otherTeacherAllocation:  # the other teacher is free in this current timeslot
									# See if this current teacher is free in any of the timeslots that this other teacher teaches this class

									otherSubjectLessonBounds = self.SUBJECT_LESSON_BOUNDS[otherSubject]
									otherSubjectLowerLessonBound = otherSubjectLessonBounds[0]
									otherSubjectUpperLessonBound = otherSubjectLessonBounds[1]

									for otherLesson in range(otherSubjectLowerLessonBound,
															 otherSubjectUpperLessonBound + 1):
										otherTimeslot = classAllocation[
											otherLesson]  # the timeslot allocated to this other lesson

										if otherTimeslot not in teacherAllocation:  # the current teacher is free in this other timeslot
											swapFound = True
											# print("swap found")
											# we can swap timeslots
											temp = copy.deepcopy(classAllocation[lesson])
											classAllocation[lesson] = copy.deepcopy(classAllocation[otherLesson])
											classAllocation[otherLesson] = temp

											break  # stop the search as we've found another lesson to swap with

						"""
						# ALTERNATIVE way to to the above, going lesson by lesson (takes a bit longer)
						subjectLessonBounds = self.SUBJECT_LESSON_BOUNDS[subject]
						subjectLowerLessonBound = subjectLessonBounds[0]
						subjectUpperLessonBound = subjectLessonBounds[1]

						for otherLesson in range(self.NUM_LESSONS):  # For each of the 55 lessons
							if otherLesson < subjectLowerLessonBound or otherLesson > subjectUpperLessonBound: # For lessons of different subjects (as lessons of same subject taught by same teacher)
								otherTimeslot = classAllocation[otherLesson]  # the timeslot allocated to this other lesson

								if otherTimeslot not in teacherAllocation: # the current teacher is free in this other timeslot
									otherSubject = self.LESSON_SUBJECTS[otherLesson]  # get the index/number of the subject that this other lesson is
									otherTeacher = self.teachingTable[currentClass][otherSubject]  # teacher that teaches this other lesson
									otherTeacherAllocation = teacherTimeslotAllocations[otherTeacher]

									if timeslot not in otherTeacherAllocation: # the other teacher is free in this current timeslot
										swapFound = True
										print("swap found")
										# we can swap timeslots
										temp = copy.deepcopy(classAllocation[lesson])
										classAllocation[lesson] = copy.deepcopy(classAllocation[otherLesson])
										classAllocation[otherLesson] = temp
										break # stop the search as we've found another lesson to swap with
						"""

						if swapFound == False:  # if we did not find another lesson to swap with (since there is a clash), then this cannot be a valid allocation
							isValidAllocation = False

				# isValidAllocation = False # For Old

				"""
					If this lesson-timeslot allocation for this class is valid, then add it in its place to the chromosome
					and add to the teacher allocations
					Then increment the class number to move on to the next class

					If this allocation is invalid (the condition below is False) then the loop will run again for the 
					same class, generating a different initial allocation to work with
				"""
				if isValidAllocation:
					catsolution.append(classAllocation)

					for lesson in self.LESSONS:  # ALT: for lesson in range(len(self.LESSONS))
						subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
						teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson
						teacherTimeslotAllocations[teacher].append(classAllocation[lesson])  # add this timeslot to this teacher's allocated timeslots

					print('Cat', i + 1, ' Class', currentClass + 1, "allocated")
					currentClass = currentClass + 1
				else:
					print("\tInvalid allocation", 'Cat', i + 1, ' Class', currentClass + 1)

			newcat.setSolution(catsolution)
			CATS.append(newcat)
			self.printSolution(catsolution)


		return CATS

	def calculateFitness(self, candidate):
		"""
					Calculates and returns the fitness of the chromosome
					:param chromosome: A chromosome in the population
					:return: Fitness of the chromosome
				"""

		"""
            HARD CONSTRAINTS
                Since we have enforced all the Hard Constraints when creating the chromosomes (feasible solutions),
                add +1 point for every Timeslot allocation in the chromosome 
                Also multiply this by the number of a teachers (so that larger and harder inputs dont get negatively affected)
                -> thus add total number of classes * 55 (number of lessons/timeslots) * num teachers

            SOFT CONSTRAINTS
                SC1:    (Reward)    +20 points for each time a class has a double-lesson period of the same subject on the same day   
                SC2:    (Penalty)   -10 for points for each time a class has more than 2 lesson periods of a subject being taught to it on the same a day
                SC3:    (Penalty)   -5 point for for each time a class has two single-lesson periods of the same subject on the same day
                SC4.1:  (Penalty)   -10 points for each time a teacher teaches for more than 4 periods consecutively
                SC4.2:	(Reward)    +10 points for each different day that a teacher teaches


        """

		# Score constant values for the Soft Constraints
		SC1 = +20
		SC2 = -10
		SC3 = -5
		SC4_1 = -10
		SC4_2 = +10

		fitness = 0

		# Hard Constraints met -> +1 point for each allocation
		fitness += self.totalNumClasses * self.NUM_LESSONS * self.numTeachers

		# for each subject evaluate the allocation (class and teacher wise)

		# SC1 - Reward double periods (of the same subject)

		# for each class i in the chromosome
		for i in range(self.totalNumClasses):

			# for each lesson j
			for j in range(
					self.NUM_LESSONS - 1):  # -1 as we comparing current lesson to the one after it so we have to stop one before the end

				# Check if lesson j and the following lesson (j+1) are both lessons of the same subject
				if self.LESSON_SUBJECTS[j] == self.LESSON_SUBJECTS[j + 1]:

					# Get the timeslots of both lessons
					timeslot1 = candidate[i][j]  # Timeslot of class i having lesson j
					timeslot2 = candidate[i][j + 1]  # Timeslot of class i having lesson j+1

					# If timeslot2 is the next (or previous) timeslot after timeslot1, then these 2 lessons form a double period
					if timeslot2 == timeslot1 + 1 or timeslot2 == timeslot1 - 1:
						fitness += SC1
				# print("SC1", i+1, j+1, "\t", timeslot1+1, timeslot2+1)

		# SC2 - Penalise more than 2 periods of a subject on the same day
		# SC3 - Penalize two separate single-lesson periods on the same day

		for i in range(self.totalNumClasses):
			Class = candidate[i]

			"""
                A 2D list representing the timeslots (and also number of times) a subject is being taught (number of lesson periods) 
                on a specific day. Rows are subjects. Columns are days. Value at [row][col] is a list indicating the timeslots that that subject's lessons
                occur on that day
                Thus values in the 2D array are initialised as an empty list
            """
			subjectsAllocation = [[[] for day in range(5)] for subject in range(self.NUM_SUBJECTS)]

			for j in range(self.NUM_LESSONS):

				subject = self.LESSON_SUBJECTS[j]  # get subject number of this lesson

				timeslot = candidate[i][j]
				dayOfTimeslot = timeslot // 11  # integer division by 11 -> 11 lessons in a day; first day (Monday) is day 0; thus Friday is 4

				subjectsAllocation[int(subject)][int(dayOfTimeslot)].append(int(timeslot))

				if len(subjectsAllocation[int(subject)][
						   int(dayOfTimeslot)]) > 2:  # If the number of timeslots (thus number of lessons periods) is greater than 2 than penalise
					fitness += SC2
				# print("SC2", i+1, j+1, "\t", subject, "\t", subjectsAllocation[subject][dayOfTimeslot])

				if len(subjectsAllocation[int(subject)][
						   int(dayOfTimeslot)]) == 2:  # If this is the second lesson period for ths subject on this day
					earlierLessonTimeslot = subjectsAllocation[int(subject)][int(dayOfTimeslot)][0]

					if timeslot != earlierLessonTimeslot + 1 and timeslot != earlierLessonTimeslot - 1:  # If they were not double lesson periods
						fitness += SC3
				# print("SC3", i+1, j+1, "\t", earlierLessonTimeslot+1, "\t", timeslot+1)

			"""
            # Shah's old code for SC2 & SC3
            subjectsAllocation = []  # a list where the indexes are the timeslots and the values are the subjects at that timeslot, for this class

            for timeslot in range(self.NUM_TIMESLOTS):
                lesson = Class.index(timeslot)  # get the lesson that is being taught at this timeslot from the chromosome
                subject = self.LESSON_SUBJECTS[lesson]  # get subject number of this lesson
                subjectsAllocation.append(subject)

            for s in range(self.NUM_TIMESLOTS - 2):
                # 3 consec periods of the same subject
                if subjectsAllocation[s] == subjectsAllocation[s + 1] and subjectsAllocation[s] == \
                        subjectsAllocation[s + 2]:
                    fitness += SC3 # Since SC3 is a negative value, a decrement will actually happen
                else:
                    continue
            counter = 0


                        for timeslot in range(self.NUM_TIMESLOTS):
                subject = subjectsAllocation[timeslot]
                for t in range(timeslot + 2, 11):
                    if subject == subjectsAllocation[t]:
                        fitness += SC3
            """

		# SC4.1 - Penalise for a teacher teaching for more than 4 periods consecutively
		# SC4.2 - Reward a teacher for each different day that they teach on

		# teacher allocation array
		teacherAllocation = self.getTeacherTimeslotAllocations(candidate)

		for teacherTimeslots in teacherAllocation:  # For each teacher (their timeslot allocations)

			# sort timeslots in order
			teacherTimeslots.sort()

			consecutiveTeaching = 0

			teachingDays = []  # The days this teacher teaches on

			for i in range(len(teacherTimeslots)):

				timeslot = teacherTimeslots[i]

				dayOfTimeslot = timeslot // 11  # integer division by 11 -> 11 lessons in a day; first day (Monday) is day 0; thus Friday is 4

				if dayOfTimeslot not in teachingDays:
					teachingDays.append(dayOfTimeslot)
					fitness += SC4_2

				if i < len(
						teacherTimeslots) - 1:  # we want to stop at the second last timeslot as we comparing each timeslot to the next
					nextTimeslot = teacherTimeslots[i + 1]

					if nextTimeslot == timeslot + 1:
						consecutiveTeaching += 1
						if consecutiveTeaching > 4:
							fitness += SC4_1
							consecutive = 0
					else:
						consecutiveTeaching = 0

		# print('Individual fitness = ', fitness)

		"""
		# fitness for csa
		BASE = 1.3
		fitnessValue = 0
		HCW = 10
		ICDW = 0.95
		ITDW = 0.6
		TEPW = 0.06  # might not use this because we don't include gaps(-1) or empty classes in our population\
		current_cat_solution = current_cat.getSolution()

		# hard constraint of assigning a teacher to more than 1 class during the same timeslot
		for j in range(len(current_cat_solution[0])):
			n = 0
			for i in range(self.totalNumClasses):
				teacherVal = current_cat_solution[i][j]
				for k in range(i + 1, self.totalNumClasses):
					if teacherVal == current_cat_solution[k][j]:
						n += 1

			fitnessValue += HCW * (BASE ** n)

		# constraint of having the same teacher for more than 2 timeslots a day
		for i in range(self.totalNumClasses):
			n = 0
			for j in range(len(current_cat_solution[i]), step=11):
				teacherVal = current_cat_solution[i][j]
				for k in range(j + 1, j + 12):
					if k < len(current_cat_solution[i]):
						if teacherVal == current_cat_solution[i][k]:
							n += 1

			if n > 2:
				fitnessValue += HCW * (BASE ** n)

		# soft constraint
		for i in range(self.totalNumClasses):
			n = 0
			for j in range(len(current_cat_solution[i])):
				teacherVal = current_cat_solution[i][j]
				for k in range(j + 1, len(current_cat_solution[i])):
					if teacherVal == current_cat_solution[i][j]:
						n += 1
			if n > 10:
				fitnessValue += ITDW * BASE

		return fitnessValue
		"""
		return fitness
		pass

	def getObjectiveValue(self, solution):
		"""
			Implementing function from superclass
			:param solution:
			:return:
		"""
		return self.calculateFitness(solution)


	def seek(self, cats):

		for current_cat in cats:
			"""
				establish candidate pool, mutate candidates, determine next position
			"""
			"""
				SMP[] Seeking memory pool, a list containing candidate solutions
			"""
			SMP = []
			"""
				SPC [] boolean to determine if we should consider self positioning
			"""
			SPC = 1

			# initialize candidates

			for i in range(3):

				new_candidate = current_cat.getSolution()
				SMP.append(new_candidate)

			"""
				CDC - dimension change ratio, percentage of dimensions that will undergo mutation
				SRD - mutation ratio, determines the extent of mutation
				Mutate the candidates
			"""


			CDC = 0.5
			SRD = 0.2


			# mutation algorithm

			for k in range((len(SMP))-SPC):  # iterate candidates
				mutatedSolution = SMP[0]
				iterSolution = SMP[k]
				SMP2 = []


				for i, row in enumerate(mutatedSolution):  # choose values to mutate
					for j, item in  enumerate(mutatedSolution):
						if i<6 and j<55:
							random_value1 = random.random()
							if random_value1 > CDC:
								random_value2 = random.random()
								l = mutatedSolution[i][j]
								mutatedSolution[i][j] = ((1 + random_value2 * SRD) * l //11)

				SMP2.append(mutatedSolution)
			SMP = SMP2
			"""
				Determine the next position from the list of candidates
			"""
			SMP.append(new_candidate)


			#  old_fitness = self.calculateFitness(current_cat.getSolution()) #
			"""
			FSsol1 = current_cat.getSolution()
			FSmax = self.calculateFitness(FSsol1)
			old_fitness = FSmax
			FSsol2 = self.global_best_cat.getSolution()
			FSmin = self.calculateFitness(FSsol2)
			equal = True
			for i in range(len(SMP) - 1):
				fitness = self.calculateFitness(SMP[i])
				if fitness > FSmax:
					FSmax = fitness
				if fitness < FSmin:
					FSmin = fitness
				if fitness != old_fitness:  # a cat having a better than initial fitness had been found
					equal = False
			FSsol3 = self.global_best_cat.getSolution()
			FSb = self.calculateFitness(FSsol3)
			

			probabilities = [1.0 for _ in SMP]
			if not equal:
				for i in range(len(SMP)):
					FSi = self.calculateFitness(SMP[i])
					Pi = abs(FSi - FSb) / abs(FSmax - FSb)  # formula from equation 15
					probabilities[i] = Pi
			"""
			# pick a random position from the candidate positions the one to move to
			# need to choose somehow, paper doesn't specify (probably using the probabilities)
			bestCandidate = 0
			idealCandidate = []
			for i in range(len(SMP)):
				candidateSolution = SMP[i]
				candidateFitness = int( self.calculateFitness(SMP[i]))
				if bestCandidate < candidateFitness:
					bestCandidate = candidateFitness
					idealCandidate = SMP[i]


			# random_pos = int(random.choices(SMP, weights=probabilities, k=1)[0]) # function returns a list
			# of size k
			current_cat.setSolution(idealCandidate)


		"""
		# add code for seeking
		# values from the paper after experimentation
		SPC = True  # self positioning consideration
		SMP = 2  # seeking memory pool for candidate solutions
		CDC = 0.1  # percentage of dimensions to mutate
		SRD = 0.1  # extent of mutation
		j = 0  # default initialisation
		candidate_positions = []
		for cat_copy in cats:
			best_fitness = self.calculateFitness(cat_copy)
			if SPC:
				j = SMP - 1
				candidate_positions.append(cat_copy)
			else:
				j = SMP
			cat_copies = []
			for i in range(0, j):
				cat_copies.append(copy.deepcopy(cat_copy))
			tc = CDC * len(self.TIMESLOTS)  # nr of timeslots we will "replace"/change
			sm = SRD * self.totalNumClasses  # total nr of swaps
			for cat in cat_copies:
				for _ in range(round(tc)):
					self.Change_Random(cat)  # insert tc random timeslots from global_best_cat to cat
				for i in range(0, round(sm)):
					cat = self.Single_Swap(cat)
					# if (self.Valid(cat)):  # if statement is not necessary if single swap only returns valid swaps
					new_fitness_value = self.calculateFitness(cat)
					if new_fitness_value <= best_fitness:
						best_fitness = new_fitness_value
						candidate_positions.append(cat)

			old_fitness = self.calculateFitness(candidate_positions[0]) #
			FSmax = best_fitness
			FSmin = self.calculateFitness(self.global_best_cat)
			equal = True
			for i in range(len(candidate_positions) - 1):
				fitness = self.calculateFitness(candidate_positions[i])
				if fitness > FSmax:
					FSmax = fitness
				if fitness < FSmin:
					FSmin = fitness
				if fitness != old_fitness:  # a cat having a better than initial fitness had been found
					equal = False

			FSb = FSmin  # minimisation problem
			probabilities = [1.0 for _ in candidate_positions]
			if not equal:
				for i in range(len(candidate_positions)):
					FSi = self.calculateFitness(candidate_positions[i])
					Pi = abs(FSi - FSb) / abs(FSmax - FSmin)  # formula from equation 15
					probabilities[i] = Pi

			# pick a random position from the candidate positions the one to move to
			# need to choose somehow, paper doesn't specify (probably using the probabilities)
			random_pos = random.choices(candidate_positions, weights=probabilities, k=1)[0]  # function returns a list
			# of size k
			cat_copy.setSolution(random_pos.getSolution())
			"""
		return


	def trace(self, cats):
		# add code for tracing
		for cat in cats:
			c1 = 2.0  # From the not-hybrid algorithm
			similarity = self.Similarity(cat)
			distance = self.totalNumClasses * len(self.TIMESLOTS) - similarity
			rand_number = random.random()
			cs = rand_number * c1 * distance  # number of cells to be swapped
			# meant to be equivalent to the velocity from the original paper

			# for _ in range(round(cs)):
				# self.Single_Swap(cat)

	def Similarity(self, cat):
		similarity = 0
		cat_solution = cat.solution
		global_best_cat_solution = self.global_best_cat.getSolution()
		for i in range(len(cat_solution)):
			for j in range(len(cat_solution[i])):
				k = int (cat_solution[i][j])
				l = int(global_best_cat_solution[i][j])
				if k==l:
					similarity += 1
		return similarity

	def Single_Swap(self, current_cat):
		randClass = random.randint(0, self.totalNumClasses)
		randCell1 = random.randint(0, 54)
		randCell2 = random.randint(0, 54)
		current_cat_solution = current_cat.getSolution()

		inCol1 = False
		inCol2 = False
		for i in range(self.totalNumClasses):
			if current_cat_solution[i][randCell1] == current_cat_solution[randClass][randCell2]:
				inCol1 = True
				break

		for i in range(self.totalNumClasses):
			if current_cat_solution[i][randCell2] == current_cat_solution[randClass][randCell1]:
				inCol2 = True
				break

		if (current_cat_solution[randClass][randCell1] != current_cat_solution[randClass][randCell2]) and (
				not inCol1) and (not inCol2):
			tempCat = current_cat_solution[randClass][randCell1]
			current_cat_solution[randClass][randCell1] = current_cat_solution[randClass][randCell2]
			current_cat_solution[randClass][randCell2] = tempCat

		current_cat.setSolution(current_cat_solution)
		return current_cat


	def Change_Random(self, cat_copy):
		"""
		changes a random column in the cat_copy solution to the corresponding column in the best cat
		:param cat_copy: cat to be changed
		:return: modified cat
		"""
		# auxilliary procedure, section 3.4.3
		rand_col = random.randint(0, len(self.TIMESLOTS) - 1)
		cat_solution = cat_copy.getSolution()
		global_best_solution = self.global_best_cat.getSolution()

		# need to first compensate for the swap we are about to make
		for row in range(len(cat_solution)):
			for col in range(len(cat_solution[row])):
				if cat_solution[row][col] == global_best_solution[row][col] and (not col == rand_col):
					cat_solution[row][col] = cat_solution[row][rand_col]
					break  # only do this once per class

		# swap
		for row in range(len(cat_solution)):
			for col in range(len(cat_solution[row])):
				cat_solution[row][col] = global_best_solution[row][col]

		cat_copy.setSolution(cat_solution)
		return cat_copy





	'''def Valid(self, current_cat: CAT):
		# check whether current cat is valid
		# shouldn't need to implement this if change random is guaranteed to return a valid solution
		return False
		
		don't think we need this
		'''
