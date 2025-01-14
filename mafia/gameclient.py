from tkinter.constants import N, TRUE, Y
from PyQt5 import QtCore, QtWidgets
import gameUI


import sys
import socket


class ReceiveThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, client_socket):
        super(ReceiveThread, self).__init__()
        self.client_socket = client_socket

    def run(self):
        while True:
            self.receive_message()

    def receive_message(self):
        message = self.client_socket.recv(1024)
        message = message.decode()

        print(message)
        self.signal.emit(message)


class Client(object):
    def __init__(self):
        self.messages = []
        self.mainWindow = QtWidgets.QMainWindow()

        # add widgets to the application window
        self.chatWidget = QtWidgets.QWidget(self.mainWindow)
        self.chat_ui = gameUI.Ui_Mafia()
        self.chat_ui.setupUi(self.chatWidget)
        self.chat_ui.inputbutton.clicked.connect(self.send_message)
        self.chat_ui.textEdit.returnPressed.connect(self.send_message)
        self.chat_ui.to_user1.clicked.connect(self.send_to_user1)
        self.chat_ui.to_user2.clicked.connect(self.send_to_user2)
        self.chat_ui.to_user3.clicked.connect(self.send_to_user3)
        self.chat_ui.to_user4.clicked.connect(self.send_to_user4)
        self.chat_ui.to_user5.clicked.connect(self.send_to_user5)
        self.chat_ui.to_user6.clicked.connect(self.send_to_user6)
        # self.chat_ui.to_user7.clicked.connect(self.send_to_user7)
        # self.chat_ui.to_user8.clicked.connect(self.send_to_user8)
        self.mainWindow.setGeometry(QtCore.QRect(500, 20,754, 595))
        

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def btn_connect_clicked(self,myid):
        nickname = myid
        host = "118.217.168.174" #localhost
        port = 9090
        try:
            port = int(port)
        except Exception as e:
            error = "Invalid port number \n'{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Port Number Error", error)
        
        if len(nickname) < 1:
            nickname = socket.gethostname()
 
        if self.connect(host, port, nickname):
            self.chatWidget.setVisible(True)
            self.chat_ui.myname.setText(nickname)
            self.recv_thread = ReceiveThread(self.tcp_client)
            self.recv_thread.signal.connect(self.show_message)
            self.recv_thread.start()
            
            print("[INFO] recv thread started")
            
            

            

        
            




        



    def show_message(self, message): ## 서버로부터 받은 메시지를 구분하는곳
        global VotePopup
        
        if self.chat_ui.to_user1.text() == "사망":
            self.chat_ui.to_user1.setDisabled(True)
        if self.chat_ui.to_user2.text() == "사망":
            self.chat_ui.to_user2.setDisabled(True)
        if self.chat_ui.to_user3.text() == "사망":
            self.chat_ui.to_user3.setDisabled(True)
        if self.chat_ui.to_user4.text() == "사망":
            self.chat_ui.to_user4.setDisabled(True)
        if self.chat_ui.to_user5.text() == "사망":
            self.chat_ui.to_user5.setDisabled(True)
        if self.chat_ui.to_user6.text() == "사망":
            self.chat_ui.to_user6.setDisabled(True) 

        if message[-2]=="!": # 마피아팀은 [-2] == !
            if message[-1]=="@": #마피아1은 [-1] == @
                self.chat_ui.myjob_image.setText("마피아")
                message = message[0:-2]
                self.chat_ui.textBrowser.append(message)
                
            
        elif message[-2]=="@": # 시민팀은 [-2] == @
            if message[-1]=="!": # 경찰은 [-1] == !
                self.chat_ui.myjob_image.setText("경찰")
                message = message[0:-2]
                self.chat_ui.textBrowser.append(message)
            
            if message[-1]=="@": # 의사는 @
                self.chat_ui.myjob_image.setText("의사")
                message = message[0:-2]
                self.chat_ui.textBrowser.append(message)
            if message[-1]=="#": # #이건 그냥 시민
                self.chat_ui.myjob_image.setText("시민")
                message = message[0:-2]
                self.chat_ui.textBrowser.append(message)
            
        
                
        
        elif message[-2]=="#": # 타이머,시간은 [-2]== #
            if message[-1]=="!": # 타이머는 [-1]== ! 
                message = message[:-2] 
                self.chat_ui.Timer.setText(message)
            
            if message[-1]=="@": # Date은 [-1] == @
                    message = message[:-2]
                    self.chat_ui.Date.setText(message)
        elif message[-2]=="*":  ## 버튼세팅
            if message[-1]=="!":## 버튼에 각각 유저이름 새기기

                UserBtnList=[]
               
                while message!="":
                    findcode = message.find("*!",0,)
                    BtnName=message[0:findcode]
                    UserBtnList.append(BtnName)
                    message=message[findcode+2:]
                
                self.chat_ui.to_user1.setText(UserBtnList[0])
                self.chat_ui.to_user2.setText(UserBtnList[1])
                self.chat_ui.to_user3.setText(UserBtnList[2])
                self.chat_ui.to_user4.setText(UserBtnList[3])
                self.chat_ui.to_user5.setText(UserBtnList[4])
                self.chat_ui.to_user6.setText(UserBtnList[5])
            elif message[-1]=="`":
                    UserDieList=[]
                    while message!="":
                        findcode = message.find("*`",0,)
                        BtnName=message[0:findcode]
                        UserDieList.append(BtnName)
                        print("죽은자명단" + UserDieList[0])
                        message=message[findcode+2:]
                    if self.chat_ui.to_user1.text() in UserDieList:
                        print("1번 소유자" + self.chat_ui.to_user1.text())
                        self.chat_ui.to_user1.setText("사망")
                    elif self.chat_ui.to_user2.text() in UserDieList:
                        self.chat_ui.to_user2.setText("사망")
                    elif self.chat_ui.to_user3.text() in UserDieList:
                        self.chat_ui.to_user3.setText("사망")
                    elif self.chat_ui.to_user4.text() in UserDieList:
                        self.chat_ui.to_user4.setText("사망")
                    elif self.chat_ui.to_user5.text() in UserDieList:
                        self.chat_ui.to_user5.setText("사망")
                    elif self.chat_ui.to_user6.text() in UserDieList:
                        self.chat_ui.to_user6.setText("사망")

            
                
                
            elif message[-1]=="@": # 특정시간대에 채팅 X  지목 O
                self.chat_ui.inputbutton.setDisabled(True)
                self.chat_ui.textEdit.setDisabled(True)
                self.chat_ui.to_user1.setDisabled(False)
                self.chat_ui.to_user2.setDisabled(False)
                self.chat_ui.to_user3.setDisabled(False)
                self.chat_ui.to_user4.setDisabled(False)
                self.chat_ui.to_user5.setDisabled(False)
                self.chat_ui.to_user6.setDisabled(False)
               
                
            elif message[-1]=="#": # 특정시간대 채팅 O 지목 X
                self.chat_ui.inputbutton.setDisabled(False)
                self.chat_ui.textEdit.setDisabled(False)
                self.chat_ui.to_user1.setDisabled(True)
                self.chat_ui.to_user2.setDisabled(True)
                self.chat_ui.to_user3.setDisabled(True)
                self.chat_ui.to_user4.setDisabled(True)
                self.chat_ui.to_user5.setDisabled(True)
                self.chat_ui.to_user6.setDisabled(True)
               

            elif message[-1]=="$": # 특정시간대 채팅X 지목X
                self.chat_ui.inputbutton.setDisabled(True)
                self.chat_ui.textEdit.setDisabled(True)
                self.chat_ui.to_user1.setDisabled(True)
                self.chat_ui.to_user2.setDisabled(True)
                self.chat_ui.to_user3.setDisabled(True)
                self.chat_ui.to_user4.setDisabled(True)
                self.chat_ui.to_user5.setDisabled(True)
                self.chat_ui.to_user6.setDisabled(True)
                

            elif message[-1]=="%": # 특정시간대 채팅O 지목O >>마피아가 밤일때
                self.chat_ui.inputbutton.setDisabled(False)
                self.chat_ui.textEdit.setDisabled(False)
                self.chat_ui.to_user1.setDisabled(False)
                self.chat_ui.to_user2.setDisabled(False)
                self.chat_ui.to_user3.setDisabled(False)
                self.chat_ui.to_user4.setDisabled(False)
                self.chat_ui.to_user5.setDisabled(False)
                self.chat_ui.to_user6.setDisabled(False)
                
            elif message[-1]=="*":
                import tkinter.messagebox
                popvote = tkinter.messagebox.askyesno('투표창','찬성하시겠습니까?')
                if popvote == True:
                    self.chat_ui.textEdit.setText('/Y')
                    self.send_message()
                    
                else:
                    self.chat_ui.textEdit.setText('/N')
                    self.send_message()
            

        elif message[-2]=="%" or message[-2]=="^": # 이거 유저버튼클릭하면 서버로 유저버튼 넘어가는데 되돌아오는거 방지하기위해 막음
                pass
        


        
        else: # 일반 채팅일경우 textbroswer로 모두에게 보여줌
            self.chat_ui.textBrowser.append(message)
            

        

    def connect(self, host, port, nickname):

        try:
            self.tcp_client.connect((host, port))
            self.tcp_client.send(nickname.encode())

            print("[INFO] Connected to server")

            return True
        except Exception as e:
            error = "Unable to connect to server \n'{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Connection Error", error)
            
            
            return False
        

   
    


    def send_to_user1(self):
        message = self.chat_ui.to_user1.text()
        message = message+"%!"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+ message[0:-2]+"] 지목했습니다."
        self.chat_ui.textBrowser.append(message)
        
    def send_to_user2(self):
        message = self.chat_ui.to_user2.text()
        message = message+"%@"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+message[0:-2]+"] 지목했습니다."    
        self.chat_ui.textBrowser.append(message)
    def send_to_user3(self):
        message = self.chat_ui.to_user3.text()
        message = message+"%#"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+message[0:-2]+"] 지목했습니다."    
        self.chat_ui.textBrowser.append(message)

    def send_to_user4(self):
        message = self.chat_ui.to_user4.text()
        message = message+"%$"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+message[0:-2]+"] 지목했습니다."    
        self.chat_ui.textBrowser.append(message)

    def send_to_user5(self):
        message = self.chat_ui.to_user5.text()
        message = message+"%^"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+message[0:-2]+"] 지목했습니다."    
        self.chat_ui.textBrowser.append(message)

    def send_to_user6(self):
        message = self.chat_ui.to_user6.text()
        message = message+"%&"
        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        message = "["+message[0:-2]+"] 지목했습니다."
        self.chat_ui.textBrowser.append(message)


    def send_message(self):
        message = self.chat_ui.textEdit.text()
        self.chat_ui.textBrowser.append("Me:"+message)
       

        print("sent: " + message) #서버창에서 확인

        try:
            self.tcp_client.send(message.encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)
        self.chat_ui.textEdit.clear()


    def show_error(self, error_type, message):
        errorDialog = QtWidgets.QMessageBox()
        errorDialog.setText(message)
        errorDialog.setWindowTitle(error_type)
        errorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        errorDialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    c = Client()
    sys.exit(app.exec())