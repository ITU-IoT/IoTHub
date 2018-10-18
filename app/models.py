from app import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    name = db.Column(db.String(64))
    roomId = db.Column(db.Integer)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64))
    Artist = db.Column(db.String(64))
    link = db.Column(db.String(128))

class CC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    room = db.Column(db.Integer)    

class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mac = db.Column(db.String(64))

class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    room = db.Column(db.Integer) 

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
