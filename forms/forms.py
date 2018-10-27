from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField,validators,SubmitField,SelectField
from controllers import locationController, lightsController
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

def GetLights():
  lights = lightsController.GetLights()
  lightNames = []
  for lId,light in lights:
    lightNames.append((lId,light))
  return lightNames

class ConnectLight(FlaskForm):
  name = SelectField("Select light", choices = GetLights())
  room = SelectField("Room", choices = GetRooms())
  submit = SubmitField("Connect")

class ConnectLightValidate(FlaskForm):
  name = IntegerField("Select light")
  room = IntegerField("Room")
  submit = SubmitField("Connect")

class ConnectSatellite(FlaskForm):
  name = TextField("Name")
  ip = TextField("IP", [validators.IPAddress("This is not a valid IP")])
  port = IntegerField("Port")
  room = SelectField("Room", choices=GetRooms())
  submit = SubmitField("Connect")

class ConnectSatelliteValidate(FlaskForm):
  name = TextField("Name")
  ip = TextField("IP", [validators.IPAddress("This is not a valid IP")])
  port = IntegerField("Port")
  room = IntegerField("Room")
  submit = SubmitField("Connect")



class ConnectCC(FlaskForm):
  name = TextField("Name of device", [validators.data_required("You need a name")])
  room = SelectField("Room", choices=GetRooms())
  submit = SubmitField("Connect")


class ConnectCCValidate(FlaskForm):
  name = TextField("Name of device", [validators.data_required("You need a name")])
  room = IntegerField("Room")
  submit = SubmitField("Connect") 

class ConnectSong(FlaskForm):
  title = TextField("Title")
  artist = TextField("Artist")
  link = TextField("Link")
  submit = SubmitField("Add song")

class ConnectMobile(FlaskForm):
  name = TextField("Name") 
  mac = TextField("MAC")
  submit = SubmitField("Add device")

class ConnectRoom(FlaskForm):
  name = TextField("Name")
  submit = SubmitField("Add Room")
