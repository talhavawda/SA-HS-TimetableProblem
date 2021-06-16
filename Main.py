

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


	teachingTable1 =
	teachingTable2 =
	teachingTable3 =





	for inputTeachingTable in [teachingTable1, teachingTable2, teachingTable3]:
		geneticAlgorithm = GeneticAlgorithm(inputTeachingTable)
		catSwarmAlgorithm = CatSwarmAlgorithm(inputTeachingTable)

		for algorithm in [geneticAlgorithm, catSwarmAlgorithm]:

			algorithm.solveTimetable()

main()


