#

import psycopg2

# set up the strings for the views and queries that will collect the data for all the questions.
# Strings to hold the views that are created for each question.
articleList = """CREATE VIEW articleList AS 
SELECT path, status, COUNT(id) AS NumOfViews FROM log 
GROUP BY (path, status) 
ORDER BY COUNT(id) DESC;
"""

goodViews = """CREATE VIEW goodviews AS
SELECT * FROM articleList 
WHERE SUBSTRING(status, 1, 6) = '200 OK' 
AND OCTET_LENGTH(path) > OCTET_LENGTH('/');
"""
# view_q3 = """
# """

# Strings to hold the sql queries to extract the information for each question.
query_q1 = """SELECT articles.title, goodviews.numofviews 
FROM articles, goodviews 
WHERE articles.slug LIKE '%'||TRIM(leading '/articles/' from goodviews.path)||'%';
"""
# query_q2 = """
# """
# query_q3 = """
# """

# Strings to hold the returned data from each query.
output_q1 = """
"""
# output_q2 = """
# """
# output_q3 = """
# """

# Strings to hold constants related to the formatted output.
# cellBorders = """
# """
# tableHeader = """
# """

# database name is declared here to be accessable to all functions.
DBNAME = "news"

# function declarations.
# set up database connections
# def connectDB():
# 	return db, cursor

# execute queries to answer each question
def question_1():
	db = psycopg2.connect(database=DBNAME)
	cursor = db.cursor()
	cursor.execute("drop view if exists goodviews;")
	cursor.execute("drop view if exists articleList;")
	cursor.execute(articleList)
	cursor.execute(goodViews)
	cursor.execute(query_q1)
	output = cursor.fetchall()

	return output

# def question_2(db):
# 	return output

# def question_3(db):
# 	return output

# format and send output to file.
def generateLog(out):
	print('{0:40} | {1:20}'.format('Article', 'Number Of Views'))
	print('-'*60)
	for ele in out:
		print('{0:40} | {1:15}'.format(ele[0], ele[1]))
		print('-'*60)


def main():

	outlog = question_1()
	# print(type(outlog))
	# print(outlog)
	generateLog(outlog)

# 
if __name__ == "__main__":
	main()
