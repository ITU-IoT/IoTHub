from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField,validators,SubmitField,SelectField
from app import db
from app.models import Room

class ConnectForm(FlaskForm):
  name = TextField("Name")
  ip = TextField("IP", [validators.IPAddress("This is not a valid IP")])
  port = IntegerField("Port")
  submit = SubmitField("Connect")

class ConnectCC(FlaskForm):
  name = TextField("Name of device")
  room = SelectField("Room", choices=Room.query.all())
