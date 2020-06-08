import unittest
import os

from pyPostcode import Api, pyPostcodeException


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.api = Api(os.environ.get('POSTCODE_API_KEY'))
        self.api.url = 'https://sandbox.postcodeapi.nu'

    def test_api_key_is_required(self):
        with self.assertRaises(pyPostcodeException):
            Api('')

    def test_api(self):
        results = self.api.getaddress('6545CA', 29)
        latitude = 51.841554
        longitude = 5.8696099

        self.assertEqual(results.postcode, '6545CA')
        self.assertEqual(results.house_number, 29)
        self.assertEqual(results.street, 'Waldeck Pyrmontsingel')
        self.assertEqual(results.city, 'Nijmegen')
        self.assertEqual(results.municipality, 'Nijmegen')
        self.assertEqual(results.province, 'Gelderland')
        self.assertEqual(results.coordinates, [longitude, latitude])
        self.assertEqual(results.x, longitude)
        self.assertEqual(results.longitude, longitude)
        self.assertEqual(results.y, latitude)
        self.assertEqual(results.latitude, latitude)
