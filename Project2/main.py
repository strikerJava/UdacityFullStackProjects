from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

from flask import session as loginState #login sesson object
import random, string

app = Flask(__name__)
engine = create_engine('sqlite:///inventory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def startPoint():
    return "Hello Flask"

@app.route('/oAuth')
def oAuthLogIn():
	sessionToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	loginState['state'] = sessionToken
	return "Token: %s" %loginState['state']

@app.route('/logOut')
def logout():
    return "logout page here"

@app.route('/database', methods = ['GET', 'POST'])
def getAllDataBase():
    return "Database listing here"

@app.route('/test')
def reset():
    return "Reset Login State. Please return to main page"

if __name__ == '__main__':
    app.secret_key = 'dummyKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)
