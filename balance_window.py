from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem
import sys
# from .ui.ui_test import Ui_Test
# from ui.ui_test import Ui_Test
# from ui.ui_second_window import Ui_Second_Window
from tr.tr_0424 import Tr_0424
# from tr.tr_pending import Tr_pending
import win32com.client #이베스트 관련
import pythoncom #이베스트 관련

# app=QApplication(sys.argv)

loader=QUiLoader()

class Balance_window(QtCore.QObject):

    # class Worker(QtCore.QThread):
    #     # def __init__(self,tr_0424):
    #     #     self.tr_0424=tr_0424

    #     def call(self,tr_0424):
    #         self.tr_0424=tr_0424

    #     def run(self):
    #         while True:
    #             #print("안녕하세요")
    #             self.sleep(2)
    #             self.tr_0424.get_account(Balance_window)

            

    def __init__(self,tr_pending):
        super().__init__()
        self.ui=loader.load('./ui/balance-window.ui',None)
        
        if self.ui is None:
            return
        
        self.ui.setWindowTitle("잔고 조회")
        self.tr_0424=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_0424)#계좌티알
        self.tr_pending=tr_pending#미체결


        # self.ui.balance_table.setItem(0,1,QTableWidgetItem(str(1)))
        # self.ui.balance_table.setItem(0,0,QTableWidgetItem(str(2)))
        # self.login_label.clicked.connect(self.do_action)
        self.ui.balance_stocks_table.setColumnWidth(7,130)
        self.ui.waiting_stocks_table.setColumnWidth(7,130)
        self.ui.balance_table.hide()
        self.tr_0424.get_account()
        # self.tr_0424.init_draw_balance_table(self)
        # self.tr_0424.callback_from_balance_window(self.insert_row_on_stocks_table,self.set_value_on_stocks_table)

        self.ui.pending_reselect.clicked.connect(self.pending_reselect)
        self.ui.pending_reselect.hide()
        # self.ui.testBtn2.clicked.connect(self.testBtn2)
        
    def pending_reselect(self):
        # self.ui.waiting_stocks_table.removeRow(1)
        # self.remove_row_on_pending_table(2)
        self.tr_pending.get_pending(self)

        
    # def testBtn2(self):
    #     print('testBtn testBtntestBtn testBtn')
    #     # self.ui.waiting_stocks_table.removeRow(1)
    #     self.remove_row_on_pending_table(0)
    #     # self.tr_0424.get_account()
        
    def clear_table(self):
        self.ui.balance_table.clear()

    def remove_row_on_stocks_table(self,index):
        self.ui.balance_stocks_table.removeRow(index)

        
    def remove_row_on_pending_table(self,index):
        # print('왜 안 처지우세요? ', index)
        self.ui.waiting_stocks_table.removeRow(index)


    def show(self):
        self.ui.show()
        # app.exec_()



    def do_action(self):
        #print('doing: ',self.name_line_edit.text())
        #print('doing2: ',self.job_line_edit.text())
        self.login_label.setText('되냐?')

    def set_value_on_table(self,column_num,value):
        # #print('set_value_on_table: ',column_num)
        # #print('set_value_on_table2: ',value)
        self.ui.balance_table.setItem(0,column_num,QTableWidgetItem(str(value)))

    
    def insert_row_on_stocks_table(self):
        #print('call_back_test@@@@@@@@@@#######')

        rowPosition=self.ui.balance_stocks_table.rowCount()
        self.ui.balance_stocks_table.insertRow(rowPosition)

    def insert_row_on_pending_table(self):
        rowPosition=self.ui.waiting_stocks_table.rowCount()
        self.ui.waiting_stocks_table.insertRow(rowPosition)

    
    def set_value_on_pending_table(self,column_num,row_num,value):
        # #print('set_value_on_table: ',column_num)
        # #print('set_value_on_table2: ',value)

        item =QTableWidgetItem(str(value))
        item.setTextAlignment(int(QtCore.Qt.AlignCenter))

        self.ui.waiting_stocks_table.setItem(row_num,column_num,item)


    def call_back_test(self):
        #print('call_back_test@@@@@@@@@@#######')
        pass

    
    def set_value_on_stocks_table(self,column_num,row_num,value):
        # #print('set_value_on_table: ',column_num)
        # #print('set_value_on_table2: ',value)

        item =QTableWidgetItem(str(value))
        item.setTextAlignment(int(QtCore.Qt.AlignCenter))
        
        self.ui.balance_stocks_table.setItem(row_num,column_num,item)

