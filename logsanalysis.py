#! /usr/bin/env python3

import psycopg2
import getpass
from termcolor import colored, cprint
from colorama import init

# use Colorama to make Termcolor work on Windows too

init()


DBNAME = "news"

# if user and password is required

DB_user = raw_input("DB user: ")
my_pass = getpass.getpass()

# creating DB queries

articles = '''
SELECT title, views::int
FROM finalview
LIMIT 3;
'''

authors = '''
SELECT name , sum(views) AS allviews
FROM finalview
GROUP BY name
ORDER BY allviews DESC;
'''

failed_req = '''
SELECT to_char(req_date,'Mon dd , yyyy') , percentage::decimal
FROM dailypercentage
WHERE (percentage > 1 AND status LIKE '404%');
'''


# create output views for queries result

def view1(x):
    for e in x:
        print('{0:24} {1:5} {2:8} {3:5}'.format(str(e[0]),
              "  --  ", str(e[1]), "views"))
        print("-" * 70)


def view2(x):

    for e in x:
        print('{0:10} {1:5} {2:>4}{3:10}'.format(str(e[0]),
              " -- ", str(e[1]), "% errors"))
        print("-" * 70)

# create function to connect to DB with or without password and execute queries


def connect():

    try:

        if len(DB_user) == 0:
            db = psycopg2.connect(database=DBNAME)
            print(colored("Connection to DB news was successfull", 'green'))
            print('\n' * 2)

        else:
            db = psycopg2.connect(database=DBNAME,
                                  user=DB_user, password=my_pass)
            print(colored("Connection to DB news was successfull", 'green'))
            print('\n' * 2)

    except psycopg2.DatabaseError as e:
        if e.pgcode is not None:
            raise

    finally:
        c = db.cursor()
        c.execute(articles)
        q1 = c.fetchall()
        cprint("What are the most popular three articles of all time?",
               'cyan', attrs=['bold'])
        print('\n')
        view1(q1)
        print('\n')

        c.execute(authors)
        q2 = c.fetchall()
        cprint("Who are the most popular article authors of all time?",
               'cyan', attrs=['bold'])
        print('\n')
        view1(q2)
        print('\n')

        c.execute(failed_req)
        q3 = c.fetchall()
        cprint("On which days did more than 1% of requests lead to errors?",
               'cyan', attrs=['bold'])
        print('\n')
        view2(q3)
        db.close()


if __name__ == '__main__':
    connect()
