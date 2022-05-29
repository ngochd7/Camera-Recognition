import sys

from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5  import QtWidgets, QtGui, QtCore
from UI.Ui import *



import cv2
import urllib.request
import numpy as np 

from src import connectToMyDatabase as cntdb
from src import detectFace
from src import training
from src import Attendence
from src import sendEmail
from src import detectHuman

import pyttsx3
engine = pyttsx3.init()

# face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
modelFile = "resource/DNN/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "resource/DNN/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

fontFace = cv2.FONT_HERSHEY_SIMPLEX
recognizer = cv2.face_LBPHFaceRecognizer.create()
    #recognizer = cv2.face_EigenFaceRecognizer.create()
    #recognizer = cv2.face_FisherFaceRecognizer.create()

recognizer.read('recognizer/trainingData.yml')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cap = cv2.VideoCapture(0) 
              
        self.a = AlertSendingEmail()
        self.ui.RegisterButton.clicked.connect(self.RegisterWindow)
        self.ui.countinueButton.clicked.connect(self.continueCamera)
        self.ui.UpdateButton.clicked.connect(self.train)
        #biến trạng thái:
        self.numSecondsHasStranger = 0 #số giây liên tục có người lạ
        self.numSecondsHasHuman = 0 #số giây liên tục có người xuất hiện
        self.isnew = True
        self.hasStranger = False
        self.notifyHasStranger = False
        self.hasHuman = False
        self.sentEmailHasHumanUnidentified = False
        self.sentEmailHasStranger = False
        self.infoStranger = ""
        self.IsAcquaintance = False
        
        #biến thời gian:
        self.timer = QTimer()
        self.timer.start(20)
        self.timer.timeout.connect(self.viewcam)

        self.timer22 = QTimer()
        self.timer22.start(100)
        # self.timer22.timeout.connect(self.viewcam2)

        self.timer2 = QTimer()
        self.timer2.start(100)
        self.timer2.timeout.connect(self.updateScreen2)

        self.timerAttendence = QTimer()
        self.timerAttendence.start(5000)
        self.timerAttendence.timeout.connect(self.setIsNewTrue)

        self.timerForDetectStranger = QTimer()
        self.timerForDetectStranger.start(300)
        self.timerForDetectStranger.timeout.connect(self.checkNumSecondsHasStranger)
 
        self.timerForMakeNotifyHasStranger = QTimer()
        self.timerForMakeNotifyHasStranger.start(300)
        self.timerForMakeNotifyHasStranger.timeout.connect(self.makeNotifyHasStranger)       

        self.timerForDetectHuman = QTimer()
        self.timerForDetectHuman.start(3000)
        self.timerForDetectHuman.timeout.connect(self.makeRequestRecognition)

        self.timerForMakenotifyHasHumanUnidentified = QTimer()
        self.timerForMakenotifyHasHumanUnidentified.start(3000)
        self.timerForMakenotifyHasHumanUnidentified.timeout.connect(self.checkNumSecondsHasHuman)
       
        self.timerForSendEmailHasStranger = QTimer()
        self.timerForSendEmailHasStranger.timeout.connect(self.setsentEmailHasStrangerFalse)

        self.timerForSendEmailHasHumanUnidentified = QTimer()
        self.timerForSendEmailHasHumanUnidentified.timeout.connect(self.setSentEmailHasHumanUnidentifiedFalse)

        self.timerForSetIsAcquaintanceFalse = QTimer()
        self.timerForSetIsAcquaintanceFalse.timeout.connect(self.setIsAcquaintanceFalse)
        # self.timerForSetIsAcquaintanceFalse.start(300000) #sẽ  được gọi sau phát hiện người quen + kích hoạt IsAcquaintance = True

        self.timerRemoveAlert = QTimer()
        self.timerRemoveAlert.start(2000)
        self.timerRemoveAlert.timeout.connect(self.removeAlertHasStranger)

        self.timerRemoveAlert1 = QTimer()
        self.timerRemoveAlert1.start(2000)
        self.timerRemoveAlert1.timeout.connect(self.removeAlertPeopleAtDoor)

    def continueCamera(self): 
        #hàm chạy khi ấn nút Tiếp Tục
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)
        recognizer.read('recognizer/trainingData.yml')
    def train(self):
        #hàm chạy khi ấn nút Cập nhật người dùng mới 
        training.train()
        print("ok")
   
    def setAlertHasStranger(self):
        self.timerRemoveAlert.stop()
        self.ui.AlertHasStranger.setText("Cảnh báo có người lạ")
        self.timerRemoveAlert.start(2000)
    def setAlertPeopleAtDoor(self):
        self.ui.AlertPeopleAtDoor.setText("Có người trước cửa")
        self.timerRemoveAlert1.start(2000)
    def removeAlertHasStranger(self):
        self.ui.AlertHasStranger.setText("")   
    def removeAlertPeopleAtDoor(self):
        self.ui.AlertPeopleAtDoor.setText("")
    
    def setSentEmailHasHumanUnidentifiedFalse(self):
        self.sentEmailHasHumanUnidentified = False
    def setsentEmailHasStrangerFalse(self):
        self.sentEmailHasStranger = False
    def setIsAcquaintanceFalse(self):
        self.IsAcquaintance = False
    def setIsNewTrue(self):
        self.isnew = True 
   

    def makeRequestRecognition(self):
        if self.hasHuman == True:
            self.hasHuman = False
            print("nhìn vào camera nhận dạng")
            self.setAlertPeopleAtDoor()
            self.numSecondsHasHuman += 3
        else: 
            self.numSecondsHasHuman = 0          
    def checkNumSecondsHasHuman(self):
        if self.numSecondsHasHuman == 9 and self.IsAcquaintance == False:
            print("nguoi la khong the nhan dien, can gui mail thong bao")
            engine.say("Please look at camera 1 for identification")
            engine.runAndWait()    
        if self.numSecondsHasHuman > 8 and self.IsAcquaintance == False:
            # self.notifyHasHumanUnidentified = True
            if self.sentEmailHasHumanUnidentified == False:
                self.sentEmailHasHumanUnidentified = True
                print("dang gui email")
                self.AlertShow()
                self.timerForSendEmailHasHumanUnidentified.stop()
                sendEmail.sendEmailNotify("database/infoStranger/human.jpg")
                print("da gui email")
                self.AlertClose()
                self.timerForSendEmailHasHumanUnidentified.start(300000)

    def checkNumSecondsHasStranger(self):
        if self.hasStranger == True:
            self.numSecondsHasStranger = self.numSecondsHasStranger + 1
            self.hasStranger = False
        else: 
            self.numSecondsHasStranger = 0
            self.notifyHasStranger = False
        if self.numSecondsHasStranger > 5:
            self.notifyHasStranger = True
            self.setAlertHasStranger()
    def makeNotifyHasStranger(self):
        if self.notifyHasStranger == True:
            if self.numSecondsHasStranger == 6:
                print("co nguoi laaaaaaaaaaaaaaaaaaaa")
                # engine.say("I cannot recognize you")
                # engine.runAndWait()
                print("noi xong")               
            if self.sentEmailHasStranger == False:
                self.sentEmailHasStranger = True
                print("đang gửi email")
                self.AlertShow()
                # self.timerForSendEmailHasStranger.stop()
                sendEmail.sendEmailNotify("database/infoStranger/Stranger.jpg")
                print("đã gửi email")
                self.AlertClose()
                self.timerForSendEmailHasStranger.start(300000)
            
    def updateScreen2(self):
        with open('database/attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            content = ""
            count = -1
            for line in myDataList:
                count += 1
            first = True
            lay12trangthaimoinhat = 12
            while count > -1:
                if first == True:
                    content = content  + myDataList[count] + '\n'
                    first = False
                else:
                    content = content + myDataList[count]

                count = count - 1
                lay12trangthaimoinhat = lay12trangthaimoinhat -1

                if lay12trangthaimoinhat == 0: break
            self.ui.Screen2.setText(content)
        f.close()

    def viewcam(self):        
        ret, img = self.cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # faces = face_cascade.detectMultiScale(img, 1.3, 5)

        frameHeight = img.shape[0]
        frameWidth = img.shape[1]
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
        net.setInput(blob)
        detections = net.forward()
        faces1 = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                x = int(detections[0, 0, i, 3] * frameWidth) 
                y = int(detections[0, 0, i, 4] * frameHeight)
                
                w = int(detections[0, 0, i, 5] * frameWidth) - x 
                h = int(detections[0, 0, i, 6] * frameHeight) - y

                #sửa về dạng hình vuông cạnh bằng h 
                x2 = x + int(w/2) - int(h/2)
                w = h 
                # print(str(w) + " " + str(h))
                faces1.append([x2, y, w, h])
        # for (x, y, w, h) in faces1:
            # cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        for (x, y, w, h) in faces1:
            try:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                id, configparser = recognizer.predict(gray[y:y+h, x:x+w])
                print(str(id)+ "---"+ str(configparser))
                if configparser < 40:
                    profile = detectFace.getProfile(id)
                    #load info to camera
                    if (profile != None):
                        self.isnew = Attendence.markAttendance(str(profile[1]), self.isnew)
                        cv2.putText(img, "Name: "   + str(profile[1]), (x + 10, y + h + 30), fontFace, 1, (0, 255, 0), 2)
                        cv2.putText(img, "Age: "    + str(profile[2]), (x + 10, y + h + 60), fontFace, 1, (0, 255, 0), 2)
                        cv2.putText(img, "Gender: " + str(profile[3]), (x + 10, y + h + 90), fontFace, 1, (0, 255, 0), 2)
                    # Kích hoạt biến IsAcquaintance True
                    self.IsAcquaintance = True
                    self.timerForSetIsAcquaintanceFalse.stop()
                    self.timerForSetIsAcquaintanceFalse.start(300000) #cho phép giữ trạng thái True trong 3 phút
                else:
                    cv2.putText(img, "unknow", (x + 10, y + h + 30), fontFace, 1, (0,255,0), 2) 
                    img2  = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
                    cv2.imwrite('database/infoStranger/Stranger.jpg', img2)
                    self.hasStranger = True
            except:
                print("loi recognizer ")
        # get image infos
        height, width, channel = img.shape       
        step = channel * width
        # create QImage from image
        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label   
        self.ui.CameraShow.setPixmap(QPixmap.fromImage(qImg))

    def viewcam2(self):         
        imgResp = urllib.request.urlopen('http://192.168.1.11:8080/shot.jpg')
        imgNp = np.array(bytearray(imgResp.read()), dtype = np.uint8)
        
        img = cv2.imdecode(imgNp, -1)
        img = cv2.resize(img, dsize=(401, 200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img, hasHuman = detectHuman.detect(img)

        # get image infos
        height, width, channel = img.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label   
        self.ui.Screen1.setPixmap(QPixmap.fromImage(qImg))
        if hasHuman == True:
            self.hasHuman = True
            cv2.imwrite('database/infoStranger/human.jpg', img)

    def RegisterWindow(self): 
        self.timer.stop()
        # release video capture
        self.cap.release()
        self.w = RegisterWindow()
        self.w.show()
    def AlertShow(self):
        self.a.show()
        print("show")
    def AlertClose(self):
        self.a.close()
        print("close")

class AlertSendingEmail(QMainWindow):
    def __init__(self):
        super().__init__()
        self.alert = Ui_Alert()
        self.alert.setupUi(self)
        print("init")

class RegisterWindow(QMainWindow):                         
    def __init__(self):
        super().__init__()
        self.ui2 = Ui_Register()
        self.ui2.setupUi(self)
        self.ui2.SaveButton.clicked.connect(self.saveData)
    def saveData(self):
        name = self.ui2.NameEdit.text()
        age =  self.ui2.spinBoxAge.value()
        id = self.ui2.spinBoxId.value()
        if self.ui2.radioButtonMale.isChecked():
            gender = "nam" 
        else: gender = "nu"

        print(id, name, age, gender)
        cntdb.insertORUpdate(id, name, age, gender)

        self.close()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Nhìn vào camera để chụp ảnh")
        msg.setWindowTitle("Thông báo")
        msg.exec_()

        self.cap2 = cv2.VideoCapture(0)
        sampleNum = 0
        while True:
            ret, img = self.cap2.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # faces = face_cascade.detectMultiScale(img, 1.3, 5)

            # faces = []
            # try:
            #     frameHeight = img.shape[0]
            #     frameWidth = img.shape[1]
            #     blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
            #     net.setInput(blob)
            #     detections = net.forward()
                
            #     for i in range(detections.shape[2]):
            #         confidence = detections[0, 0, i, 2]
            #         if confidence > 0.7:
            #             x = int(detections[0, 0, i, 3] * frameWidth)
            #             y = int(detections[0, 0, i, 4] * frameHeight)
                    
            #             w = int(detections[0, 0, i, 5] * frameWidth) - x
            #             h = int(detections[0, 0, i, 6] * frameHeight) - y
            #             faces.append([x, y, w, h])
            # except:
            #     print("loi2")
            frameHeight = img.shape[0]
            frameWidth = img.shape[1]
            blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
            net.setInput(blob)
            detections = net.forward()
            faces1 = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.7:
                    x = int(detections[0, 0, i, 3] * frameWidth) 
                    y = int(detections[0, 0, i, 4] * frameHeight)
                    
                    w = int(detections[0, 0, i, 5] * frameWidth) - x 
                    h = int(detections[0, 0, i, 6] * frameHeight) - y

                    #sửa về dạng hình vuông cạnh bằng h 
                    x2 = x + int(w/2) - int(h/2)
                    w = h 
                    # print(str(w) + " " + str(h))
                    faces1.append([x2, y, w, h])
            for (x, y, w, h) in faces1:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.imwrite('data/User.' + str(id) + '.' + str(sampleNum) + '.jpg', img[y:y+h, x:x+w])
                
                print(sampleNum)
            sampleNum += 1
            cv2.waitKey(20)
            cv2.imshow("camera", img)
            if sampleNum == 20: 
                print("da lay du lieu xong")
                break
        self.cap2.release()
        cv2.destroyWindow("camera")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())