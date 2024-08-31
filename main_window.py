from PySide6 import QtCore, QtWidgets
import PySide6.QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QDialog, QMainWindow
from PySide6.QtCore import Qt, QEvent,QObject,SIGNAL,QFile
# from ui.ui_test import Ui_Test
# from ui.ui_second_window import Ui_Second_Window
# from ui.ui_third_window import Ui_Third_Window
from tr.tr_0424 import Tr_0424

# from balance_window import Balance_window
from order_window import Order_window
from search_window import Search_window

from tr.tr_master import Tr_master
# from tr.s3_real import XReal_S3_

# import win32com.client #이베스트 관련
# import pythoncom #이베스트 관련

from dotenv import load_dotenv
import os 

# load .env
load_dotenv()


loader=QUiLoader()



#class Test(QWidget,Ui_Test)
# QtCore.QObject
class Main_window(QMainWindow):

    # def __new__(self):
    #     if not hasattr(self,'instance'):
    #         #print('싱글톤 만듬 MAIN WINDOW')
    #         self.instance=super(Main_window,self).__new__(self)
    #     else:
    #         #print('이미 싱글톤 있음  MAIN WINDOW')
    #     return self.instance

    def __init__(self,session,balance_window):
        super().__init__()
        # self.setupUi(self)
        self.session=session
        self.balance_window=balance_window
        
        self.ui=loader.load('./ui/main-window.ui',None)

        if self.ui is None:
            return



        self.ui.setWindowTitle("Xing Api Client")

        

        # self.go_to_2.clicked.connect(lambda:self.set_the_stock_code('second'))
        self.ui.to_balance_page.clicked.connect(lambda:self.open_new_window('balance'))
        self.ui.to_order_page.clicked.connect(lambda:self.open_new_window('order'))
        self.ui.to_search_page.clicked.connect(lambda:self.open_new_window('search'))

        self.ui.to_balance_page.hide()
        self.ui.to_order_page.hide()
        self.ui.to_search_page.hide()


        self.ui.login_button.clicked.connect(lambda:self.shoot_login())
        self.ui.login_button.show()

        self.ui.closeEvent=self.closeEvent

        self.ui.status_label.setStyleSheet("color: red;")

        self.account=''#계좌번호


        # self.go_to_2.clicked.connect(self.calling_master)
        # self.ui.go_to_3.clicked.connect(self.start_s3_real)
        # self.ui.summer.clicked.connect(self.call_summer)
        # self.login_label.clicked.connect(self.do_action)
        # self.ui.stock_code_label.clicked.connect(self.do_action)

        # self.XReal_S3_=XReal_S3_
        # self.tr_0424=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_0424)#계좌티알
        # self.tr_0424.get_account(self)


        # self.worker = Worker()
        # self.worker.start()

    def handle_close(self):
        #print('CLOSE!@!@')
        pass

    def set_status_label(self, string):
        
        self.ui.status_label.setText(string)

    def set_session(self,session):
        self.session=session


    # class XASessionEvents:
        
    #     def __init__(self,parent):
    #         session=win32com.client.DispatchWithEvents("XA_Session.XASession",self)

    #         url=os.environ.get('URL')
    #         port=os.environ.get('PORT')
    #         cert=os.environ.get('CERT')

    #         result=session.ConnectServer(url,port)
    #         parent.set_session(session)
    #         self.parent=parent
    #         #print("result: ",result)

    #     def OnLogin(self, code, msg):
    #         # time.sleep(5)
    #         #print('로그인 결과@@: ',msg)
    #         self.parent.possible()
    #         # query.single_request()
    #     def OnDisconnect(self, code, msg):
    #         pass

    





    def show(self):
        self.ui.show()

    def show_buttons(self):
        #print('ssap possible')
        self.ui.to_balance_page.show()
        self.ui.to_order_page.show()
        self.ui.to_search_page.show()
    

    def shoot_login(self):
        #print('@@shoot_login@@')
        server_type=os.environ.get('SERVER_TYPE')

        cert=os.environ.get('CERT')

        id=self.ui.login_id_input.text()
        pw=self.ui.login_pw_input.text()

        # print('login_cnt: ',self.session.login_cnt)

        if self.session.login_cnt >5:
            return

        self.session.Login(id,pw,cert,server_type,0)
        os.environ['PW'] = pw
        os.environ['ID'] = id


    # def closeEvent(self, event):
    #     #print('asdasdas')
    #     self.set_shut_down_flag()
    #     return super().closeEvent(event)



    def open_new_window(self,type):

        #print('ACCOUNT NO: ',self.session.account)
        os.environ['ACCOUNT'] = self.session.account
        #print('ACCOUNT NO2: ',os.environ.get('ACCOUNT'))

        if type=="balance":
            # self.window=QtWidgets.QMainWindow()
            # self.ui=Ui_Second_Window()
            # self.ui.setupUi(self.window)
            # self.balance_window=self.balance_window
            self.balance_window.show()
        elif type=='order':
            self.order_window=Order_window()
            self.order_window.show()
        elif type=='search':
            self.search_window=Search_window()
            self.search_window.showMe()



    def get_master(self):
        query=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_master)

        master_res=query.single_request()
        print('master_res: ',master_res)

        if master_res is not None:

            while Tr_master.query_state == False:
                pythoncom.PumpWaitingMessages()


    # def start_s3_real(self):
    #     xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", self.XReal_S3_)

    #     xreal.start('005930')
    #     while True:
    #         pythoncom.PumpWaitingMessages()


    def do_action(self):
        #print('doing: ',self.name_line_edit.text())
        #print('doing2: ',self.job_line_edit.text())
        pass

    def set_the_text(self,the_thing):
        self.ui.login_label.setText(the_thing)

    def set_the_stock_code(self,the_thing):
        self.ui.stock_code_label.setText(the_thing)



# STAND_BY = 0
# RECEIVED = 1

# class XASessionEvents:
#     login_state = STAND_BY    

#     # def __init__(self):


#     #     # self.main_window=Main_window()
#     #     # self.main_window.show()
#     #     session=win32com.client.DispatchWithEvents("XA_Session.XASession",self)
#     #     session.init_main_window()

#     #     url=os.environ.get('URL')
#     #     port=os.environ.get('PORT')
#     #     cert=os.environ.get('CERT')

#     #     result=session.ConnectServer(url,port)
#     #     #print("result: ",result)
        


#     def init_main_window(self):
#         self.main_window=Main_window()
#         self.main_window.show()



#     def OnLogin(self, code, msg):
#         XASessionEvents.login_state = RECEIVED
#         # time.sleep(5)
#         #print('로그인 결과@@: ',msg)
#         self.main_window.possible()
#         # query.single_request()
#     def OnDisconnect(self, code, msg):
#         pass


# session=win32com.client.DispatchWithEvents("XA_Session.XASession",XASessionEvents)
# session.init_main_window()

# url=os.environ.get('URL')
# port=os.environ.get('PORT')
# cert=os.environ.get('CERT')

# result=session.ConnectServer(url,port)
# #print("result: ",result)