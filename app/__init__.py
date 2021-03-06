from flask import Flask,Request,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import _thread
import os
import time
# from models import Satellite

CLEAN_TIMOUT = 180 #seconds

app = Flask(__name__, template_folder="templates/")
app.testing = True
app.secret_key = 'development key'
app._static_folder = os.path.abspath("static/")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/static')
def static_file(path):
    return app.send_static_file(path)

from app import routes, models
from app.models import CurrentSignals
#def CleanOldSignals():
 #   db.session.query(CurrentSignals).filter(CurrentSignals.timestamp < datetime.datetime.now() - datetime.timedelta(minutes=-1)).delete()
  #  time.sleep(CLEAN_TIMEOUT)

#_thread.start_new_thread(CleanOldSignals, ())
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Satellite': Satellite}
