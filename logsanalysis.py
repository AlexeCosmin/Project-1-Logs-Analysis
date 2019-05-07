# Database code for the DB news

import psycopg2

DBNAME= "news"

#connect to db
db=psycopg2.connect(database=DBNAME)
c=db.cursor()

#Query for 1st question
c.execute("select title , views::int from finalview limit 3;")
q1=c.fetchall()

#Query for 2nd question
c.execute("select name , sum(views) as allviews from finalview group by name order by allviews desc;")
q2=c.fetchall()

#Query for 3rd question
c.execute("select to_char(req_date,'Mon dd , yyyy') , percentage::decimal from dailypercentage where (percentage > 1 and status like '404%');")
q3=c.fetchall()

db.close()


#print questions and answers all together
print""
print "What are the most popular three articles of all time?"
print""
for e in q1:
	print str(e[0]) + "  --  " + str(e[1]) + "  views"

print""
print""
print "Who are the most popular article authors of all time?"
print""
for e in q2:
	print '{0:20} {1:5} {2:8} {3:5}'.format(str(e[0]),"\t--",str(e[1]),"views")

print""
print""
print "On which days did more than 1% of requests lead to errors?"
print""
for e in q3:
	print str(e[0]) + " -- " + str(e[1]) + "% errors"

print""
print""

