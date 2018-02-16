#!/usr/bin/python
"""
This file serves as a report generating script for the 'News' database.

It generates an onscreen report and output file to answer hardcoded queries.
"""

# This script will create a report that answers the following three questions:
# 1. What are the most popular articles of all time? Which articles have been
# accessed the most. Present this information as a sorted list with the most
# popular at the top.

# 2. Who are the most popular article authors of all time? That is when you
# sum up all of the articles each author has written, which authors get the
# most page views? Present this as a sorted list with the most popular author
# at the top.

# 3. On which days did more than 1% of requests lead to errors? The log table
# includes a column status that indicates the HTTP status code that the news
# site sent to the user's browser.

import psycopg2

# set up the strings for the views and queries that will collect the data for
# all the questions. Strings to hold the views that are created for each
# question.
# Views to simplify the queries.
articleList = """CREATE OR REPLACE VIEW articleList AS
SELECT path, status, COUNT(id) AS NumOfViews FROM log
GROUP BY (path, status)
ORDER BY COUNT(id) DESC;
"""

goodViews = """CREATE OR REPLACE VIEW goodviews AS
SELECT * FROM articleList
WHERE SUBSTRING(status, 1, 6) = '200 OK'
AND OCTET_LENGTH(path) > OCTET_LENGTH('/');
"""

# create a view with authors and their associated articles by title.
authorsTitles = """CREATE OR REPLACE VIEW name_titleView AS
SELECT name, title FROM authors, articles
WHERE authors.id = articles.author;
"""

# create a view with article title and the number of views it has.
titleViews = """CREATE OR REPLACE VIEW title_numberView AS
SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';
"""

# this gives all of the requests for each day.
dailyTotalView = """CREATE OR REPLACE VIEW daily_totalView AS
SELECT date_trunc('day', time), COUNT(*)
FROM log
GROUP BY date_trunc('day', time)
ORDER BY count DESC;
"""

# this will give all of the requests in a day that resulted in an error.
dailyErrorView = """CREATE OR REPLACE VIEW daily_errorView AS
SELECT date_trunc('day', time), COUNT(*)
FROM log WHERE status != '200 OK'
GROUP BY date_trunc('day', time)
ORDER BY count DESC;
"""

# Strings to hold the sql queries to extract the information for each question.
mostPopArticles = """SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';
"""

mostPopAuthors = """SELECT DISTINCT name, SUM(numofviews)
OVER (PARTITION BY name) AS authorviews
FROM name_titleView, title_numberView
WHERE name_titleView.title = title_numberView.title
GROUP BY (name, numofviews)
ORDER BY authorviews DESC;
"""

mostErrorDays = """SELECT PG_CATALOG.DATE(daily_totalView.date_trunc),
daily_totalView.count AS total, daily_errorView.count AS errors
FROM daily_totalView, daily_errorView
WHERE daily_totalView.date_trunc = daily_errorView.date_trunc
AND CAST(daily_errorView.count AS FLOAT)/daily_totalView.count > 0.01;
"""

# database name is declared here to be accessable to all functions.
DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
cursor = db.cursor()


def create_all_views():
    """Do cleanup in case there are any views from previous runs."""
    cursor.execute(articleList)
    cursor.execute(goodViews)
    cursor.execute(authorsTitles)
    cursor.execute(titleViews)
    cursor.execute(dailyTotalView)
    cursor.execute(dailyErrorView)


# execute queries to answer each question
def question_1():
    """
    Execute query to find the most popular articles.

    Return the output as a list of tuples.
    """
    cursor.execute(mostPopArticles)
    output = cursor.fetchall()
    return output


def question_2():
    """
    Execute query to find the most popular authors.

    Return the output as a list of tuples.
    """
    cursor.execute(mostPopAuthors)
    output = cursor.fetchall()
    return output


def question_3():
    """
    Find the dates when more than 1% of the view requests resulted in errors.

    Return the output as a list of tuples.
    """
    cursor.execute(mostErrorDays)
    output = cursor.fetchall()
    return output


# format and send output to file.
def generateLog(outq1, outq2, outq3):
    """
    Generate output strings for all three questions.

    Print formatted output to the screen and a report file.
    """
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

    # generating formatted string for output of question 3
    output_q3 = "\n\t\tDays with more than 1% error returns\n"
    output_q3 += '-'*60 + "\n"
    output_q3 += '{0:15} | {1:20} | {2:20}'.format(
                                                    'Date',
                                                    'Number Of Views',
                                                    'Number of Errors') + '\n'
    output_q3 += '-'*60 + "\n"
    for ele in outq3:
        output_q3 += '{0:15} | {1:20} | {2:15}'.format(
                                                        str(ele[0]),
                                                        ele[1], ele[2]) + "\n"
        output_q3 += '-'*60 + "\n"

    with open('report.txt', 'w') as f:
        f.write(output_q1)
        f.write(output_q2)
        f.write(output_q3)
    f.close()

    print(output_q1)
    print(output_q2)
    print(output_q3)


def main():
    """
    Call specialized functions to execute script steps and run queries.

    Print out results to screen and write to a file.
    """
    create_all_views()
    outlog_q1 = question_1()
    outlog_q2 = question_2()
    outlog_q3 = question_3()

    db.close()

    generateLog(outlog_q1, outlog_q2, outlog_q3)


if __name__ == "__main__":
    main()
