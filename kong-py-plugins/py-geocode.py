#!/usr/bin/env python3
import os
import kong_pdk.pdk.kong as kong
from geopy.geocoders import Nominatim

Schema = (
    {"location_search_header": {"type": "string"}},
    {"location_address_header": {"type": "string"}},
    {"location_lat_header": {"type": "string"}},
    {"location_long_header": {"type": "string"}},
)

version = '0.1.0'
priority = 0

# This is an example plugin that uses Python Geocoding

class Plugin(object):
    def __init__(self, config):
        self.config = config

    def access(self, kong: kong.kong):

        geolocator = Nominatim(user_agent="kong")

        location_search_header = 'x-location-search'
        location_address_header = 'x-location-address'
        location_lat_header = 'x-location-lat'
        location_long_header = 'x-location-long'

        # set defaults for header values
        if 'location_search_header' in self.config:
            location_search_header = self.config['location_search_header']

        if 'location_address_header' in self.config:
            location_address_header = self.config['location_address_header']
        
        if 'location_lat_header' in self.config:
            location_lat_header = self.config['location_lat_header']
        
        if 'location_long_header' in self.config:
            location_long_header = self.config['location_long_header']
        
        try:
            location_search = kong.request.get_header(location_search_header)
            location = geolocator.geocode(location_search)
            kong.service.request.set_header(location_address_header, location.address)
            kong.service.request.set_header(location_lat_header, location.latitude)
            kong.service.request.set_header(location_long_header, location.longitude)
        except Exception as ex:
            kong.log.error(ex)    

# add below section to allow this plugin optionally be running in a dedicated process
if __name__ == "__main__":
    from kong_pdk.cli import start_dedicated_server
    start_dedicated_server("py-geocode", Plugin, version, priority, Schema)
