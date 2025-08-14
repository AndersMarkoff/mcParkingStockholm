import os
from dotenv import load_dotenv
import mcParking
import json
import requests
import xml.etree.ElementTree as ET
import datetime

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('TRAFIKKONTORET_API_KEY')

# Load latest data from Trafikkontorets trafik- och vägdata
# https://openparking.stockholm.se/LTF-Tolken/v1/pmotorcykel/all?maxFeatures={MAXFEATURES}&outputFormat={FORMAT}&callback={CALLBACK}&apiKey={APIKEY}
payload = {'outputFormat': 'JSON', 'apiKey': api_key}
request = requests.get('https://openparking.stockholm.se/LTF-Tolken/v1/pmotorcykel/all', params=payload)
data = json.loads(request.text)

# Create a list to hold mcParking objects
parking_list = []

# Loop through the data and create mcParkering objects
for feature in data['features']:
    # Calculate the average latitude and longitude from the coordinates
    lat = 0
    lon = 0
    for coordinate in feature['geometry']['coordinates']:
        lat += coordinate[1]
        lon += coordinate[0]
    lat = lat / len(feature['geometry']['coordinates'])
    lon = lon / len(feature['geometry']['coordinates'])

    properties = feature['properties']
    parking_rate = properties.get('PARKING_RATE')
    if parking_rate.startswith('taxa'):
        length = parking_rate.find(':')
        rate = parking_rate[0:length]
    else:
        rate = parking_rate if parking_rate else None
    rate = rate.capitalize() if rate else None

    parking = mcParking.mcParking(
        address = properties.get('ADDRESS'),
        lat = lat,
        lon = lon,
        rate = rate,
        servicetime = properties.get('OTHER_INFO'),
        description = parking_rate.capitalize() if parking_rate else None,
    )

    # Add the mcParking object to the list
    parking_list.append(parking)
        
# Start building the GPX file structure
gpx = ET.Element('gpx', {
    'version': '1.1',
    'creator': 'Anders Markoff',
})
metadata = ET.SubElement(gpx, 'metadata')
ET.SubElement(metadata, 'name').text = 'MC Parking Stockholm'
ET.SubElement(metadata, 'desc').text = 'Motorcycle parking locations in Stockholm'
author = ET.SubElement(metadata, 'author')
ET.SubElement(author, 'name').text = 'Anders Markoff'
ET.SubElement(author, 'link', {'href': 'https://github.com/AndersMarkoff'})
ET.SubElement(metadata, 'link', {'href': 'https://github.com/AndersMarkoff/mcParkingStockholm'})
ET.SubElement(metadata, 'time').text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


# Loop through the mcParking objects and create GPX waypoints
for parking in parking_list:
    wpt = ET.SubElement(gpx, 'wpt', {
        'lat': str(parking.lat),
        'lon': str(parking.lon),
    })
    ET.SubElement(wpt, 'name').text = parking.address if parking.address else ''
    ET.SubElement(wpt, 'desc').text = parking.description + '\n' +  parking.servicetime if parking.description and parking.servicetime else parking.description or parking.servicetime
    ET.SubElement(wpt, 'sym').text = parking.symbol

tree = ET.ElementTree(gpx)
ET.indent(tree, space="\t", level=0)
tree.write('MC Parking Stockholm.gpx', encoding='UTF-8', xml_declaration=True, method='xml')
