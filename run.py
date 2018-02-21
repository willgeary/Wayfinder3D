
# Import Libraries
import numpy as np
import math
from datetime import datetime, date, time, timedelta
from geojson import Feature, Point, LineString, FeatureCollection
import json
import requests
import argparse
import subprocess
from string import Template
import os
import sys

# Functions
def gmaps_directions(origin, destination, mode, API_KEY):
    template = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&mode={}&key={}"
    url = template.format(origin, destination, mode, API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

def decode_polyline(polyline_str):
    """
    See:
    https://stackoverflow.com/questions/15380712/how-to-decode-polylines-from-google-maps-direction-api-in-php
    """
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lng / 100000.0, lat / 100000.0))

    return coordinates

def multimodal_directions(origin, destination, modes, API_KEY):

    # Store GeoJSON features in a list
    results = []

    # Store durations and start / stop times
    durations = []
    starttimes = []
    endtimes = []

    for mode in modes:

        # Get data from Google Maps Directions API
        data = gmaps_directions(origin, destination, mode, API_KEY)

        # Check to see if no routes returned.
        if len(data['routes']) == 0:
            sys.exit("Sorry, directions are not available for {} from {} to {}".format(mode, origin, destination))

        # Get duration in seconds
        duration = data['routes'][0]['legs'][0]['duration']['value']

        # Calculate arrival time
        arrival_time = departure_time + timedelta(0, duration)

        # Get polyline
        polyline = data['routes'][0]['overview_polyline']['points']

        # Decode polyline
        decoded_polyline = decode_polyline(polyline)

        # Create LineString
        linestring = LineString(decoded_polyline)

        # Create GeoJSON properties
        properties={'mode': mode, 'duration': duration,
                    'start': departure_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 'end': arrival_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}

        # Create GeoJSON feature
        feature = Feature(geometry=linestring, properties=properties)

        # Store feature in results list
        results.append(feature)

        # Store duration and start/stop times in lists
        durations.append(duration)
        starttimes.append(departure_time)
        endtimes.append(arrival_time)

        # Convert list of features to GeoJSON FeatureCollection
        feature_collection = FeatureCollection(results)

    return feature_collection, durations, starttimes, endtimes

def LLA2ECEF(latitude,longitude,altitude):
    """
    # LLA2ECEF - convert latitude, longitude, and altitude to
    #            earth-centered, earth-fixed (ECEF) cartesian
    #
    # USAGE:
    # [x,y,z] = lla2ecef(lat,lon,alt)
    #
    # x = ECEF X-coordinate (m)
    # y = ECEF Y-coordinate (m)
    # z = ECEF Z-coordinate (m)
    # lat = geodetic latitude (radians)
    # lon = longitude (radians)
    # alt = height above WGS84 ellipsoid (m)
    #
    # Notes: This function assumes the WGS84 model.
    #        Latitude is customary geodetic (not geocentric).
    #
    # Source: "Department of Defense World Geodetic System 1984"
    #         Page 4-4
    #         National Imagery and Mapping Agency
    #         Last updated June, 2004
    #         NIMA TR8350.2
    #
    # Michael Kleder, July 2005

    # WGS84 ellipsoid constants Radius
    # http://stackoverflow.com/questions/16614057/longitude-latitude-altitude-to-3d-cartesian-coordinate-systems
    """
    a = np.float64(6378137)
    e = 8.1819190842622 * 10**(-2)

    asq = math.pow(a, 2)
    esq = math.pow(e, 2)

    lat = math.radians(latitude)
    lon = math.radians(longitude)
    alt = altitude

    N = a / np.sqrt(1 - esq * math.pow(math.sin(lat), 2))

    x = (N + alt) * math.cos(lat) * math.cos(lon)
    y = (N + alt) * math.cos(lat) * math.sin(lon)
    z = ((1 - esq) * N + alt) * math.sin(lat)

    return x, y, z

def geojson2cartesian(data):

    # For now assume elevation is zero
    elevation = 0

    # Store cartesian coords in a list
    cartesian_coords = []

    # For every route
    for i in range(len(data['features'])):

        this_cartesian_coords = []

        for j in data['features'][i]['geometry']['coordinates']:
            cartesian_coord = LLA2ECEF(j[1], j[0], elevation)
            this_cartesian_coords.append(list(cartesian_coord))

        cartesian_coords.append(this_cartesian_coords)

    return cartesian_coords

