import os
import shutil
import cv2
sourcepath = 'dataset\Data_PreProcessing'

folderAllData_NotFair = 'dataset\Data_NotFair\All_Data_Processed'
Data_Train_NotFair = 'dataset\Data_NotFair\Data_Train'
Data_Test_NotFair = 'dataset\Data_NotFair\Data_Test'

folderAllData_Fair = 'dataset\Data_Fair\All_Data_Processed'
Data_Train_Fair = 'dataset\Data_Fair\Data_Train'
Data_Test_Fair = 'dataset\Data_Fair\Data_Test'






def combineAllData(): # copy toàn bộ hình ảnh từ 5749 thư mục chứa ảnh của 5749 người từ Data_PreProcessing về DataProcessed
    listpaths_Lv1 = [os.path.join(sourcepath, f) for f in os.listdir(sourcepath)]
    print(len(listpaths_Lv1))
    i = 0
    j = 0
    for p1 in listpaths_Lv1:
        print('numFileProcessed: ' + str(i))
        i = i + 1
        listpaths_Lv2 = [os.path.join(p1, f) for f in os.listdir(p1)]
        for p2 in listpaths_Lv2:
            j = j + 1
            #copy file from here to folder Data_Processed
            fro = p2
            to = folderAllData_NotFair +'\\' + p2.split('\\')[-1]
            shutil.copyfile(fro, to)
    print('Số lượng thư mục ảnh được lấy: ' + str(i))
    print('Số lượng ảnh được lấy: ' + str(j))

# combineAllData()

def combineDataFair(): # copy ảnh của những nguời có số lượng ảnh từ 10 đến 19 ảnh
    listpaths_Lv1 = [os.path.join(sourcepath, f) for f in os.listdir(sourcepath)]
    print(len(listpaths_Lv1))
    i = 0
    j = 0
    n = 1
    for p1 in listpaths_Lv1:
        print('numFileProcessed: ' + str(n))
        n = n + 1
        listpaths_Lv2 = [os.path.join(p1, f) for f in os.listdir(p1)]
        if len(listpaths_Lv2) > 9 and len(listpaths_Lv2) <20: # chỉ lấy dữ liệu của những người có từ 10 tới 19 bức ảnh
            i = i + 1      
            for p2 in listpaths_Lv2:
                j = j + 1
                #copy file from here to folder Data_Processed
                fro = p2
                to = folderAllData_Fair +'\\' + p2.split('\\')[-1]
                shutil.copyfile(fro, to)
        
    print('Số lượng thư mục ảnh được lấy: ' + str(i))
    print('Số lượng ảnh được lấy: ' + str(j))

# combineDataFair()


def assignIDandRename(Folder): # Gán Id cho bức ảnh và loại bỏ tên -> User.ID.index.jpg, vd aa_bb_0001.jpg -> User.0.1.jpg
    listpaths = [os.path.join(Folder, f) for f in os.listdir(Folder)]
    total = len(listpaths)
    i = 1
    namePerson = listpaths[0].split('_')[-2] #lấy tên chính của người đầu tiên
    id = 0
    numPhoto = -1
    for path in listpaths:
        fileName = path.split('\\')[-1]
        nameNewPerson = fileName.split('_')[-2]
        if(nameNewPerson == namePerson):
            numPhoto = numPhoto + 1
        else:
            namePerson = nameNewPerson
            numPhoto = 0
            id = id + 1
        newFilename = 'User.' + str(id) +'.'+ str(numPhoto)+ '.jpg'

        oldDirFile = Folder + '\\' + fileName
        newDirFile = Folder + '\\' + newFilename
        os.rename(oldDirFile,newDirFile)
        print('NumFileRenamed : ' + str(i) + '//' + str(total) + '     -     newFileName : ' + newFilename)
        i = i+1

# assignIDandRename(folderAllData_Fair)
# assignIDandRename(folderAllData_NotFair)

def createSetImageTest(folderAllData, folderDataTest): #cut toàn bộ ảnh có index == 1 sang tập test|Data_Test
    listpaths = [os.path.join(folderAllData, f) for f in os.listdir(folderAllData)]
    total = len(listpaths)
    i = 1
    for path in listpaths:        
        fileName = path.split('\\')[-1]
        indexPhoto = fileName.split('.')[-2]
        if (int(indexPhoto) == 1):
            #cut img to Data_Test
            dirFileMove = path
            toFolder = folderDataTest
            dest = shutil.move(dirFileMove, toFolder) 
            print('NumFileMoved :' + str(i) + '//' + str(total) + ',filename : ' + fileName)
            i = i+1
               

# createSetImageTest(folderAllData_Fair, Data_Test_Fair)
# createSetImageTest(folderAllData_NotFair, Data_Test_NotFair)




def createSetImageTrain(folderAllData, folderDataTrain): #Di chuyển toàn bộ ảnh còn lại trong Data_PreProcess sang Data_Train
    listpaths = [os.path.join(folderAllData, f) for f in os.listdir(folderAllData)]
    total = len(listpaths)
    i = 1
    for path in listpaths:
        dirFileMove = path
        toFolder = folderDataTrain
        dest = shutil.move(dirFileMove, toFolder)  
        print('NumFileMoved : ' + str(i) + '//' + str(total))
        i = i + 1
    print('done')

# createSetImageTrain(folderAllData_Fair, Data_Train_Fair)
# createSetImageTrain(folderAllData_NotFair, Data_Train_NotFair)

def countNumImg(folder):
    listpaths = os.listdir(folder)
    print('num photo of Folder ' + str(folder) + ' is: ' + str(len(listpaths)))

# countNumImg(Data_Train_Fair)
# countNumImg(Data_Train_NotFair)
# countNumImg(Data_Test_Fair)
# countNumImg(Data_Test_NotFair)


modelFile = "resource/DNN/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "resource/DNN/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
def detectAndCutFace(Folder): # Nhận diện mặt bằng DNN và sau đó thay thế bức ảnh cũ bằng khuôn mặt vừa dc phát hiện
    listpaths = [os.path.join(Folder, f) for f in os.listdir(Folder)]
    total = len(listpaths)
    count = 1
    for path in listpaths:
        print(str(count) + '//' + str(total))
        count = count + 1
        img = cv2.imread(path)
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

                faces.append([x, y, w, h])
        try:
            # tìm khuôn mặt chính trong bức ảnh : nó sẽ có size w*h lớn nhất 
            maxsize = 0
            mainFaceIndex = 0
            faceIndex = 0
            for (x, y, w, h) in faces:
                if w*h > maxsize:
                    maxsize = w*h
                    mainFaceIndex = faceIndex
                faceIndex = faceIndex + 1
            x, y, w, h = faces[mainFaceIndex]
            # xử lý cắt khuôn mặt thành hình vuông 
            x = x + int(w/2) - int(h/2) 
            w = h 
            img_crop = img[y:y+h, x:x+w]
            # thay thế ảnh ban đầu bằng ảnh đã cắt
            cv2.imwrite(path, img_crop)
        except:
            e = 0 

# detectAndCutFace(Data_Train_Fair)
# detectAndCutFace(Data_Train_NotFair)




