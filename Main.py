from Algorithms import *
import datetime
import time

"""Problem Constants"""
SUBJECTS = [
    "Home Language", "First Additional Language", "Mathematics", "Natural Science", "Social Science",
    "Technology", "Economic and Management Science", "Life Orientation", "Arts and Culture"
]

# Using List Comprehension to define the Lesson and Timeslot numbers
LESSONS = [lesson for lesson in range(1, 56)]
TIMESLOTS = [timeslot for timeslot in range(1, 56)]


def readInputFile(fileName: str):
    inputFile = open(fileName)

    numGr7Classes = int(inputFile.readline())
    numGr8Classes = int(inputFile.readline())
    numGr9Classes = int(inputFile.readline())

    totalnumClasses = numGr7Classes + numGr8Classes + numGr9Classes

    while True:  # Get the next non-empty/non-blank line (to skip over any blank lines between the number of classes of each grade and the number of teachers )
        lineString = inputFile.readline()
        if lineString != "\n":
            numTeachers = int(lineString)
            break

    """
		This table variable is a 2D list/array indicating the teacher to Class-Subject allocations i.e. which Teacher 
		teaches a specific subject to a specific class. The rows are the classes and the columns are the subjects,
		 and the value at [i, j] is the TeacherID of the teacher who teaches Subject j to Class i
		
		It can also be viewed as a list of lists with each sublist being a row in the table - each sublist representing a Class.
		For sublist i, the value at index j is the teacher (numerical value - TeacherID) who teaches Subject j to Class i
		

	"""
    teachingTable = []

    for Class in range(
            totalnumClasses):  # For each Class (using Uppercase so as to not be mistaken for the 'class' keyword)
        while True:  # Get the next non-empty/non-blank line (to skip over any blank lines between the number of teachers and the table itself)
            teacherAllocationString = inputFile.readline()
            if teacherAllocationString != "\n":
                break

        teacherAllocations = []  # the array of allocations of Teachers to Subjects for this Class

        for Subject in range(9):  # For each (of the 9) Subject
            teacherAllocationString = teacherAllocationString.strip()  # Remove leading and trailing whitespaces so that the beginning of the string is a numerical value representing a teacher

            """
				Get the index of the first comma in the teacherAllocationString
				In the input file, teachers are separated by commas 
				
				
			"""
            commaIndex = teacherAllocationString.find(",")

            """
				If we are at the last subject (Subject == 8), then  there wont be a comma after the 
				TeacherID for this subject in the string (commaIndex will be -1), so dont do any slicing - the TeacherID (as a string)
				for this Subject is the remaining teacherAllocationsString
	
				Else (if not the last Subject, thus there is a comma between the TeacherID for this Subject and the next Subject)
				then to get the TeacherID (as a string) for this Subject, slice from the beginning of the teacherAllocationsString till the character
				before the comma
			"""

            if commaIndex == -1:
                teacherIDString = teacherAllocationString
            else:
                teacherIDString = teacherAllocationString[:commaIndex]

            teacherID = int(teacherIDString)
            teacherAllocations.append(teacherID)
            teacherAllocationString = teacherAllocationString[
                                      commaIndex + 1:]  # Remove the teacherID for this Subject from teacherAllocationString

        teachingTable.append(teacherAllocations)

    inputFile.close()

    # A Variable of type Input to represent the input obtained from the text file
    inputInstance = Input(teachingTable, numTeachers, numGr7Classes, numGr8Classes, numGr9Classes)

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

    print(
        "\n\nSolving the Timetabling Problem for Grades 7 to 9 based on the  South African DOE's Curriculum Guidelines")
    print("using a Genetic Algorithm and Cat Swarm Optimization Algorithm and comparing the results")
    print(
        "==============================================================================================================")
    print(
        "==============================================================================================================")
    print(
        "==============================================================================================================\n\n")

    print("Subjects: ")
    for i in range(len(SUBJECTS)):
        # Subjects are represented as digits from 0 to 8 but will display as 1 to 9
        print("\tSubject ", i + 1, ": ", SUBJECTS[i], sep="")

    print("==================================================================")
    print("==================================================================\n\n")

    input1 = readInputFile("Input/easy.txt")
    input2 = readInputFile("Input/medium.txt")
    input3 = readInputFile("Input/hard.txt")

    inputNumber = 1

    for input in [input1, input2, input3]:

        print("INPUT", inputNumber)
        print("----------")
        input.print()
        print("=================================================================")

        """
			I set the pop sizes to 100 for now  so that the program runs
			TODO - determine appropriate population sizes
		"""
        populationSizeGA = 3
        populationSizeCSA = 1

        geneticAlgorithm = GeneticAlgorithm(input, populationSizeGA)
        catSwarmAlgorithm = CatSwarmAlgorithm(input, populationSizeCSA)

        for algorithm in [catSwarmAlgorithm]:
            algorithmName = type(algorithm).__name__

            print("\nSolving INPUT ", inputNumber, " using the ", algorithmName, ":", sep="")

            bestSolution, generationBestSolution, fitnessBestSolution = algorithm.solveTimetable()

            print('Optimal solution found in generation', generationBestSolution, ' with a fitness of ', fitnessBestSolution)
            algorithm.printSolution(bestSolution)


            print("\n=================================================================")

        print("\n=================================================================\n\n")

        inputNumber += 1


main()
