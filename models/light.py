from models import satellite

class Light:

    def __init__(self,satellite,name,status):
        self.satellite = satellite
        self.name = name
        self.status = status
    
    def getStatus(self):
        return self.status

    def getSatellite(self):
        return self.satellite.getName()