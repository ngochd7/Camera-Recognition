import cv2
import numpy as np 
import os 
from PIL import Image

recognizer = cv2.face_LBPHFaceRecognizer.create()
    #recognizer = cv2.face_EigenFaceRecognizer.create()
    #recognizer = cv2.face_FisherFaceRecognizer.create()

def getImagesWitdthID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    Ids = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')

        faceNp  = np.array(faceImg, 'uint8')
        faces.append(faceNp)

        #cut to give image's ID
        ID = int(imagePath.split('\\')[1].split('.')[1])
        Ids.append(ID)

    return faces, Ids

def train():
    faces, Ids = getImagesWitdthID("data")
    #Training
    recognizer.train(faces, np.array(Ids))
    #saving
    recognizer.save('recognizer/trainingData.yml')

# train()
