import json
import requests

address = "http://192.168.1.2/api/egZDzxX7ctoCDoXLKTxAPom6-a29XpVoQw1UvGpu/lights/"

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
