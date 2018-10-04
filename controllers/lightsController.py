import json
import requests

address = "http://localhost:8000/api/newdeveloper/lights/"

def UpdateLight(nmbr, putData):
    r = requests.put(address + str(nmbr) + "/state" , data = putData)