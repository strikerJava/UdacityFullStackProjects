

import psycopg2

DBNEWS = "news"


def getPopularArticles( ):
 #get the three most popular articles
 print("This is the popular Article Function")
 db = psycopg2.connect(database=DBNEWS)
 c = db.cursor()
# c.execute("SELECT SUBSTRING(path, 10 , LENGTH(path)-1), COUNT(path) FROM log WHERE path LIKE '/a%'  GROUP BY path ORDER BY COUNT(path) DESC;")

 c.execute("SELECT articles.title, COUNT(path) FROM articles, log WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1))  GROUP BY articles.title ORDER BY COUNT(path) DESC LIMIT 3;")
 #SELECT slug, title from articles; gets slug to match to path without
 #above gets the
 db.close()
 print("Got the Articles")


def getPopularAuthors( ):
 print("This is the popular Author Function")
 #select COUNT(articles.author), authors.name  from articles, authors where articles.author = authors.id GROUP BY authors.name;
 #above gets
 # SELECT articles.author, COUNT(author)
 #FROM articles, log
 #WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1))
 #GROUP BY articles.author ORDER BY COUNT(path) DESC;
 #SELECT authors.name, COUNT(author)
    #FROM authors, articles, log
    #WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1))
    #AND authors.id = articles.author GROUP BY authors.name ORDER BY COUNT(path) DESC;
 #gets it I think
 #select authors.name, articles.title FROM articles, authors  where authors.id = articles.author;
 #gets who wrote which article
 #gets count of author hits
 db = psycopg2.connect(database=DBNEWS)
 c = db.cursor()
 c.execute("SELECT authors.name, COUNT(author) FROM authors, articles, log WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1)) AND authors.id = articles.author GROUP BY authors.name ORDER BY COUNT(path) DESC;")
 db.close()
 print("Got the Authors")


def getDaysWithErrors( ):
 print("This is the function that returns days with 1% errors ")
 db = psycopg2.connect(database=DBNEWS)

 #c = db.cursor()
 #c.execute("")
 #db.close()
#print("Got the Errors")
#select count(status), substring(status,1,3) from log group by status;



getPopularArticles()
getPopularAuthors()
getDaysWithErrors()
