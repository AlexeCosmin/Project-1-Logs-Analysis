\c news

CREATE VIEW relevant AS
SELECT articles.title,
	articles.slug,
	CONCAT('/article/',articles.slug) AS path,
	authors.name
FROM articles INNER JOIN authors
ON articles.author=authors.id;


CREATE VIEW relevantlogs AS
SELECT log.path,
	relevant.title,
	relevant.name
FROM log JOIN relevant
ON log.path=relevant.path;


CREATE VIEW finalview AS
SELECT path,
	COUNT( * ) AS views,
	name,
	title
FROM relevantlogs
GROUP BY path,name,title
ORDER BY views DESC;


CREATE VIEW statuslogs AS
SELECT status,
	date(time) as req_date
FROM log;


CREATE VIEW statusperday AS
SELECT status,
	req_date,
	COUNT(status) AS requests
FROM statuslogs
GROUP BY req_date,status;


CREATE VIEW requestsperday AS
SELECT req_date,
	COUNT(req_date) AS allreq
FROM statuslogs
GROUP BY req_date;


CREATE VIEW dailypercentage AS
SELECT statusperday.status,
	statusperday.req_date,
	ROUND(100 * (statusperday.requests::numeric/requestsperday.allreq),2) AS percentage
FROM statusperday LEFT JOIN requestsperday
ON statusperday.req_date=requestsperday.req_date;