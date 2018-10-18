import json
import requests

address = "http://localhost:8000/api/newdeveloper/lights/"

def UpdateLight(nmbr, putData):
    r = requests.put(address + str(nmbr) + "/state" , data = putData)


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