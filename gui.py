from tkinter import *
import time

import recorder
import RtoS
import sorter


root = Tk()
song_name = ""

def main():

    global song_name

    text = "recording..."
    recording_label = Label(root, text=text)
    recording_label.pack()

    recorder.record()

    text = "identifying..."
    recording_label.config(text=text)


    RtoS.recordingToSpectrogram('output.wav')
    RtoS.turnimagetobiterecording("recordingspectemp.png")
    song_name = sorter.sorter()
    if song_name == "":
        failure_label = Label(root,text="We're sorry, but we weren't able to identify your song. please try to put your phone closer to the microphone or play the song you want to identify louder.")
        failure_label.pack()
    else:
        answer_label = Label(root,text="Your song is:" + song_name)
        answer_label.pack()

welcome_label = Label(root,text="Hello, and welcome to Yotam's music identification app,You play us a song, and what tell you what song it is!")
welcome_label.pack()
welcome_label1 = Label(root,text="once you press the identify button, a recording will begin, so it is critical that the song is playing before you press the button.")
welcome_label1.pack()
welcome_label2 = Label(root,text="press the button in order to start the recording!")
welcome_label2.pack()
myButton = Button(root,text="Identify!",command=main)
myButton.pack()

root.mainloop()