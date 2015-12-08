from pyPostcode import Api

postcodeapi = Api('{YOUR_API_KEY}')
result_street = postcodeapi.getaddress('1011AC')  # use p6 search
result_address = postcodeapi.getaddress('1011AC', 154)  # use address search
for result in [result_street, result_address]:
    print result.street
    print result.house_number
    print result.postcode
    print result.town
    print result.municipality
    print result.province
    print result.latitude
    print result.longitude
    print result.x
    print result.y
