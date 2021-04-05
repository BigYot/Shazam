import matplotlib.pyplot as plt
import librosa
import librosa.display
from PIL import Image
import InsertSongToDBMethods

filepath = 'output.wav'



def turnimagetobiterecording(filepath_image):
    CRIT_VALUE = 1
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

    img.save("recordingbite.png")



def recordingToSpectrogram(filepath):
    x, sr = librosa.load(filepath, sr=44100)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb,cmap='coolwarm', sr=sr, x_axis='time', y_axis='hz')
    plt.axis([0,3,300,2000])
    plt.savefig("recordingtemp.png")
    img = Image.open("recordingtemp.png")
    #(left, upper, right, lower)
    region = img.crop((175, 60, 1260, 445))
    region.save("recordingspectemp.png")


    #plt.colorbar()

    #plt.show()




recordingToSpectrogram(filepath)

turnimagetobiterecording("recordingspectemp.png")
