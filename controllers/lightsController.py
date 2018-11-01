import json
from datetime import datetime, time

import requests
from astral import Astral

from app import db
from app.models import Light, Room

address = "http://localhost:8000/api/newdeveloper/lights/" #"http://192.168.1.2/api/egZDzxX7ctoCDoXLKTxAPom6-a29XpVoQw1UvGpu/lights/"
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
    print(type(lights))

    return [(lId, l['name']) for lId, l in lights.items()]


def UpdateLight(nmbr, putData):
    r = requests.put(address + str(nmbr) + "/state", data=putData)

def ChangeColor(nmbr, xy):
    x,y = xy
    data = "{\"xy\":[" + str(x) + "," + str(y) + "]}"
    UpdateLight(nmbr, data)

def ToggleLight(nmbr):
    lights = db.session.query(Light).filter(Light.roomId == nmbr).all()
    if lights is None:
        return
    light = requests.get(address).json()['on']


def UpdateLights(roomIds, putData):
    lights = db.session.query(Light).all()

    for light in lights:
        if any(roomId for roomId in roomIds if roomId == light.roomId):
            UpdateLight(light.id, putData)


def ChangeRoom(roomIds):
    lights = db.session.query(Light).all()

    on = "{\"on\":true}"
    off = "{\"on\":false}"

    for light in lights:
        if any(roomId for roomId in roomIds if roomId ==
               light.roomId) and ShouldLightsTurnOn():
            UpdateLight(light.id, on)
        else:
            UpdateLight(light.id, off)

def ConvertHexToHSL(hexColor):
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
