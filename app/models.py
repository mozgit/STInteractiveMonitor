from db import db
from copy import deepcopy
import datetime
import json

class st_sector(db.Document):
    #This entry keeps functioning information of single sector during single run.
    run = db.IntField(required=True)
    name = db.StringField(max_length=255, required=True, unique_with='run')
    efficiency = db.FloatField()
    err_efficiency = db.FloatField()
    bias = db.FloatField()
    err_bias = db.FloatField()
    width = db.FloatField()
    err_width = db.FloatField()
    n_eff = db.FloatField()
    n_res = db.FloatField()
    #residuals = db.StringField(max_length=255, required=True, unique=True)
    meta = {
        'indexes':['run','name']
    }

    def create(self, run_number):
        """
        This function should create snapshot entry from monitoring histogram
        """
        self.run = str(run_number)
        self.name = "TestName"
        self.efficiency = run_number/100
        self.err_efficiency = run_number/1000
        self.bias = run_number/100
        self.err_bias = run_number/1000
        self.width = run_number/100
        self.err_width = run_number/1000
        self.n_eff = 80
        self.n_res = 100
        return self

    def printsector(self):
        sector = {
            'run' : self.run,
            'name' : self.name,
            'efficiency' : str(self.efficiency)+' +/- '+str(self.err_efficiency),
            'bias' : str(self.bias)+' +/- '+str(self.err_bias),
            'width' : str(self.width)+' +/- '+str(self.err_width),
            'stat_efficiency': str(self.n_eff),
            'stat_residual': str(self.n_res)
            }
        print(json.dumps(sector,sort_keys=True, indent=4))
        return True


class st_snapshot(db.Document):
    run = db.IntField(required=True, unique=True)
    snapshot = db.ListField(db.ReferenceField(st_sector))
    datetime = db.DateTimeField(default=datetime.datetime.now)
    alignment_iteration = db.IntField(default = 1)

    meta = {
        'indexes':['run']
    }
