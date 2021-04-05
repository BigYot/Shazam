from pydub import AudioSegment
import wave
import contextlib
from PIL import Image
import sqlite3
import matplotlib.pyplot as plt
import librosa
import librosa.display


def getsongtime(filepath_song):
    with contextlib.closing(wave.open(filepath_song, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def DBconversion(filepath_image):
    img = Image.open(filepath_image)
    width, height = img.size
    retStr = ""
    for x in range(width):
        for y in range(height):
            skr = img.getpixel((x,y))
            if skr[0] == 255:
                retStr = retStr + "1"
            else:
                retStr = retStr + "0"
    return retStr



def getamountofwhites(filepath_image):
    img = Image.open(filepath_image)
    width, height = img.size
    Amount_Of_Whites = 0
    for x in range(width):
        for y in range(height):
            skr = img.getpixel((x, y))
            if skr[0] == 255:
                Amount_Of_Whites += 1
    return Amount_Of_Whites


def biteToSpectrogram(filepath_song):
    x, sr = librosa.load(filepath_song, sr=44100)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    fig = plt.figure(figsize=(14, 5))

    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    #if you wish to change the length in time of each bite, change the 3 into whatever length you like(in seconds)
    plt.axis([0,3,300,2000])



    #plt.colorbar()
    plt.savefig('temp.png')
    #the line below we solve the "More than 20 figures have been opened" RuntimeWarning
    plt.cla()
    plt.close(fig)

    #return plt


def compressbite(DBstring):
    counter = 0
    mincounter = 0
    minstr = ""
    retstr = ""
    while counter < (len(DBstring)/9):
        minstr = minstr + DBstring[counter]
        counter+=1
        mincounter+=1
        if mincounter == 9:
            bincounter = 0
            for i in minstr:
                if i == "1":
                    bincounter+=1
            if bincounter > 4:
                retstr = retstr + "1"
            else:
                retstr = retstr + "0"
            mincounter = 0
            minstr = ""
    return retstr




def turnimagetobite(filepath_image,filepath_tosaveto):
    CRIT_VALUE = 0.9
    pixel_and_value = {}
    val = 0
    vallist = []

    img = Image.open(filepath_image)
    pixelMap = img.load()

    width, height = img.size

    for x in range(width):
        for y in range(height):

            skr = img.getpixel((x,y))
            if skr[1] + skr[2] != 0:
                val = skr[0]/(skr[1]+skr[2])
                vallist.append(val)
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



    region = img.crop((175, 60, 1260, 445))
    region.save(filepath_tosaveto)



