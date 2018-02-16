# Project03-Log-Analysis
Code for the third project in the Full Stack Nanodegree program from Udacity.

## Purpose and Overview

This program is to fulfill the requirements for the third project in the Udacity Fullstack Nanodegree.
The function of the program is to simulate a report generating script that pulls a static set of information from the execution logs and article database for an online website.
The information gathered will be for 3 static and pre-determined questions. These were set in the original project specfication and the queries are hardcoded in the script itself. At this time there is no capability to generate reports of different combinations without changing the code itself.
The questions answered are:
1. What are the most popular articles of all time? Which articles have been accessed the most. Present this information as a sorted list with the most popular at the top.
2. Who are the most popular article authors of all time? That is when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## Views and Queries

The following are the SQL views and queries that are run to compile the information for each question.

### Question 1 views and query

CREATE OR REPLACE VIEW articleList AS
SELECT path, status, COUNT(id) AS NumOfViews FROM log
GROUP BY (path, status)
ORDER BY COUNT(id) DESC;

CREATE OR REPLACE VIEW goodviews AS
SELECT * FROM articleList
WHERE SUBSTRING(status, 1, 6) = '200 OK'
AND OCTET_LENGTH(path) > OCTET_LENGTH('/');

SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';

### Question 2 views and query

CREATE OR REPLACE VIEW name_titleView AS
SELECT name, title FROM authors, articles
WHERE authors.id = articles.author;

CREATE OR REPLACE VIEW title_numberView AS
SELECT articles.title, goodviews.numofviews
FROM articles, goodviews
WHERE articles.slug
LIKE '%'||TRIM(leading '/articles/' FROM goodviews.path)||'%';

SELECT DISTINCT name, SUM(numofviews)
OVER (PARTITION BY name) AS authorviews
FROM name_titleView, title_numberView
WHERE name_titleView.title = title_numberView.title
GROUP BY (name, numofviews)
ORDER BY authorviews DESC;

### Question 3 views and query

CREATE OR REPLACE VIEW daily_totalView AS
SELECT date_trunc('day', time), COUNT(*)
FROM log
GROUP BY date_trunc('day', time)
ORDER BY count DESC;

CREATE OR REPLACE VIEW daily_errorView AS
SELECT date_trunc('day', time), COUNT(*)
FROM log WHERE status != '200 OK'
GROUP BY date_trunc('day', time)
ORDER BY count DESC;

SELECT PG_CATALOG.DATE(daily_totalView.date_trunc),
daily_totalView.count AS total, daily_errorView.count AS errors
FROM daily_totalView, daily_errorView
WHERE daily_totalView.date_trunc = daily_errorView.date_trunc
AND CAST(daily_errorView.count AS FLOAT)/daily_totalView.count > 0.01;

## How to run
1. To run this program must be installed on a linux system running postgres.
2. Copy the [zip file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) to the target machine.
3. Unzip the file in the project directory.
4. Run ther sql script.
5. Copy or download the Log-Analysis repo into your project directory.
6. Change to the project directory and from the commannd line run:
      `$ logGenerator.py`


