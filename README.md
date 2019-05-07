PROJECT LOGS ANALYSIS


Create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

File containing database : newsdata.sql
Source code file : logsanalysis.py
Program's output file : project1_output.txt


BRING ORDER TO CHAOS BY CREATING VIEWS IN DATABASE


Three tables:

          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant


 id column from table authors relates with author column from table articles
 slug column from table articles relates with column path from table log (slug is included in path but not equal) ... CONCAT to the rescue


# create view to put together relevant combined data from articles and authors and making possible to relate with log

CREATE VIEW relevant AS
SELECT articles.title,
	articles.slug,
	CONCAT('/article/',articles.slug) AS path,
	authors.name
FROM articles INNER JOIN authors
ON articles.author=authors.id;


# create view to show only logs relevant to articles

CREATE VIEW relevantlogs AS
SELECT log.path,
	relevant.title,
	relevant.name
FROM log JOIN relevant
ON log.path=relevant.path;


# create view to make it easier in python 

CREATE VIEW finalview AS
SELECT path,
	COUNT( * ) AS views,
	name,
	title,
FROM relevantlogs
GROUP BY path,name,title
ORDER BY views DESC;


               path                | views  |          name          |               title
------------------------------------+--------+------------------------+------------------------------------
 /article/candidate-is-jerk         | 338647 | Rudolf von Treppenwitz | Candidate is jerk, alleges rival
 /article/bears-love-berries        | 253801 | Ursula La Multa        | Bears love berries, alleges bear
 /article/bad-things-gone           | 170098 | Anonymous Contributor  | Bad things gone, say good people
 /article/goats-eat-googles         |  84906 | Ursula La Multa        | Goats eat Google's lawn
 /article/trouble-for-troubled      |  84810 | Rudolf von Treppenwitz | Trouble for troubled troublemakers
 /article/balloon-goons-doomed      |  84557 | Markoff Chaney         | Balloon goons doomed
 /article/so-many-bears             |  84504 | Ursula La Multa        | There are a lot of bears
 /article/media-obsessed-with-bears |  84383 | Ursula La Multa        | Media obsessed with bears
(8 rows)


Until here first 2 questions are covered and for the last question we need just table log and columns status and time


# create view to change data type from date with time stamp to date type for column time

CREATE VIEW statuslogs AS
SELECT status,
	date(time) as req_date,
FROM logs;


# create view to show status day by day

CREATE VIEW statusperday AS
SELECT status,
	req_date,
	COUNT(status) AS requests
FROM statuslogs
GROUP BY req_date,status;


# create view all request day by day , successful and unsuccessful

CREATE VIEW requestsperday AS
SELECT req_date,
	COUNT(req_date) AS allreq
FROM statuslogs
GROUP BY req_date;



# create view to show daily percentage for each status


CREATE VIEW dailypercentage AS
SELECT statusperday.status,
	statusperday.req_date,
	ROUND(100 * (statusperday.requests::numeric/requestsperday.allreq),2) AS percentage
FROM statusperday LEFT JOIN requestsperday
ON statusperday.req_date=requestsperday.req_date;



Now we have order and we can answer the questions by interogating views : finalview and dailypercentage
