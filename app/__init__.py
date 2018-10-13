from flask import Flask,Request,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
# from models import Satellite


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

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Satellite': Satellite}
