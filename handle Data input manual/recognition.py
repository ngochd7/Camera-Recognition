import os
import cv2
recognizer = cv2.face_LBPHFaceRecognizer.create()
  

recognizer.read('dataset/Data_Fair/Recognizer/trainingData.yml')
path = 'dataset\Data_Fair\Data_Test' 

# recognizer.read('dataset/Data_NotFair/Recognizer/trainingData.yml')
# path = 'dataset\Data_NotFair\Data_Test'

modelFile = 'resource/DNN/res10_300x300_ssd_iter_140000.caffemodel'
configFile = 'resource/DNN/deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

def recognition(img):
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            x = int(detections[0, 0, i, 3] * imgWidth) 
            y = int(detections[0, 0, i, 4] * imgHeight)        
            w = int(detections[0, 0, i, 5] * imgWidth) - x 
            h = int(detections[0, 0, i, 6] * imgHeight) - y
            # xử lý cắt khuôn mặt thành hình vuông 
            x2 = x + int(w/2) - int(h/2) 
            w = h
            faces.append([x2, y, w, h])
        
    maxsize = 0
    mainFaceIndex = 0
    faceIndex = 0
    for (x, y, w, h) in faces:
        if w*h > maxsize:
            maxsize = w*h
            mainFaceIndex = faceIndex
            faceIndex = faceIndex + 1
    x, y, w, h = faces[mainFaceIndex]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    id, configparser = recognizer.predict(gray[y:y+h, x:x+w])
    return id, configparser

def checkResult(idImg, img):
    cv2.imshow('Identifying...', img)
    cv2.waitKey(10)
    id, configparser = recognition(img)
    if int(idImg) == int(id): return 1, id,  configparser
    return 0, id, configparser
def getIdImg(path):
    filename = str(path).split('\\')[-1]
    return int(filename.split('.')[-3])
# def getNumImgTrain(Id):
#     count = 0 
#     path = 'dataset/Data_Fair/Data_Train'
#     imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
#     for p in imagePaths:
#         if int(getIdImg(p)) == int(Id) : 
#             count = count + 1
#     return count



imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
results = []
i = 1
for p in imagePaths:
    result = []
    idImg = getIdImg(p)
    img = cv2.imread(p)
    try:
        print(p)
        
        # count = getNumImgTrain(getIdImg(p))
        
        check, id,  configparser = checkResult(idImg, img)
        result.append(check)
        result.append(idImg)
        result.append(id)
        result.append(configparser)
        # result.append(count)

        results.append(result)
        print(result)
        
    except:
        result.append(2)
        result.append(idImg)
        result.append(-1)
        result.append(-1)
        # result.append(-1)

        results.append(result)
        print('loi')
        print(p)

l = len(results)
CountTrue = 0
CountRecognizer = 0 

for r in results:
    if int(r[0]) == 1:
        CountTrue = CountTrue + 1
    if int(r[0]) != 2:
        CountRecognizer = CountRecognizer + 1

TrueRatio = CountTrue/l
print('Tỷ lệ được nhận diện : ' + str(CountRecognizer) + ' / ' + str(l))
print('Tỷ lệ được nhận dạng đúng : ' + str(CountTrue) + ' / ' + str(l) + ' = ' + str(TrueRatio) )

#save
with open('dataset/Data_Fair/Result.txt', 'w', encoding='utf-8') as f:
# with open('dataset/Data_NotFair/Result.txt', 'w', encoding='utf-8') as f:
    row1 = 'Tỷ lệ được nhận dạng : ' + str(CountRecognizer) + ' / ' + str(l) + '\n'
    row2 = 'Tỷ lệ nhận dạng đúng : ' + str(CountTrue) + ' / ' + str(l) + ' = ' + str(TrueRatio) +'\n'
    row3 = 'Result | IdImg | IdRecognition | Configparser' + '\n'
    f.write(row1)
    f.write(row2)
    f.write(row3)
    for item in results:
        f.write("%s\n" % item)

