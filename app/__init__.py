import os
from flask import Flask, request, redirect, url_for, Response
from flask.ext.mongoengine import MongoEngine
from mongoengine import *
#from flask.ext.login import LoginManager
from pymongo import read_preferences

histos = {'hist':{"efficiency":{}, "bias":{}, "width":{}},'prop':{'mean':{}, 'min':{}, 'max':{}}}
collection = {}
coll_tt_d = {}
coll_it_d = {}
Drawing_mode = {'hist':'', 'prop':'', 'start_run':'', 'end_run':''}

dead_sector = ['IT1BottomX2Sector7', 'IT3TopX1Sector7']


UPLOAD_FOLDER = 'app/temp/'
ALLOWED_EXTENSIONS = set(['pkl', 'root', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config["MONGODB_SETTINGS"] = {'DB': "st_db", 'read_preference':read_preferences.ReadPreference.PRIMARY}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
db = MongoEngine(app)
#app.config.from_object('config')
#db = SQLAlchemy(app)
#login_manager = LoginManager()
#login_manager.init_app(app)
#_pool = None
client = connect('st_db')
dbs = client.st_db

from app import views, models
from engine.detectors.CreateDetectors import create_TT
from engine.detectors.CreateDetectors import create_IT
tt_d = {}
it_d = {}
