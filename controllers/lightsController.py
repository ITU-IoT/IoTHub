import json
import requests
from app.models import Room,Light
from app import db

address = "http://192.168.1.2/api/egZDzxX7ctoCDoXLKTxAPom6-a29XpVoQw1UvGpu/lights/"

def UpdateLight(nmbr, putData):
    r = requests.put(address + str(nmbr) + "/state" , data = putData)


def updateLights(roomIds, putData):
  lights = db.session.query(Light).all()

  for light in lights:
    if any(roomId for roomId in roomIds if roomId == light.roomId):
      UpdateLight(light.id, putData)


def ChangeRoom(roomIds):
  lights = db.session.query(Light).all()

  on = "{\"on\":true}"
  off = "{\"on\":false}"

  for light in lights:
    if any(roomId for roomId in roomIds if roomId == light.roomId):
      UpdateLight(light.id, on)
    else:
      UpdateLight(light.id, off)


'''
################# switch light off #################
{
    "on":false
}

################# switch light on #################
{
    "on":true
}

################# Change color of ligth #################
# between 0 and 65535
{
    hue: val
}
'''
