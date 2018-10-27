from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField,validators,SubmitField,SelectField
from controllers import locationController 
from app import db
from app.models import Room


def GetRooms():
  rooms = db.session.query(Room.name,Room.id).all()
  print(rooms)
  print(type(rooms))
  roomNames = []
  for room in rooms:
    roomNames.append((room[1],room[0]))
  return roomNames


class ConnectForm(FlaskForm):
  name = TextField("Name")
  ip = TextField("IP", [validators.IPAddress("This is not a valid IP")])
  port = IntegerField("Port")
  submit = SubmitField("Connect")



class ConnectCC(FlaskForm):
  name = TextField("Name of device")
  room = SelectField("Room", choices=GetRooms())
  submit = SubmitField("Connect")
 
