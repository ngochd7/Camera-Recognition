import sqlite3
import cv2

# recognizer = cv2.face_LBPHFaceRecognizer.create()
#     #recognizer = cv2.face_EigenFaceRecognizer.create()
#     #recognizer = cv2.face_FisherFaceRecognizer.create()

# recognizer.read('recognizer/trainingData.yml')
#give data from SQLite follow ID
def getProfile(id):
    db = sqlite3.connect("database/database.db")
    query = "Select * from People Where ID= " + str(id)
    cursor = db.execute(query)

    profile = None
    for row in cursor:
        profile = row

    db.close()
    return profile








    