from __init__ import db

class st_snapshot(db.Document):
    run = db.StringField(max_length=255, required=True, unique=True)
    body = db.DictField(required=True)
    def create(self, run_number):
        """
        This function should create snapshot entry from monitoring histogram
        """
        self.run = str(run_number)
        self.body = {
            "Sector1":{"e":0.1+float(run_number)/100., "bias":0.1+float(run_number)/100.},
            "Sector2":{"e":0.2+float(run_number)/100., "bias":0.2+float(run_number)/100.},
            "Sector3":{"e":0.3+float(run_number)/100., "bias":0.3+float(run_number)/100.}
        }
        return self

class st_sector(db.Document):
    #This entry keeps functioning information of single sector during single run.
    run = db.IntField(required=True)
    name = db.StringField(max_length=255, required=True)
    efficiency = db.FloatField()
    bias = db.FloatField()
    width = db.FloatField()
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
        self.bias = run_number/100
        self.width = run_number/100
        return self
