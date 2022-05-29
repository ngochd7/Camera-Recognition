import cv2
import os
print("nhap id:")
id = int(input())
sampleNum = 0
face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
path = "Manual_Input_Data2"
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
for imgPath in imagePaths:
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    for (x, y, w, h) in faces:
        img_crop = img[y:y+h, x:x+w]
    cv2.imwrite('data/User.' + str(id) + '.' + str(sampleNum) + '.jpg', img_crop)
    sampleNum = sampleNum + 1