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
cursor = db.cursor(buffered=True)
cursor1 = db.cursor(buffered=True)





def create_neighboors():
    command = "SELECT hashbite FROM hashtable"
    cursor1.execute(command)
    bites = cursor1.fetchall()
    jacof = 0
    jacsim = {}
    sorted_jacsim = {}
    dif = 0
    sim = 0
    for bite in bites:
        for bite1 in bites:
            if bite != bite1:
                for i in range(len(bite[0])):
                    if bite[0][i] == "1" and bite1[0][i] == "0":
                        dif+=1
                    elif bite[0][i] == "0" and bite1[0][i] == "1":
                        dif+=1
                    elif bite[0][i] == "1" and bite1[0][i] == "1":
                        dif+=1
                        sim+=1
                jacof = sim/dif
                jacsim[bite1[0]] = jacof
                sim = 0
                dif = 0
        sorted_jacsim = sorted(jacsim.items(), key=lambda x: x[1], reverse=True)
        neighstr = sorted_jacsim[0][0]
        for i in range(49):
            neighstr = neighstr + "," + sorted_jacsim[i+1][0]
        neighboors_insertion = "UPDATE hashtable SET neighboors = '{}' WHERE hashbite = '{}'".format(neighstr,bite[0])
        cursor.execute(neighboors_insertion)
        db.commit()











def getsongtime(filepath_song):
    with contextlib.closing(wave.open(filepath_song, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def insertintohashtable():
    QUERY_SIZE = 1000
    command = "SELECT songbite,hashbite FROM songbites"
    cursor.execute(command)
    biteslen = QUERY_SIZE

    while biteslen == QUERY_SIZE:
        bites = cursor.fetchmany(QUERY_SIZE)
        biteslen = len(bites)
        for bite in bites:
            command1 = "SELECT * FROM hashtable WHERE hashbite = '{}'".format(bite[1])
            cursor1.execute(command1)
            hashrow = cursor1.fetchone()
            if hashrow != None:
                bites_in_hashrow = hashrow[1]
                bites_in_hashrow = bites_in_hashrow + "," + bite[0]
                command1 = "UPDATE hashtable SET bites = '{}' WHERE bites = '{}'".format(bites_in_hashrow,hashrow[1])
                cursor1.execute(command1)
            else:
                hash_insertion = "INSERT INTO hashtable (hashbite,bites,neighboors) VALUES (%s,%s,%s)"
                data_tuple = (bite[1],bite[0],"")
                db.commit()
                cursor1.execute(hash_insertion,data_tuple)











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
        hashedstr = InsertSongToDBMethods.hasher(DBstring)
        Bite_insertion = "INSERT INTO songbites (songbite,songname,bite,hashbite) VALUES (%s,%s,%s,%s)"
        data_tuple = ("theweekndtellyourfriends" +str(start)+str(fin),"The Weeknd - Tell Your Friends ",DBstring,hashedstr)
        db.commit()
        cursor.execute(Bite_insertion,data_tuple)
        start = start + 0.2 * 1000
        fin = fin + 0.2 * 1000






#create_neighboors()
#insertintohashtable()
songtobites("D:/Yotam/The Weeknd - Tell Your Friends.wav")
#InsertSongToDBMethods.hasher(InsertSongToDBMethods.DBconversion('recordingbite.png'))











