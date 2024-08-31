from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
import sys
# from .ui.ui_test import Ui_Test
# from ui.ui_test import Ui_Test
# from ui.ui_second_window import Ui_Second_Window
from tr.tr_master import Tr_master
from tr.tr_order import Tr_order
from tr.tr_redo_order import Tr_redo_order
from tr.tr_cancel_order import Tr_cancel_order
from tr.tr_0424 import Tr_0424
from tr.tr_sc0 import Tr_sc0
# from tr.tr_sc1 import Tr_sc1
import win32com.client #이베스트 관련
import pythoncom #이베스트 관련
tr_master=Tr_master()
tr_0424=Tr_0424()

# app=QApplication(sys.argv)

loader=QUiLoader()

class Order_window(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.ui=loader.load('./ui/order-window.ui',None)

        
        if self.ui is None:
            return

        self.ui.setWindowTitle("주문")
        self.orderType='normal'
        self.orderStockCode=''
        self.orderStyle='ask'
        self.is_all_qty=True

        self.query_order=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_order)
        self.query_order.init_set_text(self.set_status_label)
        self.query_order_redo=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_redo_order)
        self.query_order_cancel=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",Tr_cancel_order)

        
        self.ui.order_tab_widget.currentChanged.connect(self.orderTabChanged)
        
        self.ui.stock_input.textChanged.connect(lambda:self.onChangeStockInput(1))
        self.ui.stock_input_3.textChanged.connect(lambda:self.onChangeStockInput(2))
        
        self.ui.stock_input_4.textChanged.connect(lambda:self.onChangeStockInput(3))
        self.ui.stock_input_5.textChanged.connect(lambda:self.onChangeStockInput(4))
        self.ui.normal_radio.setChecked(True)
        self.ui.normal_radio_2.setChecked(True)
        self.ui.all_qty_radio.setChecked(True)
        self.ui.all_qty_radio.hide()
        self.ui.some_qty_radio.hide()
        self.ui.all_qty_radio_2.hide()
        self.ui.some_qty_radio_2.hide()
        self.ui.normal_radio.clicked.connect(self.radioSelected)
        self.ui.normal_radio_2.clicked.connect(self.radioSelected_2)
        self.ui.market_radio.clicked.connect(self.radioSelected)
        self.ui.market_radio_2.clicked.connect(self.radioSelected_2)
        self.ui.order_btn.clicked.connect(self.shootOrder)
        self.ui.order_btn_2.clicked.connect(self.shootOrder)
        self.ui.order_btn_3.clicked.connect(self.shootOrder)
        self.ui.order_btn_4.clicked.connect(self.shootOrder)

        
        self.ui.all_qty_radio.clicked.connect(self.qty_radioSelected)
        self.ui.some_qty_radio.clicked.connect(self.qty_radioSelected)


        self.ui.status_label.setText('')
        self.ui.status_label.setStyleSheet("color: red;")

        

        # #print('the_balance: ',tr_0424.the_balance)
        # self.submit_btn.clicked.connect(self.do_action)
        # self.login_label.clicked.connect(self.do_action)

    
    def set_status_label(self, string):
        
        self.ui.status_label.setText(string)

    def orderTabChanged(self,tabIndex):
        #print('tabIndex: ',tabIndex)
        if tabIndex==0:
            self.orderStyle='ask'
        elif tabIndex==1:
            self.orderStyle='bid'
        elif tabIndex==2:
            self.orderStyle='redo'
        elif tabIndex==3:
            self.orderStyle='cancel'

        
        self.ui.normal_radio.setChecked(True)
        self.ui.normal_radio_2.setChecked(True)
        self.orderType='normal'
        res_1=self.onChangeStockInput(1)
        res_2=self.onChangeStockInput(2)
        res_3=self.onChangeStockInput(3)
        res_4=self.onChangeStockInput(4)


        if (res_1 is not None and
            res_2 is not None and
            res_3 is not None and
            res_4 is not None):

            self.ui.stock_input.setText('')
            self.ui.stock_input_3.setText('')
            self.ui.stock_input_4.setText('')
            self.ui.stock_input_5.setText('')


    
    def onChangeStockInput(self,num):
        
        theInput=self.ui.stock_input.text()

        if num==1:
            theInput=self.ui.stock_input.text()
        elif num==2:
            theInput=self.ui.stock_input_3.text()
        elif num==3:
            theInput=self.ui.stock_input_4.text()
        elif num==4:
            theInput=self.ui.stock_input_5.text()

        
        theDict=tr_master.master_dict.get(theInput,None)
        #print('theDict: ',theDict)

        if theDict != None:
            stockName=theDict['hname']
            self.ui.stock_name_label.setText(stockName)
            self.ui.stock_name_label_2.setText(stockName)
            self.ui.stock_name_label_3.setText(stockName)
            self.ui.stock_name_label_4.setText(stockName)
            self.orderStockCode=theDict['shcode']
        else:
            self.ui.stock_name_label.setText('')
            self.ui.stock_name_label_2.setText('')
            self.ui.stock_name_label_3.setText('')
            self.ui.stock_name_label_4.setText('')

        return 1

    
    
    def onChangeStockInput_3(self):
        theInput=self.ui.stock_input_3.text()
        
        theDict=tr_master.master_dict.get(theInput,None)
        #print('theDict: ',theDict)

        if theDict != None:
            stockName=theDict['hname']
            self.ui.stock_name_label.setText(stockName)
            self.orderStockCode=theDict['shcode']
        else:
            self.ui.stock_name_label.setText('')

    
    
    
    def onChangeStockInput_4(self):
        theInput=self.ui.stock_input_4.text()
        
        theDict=tr_master.master_dict.get(theInput,None)
        #print('theDict: ',theDict)

        if theDict != None:
            stockName=theDict['hname']
            self.ui.stock_name_label.setText(stockName)
            self.orderStockCode=theDict['shcode']
        else:
            self.ui.stock_name_label.setText('')


    
    
    def onChangeStockInput_5(self):
        theInput=self.ui.stock_input_5.text()
        
        theDict=tr_master.master_dict.get(theInput,None)
        #print('theDict: ',theDict)

        if theDict != None:
            stockName=theDict['hname']
            self.ui.stock_name_label.setText(stockName)
            self.orderStockCode=theDict['shcode']
        else:
            self.ui.stock_name_label.setText('')

            
    def onChangeOrderQtInput(self):
        theInput=self.ui.order_qt_input.text()
        

            
    def onChangeOrderWonInput(self):
        theInput=self.ui.order_won_input.text()
        
    
    def qty_radioSelected(self):

        if self.ui.all_qty_radio.isChecked()==True:
            self.is_all_qty=True
        elif self.ui.some_qty_radio.isChecked()==True:
            self.is_all_qty=False

        #print('is_all_qty: ',self.is_all_qty)


    def radioSelected(self):
        #print('radioSelected: ',self.ui.normal_radio.isChecked())
        #print('radioSelected2: ',self.ui.market_radio.isChecked())

        if self.ui.normal_radio.isChecked()==True:
            self.orderType='normal'
        elif self.ui.market_radio.isChecked()==True:
            self.orderType='market'

        #print('orderType: ',self.orderType)


    def radioSelected_2(self):
        #print('radioSelected: ',self.ui.normal_radio.isChecked())
        #print('radioSelected2: ',self.ui.market_radio.isChecked())

        if self.ui.normal_radio_2.isChecked()==True:
            self.orderType='normal'
        elif self.ui.market_radio_2.isChecked()==True:
            self.orderType='market'

        #print('orderType: ',self.orderType)
    

    def show(self):
        self.ui.show()
        # app.exec_()

    def shootOrder(self):
        #print('orderStyle: ',self.orderStyle)

        if self.orderStyle=='ask':

            #print('stockInput: ',self.ui.stock_input.text())
            #print('orderType: ',self.orderType)
            #print('orderQtInput: ',self.ui.order_qt_input.text())
            #print('orderWonInput: ',self.ui.order_won_input.text())
            #print('orderStockCode: ',self.orderStockCode)
            #print('orderStyle: ',self.orderStyle)

            self.query_order.shoot_order(
                self.orderStockCode,
                self.ui.order_qt_input.text(),
                1,
                2,
                self.ui.order_won_input.text(),
                self.orderStyle,
                self.orderType
                )
            
            self.ui.status_label.setText('매도 주문 완료')
            self.ui.status_label.setStyleSheet("color: blue;")

        
        elif self.orderStyle=='bid':
            #print('stockInput: ',self.ui.stock_input_3.text())
            #print('orderType: ',self.orderType)
            #print('orderQtInput_2: ',self.ui.order_qt_input_2.text())
            #print('orderWonInput_2: ',self.ui.order_won_input_2.text())
            #print('orderStockCode: ',self.orderStockCode)
            #print('orderStyle: ',self.orderStyle)

            
            self.query_order.shoot_order(
                self.orderStockCode,
                self.ui.order_qt_input_2.text(),
                1,
                2,
                self.ui.order_won_input_2.text(),
                self.orderStyle,
                self.orderType
                )
            self.ui.status_label.setText('매수 주문 완료')
            self.ui.status_label.setStyleSheet("color: red;")

        elif self.orderStyle=='redo':
            #print('orgNoInput: ',self.ui.org_no_input.text())
            #print('stockInput: ',self.ui.stock_input_4.text())
            #print('orderType: ',self.orderType)

            #print('order_qt_input_3: ',self.ui.order_qt_input_3.text())
            #print('orderWonInput_3: ',self.ui.order_won_input_3.text())
            #print('orderStyle: ',self.orderStyle)
            #print('is_all_qty: ',self.is_all_qty)

            self.query_order_redo.shoot_order(
                self.orderStockCode,
                self.ui.order_qt_input_3.text(),
                1,
                2,
                self.ui.order_won_input_3.text(),
                self.orderStyle,
                self.orderType,
                self.ui.org_no_input.text(),
                )
            
            
            self.ui.status_label.setText('정정 주문 완료')
            self.ui.status_label.setStyleSheet("color: black;")
        
        elif self.orderStyle=='cancel':
            #print('orgNoInput: ',self.ui.org_no_input_2.text())
            #print('orderType: ',self.orderStyle)

            #print('order_qt_input_4: ',self.ui.order_qt_input_4.text())
            #print('orderStyle: ',self.orderStyle)
            
            self.query_order_cancel.shoot_order(
                self.orderStockCode,
                self.ui.order_qt_input_4.text(),
                1,
                2,
                3,
                self.orderStyle,
                self.orderType,
                self.ui.org_no_input_2.text(),
                )
            
            
            self.ui.status_label.setText('취소 주문 완료')
            self.ui.status_label.setStyleSheet("color: black;")

    def do_action(self):
        #print('doing: ',self.name_line_edit.text())
        #print('doing2: ',self.job_line_edit.text())
        self.login_label.setText('되냐?')

    def set_the_text(self,the_thing):
        #print('세팅한다: ',the_thing)
        self.login_label.setText(the_thing)
    def set_the_stock_code(self,the_thing):
        #print('세팅한다2: ',the_thing)
        self.stock_code_label.setText(the_thing)
