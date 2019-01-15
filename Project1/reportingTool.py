import psycopg2

DBNEWS = "news"


def getPopularArticles():
    print("Fetching the top three articles")
    db = psycopg2.connect(database=DBNEWS)
    c = db.cursor()
    c.execute("SELECT articles.title, COUNT(path) FROM articles, log"
              + " WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1))"
              + " GROUP BY articles.title ORDER BY COUNT(path) DESC LIMIT 3;")
    result = c.fetchall()
    print ("The most popular articles")
    print ("------------------------")
    print ('Article 1: ' + str(result[0][0]) + ' with ' + str(result[0][1]) + ' Hits!')
    print ('Article 2: ' + str(result[1][0]) + ' with ' + str(result[1][1]) + ' Hits!')
    print ('Article 3: ' + str(result[2][0]) + ' with ' + str(result[2][1]) + ' Hits!')
    print ("------------------------")
    db.close()
    print (" ")


def getPopularAuthors():
	print("Fetching the most popular authors")
	db = psycopg2.connect(database=DBNEWS)
	c = db.cursor()
	c.execute("SELECT authors.name, COUNT(author) FROM authors, articles, log WHERE articles.slug = (SUBSTRING(path, 10 , LENGTH(path)-1)) AND authors.id = articles.author GROUP BY authors.name ORDER BY COUNT(path) DESC;")
	result = c.fetchall()
	db.close()
	print ("The most popular Authors")
	print ("------------------------")
	print ('Author 1: ' + str(result[0][0]) + ' with ' + str(result[0][1]) + ' Hits!')
	print ('Author 2: ' + str(result[1][0]) + ' with ' + str(result[1][1]) + ' Hits!')
	print ('Author 3: ' + str(result[2][0]) + ' with ' + str(result[2][1]) + ' Hits!')
	print ('Author 4: ' + str(result[3][0]) + ' with ' + str(result[3][1]) + ' Hits!')
	print ("------------------------")
	print (" ")


def getDaysWithErrors():
	print ('The days where there was more then 1% errors visiting the website')
	db = psycopg2.connect(database=DBNEWS)
	c = db.cursor()
	c.execute('select count(status), substring(status,1,3) ' + 'as "HTTP Code", time::timestamp::date as "Date" '+ 'from  log group by status, time::timestamp::date ' + 'order by time::timestamp::date;')
	result = c.fetchall() 
	x = 0
	print ("------------------------")
	while x < 60:
		percent = long(( result[x+1][0] ) / ( result[x+1][0] + result[x][0]))
		if percent > .01:
			print(str(result[0][2]) + ' is over 1 percent')
		x += 2
	db.close()
	print ("------------------------")



getPopularArticles()
getPopularAuthors()
getDaysWithErrors()