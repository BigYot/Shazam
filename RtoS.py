import os
import matplotlib.pyplot as plt
import wave
import pylab
import librosa
import librosa.display

#to play audio
#import IPython.display as ipd

def recordingToSpectrogram():
    x, sr = librosa.load('output.wav', sr=44100)

    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')

    plt.colorbar()

    plt.show()

recordingToSpectrogram()


