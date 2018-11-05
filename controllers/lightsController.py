import json
from datetime import datetime, time

import requests
from astral import Astral

from app import db
from app.models import Light, Room

address = "http://192.168.1.2/api/egZDzxX7ctoCDoXLKTxAPom6-a29XpVoQw1UvGpu/lights/"
ambientBrightness = 1000  # is a value between 0 and 1024

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
    sun = CITY.sun(date=datetime.now(), local=True)
    sunrise = sun['dawn'].timestamp()
    sunset = sun['sunset'].timestamp()
    isNight = timeNow >= sunset or timeNow <= sunrise
    print(isNight)
    return ambientBrightness < AMBIENT_BRIGHTNESS_THRESHOLD and isNight


def GetLights():
    lights = requests.get(address).json()
    return [(lId, l['name']) for lId, l in lights.items()]


def UpdateLight(nmbr, putData):
    print("update light nr., ",nmbr, " with data: ", str(putData))
    r = requests.put(address + str(nmbr) + "/state", data=str(putData))

def ChangeColor(nmbr, xy):
    x,y = xy
    data = {"xy":[x,y]}
    print(data)
    UpdateLight(nmbr, data)

def ToggleLights(roomId):
    room = db.session.query(Room).filter(Room.id == roomId).first()
    lights = db.session.query(Light).join(Room, Room.id == Light.roomId).filter(Light.roomId == roomId).all()
    if room is None:
        return
    if room.lightsOn:
        for light in lights:
            UpdateLight(light.id, str({'on':False}))
        room.lightsOn = 0
    else:
        for light in lights:
            x, y = ConvertHexToXY(light.hex)
            UpdateLight(light.id, str({'on':True, 'xy':[x,y]}))
        UpdateLights([roomId], str({'on':True}))
        room.lightsOn = 1
    db.session.commit()

def UpdateLights(roomIds, putData):
    lights = db.session.query(Light).all()

    for light in lights:
        if any(roomId for roomId in roomIds if roomId == light.roomId):
            UpdateLight(light.id, putData)


def ChangeRoom(roomIds):
    onLights = db.session.query(Light, Room).join(Room, Room.id == Light.roomId).filter(Light.roomId.in_(roomIds)).all()
    offLights = db.session.query(Light).join(Room, Room.id == Light.roomId).filter(~Light.roomId.in_(roomIds)).all()
    for light, room in onLights:
        if ShouldLightsTurnOn() and room.lightsOn:
            x, y = ConvertHexToXY(light.hex)
            UpdateLight(light.id, str({'on':True, 'xy':[x,y]}))
        else:
            UpdateLight(light.id, str({'on':False}))
    for light in offLights:
        UpdateLight(light.id, str({'on':False}))

def ConvertHexToXY(hexColor):
    # First convert hex to rgb
    rgbColor = HexToRGB(hexColor)
    # Normalize RGB Color
    rgbNorm = NormalizeRGB(rgbColor)
    # Apply Gamma correctiono
    rgbGamma = ApplyGammaToRGB(rgbNorm)
    # RGB to XYZ
    xyz = RGBtoXYZ(rgbGamma)
    # XYZ to XY
    xy = XYZtoXY(xyz)
    return xy


def HexToRGB(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    step = int(hlen/3)
    return tuple(int(hex[i:i+int(hlen/3)], 16) for i in range(0, hlen, step))

def NormalizeRGB(rgb):
    x,y,z = rgb
    return(x/255, y/255, z/255)


def ApplyGammaToRGB(rgb):
    red, green, blue = rgb
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if  (red > 0.04045) else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if  (green > 0.04045) else (green / 12.92)
    blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4) if  (blue > 0.04045) else (blue / 12.92)
    return (red, green, blue)
    
def RGBtoXYZ(rgb):
    red, green, blue = rgb
    x = red * 0.664511 + green * 0.154324 + blue * 0.162028
    y = red * 0.283881 + green * 0.668433 + blue * 0.047685
    z = red * 0.000088 + green * 0.072310 + blue * 0.986039
    return (x,y,z)

def XYZtoXY(xyz):
    X, Y, Z = xyz
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    return (x,y)






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
