from db import db
from copy import deepcopy

class st_sector(db.Document):
    #This entry keeps functioning information of single sector during single run.
    run = db.IntField(required=True)
    name = db.StringField(max_length=255, required=True)
    efficiency = db.FloatField()
    err_efficiency = db.FloatField()
    bias = db.FloatField()
    err_bias = db.FloatField()
    width = db.FloatField()
    err_width = db.FloatField()
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
        return self

