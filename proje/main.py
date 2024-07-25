import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
import json
import os

import subprocess

import cv2
import test

data_file = 'data.txt'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import shutil
import time
from datetime import datetime
import threading

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 705)

        #---------- list_free_cam
        self.list_free_cam = QListWidget(Dialog)
        self.list_free_cam.setGeometry(QtCore.QRect(10, 10, 250, 500))
        self.list_free_cam.setObjectName("list_free_cam")
        
        #---------- list_added
        self.list_added = QListWidget(Dialog)
        self.list_added.setGeometry(QtCore.QRect(940, 10, 250, 500))
        self.list_added.setObjectName("list_added")
        
        #---------- btn_add
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(170, 520, 90, 28))
        self.btn_add.clicked.connect(self.btn_add_click)
        self.btn_add.setObjectName("btn_add")

        #---------- btn_remove
        self.btn_remove = QtWidgets.QPushButton(Dialog)
        self.btn_remove.setGeometry(QtCore.QRect(1100, 520, 90, 28))
        self.btn_remove.clicked.connect(self.btn_remove_click)
        self.btn_remove.setObjectName("btn_remove")

        #---------- btn_settings
        self.btn_settings = QtWidgets.QPushButton(Dialog)
        self.btn_settings.setGeometry(QtCore.QRect(1100, 670, 90, 28))
        self.btn_settings.clicked.connect(self.btn_settings_click)
        self.btn_settings.setObjectName("btn_settings")
        
        #---------- btn_start
        self.btn_start = QtWidgets.QPushButton(Dialog)
        self.btn_start.setGeometry(QtCore.QRect(830, 670, 90, 28))
        self.btn_start.clicked.connect(self.btn_start_click)        
        self.btn_start.setObjectName("btn_start")

        #---------- btn_stop
        self.btn_stop = QtWidgets.QPushButton(Dialog)
        self.btn_stop.setGeometry(QtCore.QRect(710, 670, 90, 28))
        self.btn_stop.clicked.connect(self.btn_stop_click)   
        self.btn_stop.setObjectName("btn_stop") 

        #---------- kamerlar
        self.kameralar = QtWidgets.QGroupBox(Dialog)
        self.kameralar.setGeometry(QtCore.QRect(270, 10, 650, 650))
        self.kameralar.setObjectName("kameralar")
        
        self.cam0 = QtWidgets.QLabel(self.kameralar)
        self.cam0.setGeometry(QtCore.QRect(5, 5, 300, 300))
        self.cam0.setObjectName("cam0")
        
        self.cam1 = QtWidgets.QLabel(self.kameralar)
        self.cam1.setGeometry(QtCore.QRect(330, 5, 300, 300))
        self.cam1.setObjectName("cam1")
        
        self.cam3 = QtWidgets.QLabel(self.kameralar)
        self.cam3.setGeometry(QtCore.QRect(330, 350, 300, 300))
        self.cam3.setObjectName("cam3")
        
        self.cam2 = QtWidgets.QLabel(self.kameralar)
        self.cam2.setGeometry(QtCore.QRect(5, 350, 300, 300))
        self.cam2.setObjectName("cam2")
        
        #---------- txt_ip
        self.txt_ip = QtWidgets.QLineEdit(Dialog)
        self.txt_ip.setGeometry(QtCore.QRect(40, 570, 221, 31))
        self.txt_ip.setObjectName("txt_ip")
        
        #---------- txt_name
        self.txt_name = QtWidgets.QLineEdit(Dialog)
        self.txt_name.setGeometry(QtCore.QRect(40, 620, 221, 31))
        self.txt_name.setObjectName("txt_name")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 570, 55, 16))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 620, 55, 16))
        self.label_2.setObjectName("label_2")
        
        #---------- btn_ipadd
        self.btn_ipadd = QtWidgets.QPushButton(Dialog)
        self.btn_ipadd.setGeometry(QtCore.QRect(172, 660, 91, 31))
        self.btn_ipadd.clicked.connect(self.btn_ipadd_click)
        self.btn_ipadd.setObjectName("btn_ipadd")

        self.classes = None
        self.running = True     
        self.sleeptime = 301
        self.totaltime = 0
        self.first = True
        self.load()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kamera Takip"))
        self.btn_add.setText(_translate("Dialog", "Ekle"))
        self.btn_remove.setText(_translate("Dialog", "Çıkar"))
        self.btn_settings.setText(_translate("Dialog", "Ayarlar"))
        self.btn_start.setText(_translate("Dialog", "Başlat"))
        self.btn_stop.setText(_translate("Dialog", "Durdur"))
        self.kameralar.setTitle(_translate("Dialog", "Kameralar"))
        self.label.setText(_translate("Dialog", "IP"))
        self.label_2.setText(_translate("Dialog", "Ad"))
        self.btn_ipadd.setText(_translate("Dialog", "IP Ekle"))

    def load(self):
        veriler = Ui_Dialog.read_data()
        for veri in veriler:
            item_text = f"{veri['name']}"
            self.list_free_cam.addItem(item_text)


    def btn_add_click(self):
        if self.list_added.count() < 4:
            selected_items = self.list_free_cam.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.list_added.addItem(f"{item.text()}")
                    self.list_free_cam.takeItem(self.list_free_cam.row(item))
            else:
                QMessageBox.information(None, "Uyarı", "Lütfen bir öğe seçin.")
        else:
            QMessageBox.information(None, "Uyarı", "Dörtten fazla kamera desteklemez.")
    
    def btn_remove_click(self):
        selected_items = self.list_added.selectedItems()
        if selected_items is not None:
            for item in selected_items:
                self.list_free_cam.addItem(item.text())
                self.list_added.takeItem(self.list_added.row(item))

    def btn_settings_click(self):
        subprocess.Popen(['python', 'form_settings.py'])


    def btn_ipadd_click(self):
        name = self.txt_name.text()
        ip = self.txt_ip.text()
        Ui_Dialog.save_data(name, ip)
        self.list_free_cam.addItem(name)

    def btn_stop_click(self):
        self.running = False
        cv2.destroyAllWindows()

    def btn_start_click(self):
        self.running = True
        items = []
        for index in range(self.list_added.count()):
            item = self.list_added.item(index)
            items.append(item.text())
        
        for idx, item in enumerate(items):
            threading.Thread(target=self.add_cam, args=(item, idx)).start()

    def reload_cam(self):
        self.running = False
        cv2.destroyAllWindows()
        
        self.running = True
        items = []
        for index in range(self.list_added.count()):
            item = self.list_added.item(index)
            items.append(item.text())
        
        for idx, item in enumerate(items):
            threading.Thread(target=self.add_cam, args=(item, idx)).start()

    def add_cam(self, url, camIndex):
        starttime = time.time()
        object_detected = False

        ip = Ui_Dialog.find_ip_by_name(url)
        cap = cv2.VideoCapture(ip)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))

        while cap.isOpened() and self.running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (600, 600) if camIndex == 0 else (300, 300))
            aframe, class_name = test.detector(frame)
            self.display_Image(aframe, camIndex)

            if self.sleeptime > 120:
                self.totaltime = round((time.time() - starttime), 0)
                if class_name in ['person', 'car']:
                    self.sleeptime = 0
                    object_detected = True

            elif object_detected and self.totaltime < 60:
                self.totaltime = round((time.time() - starttime), 0)
                if self.totaltime % 12 == 0:
                    filename = f'temp/temp_{self.totaltime // 12}.png'
                    cv2.imwrite(filename, aframe)

            elif self.totaltime > 59 and object_detected:
                object_detected = False
                self.first = True
                Ui_Dialog.send_mail(datetime.now())
                Ui_Dialog.clean()

            elif self.totaltime > 59 and self.first:
                self.first = False
                self.sleeptime = 0
                self.totaltime = 0
                self.reload_cam()

            self.sleeptime = round((time.time() - starttime), 0)
            cv2.waitKey(1)

        cap.release()

    def display_Image(self, img, labelIndex=0):
        qformat = QImage.Format_Indexed8
        if img.shape[2] == 4:
            qformat = QImage.Format_RGBA888
        else:
            qformat = QImage.Format_RGB888
                
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()

        if labelIndex == 0:
            self.cam0.setGeometry(QtCore.QRect(5, 5, 600, 600))
            self.cam0.setPixmap(QPixmap.fromImage(img))
            self.cam0.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
        elif labelIndex == 1:
            self.cam0.setGeometry(QtCore.QRect(150, 5, 300, 300))
            self.cam1.setGeometry(QtCore.QRect(150, 305, 300, 300))
            self.cam1.setPixmap(QPixmap.fromImage(img))
            self.cam1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
        elif labelIndex == 2:
            self.cam0.setGeometry(QtCore.QRect(5, 5, 300, 300))
            self.cam1.setGeometry(QtCore.QRect(150, 305, 300, 300))
            self.cam2.setGeometry(QtCore.QRect(150, 305, 300, 300))
            self.cam2.setPixmap(QPixmap.fromImage(img))
            self.cam2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        elif labelIndex == 3:
            self.cam3.setPixmap(QPixmap.fromImage(img))
            self.cam3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        

    def clean():
        temp_folder = 'temp/'
        if os.path.exists(temp_folder):
            for filename in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Dosyaları veya sembolik linkleri silme
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Alt klasörleri ve içeriğini silme
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            print(f"{temp_folder} does not exist")

        print("Temp folder cleaned up.")

    def send_mail(timeNow):
        veriler = Ui_Dialog.read_settings()
        sender = veriler[0]['sender']
        receiver = veriler[0]['receiver']
        sender_password = veriler[0]['sender_password']
        smtp_server = veriler[0]['smtp_server']
        smtp_server_port = veriler[0]['smtp_server_port']

        # E-posta gönderen ve alıcı bilgileri
        fromaddr = sender
        toaddr = receiver

        # E-posta mesajı oluşturma
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Your subject"

        # E-posta içeriği ekleme
        body = str(timeNow) +" tarihinde bir hareketilik algılandı. Algılanan nesneler ektedir."
        msg.attach(MIMEText(body, 'plain'))

        # Temp klasöründeki tüm dosyaları ekleme
        directory = "temp"
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                attachment = open(filepath, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                msg.attach(part)
                attachment.close()

        # SMTP sunucusuna bağlanma ve e-posta gönderme
        s = smtplib.SMTP(smtp_server, smtp_server_port)
        s.starttls()
        s.login(fromaddr, sender_password) 
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()


    def save_data(name, ip):
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        data.append({'name': name, 'ip': ip})
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def read_data():
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []

    def find_ip_by_name(name):
            veriler = Ui_Dialog.read_data()
            for veri in veriler:
                if veri['name'] == name:
                    return veri['ip']
            return None

    def read_settings():
        try:
            with open('settings.txt', 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
