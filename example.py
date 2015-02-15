from pyPostcode import Api

postcodeapi = Api('{YOUR_API_KEY}')
result_street = postcodeapi.getaddress('1011AC')  # use p6 search
result_address = postcodeapi.getaddress('1011AC', 154)  # use address search
print result_street._data, result_address._data
