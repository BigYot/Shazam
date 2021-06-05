import InsertSongToDBMethods
import mysql.connector




db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "songbites"
)
cursor = db.cursor()

jacsimcomp_global = {}








def sorter():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="songbites"
    )
    cursor = db.cursor(buffered=True)
    jacsim = {}
    bitestr = InsertSongToDBMethods.DBconversion("recordingbite.png")
    hashedbite = InsertSongToDBMethods.hasher(bitestr)
    most_sim_hashbite = sort_hashbite(hashedbite)
    cursor.execute("SELECT neighboors FROM hashtable WHERE hashbite = '{}'".format(most_sim_hashbite[0]))
    temp_neighboors = cursor.fetchall()
    #print(temp_neighboors)
    neighboors = temp_neighboors[0][0].split(",")



    for neighboor in neighboors:
        cursor.execute("SELECT bites FROM hashtable WHERE hashbite = '{}'".format(neighboor))
        temp_bites = cursor.fetchall()
        bites = temp_bites[0][0].split(",")
        for bite in bites:


            dif = 0
            sim = 0
            cursor.execute("SELECT bite FROM SongBites WHERE songbite = '{}'".format(bite))
            songbite = cursor.fetchall()
            for i in range(len(songbite[0][0])):
                if bitestr[i] == "1" and songbite[0][0][i] == "0":
                    dif+=1
                elif bitestr[i] == "0" and songbite[0][0][i] == "1":
                    dif+=1
                elif bitestr[i] == "1" and songbite[0][0][i] == "1":
                    sim+=1
                    dif+=1
            jacof = sim/dif
            jacsim[bite] = jacof
            sim = 0
            dif = 0
    sorted_jacsim = sorted(jacsim.items(),key=lambda x: x[1],reverse=True)




    counter = 0
    for key in sorted_jacsim:
        cursor.execute("SELECT songname FROM SongBites WHERE songbite = '{}'".format(key[0]))
        name = cursor.fetchall()
        
        if key[1] >= 0.15:
            return name[0][0]
        else: return ""
        
        print(key[0] + "," +  name[0][0] + " , " + str(key[1]))
        '''
        if counter == 10:
            break
        counter+=1
        '''








def sort_hashbite(hashbite):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="songbites"
    )
    cursor1 = db.cursor()
    rec_hashbite = ""
    if len(hashbite) > 1:
        rec_hashbite = hashbite
    else: rec_hashbite = InsertSongToDBMethods.hasher(InsertSongToDBMethods.DBconversion("recordingbite.png"))
    temp_hashbite = rec_hashbite
    done = False
    change = 1
    while True:
        temp_hashbite = rec_hashbite
        bit_arr = [None] * change
        for j in range(change):
            bit_arr[j] = j
        while True:
            for j in bit_arr:
                if temp_hashbite[j] == "1":
                    temp_hashbite = temp_hashbite[:j] + "0" + temp_hashbite[j+1:]
                else: temp_hashbite = temp_hashbite[:j] + "1" + temp_hashbite[j+1:]
            cursor1.execute("SELECT hashbite FROM hashtable WHERE hashbite = '{}'".format(temp_hashbite))
            result = cursor1.fetchall()
            if len(result) != 0:
                return result[0]
            if bit_arr[len(bit_arr) - 1] != 30:
                bit_arr[len(bit_arr) - 1]+=1
            else:
                for t in range(len(bit_arr)):
                    if bit_arr[len(bit_arr) - 1 - t] == 30 - t:
                        '''
                        print(bit_arr[len(bit_arr) - 1 - t])
                        print(t)
                        print(len(bit_arr))
                        '''
                        if t == len(bit_arr) - 1:
                            done = True
                        pass
                    else:
                        #print(t)
                        for r in reversed(range(t+1)):
                            #print(r)
                            if r == t:
                                bit_arr[len(bit_arr) - r - 1]+=1
                            else:
                                #print(r)
                                bit_arr[len(bit_arr) - r - 1] = bit_arr[len(bit_arr) - r - 2] + 1
                        break
                        temp_hashbite = rec_hashbite
            if done == True:
                    #print("check")
                    change+=1
                    done = False
                    break

            temp_hashbite = rec_hashbite
























sorter()
#test()
#test1()
#sort_hashbite()













