# from PySide6 import QtCore, QtWidgets
# import PySide6.QtGui
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtWidgets import QWidget
# from ui.ui_test import Ui_Test
# # from ui.ui_second_window import Ui_Second_Window
# from ui.ui_third_window import Ui_Third_Window
# from tr.tr_0424 import Tr_0424

# # from balance_window import Second_Window

# from tr.tr_master import Tr_master
# # from tr.s3_real import XReal_S3_

# import win32com.client #이베스트 관련
# import pythoncom #이베스트 관련



# loader=QUiLoader()

# #class Test(QWidget,Ui_Test)
# class Test(QtCore.QObject):
#     #print('싱글톤 생성: TEST')

#     def __init__(self,XReal_S3_,set_shut_down_flag):
#         super().__init__()
#         # self.setupUi(self)
#         self.ui=loader.load('./ui/test.ui',None)
#         self.ui.setWindowTitle("Xing Api Client By dev")

#         # self.go_to_2.clicked.connect(lambda:self.set_the_stock_code('second'))
#         self.ui.to_balance_page.clicked.connect(lambda:self.open_new_window('second'))
#         # self.go_to_2.clicked.connect(self.calling_master)
#         # self.ui.go_to_3.clicked.connect(self.start_s3_real)
#         # self.ui.summer.clicked.connect(self.call_summer)
#         # self.login_label.clicked.connect(self.do_action)
#         # self.ui.stock_code_label.clicked.connect(self.do_action)

#         self.XReal_S3_=XReal_S3_
#         self.set_shut_down_flag=set_shut_down_flag
#         # self.tr_0424=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_0424)#계좌티알
#         # self.tr_0424.get_account(self)

#     def show(self):
#         self.ui.show()


#     def closeEvent(self, event):
#         self.set_shut_down_flag()
#         # return super().closeEvent(event)



#     def open_new_window(self,type):

#         if type=="second":
#             # self.window=QtWidgets.QMainWindow()
#             # self.ui=Ui_Second_Window()
#             # self.ui.setupUi(self.window)
#             # self.second_window=Second_Window()
#             # self.window.setWindowTitle('열려라!!!!!!!!!!!!!!!!!!!')
#             self.second_window.show()
#         else:
#             self.window=QtWidgets.QMainWindow()
#             self.ui=Ui_Third_Window()
#             self.ui.setupUi(self.window)
#             self.window.setWindowTitle('열려라!!!!!!!!!!!!!!!!!!!')
#             self.window.show()


#     def get_master(self):
#         query=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_master)

#         query.single_request()
#         while Tr_master.query_state == False:
#             pythoncom.PumpWaitingMessages()



#     def start_s3_real(self):
#         xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", self.XReal_S3_)

#         xreal.start('005930')
#         while True:
#             pythoncom.PumpWaitingMessages()


#     def do_action(self):
#         #print('doing: ',self.name_line_edit.text())
#         #print('doing2: ',self.job_line_edit.text())
#         self.ui.login_label.setText('되냐?')

#     def set_the_text(self,the_thing):
#         #print('세팅한다: ',the_thing)
#         self.ui.login_label.setText(the_thing)

#     def set_the_stock_code(self,the_thing):
#         #print('세팅한다2: ',the_thing)
#         self.ui.stock_code_label.setText(the_thing)
