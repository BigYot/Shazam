import numpy as np
from PIL import Image

CRIT_VALUE = 1.15
IMG_WIDTH = 863
IMG_HEIGHT = 379
lollist = []
pixel_and_value = {}
val = 0

img = Image.open('Figure_3h.png')
pixelMap = img.load()

for x in range(IMG_WIDTH):
    for y in range(IMG_HEIGHT):

        skr = img.getpixel((x,y))
        if skr[1] + skr[2] != 0:
            val = skr[0]/(skr[1]+skr[2])
            pixel_and_value[(x,y)] = val
        else:
             pixel_and_value[(x,y)] = 0

        lollist.append(val)

#try dividing red value by sum of blue and green values for each pixel and pick the largest ones

for pix in pixel_and_value:
    if pixel_and_value[pix] > CRIT_VALUE:
        pixelMap[pix[0], pix[1]] = (255,255,255,255)
        img.putpixel(pix,(255,255,255,255))
    else:
        pixelMap[pix[0], pix[1]] = (0, 0, 0, 255)
        img.putpixel(pix, (0, 0, 0, 255))


#lollist.sort()
#print(len(lollist))
img.show()

#for i in lollist:
   # print(i)