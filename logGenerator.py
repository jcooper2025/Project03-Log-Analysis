#

import psycopg2

# set up the strings for the views and queries that will collect the data for all the questions.
# Strings to hold the views that are created for each question.
view_q1 = """
"""
view_q2 = """
"""
view_q3 = """
"""

# Strings to hold the sql queries to extract the information for each question.
query_q1 = """
"""
query_q2 = """
"""
query_q3 = """
"""

# Strings to hold the returned data from each query.
output_q1 = """
"""
output_q2 = """
"""
output_q3 = """
"""

# Strings to hold constants related to the formatted output.
cellBorders = """
"""
tableHeader = """
"""

# function declarations.
# set up database connections
def connectDB():
	return db

# execute queries to answer each question
def question_1(db):
	return output

def question_2(db):
	return output

def question_3(db):
	return output

# format and send output to file.
def generateLog(out):


def main():
	
# 
if __name__ == "__main__":
	main()
