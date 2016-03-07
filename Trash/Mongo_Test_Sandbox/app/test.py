from __init__ import db
from models import st_sector
import pickle
import datetime
import random
f = open('/Users/ilya/ST_Monitor/Mongo_Test_Sandbox/app/NameList.pkl')
NameList = pickle.load(f) 

#ss = st_snapshot(run = "1", body = {})
#ss.save()

#k = st_snapshot().create("2")
#k.save()

#st_snapshot(run = "3", body = {}).save()
        
random.seed(datetime.datetime.now().microsecond)

for i in range(0, 10):
    for name in NameList['TTNames']:
        st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1)).save()
    for name in NameList['ITNames']:
        st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1)).save()


from mongoengine import *
client = connect('st_db')
for document in client.st_db.st_sector.find():
    print document
