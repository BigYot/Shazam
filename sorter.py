import sqlite3
import InsertSongToDBMethods
import mysql.connector
import gc


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "songbites"
)
cursor = db.cursor()








#unp = sqlite3.connect('D:\Yotam\Song_Bites.db')
#cursor = unp.cursor()


def test():
    db = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=D:\Yotam\Song_Bites.db;UID=me;PWD=pass')
    cursor1 = db.cursor()



def sorter():
    #jacsim stands for Jaccard Coefficent, a way to calculate simalarity between sets, and in our case, songs
    jacsim = {}
    jacsimcomp = {}
    #this method of obtaining the amountofwhite for the bites is not the most efficent, and the ultimate way to do so is to retrieve it when retreiving the bites themselves
    amountofwhitesdict = {}
    amountofwhites = InsertSongToDBMethods.getamountofwhites("recordingbite.png")
    print("Recording's amount of whites - " + str(amountofwhites))
    bitestr = InsertSongToDBMethods.DBconversion("recordingbite.png")
    compressstr = InsertSongToDBMethods.compressbite(bitestr)
    cursor.execute("SELECT * FROM SongBites")
    biteslen = 1000





    while biteslen == 1000:
        bites = cursor.fetchmany(size=1000)
        biteslen = len(bites)


        for bite in bites:
            #print(bite[0])
            # print(len(bite[2]))
            sim = 0
            dif = 0
            for i in range(len(bite[4])):
                if compressstr[i] == "1" and bite[4][i] == "0":
                    dif += 1
                elif compressstr[i] == "0" and bite[4][i] == "1":
                    dif += 1
                elif compressstr[i] == "1" and bite[4][i] == "1":
                    sim += 1
                    dif += 1
            jacoscomp = sim / dif
            jacsimcomp[bite[0]] = jacoscomp



    sorted_jacsimcomp = sorted(jacsimcomp.items(), key=lambda x: x[1], reverse=True)
    first_1000_sorted_jacsimcomp = sorted_jacsimcomp[:1000]
    sim = 0
    dif = 0

    print(first_1000_sorted_jacsimcomp[0])

    for bite in first_1000_sorted_jacsimcomp:
        cursor.execute("SELECT bite FROM SongBites WHERE songbite = '{}'".format(bite[0]))
        songbite = cursor.fetchall()
        #print(songbite[0][0])
     #need to fix this, bite[2] length and bitestr length are not the same for some reason
        for i in range(len(songbite[0][0])):
            if bitestr[i] == "1" and songbite[0][0][i] == "0":
                dif+=1
            elif bitestr[i] == "0" and songbite[0][0][i] == "1":
                dif+=1
            elif bitestr[i] == "1" and songbite[0][0][i] == "1":
                sim+=1
                dif+=1
        jacof = sim/dif
        jacsim[bite[0]] = jacof
        cursor.execute("SELECT amountofwhites FROM SongBites WHERE songbite = '{}'".format(bite[0]))
        amountofwhitesbite = cursor.fetchall()
        amountofwhitesdict[bite[0]] = amountofwhitesbite
        sim = 0
        dif = 0
    sorted_jacsim = sorted(jacsim.items(),key=lambda x: x[1],reverse=True)








    counter = 0
    for key in sorted_jacsim:
        print(key[0] + " , " + str(key[1]) + ", amount of whites - " + str(amountofwhitesdict[key[0]]) + " , similarity between compressed bites: " + str(jacsimcomp[key[0]]) )
        if counter == 10:
            break
        counter+=1
    print("/n")
    print("highest similarity among compressed bit")
    print("/n")
    counter = 0
    for key in sorted_jacsimcomp:
        print(key[0] + " , " + str(key[1]))
        if counter == 10:
            break
        counter+=1


sorter()
#test()













