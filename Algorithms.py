import copy
import random
import datetime
import time
import math
import typing


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
        # start = datetime.datetime.now()
        start = time.time()

        initialPopulation = self.initialisePopulation()

        # end = datetime.datetime.now()
        end = time.time()

        timeTaken = end - start
        print("Time taken to init:", timeTaken, "seconds")

        # Set benchmark fitness to the individual at 0
        bestIndividual = initialPopulation[0]
        bestFitness = self.calculate_fitness(bestIndividual)
        indexOfBestSoln = 0
        iterrations = 0
        # Continue updating for a 1000 iterations if the best representation has not been changed
        iterationsSinceLastUpdate = 0
        print("METHODS NOT IMPLEMENTED YET - MIGHT THROW AN ERROR SOMEWHERE")
        while iterationsSinceLastUpdate < 1000:
            iterrations += 1
            foundBetterSoln = False
            # calculate the fitness of the population and update the best fitness if necessary
            for individual in initialPopulation:
                individualFitness = self.calculate_fitness(individual)
                if individualFitness > bestFitness:
                    bestIndividual = individual
                    bestFitness = individualFitness
                    foundBetterSoln = True
                    indexOfBestSoln = iterrations
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
        print('Solution found in ', indexOfBestSoln, ' evolutions with a fitness of ', bestFitness)
        print(bestIndividual)

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

        for i in range(self.populationSize):  # Create chromosome individual i

            """
				Chromosome i is a 2D-array / a list of sub-lists with the number of rows (sublists being seld.totalNumClasses)
				and the number of columns (size of a sublist)  being 55 (representing the lessons)
			"""
            newIndividual = []  # Chromosome i

            # Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers) as we building the chromosome
            teacherTimeslotAllocations = self.getEmptyTeacherAllocation()

            currentClass = 0

            while currentClass < self.totalNumClasses:  # Create timeslot allocation for each class j in chromosome i

                # generate an lesson-timeslot allocation  for class j

                # classAllocation = list(range(55))
                # random.shuffle(classAllocation)

                classAllocation = random.sample(self.TIMESLOTS, len(
                    self.TIMESLOTS))  # random.sample(list, size) returns a new shuffled list. The original list remains unchanged.

                """
					Determine if this class allocation a valid one with respect to teacher times
					(i.e. there are (currently) no timeslot conflicts for any teacher when adding this allocation- 
					Hard Constraint 3: A teacher can only teach one lesson in a specific timeslot)
				"""
                isValidAllocation = True

                for lesson in range(len(self.LESSONS)):  # For each of the 55 lessons that we allocated a timeslot

                    timeslot = classAllocation[lesson]  # the timeslot allocated to this lesson

                    subject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this lesson is
                    teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson

                    # check if this teacher is not already teaching in this timeslot

                    teacherAllocation = teacherTimeslotAllocations[teacher]

                    if timeslot in teacherAllocation:  # teacher is already allocated to this timeslot - i.e. there is a clash
                        # BELOW IS TO SWAP WHEN THERE'S A CLASH - SEEMS TO BE TAKING LONGER THAN JUST GENERATING A NEW ALLOCATION FOR THIS CLASS
                        """
						# Find another teacher that teaches this class to swap with
						swapFound = False

						for otherLesson in range(len(self.LESSONS)):  # For each of the 55 lessons
							if otherLesson != lesson:
								otherTimeslot = classAllocation[lesson]  # the timeslot allocated to this other lesson

								if otherTimeslot not in teacherAllocation: # the current teacher is free in this other timeslot
									otherSubject = self.LESSON_SUBJECTS[lesson]  # get the index/number of the subject that this other lesson is
									otherTeacher = self.teachingTable[currentClass][subject]  # teacher that teaches this other lesson
									otherTeacherAllocation = teacherTimeslotAllocations[teacher]

									if timeslot not in otherTeacherAllocation: # the other teacher is free in this current timeslot
										swapFound = True
										# we can swap timeslots
										classAllocation[lesson] = otherTimeslot
										classAllocation[otherLesson] = timeslot
										break # stop the search as we've found another lesson to swap with


						if swapFound == False: # if we did not find another lesson to swap with (since there is a clash), then this cannot be a valid allocation
							isValidAllocation = False
						"""

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
                        subject = self.LESSON_SUBJECTS[
                            lesson]  # get the index/number of the subject that this lesson is
                        teacher = self.teachingTable[currentClass][subject]  # teacher that teaches this lesson
                        teacherTimeslotAllocations[teacher].append(
                            classAllocation[lesson])  # add this timeslot to this teacher's allocated timeslots

                    currentClass = currentClass + 1
                    print('individual', i + 1, ' class', currentClass, '\n',
                          classAllocation)  # i+1 as we want to display starting from 1

            population.append(newIndividual)

        return population

    def getEmptyTeacherAllocation(self) -> [[]]:
        teacherTimeslotAllocations = []
        for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
            teacherAllocation = []
            teacherTimeslotAllocations.append(teacherAllocation)
        return teacherTimeslotAllocations

    def getTeacherAllocation(self, chromosome):
        teacherAllocation = self.getEmptyTeacherAllocation()
        # take the individuals distibution and assign to relevant teachers
        for i in range(len(chromosome)):
            for j in range(len(chromosome[i])):
                sub = self.LESSON_SUBJECTS[j]
                teacher = self.teachingTable[i][sub]
                teacherAllocation[teacher].append(chromosome[i][j])
        return teacherAllocation

    def mutation(self, chromosome):
        mutatedChromosome = []
        teacherAllocation = self.getTeacherAllocation(chromosome)
        for i in range(len(chromosome)):
            # get the class i
            classI = chromosome[i]
            isMutated = False
            MAX_ITER = len(classI)
            for j in range(MAX_ITER):
                # get a random period
                x1 = random.randint(0, 54)
                # get a second random period
                x2 = random.randint(0, 54)
                period1 = classI[x1]
                period2 = classI[x2]
                # get the 2 relevant subjects
                subject1 = self.LESSON_SUBJECTS[x1]
                subject2 = self.LESSON_SUBJECTS[x2]
                teacher1 = self.teachingTable[i][subject1]
                teacher2 = self.teachingTable[i][subject2]
                # get the teacher allocations of those subjects
                teacherAlloc1 = teacherAllocation[teacher1]
                teacherAlloc2 = teacherAllocation[teacher2]
                if period1 not in teacherAlloc2 and period2 not in teacherAlloc1:
                    isMutated = True
                    # update teacher allocations for future
                    teacherAlloc1.remove(period1)
                    teacherAlloc1.append(period2)
                    teacherAlloc2.remove(period2)
                    teacherAlloc1.append(period1)
                    # updating the class
                    classI[x1] = period2
                    classI[x2] = period1
                if isMutated:
                    break
            # The loop will run and the mutated class will be added to the new chromosome
            mutatedChromosome.append(classI)
            print(mutatedChromosome)
        return mutatedChromosome

    def crossover(self, chromosome1, chromosome2):
        # TODO: Crossover
        return chromosome1

    def selection(self, population):
        # TODO: Selection
        parent1 = population[0]  # population[random.randint(0, len(population))]
        parent2 = population[1]  # population[random.randint(0, len(population))]
        return parent1, parent2

    def calculate_fitness(self, chromosome):
        # TODO: GA fitness
        # return fitness of chromosome
        # +5 for every correct allocation. Do we need this?
        # +3 for a double period [done]
        # -2 for more than 2 periods on a subject in a day [done]
        # -1 for two single periods on the same day for a subject [done]
        # -2 for each time a teacher teaches for more than 4 periods consecutively [done]
        fitness = 0
        # for each subject evaluate the allocation (class and teacher wise)
        # empty teacher allocation array
        teacherAllocation = self.getTeacherAllocation(chromosome)
        # check to see if any teacher works more than 4periods at once
        for teacher in teacherAllocation:
            workingPeriods = teacher
            # sort in order [0, 54]
            workingPeriods.sort()
            consecutive = 0
            for i in range(len(workingPeriods) - 1):
                if workingPeriods[i] + 1 == workingPeriods[i + 1]:
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
            for j in range(len(chromosome[i]) - 1):
                # for each slot after j
                for k in range(j + 1, len(chromosome[i]) - 1):
                    # get subject being held at j
                    subject1 = self.LESSON_SUBJECTS[j]
                    # get subject being held at k
                    subject2 = self.LESSON_SUBJECTS[k]
                    # check if they are the same subject
                    if subject1 == subject2:
                        # check if they are consecutive
                        if chromosome[i][j] + 1 == chromosome[i][k]:
                            fitness += 3
                    else:
                        break
        # penalize two seperate periods on the same day
        for gene in chromosome:
            subjectsAllocatedForClass = []
            for g in range(len(gene)):
                pos = gene.index(g)
                subject = self.LESSON_SUBJECTS[pos]
                subjectsAllocatedForClass.append(subject)
            for s in range(len(subjectsAllocatedForClass) - 2):
                # 3 consec periods of the same subject
                if subjectsAllocatedForClass[s] == subjectsAllocatedForClass[s + 1] and subjectsAllocatedForClass[s] == \
                        subjectsAllocatedForClass[s + 2]:
                    fitness -= 2
                else:
                    continue
            counter = 0
            # check if there is 2 periods of the same subjects in the same day[not consecutive]
            for s in range(len(subjectsAllocatedForClass)):
                subject = subjectsAllocatedForClass[s]
                for t in range(s + 2, 11):
                    if subject == subjectsAllocatedForClass[t]:
                        fitness -= 1
        print('Individual fitness = ', fitness)
        return fitness


