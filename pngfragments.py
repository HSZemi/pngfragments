#! /usr/bin/env python3

from PIL import Image
from random import shuffle
import sys, os

if(len(sys.argv) == 3):
	filename = sys.argv[1]
	number_of_images = int(sys.argv[2])
elif(len(sys.argv) == 2):
	filename = sys.argv[1]
	number_of_images = 5
else:
	print("Usage: {0} image_file_name.png [number_of_parts]".format(sys.argv[0]))
	sys.exit(1)

if(not os.path.isfile(filename)):
	print("File {0} not found!".format(filename))
	sys.exit(1)


img = Image.open(filename)

if (img.format == 'PNG' and img.mode == 'RGBA'):
	basename = filename[:-4]
else:
	print("File {0} does not seem to be a .png file in RGBA mode.".format(filename))
	sys.exit(1)

width = img.size[0]
height = img.size[1]

print("Examining {0}x{1} image {2}...".format(width, height, filename))

colorpixels = []
pix = img.load()

for x in range(width):
	for y in range(height):
		pixel = pix[x,y]
		if(pixel[3] != 0):
			colorpixels.append((x,y))

print("Found {0} non-transparent pixels.".format(len(colorpixels)))
shuffle(colorpixels)

outputs = []
# create x new images
for i in range(number_of_images):
	outputs.append(Image.new(img.mode, img.size))
	outpix = outputs[i].load()
	start = i * len(colorpixels) // number_of_images
	end = ((i+1) * len(colorpixels) // number_of_images)

	for (x,y) in colorpixels[start:end]:
		outpix[x,y] = pix[x,y]
		
	print("Creating {0}-{1}.png".format(basename, i))
	outputs[i].save("{0}-{1}.png".format(basename, i))

