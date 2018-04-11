# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.parking_spot import ParkingSpot  # noqa: E501
from swagger_server.test import BaseTestCase


class TestParkingspotController(BaseTestCase):
    """ParkingspotController integration test stubs"""

    def test_add_parking_spot(self):
        """Test case for add_parking_spot

        Add a new parking spot to the street
        """
        body = ParkingSpot()
        response = self.client.open(
            '/v1/parkingspots',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_parking_spot(self):
        """Test case for delete_parking_spot

        Deletes a parking spot
        """
        response = self.client.open(
            '/v1/parkingspots/{spotId}'.format(spotId=789),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_parking_spots(self):
        """Test case for find_parking_spots

        Find parking spots by status
        """
        query_string = [('latitude', 3.4),
                        ('longitude', 3.4),
                        ('radius', 3.4),
                        ('status', 'status_example')]
        response = self.client.open(
            '/v1/parkingspots',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getparking_spot_by_id(self):
        """Test case for getparking_spot_by_id

        Find parking spot by ID
        """
        response = self.client.open(
            '/v1/parkingspots/{spotId}'.format(spotId=789),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_parking_spot_status(self):
        """Test case for update_parking_spot_status

        Updates a parking spot with new availability status 
        """
        body = ParkingSpot()
        response = self.client.open(
            '/v1/parkingspots/{spotId}'.format(spotId=789),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
