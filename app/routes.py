from flask import render_template,request
from app import app,db
from controllers import postController as pC
from controllers import lightsController as lC
from app.models import Satellite
import json

@app.route("/")
def hello():
  s = Satellite.query.all()
  return render_template("info.html", sats=s)

@app.route("/lights/<int:number>", methods=['PUT'])
def updateLight(number):
    lC.UpdateLight(number, request.data)

@app.route("/home/<string:name>", methods=['POST', 'GET'])
def home(name):
    s = Satellite.query.filter(Satellite.name == name)
    if not s.first():
        return render_template("home.html", name="fuck")
    return render_template("home.html", name=s.first().name)


@app.route("/connect/<string:ip>/<int:port>/<string:name>")
def connectSatellite(ip,port,name):
    s = Satellite.query.filter(Satellite.ip == ip).filter(Satellite.port == port)
    if not s.first(): #if no results found
        satellite = Satellite(ip=ip,port=port,name=name)
        db.session.add(satellite)
        db.session.commit()
        return("added!")
    return("nope!")
        
@app.route("/connect",methods=['POST','GET'])
def connect():
    print(request.method)

    if request.method == 'POST':
        return connectPOST(request)
    elif request.method == 'GET':
        return connectGET(request)
    else:
        return render_template('home.html',name="marek")

def connectPOST(request):
    if not request.json:
        return "wrong"
    #print(request.json)
    #return json.dumps(request.json)
    return pC.decode(request)
def connectGET(request):
    return request.method
