from sqlalchemy import ForeignKey
from app import db


class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))


class CurrentSignals(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  mobileId = db.Column(db.Integer, ForeignKey('mobile.id'))
  roomId = db.Column(db.Integer, ForeignKey('room.id'))
  rssi = db.Column(db.Integer)
  timestamp = db.Column(db.DateTime)

class Satellite(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ip = db.Column(db.String(64))
  port = db.Column(db.Integer)
  name = db.Column(db.String(64))
  roomId = db.Column(db.Integer, ForeignKey('room.id'))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    artist = db.Column(db.String(64))
    link = db.Column(db.String(128))

class CC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    roomId = db.Column(db.Integer, ForeignKey('room.id'))    

class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mac = db.Column(db.String(64))

class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    roomId = db.Column(db.Integer, ForeignKey('room.id')) 

# '''
# Room model:
# ###########################################################################################################
# #                                                                                                         #
# #             id                                                                                          #
# #             name                                                                                        #
# #                                                                      #####################              #
# #                                                                      #         #         #              #
# #                                                                      #         #         #              #
# #                                                                      #         #         #              #
# #                                                                      #####################              #
# #                                                                      #         #         #              #
# #                                                                      #         #         #              #
# #                                                                      #         #         #              #
# #                                                                      #####################              #
# #                                                                                                         #
# #           ##################################                                                            #
# #           #                #               #                                                            #
# #           #                #               #                                                            #
# #       #####                #               #####                                                        #
# #       #   #                #               #   #                                                        #
# #       #   ##################################   #                                                        # 
# #       #   #                                #   #                                                        #
# #       #   #                                #   #                                                        #
# ###########################################################################################################

# '''