def cartesian2czml(data, durations, cartesian):
    """
    Appends seconds since epoch to each cartesian coordinate
    Per the CZML specifications
    """
    # Intermediate outputs
    timesteps = []
    for i in range(len(data['features'])):
        number_of_coords = len(data['features'][i]['geometry']['coordinates'])
        seconds_between_coord = round(float(durations[i]) / (number_of_coords-1))

        timer = 0.0
        seconds_since_epoch = []
        for i in range(number_of_coords):
            seconds_since_epoch.append(timer)
            timer += seconds_between_coord
        timesteps.append(seconds_since_epoch)

    # List of cartesian coords by route
    list_of_cartesian_coords_by_packet = []
    for i in range(len(data['features'])):
        number_of_coords_per_route = len(data['features'][i]['geometry']['coordinates'])
        route = cartesian[i]
        times = timesteps[i]

        cartesian_coords_by_packet = []
        for j in range(len(route)):
            x = route[j][0]
            y = route[j][1]
            z = route[j][2]
            time = times[j]

            cartesian_coords_by_packet.append(time)
            cartesian_coords_by_packet.append(x)
            cartesian_coords_by_packet.append(y)
            cartesian_coords_by_packet.append(z)

        list_of_cartesian_coords_by_packet.append(cartesian_coords_by_packet)

    return list_of_cartesian_coords_by_packet

def generate_cesium(data, modes, starttimes, endtimes, czml):

    CZML = []

    # Metadata
    id_ = 'document'
    version = '1.0'
    id_names = modes

    # Append meta data
    meta =  {u'id': u'{}'.format(id_),
             u'version': u'{}'.format(version)}
    CZML.append(meta)

    # Find min and max datetimes
    minDate = min(starttimes).strftime('%Y-%m-%dT%H:%M:%SZ')
    maxDate = max(endtimes).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Set path colors by mode
    colors = {'driving': [255, 255, 0, 255],
              'transit': [0, 191, 255, 255],
              'bicycling': [0, 255, 0, 255],
              'walking': [250, 128, 114, 255]}

    label_fillColors = [colors[i] for i in modes]
    path_material_colors = label_fillColors

    for i in range(len(data['features'])):

        # availability
        availability_start = starttimes[i].strftime('%Y-%m-%dT%H:%M:%SZ')
        availability_stop = endtimes[i].strftime('%Y-%m-%dT%H:%M:%SZ')

        # interval
        interval_start = minDate
        interval_stop = maxDate

        # billboard
        eyeOffset = [0.0, 0.0, .0]
        horizontalOrigin = 'CENTER'
        pixelOffset = [0.0, 0.0]
        scale = 0.8333333333333334
        show_boolean = True
        verticalOrigin = 'BOTTOM'

        # label
        label_fillColor = label_fillColors[i]
        label_font = 'bold 30px sans-serif'
        label_horizontalOrigin = 'LEFT'
        label_outlineColor = [0, 0, 0, 255]
        label_pixelOffset = [10.0, 0.0]
        label_scale = 1.0
        label_scale_boolean = True
        label_scale_interval = u'{}/{}'.format(interval_start, interval_stop)
        label_style = 'FILL'
        label_text = modes[i]
        label_verticalOrigin = 'BOTTOM'

        # path
        path_material_color_interval = u'{}/{}'.format(interval_start, interval_stop)
        path_material_color_rgba = path_material_colors[i]
        path_show_boolean = True
        path_show_interval = u'{}/{}'.format(interval_start, interval_stop)
        path_width_interval = u'{}/{}'.format(interval_start, interval_stop)
        path_width_number = 3.0

        # position
        position_epoch = availability_start
        position_interpolationDegree = 1
        position_interpolationAlgorithm = 'LAGRANGE'

        # cartesian coordinates
        position_cartesian = czml[i]

        # The actual output
        output = {
            u'availability': u'{}/{}'.format(availability_start, availability_stop),
            u'billboard':
                {
                    u'eyeOffset':
                        {
                            u'cartesian': eyeOffset
                        },
                    u'horizontalOrigin': u'{}'.format(horizontalOrigin),
                    u'pixelOffset':
                        {
                            u'cartesian2': pixelOffset
                        },
                    u'scale': scale,
                    u'show':
                        [
                          {
                            u'boolean': show_boolean,
                            u'interval': u'{}/{}'.format(interval_start, interval_stop)
                          }
                        ],
                    u'verticalOrigin': u'{}'.format(verticalOrigin)
                },
            u'label':
                {
                    u'fillColor':
                        [
                          {
                            u'interval': u'{}/{}'.format(interval_start, interval_stop),
                            u'rgba': label_fillColor
                          }
                        ],
                    u'font': u'{}'.format(label_font),
                    u'horizontalOrigin': u'{}'.format(label_horizontalOrigin),
                    u'outlineColor':
                        {
                            u'rgba': label_outlineColor
                        },
                    u'pixelOffset':
                        {
                            u'cartesian2': label_pixelOffset
                        },
                    u'scale': label_scale,

                    u'show':
                        [
                          {
                            u'boolean': label_scale_boolean,
                            u'interval': label_scale_interval
                          }
                        ],
                    u'style': u'{}'.format(label_style),
                    u'text': u'{}'.format(label_text),
                    u'verticalOrigin': u'{}'.format(label_verticalOrigin)
                },

            u'id': u'{}'.format(id_names[i]),
            u'path':
                {
                    u'material':
                    {
                        u'solidColor':
                        {
                            u'color':
                            {
                                u'interval': path_material_color_interval,
                                u'rgba': path_material_color_rgba
                            }
                        }
                    },
                    u'show':
                    [
                      {
                        u'boolean': path_show_boolean,
                        u'interval': path_show_interval
                      }
                    ],
                    u'width':
                    [
                      {
                        u'interval': path_width_interval,
                        u'number': path_width_number
                      }
                    ]
            },
            u'position':
                {
                    u'epoch': u'{}'.format(position_epoch),
                    u'interpolationDegree': position_interpolationDegree,
                    u'interpolationAlgorithm': u'{}'.format(position_interpolationAlgorithm),
                    u'cartesian': position_cartesian
                }
        }
        CZML.append(output)

    return CZML