"""
	CAT SWARM OPTIMIZATION ALGORITHM
"""


class CatSwarmAlgorithm(TimetableAlgorithm):
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
            self.solution = [[]]
            """current solution the cat possesses
			"""


        def setState(self, newState: int):
            """
					setter for state
			"""
            self.state = newState


        def setSolution(self, newSolution: [[]]):
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

        # set global best fitness to worst possible
        global_best_fitness = 1000000  # may need to change once we determine objective function, place holder value for now

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
                # copied it as is from the paper, but I think we want to maximise - need to change it here and in seek
                if current_cat_fitness <= global_best_fitness:  # assuming out fitness function wants to minimise
                    global_best_fitness = current_cat_fitness
                    self.global_best_cat = current_cat

                # choose a random value between 0 and 1
                random_value = random.random()
                # is random number > MR
                if random_value > MR:
                    # current_cat[self.mode_index] = self.SEEKING
                    current_cat.setState(self.CAT.SEEKING)
                # self.seek(current_cat)
                else:
                    # current_cat[self.mode_index] = self.TRACING
                    current_cat.setState(self.CAT.TRACING)
                # self.trace(current_cat) put the "behaviour" here bc it's not clear where it should go, and in the
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
        # Execute local search refining procedure in order to improve the quality of resultant time timetable
        # regarding teachers gaps
        return self.global_best_cat

    def intialiseCats(self):
        # initialise n cats (paper says 30, we may need to change)
        # revisiting the logic later
        CATS = []  # list of individual cats -> size will be self.populationSize after we add all the cats

        for i in range(self.populationSize):  # Create cat i

            teacherClassAlloc = list(range(1, 56))

            # rows = classes, cols= timeslots
            new_allocation = [[0 for i in range(len(self.TIMESLOTS))] for j in range(self.totalNumClasses)]  # cat i
            for j in range(len(new_allocation[0])):
                random.shuffle(teacherClassAlloc)
                for i in range(len(new_allocation)):
                    new_allocation[j][i] = teacherClassAlloc[i]

            new_cat = self.CAT()
            new_cat.setSolution(new_allocation)
            CATS.append(new_cat)

            # Build a Teacher-Timeslot allocation table (to keep track of timeslots already assigned to the Teachers)
            # as we building the chromosome

            teacherTimeslotAllocations = []

            for teacher in range(self.numTeachers):  # Add an empty array for each Teacher
                teacherAllocation = []
                teacherTimeslotAllocations.append(teacherAllocation)

        return CATS

    def evaluateFitness(self, current_cat: CAT):
        # change later
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
                for k in range(j+1, len(current_cat_solution[i])):
                    if teacherVal == current_cat_solution[i][k]:
                        n += 1
            if n>10 :
                fitnessValue += ITDW * BASE

        return fitnessValue

    def seek(self, cats: typing.List[CAT]):
        # add code for seeking
        # values from the paper after experimentation
        SPC = True
        SMP = 2
        CDC = 0.1
        SRD = 0.1
        j = 0  # default initialisation
        candidate_positions = []
        for cat_copy in cats:
            best_fitness = self.evaluateFitness(cat_copy)
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
                    new_fitness_value = self.evaluateFitness(cat)
                    if new_fitness_value <= best_fitness:
                        best_fitness = new_fitness_value
                        candidate_positions.append(cat)

            old_fitness = self.evaluateFitness(candidate_positions[0])
            FSmax = best_fitness
            FSmin = self.evaluateFitness(self.global_best_cat)
            equal = True
            for i in range(len(candidate_positions) - 1):
                fitness = self.evaluateFitness(candidate_positions[i])
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
                    FSi = self.evaluateFitness(candidate_positions[i])
                    Pi = abs(FSi - FSb) / abs(FSmax - FSmin)
                    probabilities[i] = Pi

            # pick a random position from the candidate positions the one to move to
            # need to choose somehow, paper does't specify (probably using the probabilities)
            random_pos = random.choices(candidate_positions, weights=probabilities, k=1)[0]  # function returns a list
            # of size k
            cat_copy.setSolution(random_pos.getSolution())

    def trace(self, cats: typing.List[CAT]):
        # add code for tracing
        for cat in cats:
            c1 = 1  # i can't find where they set this value??? or explain it???
            similarity = self.Similarity(cat)
            distance = self.totalNumClasses * len(self.TIMESLOTS) - similarity
            rand_number = random.random()
            cs = rand_number * c1 * distance  # number of cells to be swapped

            for _ in range(round(cs)):
                self.Single_Swap(cat)

    def Similarity(self, cat: CAT):
        similarity = 0
        cat_solution = cat.getSolution()
        global_best_cat_solution = self.global_best_cat.getSolution()
        for i in range(len(cat_solution)):
            for j in range(len(cat_solution[i])):
                if cat_solution[i][j] == global_best_cat_solution[i][j]:
                    similarity += 1
        return similarity

    def Single_Swap(self, current_cat: CAT):
        randClass = random.randint(0, self.totalNumClasses)
        randCell1 = random.randint(0, 56)
        randCell2 = random.randint(0, 56)
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
            current_cat_solution[randClass][randCell1] = current_cat[randClass][randCell2]
            current_cat_solution[randClass][randCell2] = tempCat

        current_cat.setSolution(current_cat_solution)
        return current_cat

    def Change_Random(self, cat_copy: CAT):
        # auxilliary procedure, section 3.4.3
        rand_col = random.randint(0, len(self.TIMESLOTS) - 1)
        cat_solution = cat_copy.getSolution()
        global_best_solution = self.global_best_cat.getSolution()
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
