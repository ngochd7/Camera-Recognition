import cv2
import numpy as np 
import os 
from PIL import Image

recognizer = cv2.face_LBPHFaceRecognizer.create()
    

def getImagesWitdthID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    Ids = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')

        faceNp  = np.array(faceImg, 'uint8')
        faces.append(faceNp)

        #cut to give image's ID
        ID = int(imagePath.split('\\')[-1].split('.')[1])
        Ids.append(ID)

    return faces, Ids

def train(folderTrain, savePath):
    faces, Ids = getImagesWitdthID(folderTrain)
    #Training
    print('Training...')
    recognizer.train(faces, np.array(Ids))
    #saving
    recognizer.save(savePath)


Data_Train_Fair = 'dataset\Data_Fair\Data_Train'
Data_Train_NotFair = 'dataset\Data_NotFair\Data_Train'
Data_Fair_Recognizer = 'dataset/Data_Fair/Recognizer/trainingData.yml'
Data_NotFair_Recognizer = 'dataset/Data_NotFair/Recognizer/trainingData.yml'


# Chạy 2 dòng này :
train(Data_Train_Fair, Data_Fair_Recognizer)
# train(Data_Train_NotFair, Data_NotFair_Recognizer)