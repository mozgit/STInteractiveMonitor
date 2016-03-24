from appl import app
from flask.ext.mongoengine import MongoEngine
from mongoengine import *
db = MongoEngine(app)
#client = connect('st_db')
#dbs = client.st_db