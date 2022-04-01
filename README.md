# kong-plugin-py-geocode

A Kong Custom Plugin using the Python PDK that performs geocoding using the [GeoPy](https://geopy.readthedocs.io/en/stable/) library.

When making an API request to Kong, the caller should be able to pass location search keywords such as “Trafalgar Square” in the request header. The plugin will use the GeoPy library to lookup the address for the search terms, determine the latitude and longitude for the address, and add them as additional headers to the request before passing it to the upstream.

## Usage

1. Clone this repo - remember to use --recurse-submodules

```code
$ git clone --recurse-submodules https://github.com/Kong/kong-plugin-py-geocode
$ cd kong-plugin-py-geocode
$ docker compose up
```

The docker compose file sets up the following:

- Creates a custom Kong image from the base image, installing the kong python pdk as well as the GeoPy python library
- Starts up a Kong Gateway instance in the [dbless mode](https://docs.konghq.com/gateway/2.8.x/reference/db-less-and-declarative-config/) 
- Mounts the Kong declarative config and Python plugin file to the Kong instance using docker volumes

2. Testing the plugin

Send a request using curl with the 'x-location-search' header set to some location search keywords:

```code
curl localhost:8000/any -H 'x-location-search:"Trafalgar Square"'                                                                                                                                                        
{
  "args": {},
  "data": "",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.68.0",
    "X-Amzn-Trace-Id": "Root=1-6246cc5b-52a77b5d39a34a9f7d836589",
    "X-Forwarded-Host": "localhost",
    "X-Forwarded-Path": "/any",
    "X-Forwarded-Prefix": "/any",
    "X-Location-Address": "Trafalgar Square, St. James's, Covent Garden, City of Westminster, London, Greater London, England, WC2, United Kingdom",
    "X-Location-Lat": "51.508037",
    "X-Location-Long": "-0.12804941070725",
    "X-Location-Search": "\"Trafalgar Square\""
  },
  "json": null,
  "method": "GET",
  "origin": "192.168.48.1, 116.14.136.90",
  "url": "http://localhost/anything"
}

```
As you can see, the  custom plugin has looked up the location address, latitude and longitude and added them as upstream headers which are reflected by the httpbin response.

