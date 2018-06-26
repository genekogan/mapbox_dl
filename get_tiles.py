from random import random
import urllib
import argparse
import os



parser = argparse.ArgumentParser()
parser.add_argument("--key", required=True, help="API key")
parser.add_argument("--width", default=512, required=True, type=int, help="width")
parser.add_argument("--height", default=512, required=True, type=int, help="height")
parser.add_argument("--zoom", default=17, required=True, type=int, help="zoom")
parser.add_argument("--num_images", required=True, type=int, help="num images")
parser.add_argument("--output_dir", required=True, type=str, help="where to save images")
args = parser.parse_args()

style_map = 'genekogan/cj5uwgixd5y1m2roclrqc51fh'
style_sat = 'mapbox/satellite-v9'


lng_min, lat_min = 40.563883, -74.004503
lng_max, lat_max = 40.895277, -73.732700

#-73.995890,40.742779 lng, lat

def get_style(style, location, zoom, width, height):
	lng, lat = location
	url = 'https://api.mapbox.com/styles/v1/%s/static/%f,%f,%d,0,0/%dx%d?access_token=%s'%(style, lng, lat, zoom, width, height, args.key)
	return url
	

def download_map_sat(dir_out, t, lat, lng, zoom, out_w, out_h):
	url_map = get_style(style_map, (lat, lng), zoom, out_w, out_h)
	url_sat = get_style(style_sat, (lat, lng), zoom, out_w, out_h)
	urllib.urlretrieve(url_map, "%s/map/map%05d_%f,%f.png"%(dir_out, t,lat,lng))
	urllib.urlretrieve(url_sat, "%s/sat/sat%05d_%f,%f.png"%(dir_out, t,lat,lng))


def main():
	w, h = args.width, args.height
	n = args.num_images
	zoom = args.zoom
	output_dir = args.output_dir

	os.system('mkdir %s'%output_dir)
	os.system('mkdir %s/map'%output_dir)
	os.system('mkdir %s/sat'%output_dir)
	
	for t in range(n):
		if t % 10 == 0:
			print("done %d of %d" % (t, n))
		lng = lng_min + (lng_max-lng_min) * random()
		lat = lat_min + (lat_max-lat_min) * random()
		download_map_sat(output_dir, t, lat, lng, zoom, w, h)

		
main()