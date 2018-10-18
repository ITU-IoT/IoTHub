from app import db

class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    roomId = db.Column(db.Integer)
    port = db.Column(db.Integer)
    name = db.Column(db.String(64))

class song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    link = db.Column(db.String(128))

class cc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    room = db.Column(db.Integer)    

class mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mac = db.Column(db.String(64))

class light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    room = db.Column(db.Integer) 

class room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

'''
Room model:
###########################################################################################################
#                                                                                                         #
#             id                                                                                          #
#             name                                                                                        #
#                                                                      #####################              #
#                                                                      #         #         #              #
#                                                                      #         #         #              #
#                                                                      #         #         #              #
#                                                                      #####################              #
#                                                                      #         #         #              #
#                                                                      #         #         #              #
#                                                                      #         #         #              #
#                                                                      #####################              #
#                                                                                                         #
#           ##################################                                                            #
#           #                #               #                                                            #
#           #                #               #                                                            #
#       #####                #               #####                                                        #
#       #   #                #               #   #                                                        #
#       #   ##################################   #                                                        # 
#       #   #                                #   #                                                        #
#       #   #                                #   #                                                        #
###########################################################################################################

'''
