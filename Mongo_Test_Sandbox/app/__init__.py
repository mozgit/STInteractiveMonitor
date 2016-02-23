from mongoengine import *
from flask import Flask, request, redirect, url_for, Response
from flask.ext.mongoengine import MongoEngine
from pymongo import read_preferences

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "st_db", 'read_preference':read_preferences.ReadPreference.PRIMARY}

client = connect('st_db')
client.drop_database("st_db")
db = MongoEngine(app)

#from app import views
