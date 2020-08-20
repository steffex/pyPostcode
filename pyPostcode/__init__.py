#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
pyPostcode by Stefan Jansen
pyPostcode is an api wrapper for http://postcodeapi.nu
'''

try:
    from urllib.request import urlopen, Request  # for Python 3
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, Request, HTTPError  # for Python 2

import json
import logging
from warnings import warn


__version__ = '0.6'


class pyPostcodeException(Exception):

    def __init__(self, id, message):
        self.id = id
        self.message = message


class Api(object):

    def __init__(self, api_key, api_version=(3, 0, 0)):
        if not api_key:
            raise pyPostcodeException(
                0, "Please request an api key on http://postcodeapi.nu")

        self.api_key = api_key
        self.api_version = api_version
        if (2, 0, 0) <= api_version < (3, 0, 0):
            self.url = 'https://postcode-api.apiwise.nl'
        else:
            self.url = 'https://api.postcodeapi.nu'

    def handleresponseerror(self, status):
        if status in [401, 403]:
            msg = "Access denied! Api-key missing or invalid"
        elif status == 404:
            msg = "No result found"
        elif status == 500:
            msg = "Unknown API error"
        else:
            msg = "dafuq?"

        raise pyPostcodeException(status, msg)

    def request(self, path=None):
        '''Helper function for HTTP GET requests to the API'''

        headers = {
            "Accept": "application/json",
            "Accept-Language": "en",
            # this is the v2 and v3 api key
            "X-Api-Key": self.api_key,
        }

        try:
            result = urlopen(Request(
                self.url + path, headers=headers,
            ))
        except HTTPError as err:
            self.handleresponseerror(err.code)

        if result.getcode() != 200:
            self.handleresponseerror(result.getcode())

        resultdata = result.read()

        if isinstance(resultdata, bytes):
            resultdata = resultdata.decode("utf-8")  # for Python 3
        jsondata = json.loads(resultdata)

        if (2, 0, 0) <= self.api_version < (3, 0, 0):
            data = jsondata.get('_embedded', {}).get('addresses', [])
            if data:
                data = data[0]
            else:
                data = None
        else:
            data = jsondata

        return data

    def getaddress(self, postcode, house_number=None):
        if (2, 0, 0) <= self.api_version < (3, 0, 0):
            path = '/v2/addresses/?postcode={postcode}'
            if house_number is not None:
                path += '&number={house_number}'
            resource = ResourceV2
        else:
            if house_number is None:
                raise ValueError('"house_number" cannot be None')
            path = '/v3/lookup/{postcode}/{house_number}'
            resource = ResourceV3
        path = path.format(
            postcode=str(postcode), house_number=str(house_number))

        try:
            data = self.request(path)
        except pyPostcodeException as e:
            logging.error(
                'Error looking up %s%s%s on %s: %d %s',
                postcode, house_number and ' ' or '', house_number, self.url,
                e.id, e.message)
            data = None
        except Exception as e:
            logging.exception(e)
            data = None

        if data is not None:
            return resource(data)
        else:
            return False


class Resource:

    def __init__(self, data):
        self._data = data

    def not_implemented(self):
        raise NotImplementedError

    street = property(not_implemented)
    house_number = property(not_implemented)
    postcode = property(not_implemented)
    town = property(not_implemented)
    municipality = property(not_implemented)
    province = property(not_implemented)
    latitude = property(not_implemented)
    longitude = property(not_implemented)
    x = property(not_implemented)
    y = property(not_implemented)
    coordinates = property(not_implemented)


class ResourceV2(Resource):

    @property
    def street(self):
        return self._data['street']

    @property
    def house_number(self):
        '''
        House number can be empty when postcode search
        is used without house number
        '''
        return self._data.get('number', self._data.get('house_number'))

    @property
    def postcode(self):
        return self._data.get('postcode')

    @property
    def town(self):
        return self._data.get('city', {}).get('label', self._data.get('town'))

    @property
    def municipality(self):
        result = self._data.get('municipality', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result

    @property
    def province(self):
        result = self._data.get('province', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result

    def _get_geo_coordinates(self, geo_type):
        return self._data.get('geo', {}).get('center', {}).get(geo_type)\
            .get('coordinates', [None, None])

    @property
    def latitude(self):
        if self._data.get('latitude'):
            return self._data.get('latitude')
        return self._get_geo_coordinates('wgs84')[1]

    @property
    def longitude(self):
        if self._data.get('longitude'):
            return self._data.get('longitude')
        return self._get_geo_coordinates('wgs84')[0]

    @property
    def x(self):
        if self._data.get('x'):
            return self._data.get('x')
        return self._get_geo_coordinates('rd')[0]

    @property
    def y(self):
        if self._data.get('y'):
            return self._data.get('y')
        return self._get_geo_coordinates('rd')[1]


class ResourceV3(Resource):

    @property
    def street(self):
        return self._data['street']

    @property
    def house_number(self):
        return self._data.get('number')

    @property
    def postcode(self):
        return self._data.get('postcode')

    @property
    def city(self):
        return self._data.get('city')

    @property
    def town(self):
        warn('Use the attribute "city" instead',
             DeprecationWarning, stacklevel=2)
        return self.city

    @property
    def municipality(self):
        return self._data.get('municipality')

    @property
    def province(self):
        return self._data.get('province')

    @property
    def coordinates(self):
        return self._data.get('location', {}).get('coordinates')

    @property
    def latitude(self):
        coordinates = self.coordinates
        return coordinates and coordinates[1] or None

    @property
    def longitude(self):
        coordinates = self.coordinates
        return coordinates and coordinates[0] or None

    @property
    def x(self):
        return self.longitude

    @property
    def y(self):
        return self.latitude
