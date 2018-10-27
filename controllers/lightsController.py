import json
import requests
from app.models import Room,Light
from astral import Astral
from app import db
from datetime import datetime, time

address = "http://192.168.1.2/api/egZDzxX7ctoCDoXLKTxAPom6-a29XpVoQw1UvGpu/lights/"
ambientBrightness = 1000 #is a value between 0 and 1024

CITY_NAME = 'Copenhagen'
a = Astral()
a.solar_depression = 'civil'
CITY = a[CITY_NAME]

AMBIENT_BRIGHTNESS_THRESHOLD = 200

def SetAmbientBrightness(value):
    global ambientBrightness
    ambientBrightness = value

def ShouldLightsTurnOn():
    global ambientBrightness
    timeNow = datetime.now().timestamp()
    sun = CITY.sun(date = datetime.now(), local = True)
    sunrise = sun['dawn'].timestamp()
    sunset = sun['sunset'].timestamp() 
    isNight = timeNow >= sunset or timeNow <= sunrise
    print(isNight)
    return ambientBrightness < AMBIENT_BRIGHTNESS_THRESHOLD and not isNight

def GetLights():
  lights = requests.get(address).json()
  return [(lId, l['name']) for lId,l in lights.items()]

def GetLightName(id):
  lights = requests.get(address).json()
  return [l['name'] for lId,l in lights.items() if lId == id]

def UpdateLight(nmbr, putData):
    r = requests.put(address + str(nmbr) + "/state" , data = putData)


def UpdateLights(roomIds, putData):
  lights = db.session.query(Light).all()

  for light in lights:
    if any(roomId for roomId in roomIds if roomId == light.roomId):
      UpdateLight(light.uuid, putData)


def ChangeRoom(roomIds):
    lights = db.session.query(Light).all()

    on = "{\"on\":true}"
    off = "{\"on\":false}"

    for light in lights:
      if any(roomId for roomId in roomIds if roomId == light.roomId) and ShouldLightsTurnOn():
        UpdateLight(light.uuid, on)
      else:
        UpdateLight(light.uuid, off)
  

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
