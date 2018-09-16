from random import random
import urllib
import argparse
import os
from os import listdir
from os.path import isfile, join
from random import random
from PIL import Image
import numpy as np



parser = argparse.ArgumentParser()
parser.add_argument("--in_path", required=True, type=str, help="where images stored")
parser.add_argument("--frac", type=float, help="cropping ratio before resizing", default=0.6667)
parser.add_argument("--w", type=int, help="output image width")
parser.add_argument("--h", type=int, help="output image height")
parser.add_argument("--label_map", type=int, default=0, help="make indexed label map (default 0)")
parser.add_argument("--combine", default=0, required=True, type=int, help="to concatenate images or not (default 1)")
args = parser.parse_args()


colors = [[255, 255, 255], [0, 0, 0], [255, 0, 0], [10, 255, 10], [0, 0, 255]]
# unlabeled, road, building, park, water

def convert_image_to_label_map(img, colors):
	h, w = np.array(img).shape[0:2]
	pixels = np.array(list(img.convert('RGB').getdata()))
	dists = np.array([np.sum(np.abs(pixels-c), axis=1) for c in colors])
	classes = np.argmin(dists, axis=0).reshape((h, w)).astype('int64')
	img2 = Image.fromarray(np.uint8(classes)).convert('L')
	return img2


def unconvert_image_to_label_map(img, colors):
	h, w = np.array(img).shape[0:2]
	pixels = np.array(list(img.convert('L').getdata()))
	pixels_clr = np.array([colors[p] for p in pixels]).reshape((h, w, 3))
	img2 = Image.fromarray(np.uint8(pixels_clr))
	return img2


def upsample(img, w2, h2):
    h1, w1 = img.height, img.width
    r = max(float(w2)/w1, float(h2)/h1)
    img = img.resize((int(r*w1), int(r*h1)), resample=Image.BICUBIC)
    return img


def crop_resize(img, frac, w2, h2):
    if img.height<h2 or img.width<w2:
        img = upsample(img, w2, h2)
       
    ar = float(w2 / h2)
    h1, w1 = img.height, img.width

    if float(w1) / h1 > ar:
        h1_crop = min(h2, h1 * frac)
        w1_crop = h1_crop * ar
    else:
        w1_crop = min(w2, w1 * frac)
        h1_crop = w1_crop / ar

    xr, yr = 0.5, 0.5 #random(), random()
    x_crop, y_crop = (w1 - w1_crop - 1) * xr, (h1 - h1_crop - 1) * yr
    h1_crop, w1_crop, y_crop, x_crop = int(h1_crop), int(w1_crop), int(y_crop), int(x_crop)
    img_crop = img.crop((x_crop, y_crop, x_crop+w1_crop, y_crop+h1_crop))
    img_resize = img_crop.resize((w2, h2), Image.BICUBIC)
    
    return img_resize


def main():

	in_path = args.in_path
	out_path = '%s_combined'%in_path
	if args.combine==0:
		out_path = '%s_mod'%in_path
		out_pathS = '%s/sat'%out_path
		out_pathM = '%s/map'%out_path

	if args.combine==1:
		os.system('mkdir %s'%out_path)
	else:
		os.system('mkdir %s'%out_path)
		os.system('mkdir %s'%out_pathS)
		os.system('mkdir %s'%out_pathM)

	filesS = [f for f in listdir(in_path+"/sat") if isfile(join(in_path+"/sat", f)) and f != ".DS_Store" and 'sat' in f]
	filesM = [f for f in listdir(in_path+"/map") if isfile(join(in_path+"/map", f)) and f != ".DS_Store" and 'map' in f]

	for f in range(len(filesS)):
		#	idx = int(filesS[f][3:8])
			
		nameS = filesS[f]
		nameM = "map"+filesS[f][3:]

		if f % 10 == 0:
			print("copied %d / %d"%(f, len(filesS)))
			
		pathS = '%s/%s'%(in_path+"/sat/",nameS)
		pathM = '%s/%s'%(in_path+"/map/",nameM)

		if not isfile(pathM) or not isfile(pathS):
			print("cant find ", nameS, nameM)
			continue

		imgS = Image.open(pathS)
		imgM = Image.open(pathM)

		# post-pocess imgS + imgM


		w, h = imgS.width, imgS.height

		if args.w != w or args.h != h:
			imgS = crop_resize(imgS, args.frac, args.w, args.h)
			imgM = crop_resize(imgM, args.frac, args.w, args.h)
			w, h = imgS.width, imgS.height

		if args.label_map==1:
			imgM = convert_image_to_label_map(imgM, colors)


		if args.combine==1:
			imgC = Image.new('RGB', (2*w, h))
			imgC.paste(imgM, (0, 0))
			imgC.paste(imgS, (w, 0))

			destPath = '%s/%08d.png' % (out_path, f)
			imgC.save(destPath)

		else:

			destPathS = '%s/%08d.png' % (out_pathS, f)
			destPathM = '%s/%08d.png' % (out_pathM, f)
			imgS.save(destPathS)
			imgM.save(destPathM)




main()