import requests
from io import BytesIO
from math import log, exp, tan, atan, pi, ceil
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
import gpxpy

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0
GOOGLE_MAPS_API_KEY = 'your_API_key'  # set to 'your_API_key'


def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) / 180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py


def pixelstolatlon(px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon


def get_maps_image(NW_lat_long, SE_lat_long, zoom=15):

    ullat, ullon = NW_lat_long
    lrlat, lrlon = SE_lat_long

    # Set some important parameters
    scale = 1
    maxsize = 640

    # convert all these coordinates to pixels
    ulx, uly = latlontopixels(ullat, ullon, zoom)
    lrx, lry = latlontopixels(lrlat, lrlon, zoom)

    # calculate total pixel dimensions of final image
    dx, dy = lrx - ulx, uly - lry

    # calculate rows and columns
    cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))

    # calculate pixel dimensions of each small image
    bottom = 120
    largura = int(ceil(dx/cols))
    altura = int(ceil(dy/rows))
    alturaplus = altura + bottom

    # assemble the image from stitched
    final = Image.new("RGB", (int(dx), int(dy)))
    for x in range(cols):
        for y in range(rows):
            dxn = largura * (0.5 + x)
            dyn = altura * (0.5 + y)
            latn, lonn = pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
            position = ','.join((str(latn), str(lonn)))
            urlparams = {'center': position,
                         'zoom': str(zoom),
                         'size': '%dx%d' % (largura, alturaplus),
                         'maptype': 'satellite',
                         'sensor': 'false',
                         'scale': scale}
            if GOOGLE_MAPS_API_KEY is not None:
                urlparams['key'] = GOOGLE_MAPS_API_KEY

            url = 'http://maps.google.com/maps/api/staticmap'
            try:
                response = requests.get(url, params=urlparams)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            im = Image.open(BytesIO(response.content))
            final.paste(im, (int(x*largura), int(y*altura)))

    return final


def get_lat_lon_points(data_path):

    data = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    data_gpx = [f for f in data if f.find(".gpx") != -1]

    lat = []
    lon = []

    for activity in data_gpx:
        gpx_filename = join(data_path, activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)

    return lat, lon


def get_lat_lon_region(lat, lon, offset=0.002):

    max_lat = round(max(lat) + offset, 6)
    min_lat = round(min(lat) - offset, 6)
    max_lon = round(max(lon) + offset, 6)
    min_lon = round(min(lon) - offset, 6)

    NW_lat_lon = (max_lat, min_lon)
    SE_lat_lon = (min_lat, max_lon)

    return NW_lat_lon, SE_lat_lon


def get_pixel_position(draw_coord, starting_coord, zoom=15):

    y_lat, x_lon = draw_coord
    y0_lat, x0_lon = starting_coord

    y_px, x_px = latlontopixels(y_lat, x_lon, zoom)
    y0_px, x0_px = latlontopixels(y0_lat, x0_lon, zoom)

    y, x = y0_px - y_px, x0_px - x_px

    y, x = abs(ceil(x)), abs(ceil(y))

    return y, x
