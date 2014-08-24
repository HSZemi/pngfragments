#! /usr/bin/env python3

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from random import shuffle
import sys, os

fonts = [("LinBiolinum_Rah.ttf","Linux Biolinum, Regular"),
	    ("LinBiolinum_RIah.ttf","Linux Biolinum, Italic"),
	    ("LinLibertine_Mah.ttf","Linux Libertine Mono, Regular"),
	    ("LinLibertine_Rah.ttf","Linux Libertine, Regular"),
	    ("LinLibertine_RIah.ttf","Linux Libertine, Italic"),
	    ("SourceSansPro-Regular.ttf","Source Sans Pro, Regular"),
	    ("SourceSansPro-Semibold.ttf","Source Sans Pro, Demi Bold")]


if(len(sys.argv) != 2):
	print("Usage: {0} [desired-filename.png]".format(sys.argv[0]))
	sys.exit(1)
else:
	filename = sys.argv[1]


if(os.path.isfile(filename)):
	answer = input("File {0} already exists! Overwrite? (yes/no)".format(filename))
	if(answer == 'no' or answer == 'n'):
		sys.exit(0)

print("Step 1/4 - Please select your desired font:")
fontindex = -1
while fontindex < 0:
	for i in range(len(fonts)):
		print("[{0}] {1}".format(i, fonts[i][1]))
	try:
		fontindex = int(input("Which Font would you like to use?\n:"))
		if(fontindex < 0 or fontindex > (len(fonts)-1)):
			print("Please enter a valid number between 0 and {0}.".format(len(fonts)-1))
	except ValueError:
		print("Please enter a valid number between 0 and {0}.".format(len(fonts)-1))


print("Step 2/4 - Please enter the desired font size:")
fontsize = 0
while fontsize < 1:
	try:
		fontsize = int(input("Which size do you wish your text to have?\n:"))
		if(fontsize < 1):
			print("Please enter a valid number greater than 0.")
	except ValueError:
		print("Please enter a valid number greater than 0.")


print("Step 3/4 - Enter your lines of text; double press Enter when done:")
lines = []
schnitzel_was_here = False
while( not schnitzel_was_here):
	line = input(": ")
	if(line == ''):
		 schnitzel_was_here = True
	else:
		lines.append(line)
	

print("Step 4/4 - Fragmentation")
number_of_images = None
while(number_of_images == None):
	try:
		number_of_images = int(input("How many fragments to you want to be created?\n(enter a value < 1 to skip this step)\n:"))
	except ValueError:
		print("Please enter a valid number.")

# font = ImageFont.truetype("Arial-Bold.ttf",14)
font = ImageFont.truetype("Fonts/{0}".format(fonts[fontindex][0]),fontsize)

width = 20
height = 20
lineskip = fontsize//2
for line in lines:
	w, h = font.getsize(line)
	width = max(width, w+20)
	height += h
	height += lineskip

img=Image.new("RGBA", (width,height),(255,255,255,0))
draw = ImageDraw.Draw(img)

offset = 10
for line in lines:
	w, h = font.getsize(line)
	draw.text((10, offset), line, (0,0,0), font=font)
	offset += h + lineskip
#draw.text((10, 10),lines[0],(0,0,0),font=font)
draw = ImageDraw.Draw(img)
img.save(filename)

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



#img = Image.open(filename)

basename = filename[:-4]


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
