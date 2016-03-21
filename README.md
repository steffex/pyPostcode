pyPostcode
==========

##Introduction

This is a Python library to request information from the PostcodeApi.nu API.
This API allows you to search for Dutch addresses using zipcodes.

For more information about this API, please visit http://postcodeapi.nu

This library supports only the v2 api.


##Installation

###PyPI
```pip install pyPostcode```

###Manually

pyPostcode consists of a single file (pyPostcode.py) that you can put in your python search path or in site-packages (or dist-packages depending on the platform)
You can also simply run it by putting it in the same directory as you main script file or start a python interpreter in the same directory.
pyPostcode works with Python 2.7.x (you're welcome to test other versions)

###API-key

The API can only be used when you have your own API-key.
You can request this key by visiting: http://www.postcodeapi.nu/#pakketten


##Example

###Basic usage

Get the address by using the zipcode and the house number

```python
#!/usr/bin/python

from pyPostcode import Api

postcodeapi = Api('{YOUR_API_KEY}') # Set your own API-key
result = postcodeapi.getaddress('1011AC', 154) # use address search
print result.street, result.house_number, result.town
```

###Result data

the following information can be gathered from the result:

* street
* house_number
* postcode
* town
* municipality
* province
* latitude
* longitude
* x ([Rijksdriehoek]/[Trigonometrical] coordinate)
* y ([Rijksdriehoek]/[Trigonometrical] coordinate)

##License

"PostcodeApi" is owned by Apiwise, see http://postcodeapi.nu for more information.
I am in no way affiliated with PostcodeAPI or the Apiwise organization.

[Rijksdriehoek]: http://nl.wikipedia.org/wiki/Rijksdriehoekscoördinaten
[Trigonometrical]: http://en.wikipedia.org/wiki/Triangulation_station

