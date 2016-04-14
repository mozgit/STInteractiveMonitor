import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import db
from app.models import st_sector, st_snapshot
import ROOT as R
import pickle
from mongoengine import *
import datetime
import random
from Create_Maps import IT_Map as IT_Map_f
from Create_Maps import TT_Map as TT_Map_f
from db_info import find_existing_runs
from db_info import list_runs
from AddOneFill import add_run
#from ToyData import fill_random

def fill_random(nNentries=10):
    random.seed(datetime.datetime.now().microsecond)
    TT_Map = TT_Map_f()
    IT_Map = IT_Map_f()    
    for i in range(0, nNentries):
        snapshot = []
        for name in TT_Map:
            sector=st_sector(name = TT_Map[name], run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1),
                                            err_efficiency = random.random()/10, err_bias = (random.random()-0.5)/10, err_width = 0)
            sector.save()
            snapshot.append(sector)

        for name in IT_Map:
            sector = st_sector(name = IT_Map[name], run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1),
                                            err_efficiency = random.random()/10, err_bias = (random.random()-0.5)/10, err_width = 0)
            sector.save()
            snapshot.append(sector)
        st_snapshot(run = i, snapshot = snapshot).save()
    return True



def print_content():
    client = connect('st_db')
    for document in st_sector.objects():
        print document.printsector()
    return True

def clear_db():
    client = connect('st_db')
    st_sector.drop_collection()
    st_snapshot.drop_collection()
    return True    


if __name__ == "__main__":
    #client = connect('st_db')
    #dbs = client.st_db
    #fill_random(10)
    #print "Befre clenaing"
    #print_content()
    #print "Cleaning"
    clear_db()
    #print "After cleaning"
    #print_content()
    #add_run(1, "/Users/ilya/TempData/1.root")
    #add_run(2, "/Users/ilya/TempData/2.root")    
    #add_run(3, "/Users/ilya/TempData/3.root")
    #add_run(200, "/Users/ilya/TempData/Brunel-1000ev-histos.root")
    fill_random(100)
    #print find_existing_runs(0, 6)