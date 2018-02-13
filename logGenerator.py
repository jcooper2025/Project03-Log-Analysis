#

# This script will create a report that answers the following three questions:
# 1. What are the most popular articles of all time? Which articles have been
# accessed the most. Present this information as a sorted list with the most
# popular at the top.

# 2. Who are the most popular article authors of all time? That is when you sum up
# all of the articles each author has written, which authors get the most page
# views? Present this as a sorted list with the most popular author at the top.

# 3. On which days did more than 1% of requests lead to errors? The log table
# includes a column status that indicates the HTTP status code that the news
# site sent to the user's browser.

import psycopg2

# set up the strings for the views and queries that will collect the data for
# all the questions. Strings to hold the views that are created for each
# question.
# Views to simplify the queries.
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
authorsTitles = """CREATE VIEW name_titleView AS
SELECT name, title FROM authors, articles
WHERE authors.id = articles.author;
"""
titleViews = """CREATE VIEW title_numberView AS
SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';
"""

# Strings to hold the sql queries to extract the information for each question.
mostPopArticles = """SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';
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
#   return db, cursor


def create_all_views():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    # do cleanup in case there are any views from previous runs.
    cursor.execute("drop view if exists name_titleView cascade;")
    cursor.execute("drop view if exists title_numberView cascade;")
    cursor.execute("drop view if exists goodviews cascade;")
    cursor.execute("drop view if exists articleList cascade;")
    cursor.execute(articleList)
    cursor.execute(goodViews)
    cursor.execute(authorsTitles)
    cursor.execute(titleViews)
    db.close()


# execute queries to answer each question
def question_1():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(mostPopArticles)
    output = cursor.fetchall()
    db.close()

    return output

# def question_2(db):
#   return output

# def question_3(db):
#   return output


# format and send output to file.
def generateLog(out):
    output_q1 = "\n\t\tArticles Ranked by Popularity\n"
    output_q1 += '-'*60 + "\n"
    output_q1 += '{0:40} | {1:20}'.format('Article', 'Number Of Views') + '\n'
    output_q1 += '-'*60 + "\n"
    for ele in out:
        output_q1 += '{0:40} | {1:15}'.format(ele[0], ele[1]) + "\n"
        output_q1 += '-'*60 + "\n"

    with open('report.txt', 'w') as f:
        f.write(output_q1)
    f.close()

    print("\n\t\tArticles Ranked by Popularity\n")
    print('-'*60)
    print('{0:40} | {1:20}'.format('Article', 'Number Of Views'))
    print('-'*60)
    for ele in out:
        print('{0:40} | {1:15}'.format(ele[0], ele[1]))
        print('-'*60)


def main():

    create_all_views()
    outlog = question_1()
    # print(type(outlog))
    # print(outlog)
    generateLog(outlog)

#
if __name__ == "__main__":
    main()
