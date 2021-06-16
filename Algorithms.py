class Input():
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
	LESSONS = [lesson for lesson in range(1, 56)]
	TIMESLOTS = [timeslot for timeslot in range(1, 56)]



	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor

			:param input:	An object of type Input containing the teachingTable, numTeachers, numGr7Classes, numGr8Classes,
			and numGr9Classes of this problem instance

			:param teachingTable:	A 2D list/array indicating the teacher to Class-Subject allocations
			The rows are the classes and the columns are the subjects, and the value at [i, j] is the TeacherID of
			the teacher who teachers Subject j to Class i

			:param populationSize	the size of the population to use for the Algorithm

		"""


	def solveTimetable(self):
		"""
			Solve the Timetable Problem using this algorithm
			The function can call helper functions defined in the subclass that it can use to solve

			:return:The optimal feasible solution after the termination critera has been met
		"""


class GeneticAlgorithm(TimetableAlgorithm):

	def __init__(self, input: Input, populationSize: int = 100):
		"""
			Constructor for the Genetic Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm
			Popuzlation Size is assigned a default value of 100

		"""

		self.teachingTable = input.teachingTable
		self.numTeachers = input.numTeachers
		self.numGr7Classes = input.numGr7Classes
		self.numGr8Classes = input.numGr8Classes
		self.numGr9Classes = input.numGr9Classes
		self.populationSize = populationSize

	def solveTimetable(self):
		"""
			Implementing this abstract function defined in the superclass

			Solve the Timetable Problem using this Genetic algorithm

			:return:The optimal feasible solution after the termination critera has been met
		"""




class CatSwarmAlgorithm(TimetableAlgorithm):
	def __init__(self, input: Input, populationSize: int):
		"""
			Constructor for the Cat Swarm Optimization Algorithm

			Parameters are the same as that of its superclass TimetableAlgorithm

		"""

		self.teachingTable = input.teachingTable
		self.numTeachers = input.numTeachers
		self.numGr7Classes = input.numGr7Classes
		self.numGr8Classes = input.numGr8Classes
		self.numGr9Classes = input.numGr9Classes
		self.populationSize = populationSize



	def solveTimetable(self):
		"""
			Implementing this abstract function defined in the superclass

			Solve the Timetable Problem using this Cat Swarm Optimization algorithm
			This function can call helper functions defined in the subclass that it can use to solve

			:return:The optimal feasible solution after the termination critera has been met
		"""

