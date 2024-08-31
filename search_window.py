from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader
# from PySide2.QtWidgets import QTableWidgetItem, QFileDialog
from PySide6.QtWidgets import *
from PySide6.QtWidgets import   QDialog
from PySide6.QtCore import QEvent, QObject, SIGNAL,QFile
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox)

import sys
# from .ui.ui_test import Ui_Test
# from ui.ui_test import Ui_Test
# from ui.ui_second_window import Ui_Second_Window
from tr.tr_0424 import Tr_0424
from tr.tr_1857 import Tr_1857
import win32com.client #이베스트 관련
import pythoncom #이베스트 관련
import os
from ui.ui_search_window import Ui_Form

# app=QApplication(sys.argv)

class MyEventFilter(QObject):
    def eventFilter(self, watched, event):
        if event.type() == QEvent.Close:
            #print("Event filter: Window is being closed.")
            # Add your custom logic here if needed
            pass
        return super().eventFilter(watched, event)

loader=QUiLoader()
#QWidget
class Search_window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        # self=loader.load('./ui/search-window.ui',None)
        self.setupUi(self)




        # loader = QUiLoader()
        # ui_file = QFile('./ui/search-window.ui')
        # ui_file.open(QFile.ReadOnly)
        # self = loader.load(ui_file)
        # ui_file.close()

        # event_filter = MyEventFilter()
        # self.installEventFilter(event_filter)

        
        
        #print('자기소개 SEARCH_WINDOW: ',dir(self))
        # uic.loadUi('./ui/search-window.ui', self)
        self.setWindowTitle("종목 검색")        
        self.tr_1857=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_1857)
        self.tr_1857.init_callbacks(self.set_value_on_table,self.insert_row_on_stocks_table)


        # self.balance_table.setItem(0,1,QTableWidgetItem(str(1)))
        # self.balance_stocks_table.setColumnWidth(7,130)
        # self.balance_table.setItem(0,0,QTableWidgetItem(str(2)))
        self.file_select_button.clicked.connect(self.selectFile)
        # self.end_btn.clicked.connect(self.handle_close_event)
        # self.destroyed.connect(self.handle_close_event)

        self.closeEvent=self.handle_close_event
        # self.installEventFilter(self)
        #print('init search window')

    # def __init__(self, parent=None):
    #     super().__init__(parent)

    #     # Load the UI file
    #     loader = QUiLoader()
    #     ui_file = QFile('./ui/search-window.ui')  # Replace with your UI file path
    #     ui_file.open(QFile.ReadOnly)
    #     self = loader.load(ui_file)
    #     ui_file.close()

    #     # Set up the UI and connections
    #     self.setCentralWidget(self)
    #     self.setWindowTitle("Search Window")
        
    #     # Connect the close event to a custom handler
    #     self.closeEvent = self.handle_close_event

    def closeEvent(self, event) -> None:
        #print('a')
        self.tr_1857.manually_stop()
        return super().closeEvent(event)

    def handle_close_event(self, event):
        # Perform desired action when the window is closed
        self.tr_1857.manually_stop()
        #print("Search window closed!")
        self.close()
        # super().closeEvent(event)

    def showMe(self):
        self.show()
        # app.exec_()

    # def closeEvent(self, event):
    #     #print('IM CLOSING!!!@!')
    #     super().closeEvent(event)

    def selectFile(self):
        the_path=os.environ.get('ROOT_FILE_PATH')+"\\ACF"
        fname = QFileDialog.getOpenFileName(
            parent=self,
            caption='ACF 파일 선택',
            dir=the_path)
        
        #print('the_acf: ',fname[0])
        self.tr_1857.go_search(fname[0])


    def set_value_on_table(self,column_num,row_num,value):
        # #print('set_value_on_table: ',column_num)
        # #print('set_value_on_table2: ',value)
        self.search_stocks_table.setItem(row_num,column_num,QTableWidgetItem(str(value)))

    
    def insert_row_on_stocks_table(self):
        rowPosition=self.search_stocks_table.rowCount()
        # #print('테이블 개수: ',rowPosition)
        self.search_stocks_table.insertRow(rowPosition)
        return rowPosition


