from gps.utils import get_maps_image, get_lat_lon_points, get_lat_lon_region
from image.utils import create_heatmap, draw_coordinate
import time
import argparse
import cv2

# Arguments parser
parser = argparse.ArgumentParser(
        description='Generate heatmap from GPX tracks')
optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument('-m', '--mountain_name', required=True, type=str,
                      help='Mountain name for output file')
required.add_argument('-tpath', '--tracks_path', required=True, type=str,
                      help='Path to the GPX tracks')
optional.add_argument('--z', '--zoom', nargs='?', dest='zoom',
                      default=15, type=int,
                      help='Satellite image zoom')
optional.add_argument('--pxe', '--px_error', nargs='?', dest='px_error',
                      default=5, type=int,
                      help='Pixel error value to differentiate between tracks')
parser._action_groups.append(optional)

# Prepare general data
args = parser.parse_args()
mountain_name = args.mountain_name
tracks_path = args.tracks_path
zoom = args.zoom
px_error = args.px_error*zoom


timestr = time.strftime("%Y%m%d%H%M%S_")

# Prepare GPS data
lat, lon = get_lat_lon_points(tracks_path)
NW_lat_long, SE_lat_long = get_lat_lon_region(lat, lon)

# Obtain Satellite image from the mountain using Google Maps API
result = get_maps_image(NW_lat_long, SE_lat_long, zoom)
image_file = tracks_path + timestr + mountain_name + '_satellite.png'
result.save(image_file)

# Draw the coordinates on the image
img = cv2.imread(image_file)
previousCoord = NW_lat_long
for i in range(0, len(lat)):
    drawCoord = (lat[i], lon[i])
    img = draw_coordinate(img, drawCoord, NW_lat_long,
                          previousCoord, zoom, px_error)
    previousCoord = drawCoord

# Create Heatmap
img_0 = cv2.imread(image_file)
result = create_heatmap(img, img_0, colorMap=cv2.COLORMAP_HOT)

# Save final image
final_image_file = tracks_path + timestr + mountain_name + '_heatmap.png'
cv2.imwrite(final_image_file, result)
print('Image created. Open file: ' + final_image_file)
