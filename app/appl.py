from flask import *
from db_config import *
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': db_host,
    'port':  db_port
}