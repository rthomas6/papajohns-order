import requests
import usaddress

def expand_road_types(name):
    names = {
            'Dr'  : 'Drive',
            'Dr.' : 'Drive',
            'St'  : 'Street',
            'St.' : 'Street'
            }
    return names.get(name, name)

address = ('2399 Tammeron Dr. SW, '
           'Marietta, GA 30064')

ad, _ = usaddress.tag(address)
print(ad)

if 'StreetNamePreType' in ad:
    ad['StreetNamePreType'] = expand_road_types(ad['StreetNamePreType'])
if 'StreetNamePostType' in ad:
    ad['StreetNamePostType'] = expand_road_types(ad['StreetNamePostType'])

street_addr_keys = ['AddressNumberPrefix', 'AddressNumber', 'AddressNumberSuffix',
        'StreetNamePreDirectional', 'StreetNamePreModifier', 'StreetNamePreType',
        'StreetName', 'StreetNamePostType', 'StreetNamePostModifier',
        'StreetNamePostDirectional']

street_addr_names = [ad.get(s) for s in street_addr_keys]
street_addr_list = list(filter(None, street_addr_names))
print(street_addr_list)

addr_plussed = [s + '+' for s in street_addr_list[:-1]]
addr_str = ''.join(addr_plussed) + ad.get(street_addr_keys[-1])
print(addr_str)

store_search_params = {
        'target' : 'menu',
        'ambiguous-street-number' : '',
        'ambiguous-block-ranges' : '0',
        'searchType' : 'DELIVERY',
        'residential-us-city' : ad.get('PlaceName'),
        'residential-state' : ad.get('StateName'),
        'zipcode' : ad.get('ZipCode'),
        'streetaddress' : addr_str,
        'residential-roomnumber' : ad.get('OccupancyIdentifier'),
        'aptstefloor' : ad.get('OccupancyType', 'NON') }

start_session = requests.get('https://www.papajohns.com/order/stores-near-me')
#print(start_session.cookies)
resp = requests.get('https://www.papajohns.com/order/storesSearch', store_search_params, cookies=start_session.cookies)
print(resp.url)
print(resp.history)
