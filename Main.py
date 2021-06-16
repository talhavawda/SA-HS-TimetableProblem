from Algorithms import *



def readInputFile(fileName: str):

	inputFile = open(fileName)
	inputInstance = Input() # A Variable of type Input to represent the input obtained from the text file

	inputInstance.numGr7Classes = int(inputFile.readline())
	inputInstance.numGr9Classes = int(inputFile.readline())
	inputInstance.numGr9Classes = int(inputFile.readline())

	totalnumClasses = inputInstance.numGr7Classes + inputInstance.numGr8Classes + inputInstance.numGr9Classes

	while True:  # Get the next non-empty/non-blank line (to skip over any blank lines between the number of classes of each grade and th number of teachers )
		lineString = inputFile.readline()
		if lineString != "\n":
			inputInstance.numTeachers = int(lineString)
			break


	for c in range(totalnumClasses): # For each class
		



	"""
		This table variable is a 2D list/array indicating the teacher to Class-Subject allocations i.e. which Teacher 
		teaches a specific subject to a specific class. The rows are the classes and the columns are the subjects,
		 and the value at [i, j] is the TeacherID of the teacher who teaches Subject j to Class i
		
		It can also be viewed as a list of lists with each sublist being a row in the table - each sublist representing a Class.
		For sublist i, the value at index j is the teacher (numerical value) i who teaches Subject j to Class i
		

	"""
	teachingTable = []





	return inputInstance


def main():
	"""
		The main function of the program
		It reads in the input text files, determines the relevant Data Structure variables,
		solves the South African High School Timetable Problem (for Grades 7 to 9)
		using Genetic Algorithm and Cat Swarm Optimization Algorithm,
		and displays the results (by calling the relevant functions)

	:return: None

	"""

	print("\n\nSolving the Timetabling Problem for Grades 7 to 9 based on the  South African DOE's Curriculum Guidelines")
	print("using a Genetic Algorithm and Cat Swarm Optimization Algorithm and comparing the results")
	print("==============================================================================================================\n\n")


	input1 = readInputFile("Input/SampleInput1.txt")
	input2 = readInputFile("Input/SampleInput2.txt")
	input3 = readInputFile("Input/SampleInput3.txt")


	for input in [input1, input2, input3]:

		populationSizeGA =
		populationSizeCSA =

		geneticAlgorithm = GeneticAlgorithm(input, populationSizeGA)
		catSwarmAlgorithm = CatSwarmAlgorithm(input, populationSizeCSA)

		for algorithm in [geneticAlgorithm, catSwarmAlgorithm]:
			algorithm.solveTimetable()


main()


