# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.parking_spot import ParkingSpot



class Memory:
    """store all data like parking spots and reveration status in memory to avoid using a heavy database
    """

    def __init__(self):
        self.spots = {} # store all parking spots
        # self.available_queue = [] # available parking spots in Q if only one street
        # self.booked_queue = [] # booked parking spots in Q if only one street
    

    def insert(self, spot):
        # validate data type
        if type(spot) != ParkingSpot:
            return -1
        if self.ifExisted(spot.id):
            return 409
        self.spots[spot.id] = spot
        return 0
        
    def select(self, spot_id=None):
        if spot_id != None:
            if not self.ifExisted(spot_id):
                return 

            return self.spots[spot.id]
        else:
            return self.spots.values()
            
    def update(self, spot_id, spot):
        # validate data type
        if type(spot) != ParkingSpot:
            return -1
            
        # check if it is not found
        if not self.ifExisted(spot_id):
            return 404
            
        self.spots[spot.id] = spot
        return 0
        
    def delete(self, spot_id):
        # check if it is not found
        if not self.ifExisted(spot_id):
            return 404

        self.spots.pop(spot_id)
        return 0
    
    def ifExisted(self, spot_id):
        # check if it is not found
        return spot_id in self.spots
