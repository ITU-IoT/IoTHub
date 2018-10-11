from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField,validators,SubmitField

class ConnectForm(FlaskForm):
  name = TextField("Name")
  ip = TextField("IP", [validators.IPAddress("This is not a valid IP")])
  port = IntegerField("Port")
  submit = SubmitField("Connect")
