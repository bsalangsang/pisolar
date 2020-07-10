from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget
from mdlFunction import modFunc
from datetime import datetime

import sqlExec
import base64
import random

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

shsCode = ""
machineCode = ""


class UI_trnPayment(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_trnPayment, self).__init__()
        uic.loadUi("trnPaymentUIDesign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("UI_trnPayment: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.onLoadEvent()
    
    
    def onLoadEvent(self):
      
        self.fillComboData() # LEDGER
        self.cboType.addItem(" ")
        self.cboType.addItem("DEBIT")
        self.cboType.addItem("CREDIT")
        self.dtSlipDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.txtDef()

    def saveTrans(self):
        try:
            g = datetime.date(self.dtSlipDate.text())
        except Exception as e:
            QMessageBox.critical(self,"ATTENTION!!!",getattr(e, 'message', str(e)))
             
              #date_str = datetime.strptime(dateNow,"%m/%d/%y")
        #print(type(date_str))

        #print("{:%d %b, %Y}".format(dateNow))

        #rint(dateNow.format("yyyy-MM-dd"))
        pass

    def fillComboData(self):
        fetchValues = sqlFunc.fetchSql("SELECT DISTINCT " + 
                                      "man_customers.customerCode AS 'CODE', " + 
                                      "CONCAT(fName, ' ',mName,' ',lName) AS 'CUSTOMER_' " + 
                                      "FROM man_customers " +
                                     "LEFT JOIN man_shs ON man_shs.customerNo = man_customers.customerNo " +
                                      "WHERE man_customers.isActive = 'Y'",
                                      "True")

        self.cboLgrCus.addItem(" ")
        for row in fetchValues:
            self.cboLgrCus.addItem(str(row[1]), row[0])
       
        print("fillComboDataLedger is working!!")
    
    @QtCore.pyqtSlot()
    def fillComboDataPassVal(self):
        fetchValues = sqlFunc.fetchSql("SELECT " + 
                                     "shsCode AS 'NO.', " + 
                                     "shsName AS 'MACHINE_' " + 
                                     "FROM man_shs "
                                     "WHERE customerCode = '"+ str(self.cboLgrCus.currentData()) +"' "
                                     "AND isActive = 'Y'",
                                     "True")
        
        self.cboLgrMach.clear()
        #objComboBox.clear
        for row in fetchValues:
            self.cboLgrMach.addItem(str(row[1]), row[0])
            #objComboBox.addItem(str(row[1]), row[0])
    
    def txtDef(self):

        self.txtSlipNo.setText("")
        self.txtSlipNo.setText(modFunc.getNextPkey("","ldgrNo","ldgr_shs",6,True,"PTN"))
        self.cboLgrCus.selectedIndex = 0
        self.cboLgrMach.selectedIndex = 0
        self.txtRefNo.setText("")
        self.cboType.selectedIndex = 0
        self.txtAmount.setText("")
      

    def saveLedgerRecord(self):
        btnReply = QMessageBox.question(self, 'Attention', "Do you Want to Save this Record?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnReply == QMessageBox.Yes:

            #==================================================
            # PREP VALUES
            #==================================================

            if self.cboType.currentText() == "DEBIT":
                tType = "1"
                tRemarks = "DEBITTED TO " + self.cboLgrCus.currentText()
            else:
                tType = "2"
                tRemarks = "CREDITTED TO " + self.cboLgrCus.currentText()
            
            tShsCode = self.cboLgrMach.currentData()
            tSlipDate = self.dtSlipDate.text()
            tCusCode = self.cboLgrCus.currentData()
            tRefNo = self.txtRefNo.text()
            iBalance =  modFunc.getNewBalance("ldgr_shs","shsNo",tShsCode,tType,self.txtAmount.text())
            
            #==================================================
            # SAVE RECORD
            #==================================================

            tTable = "ldgr_shs"
            tFields = "ldgrNo,ldgrDate,ldgrTypeNo,refNo,shsNo,shsCode,amount,balance,remarks"
            tString = "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tValues = (self.txtSlipNo.text(),
                       tSlipDate,
                       tType,
                       tRefNo,
                       tShsCode,
                       tShsCode,
                       self.txtAmount.text(),
                       iBalance,
                       tRemarks)
                                         
            itr = sqlFunc.execSql("insert",tTable,tFields,tString,tValues,"customerNo")
            if itr == "success":
                QMessageBox.information(self,"Attention!","Successfully Saved")
                self.txtDef()
                print("SAVE Function Are Working!!!") #for Debugging purposes
            else:
                QMessageBox.critical(self,"Attention!","ERROR!")      
                self.cboCustomer.selectedIndex = 0
                self.show()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_trnPayment()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())