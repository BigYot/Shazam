from pydub import AudioSegment
import wave
import contextlib
import InsertSongToDBMethods
import mysql.connector
import sqlite3


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "songbites"
)
cursor = db.cursor()



#InsertSongToDBMethods.turnimagetobite("lol.png")


def getsongtime(filepath_song):
    with contextlib.closing(wave.open(filepath_song, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration








def songtobites(filepath_song):
    songtime = getsongtime(filepath_song)
    start = 0 * 1000
    fin = 3 * 1000

    while fin/1000 <= songtime:
        newAudio = AudioSegment.from_wav(filepath_song)
        newAudio = newAudio[start:fin]
        newAudio.export('newSound.wav', format="wav")
        InsertSongToDBMethods.biteToSpectrogram('newSound.wav')
        InsertSongToDBMethods.turnimagetobite('temp.png','bitetemp.png')
        DBstring = InsertSongToDBMethods.DBconversion('bitetemp.png')
        amountofwhites = InsertSongToDBMethods.getamountofwhites('bitetemp.png')
        compressedstr = InsertSongToDBMethods.compressbite(DBstring)
        Bite_insertion = "INSERT INTO songbites (songbite,songname,bite,amountofwhites,compstr) VALUES (%s,%s,%s,%s,%s)"
        data_tuple = ("kanyewestdevilinanewdress" +str(start)+str(fin),"Kanye West - Devil In ",DBstring,amountofwhites,compressedstr)
        db.commit()
        cursor.execute(Bite_insertion,data_tuple)
        start = start + 0.2 * 1000
        fin = fin + 0.2 * 1000



songtobites("D:/Yotam/Kanye West - Devil In A New Dress.wav")









