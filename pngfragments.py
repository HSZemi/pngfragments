#! /usr/bin/env python3

from PIL import Image
from random import shuffle
import sys, os

htmlsnippet = '''<div style="height: {0}px;">
<div style="position: relative;">
{1}
</div>
</div>'''

pictureline = '''<div style="position: absolute; top: 0px; left: 0px; z-index: {0};"><img src="{1}" alt="" /></div>\n'''

fullhtmldocument = '''<!DOCTYPE html>
<head>
	<meta charset="UTF-8">
	<title>pngfragments</title>
</head>
<body>
{0}
</body>
</html>'''


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

#print(img.format)

if (img.format in ('PNG', 'JPEG', 'TIFF')):
	basename = filename[:-4]
else:
	print("File {0} does not seem to be a .png, .jpg, .gif or .tif file.".format(filename))
	sys.exit(1)

width = img.size[0]
height = img.size[1]

print("Examining {0}x{1} image {2}...".format(width, height, filename))

colorpixels = []
pix = img.load()

for x in range(width):
	for y in range(height):
		pixel = pix[x,y]
		if(img.mode == 'RGBA' and pixel[3] == 0):
			pass
		else:
			colorpixels.append((x,y))

print("Found {0} non-transparent pixels.".format(len(colorpixels)))
shuffle(colorpixels)

outputs = []
# create x new images
for i in range(number_of_images):
	outputs.append(Image.new('RGBA', img.size))
	outpix = outputs[i].load()
	start = i * len(colorpixels) // number_of_images
	end = ((i+1) * len(colorpixels) // number_of_images)

	for (x,y) in colorpixels[start:end]:
		outpix[x,y] = pix[x,y]
		
	print("Creating output/{0}-{1}.png".format(basename, i))
	outputs[i].save("output/{0}-{1}.png".format(basename, i))


# create snippet
print("Creating output/snippet.txt")
lines = ''
for i in range(number_of_images):
	lines += pictureline.format(i, "{0}-{1}.png".format(basename, i))

snippet = htmlsnippet.format(height + 10, lines)
f = open("output/snippet.txt", 'w')
print(snippet, file=f)
f.close()

# create full html document
print("Creating output/pngfragments.html")
f = open("output/pngfragments.html", 'w')
print(fullhtmldocument.format(snippet), file=f)
f.close()
