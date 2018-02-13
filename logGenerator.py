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

mostPopAuthors = """SELECT DISTINCT name, SUM(numofviews)
OVER (PARTITION BY name) AS authorviews
FROM q2v1, q2v2
WHERE q2v1.title = q2v2.title
GROUP BY (name, numofviews)
ORDER BY authorviews DESC;
"""
# query_q3 = """
# """

# database name is declared here to be accessable to all functions.
DBNAME = "news"


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

def question_2():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(mostPopAuthors)
    output = cursor.fetchall()
    db.close()

    return output

# def question_3(db):
#   return output


# format and send output to file.
def generateLog(outq1, outq2):
    # generating formatted string for output of question 1
    output_q1 = "\n\t\tArticles Ranked by Popularity\n"
    output_q1 += '-'*60 + "\n"
    output_q1 += '{0:40} | {1:20}'.format('Article', 'Number Of Views') + '\n'
    output_q1 += '-'*60 + "\n"
    for ele in outq1:
        output_q1 += '{0:40} | {1:15}'.format(ele[0], ele[1]) + "\n"
        output_q1 += '-'*60 + "\n"

    # generating formatted string for output of question 2
    output_q2 = "\n\t\tAuthors Ranked by Popularity\n"
    output_q2 += '-'*60 + "\n"
    output_q2 += '{0:40} | {1:20}'.format('Authors', 'Number Of Views') + '\n'
    output_q2 += '-'*60 + "\n"
    for ele in outq2:
        output_q2 += '{0:40} | {1:15}'.format(ele[0], ele[1]) + "\n"
        output_q2 += '-'*60 + "\n"


    with open('report.txt', 'w') as f:
        f.write(output_q1)
        f.write(output_q2)
    f.close()

    print(output_q1)
    print(output_q2)


def main():

    create_all_views()
    outlog_q1 = question_1()
    outlog_q2 = question_2()

    # print(type(outlog))
    # print(outlog)
    generateLog(outlog_q1, outlog_q2)

#
if __name__ == "__main__":
    main()