# Main
if __name__ == "__main__":

    departure_time = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", help="Origin")
    parser.add_argument("--destination", help="Destination")
    parser.add_argument("--modes", help="Driving, Transit, Bicycling or Walking", default="driving, transit, bicycling, walking")
    parser.add_argument("--key", help="Google Maps Directions API Key", default='AIzaSyC2dX9jXmdYtYYdNOxu6CLoKYUIXb2IN2Y')

    args = parser.parse_args()

    # Inputs
    origin = args.origin
    destination = args.destination
    modes = args.modes.split(",")
    key = args.key

    # Data processing
    print("Getting directions from Google Maps")
    data, durations, starttimes, endtimes = multimodal_directions(origin, destination, modes, key)

    print("Converting 2D to 3D")
    cartesian = geojson2cartesian(data)

    print("Generating Cesium scene")
    czml = cartesian2czml(data, durations, cartesian)
    cesium_scene = generate_cesium(data, modes, starttimes, endtimes, czml)

    # Save CZML output
    outfilename = 'data.czml'
    with open(outfilename, 'w') as f:
        json.dump(cesium_scene, f)

    # Generate html file from Template
    module_path = os.path.join(os.path.dirname(__file__))
    template_path = os.path.join(module_path, 'templates', 'template.html')
    with open(template_path) as f:
        template = f.read()
    s = Template(template)

    start_lat = data['features'][0]['geometry']['coordinates'][0][1]
    start_lon = data['features'][0]['geometry']['coordinates'][0][0]
    end_lat = data['features'][0]['geometry']['coordinates'][-1][1]
    end_lon = data['features'][0]['geometry']['coordinates'][-1][0]

    with open("index.html", "w") as f:
        f.write(
            s.substitute(
                START_LAT=start_lat,
                START_LON=start_lon,
                END_LAT=end_lat,
                END_LON=end_lon,
                ORIGIN=origin,
                DESTINATION=destination
            )
        )

    # Run server
    print("Open your browser to http://localhost:8000/")
    bashCommand = "python3 -m http.server"
    output = subprocess.check_output(['bash','-c', bashCommand])
