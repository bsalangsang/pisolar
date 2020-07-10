from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget

import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

class UI_trnLedger(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_trnLedger, self).__init__()
        uic.loadUi("ledgerUIDesign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("LEDGER: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.onLoadEvent()
      
        #self.cboLgrCus.currentTextChanged.connect(lambda : self.fillComboDataPassVal(self.cboLgrCus.currentData(),self.cboLgrMach))
        #self.cboLgrCus.currentTextChanged.connect(self.fillComboDataPassVa()l)
        #self.btnFetch.clicked.connect(lambda : self.fetchAcctRecord("LEDGER",self.cboLgrCus,self.cboLgrMach))
      
    def onLoadEvent(self):
      
        self.fillComboData() # LEDGER


    #=-----------------------------------------------------------------------------=
    # LEDGER
    #=-----------------------------------------------------------------------------=
    
    #def fetchAcctRecord(self, tTarget, cboCus, cboMach):
    def fetchAcctRecord(self):   
        print(self.cboLgrCus.currentData() + " " + self.cboLgrMach.currentData())
        fetchValues = sqlFunc.fetchSql("SELECT " + 
                                      "man_shs.shsCode AS 'CODE_', " + 
                                      "man_shs.shsName AS 'MACHINE_', " + 
                                      "man_shs.serialNo AS 'SERIAL_', " + 
                                      "man_shs.simNo AS 'SIM_NO', " + 
                                      "man_shs.firmwareVer AS 'FIRMWARE_', " + 
                                      "man_shs.softwareVer AS 'SOFTWARE_', " +
                                      " " +
                                      "man_customers.customerCode AS 'CODE_', " + 
                                      "CONCAT(man_customers.fName, ' ',man_customers.mName,' ',man_customers.lName) AS 'CUSTOMER_', " + 
                                      "man_customers.address AS 'ADDRESS_', " + 
                                      "CONCAT(man_customers.contact1, ' / ',man_customers.contact2) AS 'CONTACT_' " + 
                                      "FROM man_shs " +
                                      "LEFT JOIN man_customers ON man_customers.customerNo = man_shs.customerNo " +
                                      "WHERE man_shs.customerCode = '"+ str(self.cboLgrCus.currentData()) +"' "
                                      "AND man_shs.shsCode = '"+ str(self.cboLgrMach.currentData()) +"' "
                                      "AND man_shs.isActive = 'Y'",
                                      "False")
        row = ""
        for row in fetchValues:
            print(row)
        
           # self.txtLgrCusCode.setText(str(row[6]))
           # self.txtLgrCusName.setText(str(row[7]))
           # self.txtLgrShsCode.setText(str(row[0]))
           # self.txtLgrShsName.setText(str(row[1]))
           # self.fillLedgerRecord(str(self.cboLgrMach.currentData()))
        
    def fillLedgerRecord(self):
        
        fetchValues = sqlFunc.fetchSql("SELECT " + 
                                      "ldgr_shs.ldgrdate AS 'DATE_', " + 
                                      "ldgr_shs.ldgrNo AS 'ctrlNo', " + 
                                      "ldgr_shs.remarks AS 'REMARKS_', " +
                                      "IF(ldgr_shs.ldgrTypeNo='2', FORMAT(amount,2),'') AS 'credit', " + 
                                      "IF(ldgr_shs.ldgrTypeNo='1', FORMAT(amount,2),'') AS 'debit', " +
                                      "FORMAT(ldgr_shs.balance,2) AS 'balance', " +
                                      "IF(ldgr_shs.isActive='Y', 'ACTIVE', 'INACTIVE') AS 'status' " +
                                      "FROM ldgr_shs " +
                                      "LEFT JOIN man_shs ON man_shs.shsNo = ldgr_shs.shsNo " +
                                      "WHERE ldgr_shs.shsCode = '" + self.cboLgrMach.currentData() + "' "
                                      "AND ldgr_shs.isActive = 'Y'",
                                      "True")
        
        rowCount = 0
        self.tblLedger.setRowCount(0) #clear table list
        for row_number, row_data in enumerate(fetchValues):
            self.tblLedger.insertRow(row_number)
            rowCount = rowCount + row_number
            for column_number, data in enumerate(row_data):
                self.tblLedger.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.tblLedger.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tblLedger.resizeColumnsToContents()
      
    def getNewBalance(self, tTable, tColumn, tValue, tType, tAmount):

        fetchValues= sqlFunc.fetchSql("SELECT " + 
                                      "balance " +
                                      "FROM " + tTable + " " +
                                      "WHERE " + tColumn + "='" + tValue + "' " +
                                      "ORDER BY ctrlNo DESC LIMIT 0,1",
                                      "False"
                                       )

        cleanBalance = ""

        for lastBalance in fetchValues:
            try:
                cleanBalance = lastBalance[0]
            except:
                cleanBalance = 0

        newBalance = ""
        try:
            if tType == "1":
                newBalance = int(cleanBalance) - int(tAmount)
            else:
                newBalance = cleanBalance + tAmount
        except ValueError as ve:
            print(ve)

        #aaa = str(newBalance.replace('-',''))
        if int(newBalance) < 0:
            newBalance = newBalance / -1
        return newBalance

    #=-----------------------------------------------------------------------------=
    # GENERIC FUNCTION 
    #=-----------------------------------------------------------------------------=
    def getNextPkeyNo(self):
        fetchValues= sqlFunc.fetchSql("SELECT " + 
                                      "MAX(ldgrNo) " +
                                      "FROM ldgr_shs " ,
                                      "False"
                                       )

        for row in fetchValues:
            if row[0] == None:
                row = "1"
            else:
                row = int(row[0]) + 1
        return row
    
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
        #for x in str(fetchValues):
        #    self.cboCustomer.addItems(x)

    @QtCore.pyqtSlot()
    #def fillComboDataPassVal(self, values, objComboBox):
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
    
    
    def managePaymentSlot(self):
        print("Main: self.manageCustomerSlot()")
        #QtWidgets.qApp.removeEventFilter(self)
        self.paymentWindow = UI_trnPayment()
        self.paymentWindow.txtCustomer.setText(str(self.txtLgrCusName.text()))
        self.paymentWindow.txtMachine.setText(str(self.txtLgrShsName.text()))
               
        self.paymentWindow.show()
        self.setFocus()

  

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_trnLedger()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())