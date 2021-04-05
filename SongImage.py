import numpy as np
from PIL import Image
import sqlite3



CRIT_VALUE = 1.1
IMG_WIDTH = 863
IMG_HEIGHT = 379
pixel_and_value = {}
val = 0

unp = sqlite3.connect('D:\Yotam\Song_Bites.db')
cursor = unp.cursor()

filepath = 'xdd.png'



def getamountofwhites():
    Amount_Of_Whites = 0
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            skr = img.getpixel((x, y))
            if skr[0] == 255:
                Amount_Of_Whites += 1
    return Amount_Of_Whites


def DBconversion():
    retStr = ""
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            skr = img.getpixel((x,y))
            if skr[0] == 255:
                retStr = retStr + "1"
            else:
                retStr = retStr + "0"
    return retStr


def turnsongtoimage(filepath):

    img = Image.open(filepath)
    pixelMap = img.load()

    width, height = img.size

    for x in range(width):
        for y in range(height):

            skr = img.getpixel((x,y))
            if skr[1] + skr[2] != 0:
                val = skr[0]/(skr[1]+skr[2])
                pixel_and_value[(x,y)] = val
            else:
                pixel_and_value[(x,y)] = 0





    for pix in pixel_and_value:
        if pixel_and_value[pix] > CRIT_VALUE:
            pixelMap[pix[0], pix[1]] = (255,255,255,255)
            img.putpixel(pix,(255,255,255,255))
        else:
            pixelMap[pix[0], pix[1]] = (0, 0, 0, 255)
            img.putpixel(pix, (0, 0, 0, 255))

    img.show()


#getamountofwhites()
#Bite_insertion = "INSERT INTO SongBites VALUES(?,?,?,?)"
#data_tuple = ("daftpunkonemoretime003000003300","Daft Punk - One More Time",DBconversion(),getamountofwhites())
#cursor.execute(Bite_insertion,data_tuple)
#unp.commit()


turnsongtoimage(filepath)




