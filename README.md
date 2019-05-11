# PROJECT LOGS ANALYSIS


Create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

File containing database : newsdata.sql. You can download the file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it.  
File with views created : views.sql  
Source code file : logsanalysis.py  
Program's output file : project1_output.txt  
Requirements : Python and Postgres installed  
Python modules required : termcolor and colorama. If not already installed, write in command line
'pip install colorama termcolor'  
Prior running the program , you have to set up the database, therefore :

## Steps to set up database

_If no password is requireed to connect to Postgres , '-U postgres' is not required in step 1 and 4_

* Step 1:  Connect to Postgres -- psql -U postgres
* Step 2:  Create new db news -- create database news;
* Step 3:  Exit Postgres -- \q
* Step 4:  Import data from newsdata.sql file to db news and connect to it -- psql -U postgres -d news -f newsdata.sql
* Step 5:  Create views
* Step 6:  Exit db by typing \q and run program -- python logsanalysis.py , if no user and password is required in order to connect to DB , press Enter when DB user and password is requested


_If views.sql was downloaded:_

* Step 4:  Import data from newsdata.sql file to db news -- psql -U postgres -f newsdata.sql
* Step 5:  Create views from views.sql -- psql -U postgres -f views.sql
* Step 6:  Run program -- python logsanalysis.py , if no user and password is required in order to connect to DB , press Enter when DB user and Password is requested


**BRING ORDER TO CHAOS BY CREATING VIEWS IN DATABASE**


Three tables inside database NEWS:

| Schema | Name | Type | Owner |
| :---: | :---: | :---: | :---: |
| public | articles | table | vagrant |
| public | authors | table | vagrant |
| public | log | table | vagrant |

 id column from table authors relates with author column from table articles
 slug column from table articles relates with column path from table log (slug is included in path but not equal) ... CONCAT to the rescue


### create view to put together relevant combined data from articles and authors and making possible to relate with log

    CREATE VIEW relevant AS
    SELECT articles.title,
    articles.slug,
    CONCAT('/article/',articles.slug) AS path,
    authors.name
    FROM articles INNER JOIN authors
    ON articles.author=authors.id;


### create view to show only logs relevant to articles

    CREATE VIEW relevantlogs AS
    SELECT log.path,
    relevant.title,
    relevant.name
    FROM log JOIN relevant
    ON log.path=relevant.path;


### create view to make it easier in python 

    CREATE VIEW finalview AS
    SELECT path,
    COUNT( * ) AS views,
    name,
    title
    FROM relevantlogs
    GROUP BY path,name,title
    ORDER BY views DESC;


### create view to change data type from date with time stamp to date type for column time

    CREATE VIEW statuslogs AS
    SELECT status,
    date(time) as req_date
    FROM log;


### create view to show status day by day

    CREATE VIEW statusperday AS
    SELECT status,
    req_date,
    COUNT(status) AS requests
    FROM statuslogs
    GROUP BY req_date,status;


### create view all request day by day , successful and unsuccessful

    CREATE VIEW requestsperday AS
    SELECT req_date,
    COUNT(req_date) AS allreq
    FROM statuslogs
    GROUP BY req_date;


### create view to show daily percentage for each status

    CREATE VIEW dailypercentage AS
    SELECT statusperday.status,
    statusperday.req_date,
    ROUND(100 * (statusperday.requests::numeric/requestsperday.allreq),2) AS percentage
    FROM statusperday LEFT JOIN requestsperday
    ON statusperday.req_date=requestsperday.req_date;


_Now evrything is set up , we have order and we can answer the questions by interogating views : finalview and dailypercentage_

