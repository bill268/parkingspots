import connexion
import six
from math import radians, sin, cos, acos

from flask import jsonify
from flask import Response
from swagger_server.models.parking_spot import ParkingSpot  # noqa: E501
from swagger_server import util
from swagger_server.store.memory import Memory
store = Memory()


def getDistance(spot, latitude=None, longitude=None):
    """
    calculate distance between two points using latitude and longitude.
    """
    slat = radians(latitude)
    slon = radians(longitude)
    elat = radians(spot.latitude)
    elon = radians(spot.longitude)
    return 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))


def spotMatched(spot, latitude=None, longitude=None, radius=None, status=None):
    """
    return boolean to define if we should filter it out for the query condition
    """
    # check if match the availability_status or not 
    if status and status <> spot.status:
        return False
    # check if in the circle or not
    if latitude and longitude and radius:
        return getDistance(spot, latitude, longitude) <= radius
    
    return True
    
    
def add_parking_spot(body):  # noqa: E501
    """Add a new parking spot to the street

     # noqa: E501

    :param body: parking spot object that needs to be added to the street
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ParkingSpot.from_dict(connexion.request.get_json())  # noqa: E501
        
	code = store.insert(body)
	if code == 0:
        resp = Response(json.dumps(store.select(body.id)), status=201, mimetype='application/json')
	elif code == -1:
        message = {
                'status': 500,
                'message': 'unexpected internal server error',
        }
        resp = jsonify(message)
        resp.status_code = 500
    else:
        message = {
                'status': 409,
                'message': 'already existed',
        }
        resp = jsonify(message)
        resp.status_code = 409
	return resp


def delete_parking_spot(spotId):  # noqa: E501
    """Deletes a parking spot

     # noqa: E501

    :param spotId: ID of parking spot to delete
    :type spotId: int

    :rtype: None
    """
	code = store.delete(spotId)
	if code == 0:
        resp = jsonify()
        resp.status_code = 204
    else:
        message = {
                'status': 404,
                'message': 'not found this parking spot: ' + spotId,
        }
        resp = jsonify(message)
        resp.status_code = 404
	return resp

    
def find_parking_spots(latitude=None, longitude=None, radius=None, status=None):  # noqa: E501
    """Find parking spots by status

    return a list parking spots # noqa: E501

    :param latitude: Latitude coordinate around which to filter.
    :type latitude: float
    :param longitude: Longitude coordinate around which to filter.
    :type longitude: float
    :param radius: Radius (distance), in meters, from the coordinate.
    :type radius: float
    :param status: availability_status of the parking spot to filter
    :type status: str

    :rtype: List[ParkingSpot]
    """
    spots = store.select()
    output = [spot for spot in spots if spotMatched(spot, latitude, longitude, radius, status)]
    resp = jsonify(output)
    resp.status_code = 200
    return resp


def getparking_spot_by_id(spotId):  # noqa: E501
    """Find parking spot by ID

    Returns a single parking spot # noqa: E501

    :param spotId: ID of parking spot to return
    :type spotId: int

    :rtype: ParkingSpot
    """
    spot = store.select(spotId)
	if spot:
        resp = jsonify(spot)
        resp.status_code = 200
    else:
        message = {
                'status': 404,
                'message': 'not found this parking spot: ' + spotId,
        }
        resp = jsonify(message)
        resp.status_code = 404
	return resp


def update_parking_spot_status(spotId, body):  # noqa: E501
    """Updates a parking spot with new availability status 

     # noqa: E501

    :param spotId: ID of parking spot to update
    :type spotId: int
    :param body: parking spot object include the new availability status
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ParkingSpot.from_dict(connexion.request.get_json())  # noqa: E501
    
    spot = store.select(spotId)
    if not spot: 
        message = {
                'status': 404,
                'message': 'not found this parking spot: ' + spotId,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
        
    spot.status = body.status    
	code = store.update(spot)
	if code == 0:
        resp = Response(json.dumps(spot), status=200, mimetype='application/json')
	elif code == -1:
        message = {
                'status': 500,
                'message': 'unexpected internal server error',
        }
        resp = jsonify(message)
        resp.status_code = 500
    else:
        message = {
                'status': 409,
                'message': 'already existed',
        }
        resp = jsonify(message)
        resp.status_code = 409
	return resp
