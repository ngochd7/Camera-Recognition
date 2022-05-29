import sqlite3
import os

databaseDir = "database/database.db"

def connectToDatabase():
    try:
        db = sqlite3.connect(databaseDir)
        print("ketnoithanhcong")
        return db
    except:
        print("thatbai")
        return None

def showDatabase():
    db = connectToDatabase()
    query = "Select * From People"
    cur = db.execute(query)
    for line in cur:
        print(line)
def clearDatabase():
    db = connectToDatabase()
    query = "DELETE FROM People"
    db.execute(query)
    db.commit()
    db.close()

def insertORUpdate(id, name, age, gender):
    db = connectToDatabase()
    query = "SELECT * FROM People WHERE ID = "+ str(id)

    cursor = db.execute(query)
    isREcordExist = 0

    for row in cursor:
        isREcordExist = 1

    if isREcordExist == 0:
        query = "Insert into People(ID, Name, Age, Gender) values(" + str(id) + ",'" + str(name) + "'," + str(age) + ",'" + str(gender) + "')"
    else:
        query = "Update People set Name = '" + str(name) + "', Age = " + str(age) + ", Gender = '" + str(gender) + "' Where ID = " +str(id)
    # print("2",query)

    db.execute(query)
    db.commit()
    db.close()


# clearDatabase()
# showDatabase()