# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from app import app
from multiprocessing import Pool


manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = False,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    #_pool = Pool(processes=4)
    manager.run()