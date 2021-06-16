from Algorithms import *



def readInputFile(filename: str):


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


	input1 = readInputFile("Input/SampeInput1.txt")
	input2 = readInputFile("Input/SampeInput2.txt")
	input3 = readInputFile("Input/SampeInput3.txt")


	input1 = []
	input2 = []
	input3 = []


	for sampleInput in [input1, input2, input3]:
		teachingTable = sampleInput[0]
		numTeachers = sampleInput[1]
		numGr7Classes = sampleInput[2]
		numGr8Classes = sampleInput[3]
		numGr9Classes = sampleInput[4]

		populationSizeGA =
		populationSizeCSA =

		geneticAlgorithm = GeneticAlgorithm(teachingTable, numTeachers, numGr7Classes, numGr8Classes, numGr9Classes, populationSizeGA)
		catSwarmAlgorithm = CatSwarmAlgorithm(teachingTable, numTeachers, numGr7Classes, numGr8Classes, numGr9Classes, populationSizeCSA)

		for algorithm in [geneticAlgorithm, catSwarmAlgorithm]:

			algorithm.solveTimetable()


main()


