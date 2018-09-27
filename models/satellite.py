class Satellite:
    def __init__(self,ip,port,name):
        self.ip = ip
        self.port = port
        self.name = name
    
    def getConnection(self):
        return ("%s:%s",self.ip,self.port)

    def getName(self):
        return ("%s",self.name)

    