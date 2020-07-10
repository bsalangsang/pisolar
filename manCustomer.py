from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget
from mdlFunction import modFunc

import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

class UI_manCustomer(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_manCustomer, self).__init__()
        uic.loadUi("manCustomerUIDesign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("Main: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.onLoadEvent()

    def onLoadEvent(self):
        
        self.fillTableDataCustomer() 
       
    #=-----------------------------------------------------------------------------=
    #  CORE FUNCTION
    #=-----------------------------------------------------------------------------=
    
    def fillTableDataCustomer(self):
        fetchValues = sqlFunc.fetchSql("select " + 
                                      "customerCode AS 'CODE_', " + 
                                      "fName AS 'FIRST_', " + 
                                      "mName AS 'MIDDLE_', " + 
                                      "lName AS 'LAST_', " +
                                      "address AS 'ADDRESS_', " + 
                                      "contact1 AS 'CONTACT_NO.1', " + 
                                      "customerNo AS 'No.', " + 
                                      "isActive AS 'STATUS_' " + 
                                      "FROM man_customers " +
                                      "WHERE isActive = 'Y'",
                                      "True")
        
        rowCount = 0
        self.tblCustList.setRowCount(0) #clear table list
        for row_number, row_data in enumerate(fetchValues):
            self.tblCustList.insertRow(row_number)
            rowCount = rowCount + row_number
            for column_number, data in enumerate(row_data):
                self.tblCustList.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
        self.tblCustList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tblCustList.resizeColumnsToContents()
        
        self.gbCustList.setTitle("Record(s) Found: " + str(rowCount))  

        x = 0
        for row in fetchValues:
            if x > 0:
                break
            else:
                self.txtCode.setText(row[0])
                self.txtFname.setText(row[1])
                self.txtMname.setText(row[2])
                self.txtLname.setText(row[3])
                self.txtAddress.setText(row[4])
                self.txtContact1.setText(row[5])
                self.lblPkeyCus.setText(row[6])
            x = x + 1

        print("Man Customer: fillTableDataCustomer working. . .") #for Debugging purposes
     

    def saveUpdateRecordCustomer(self, btnUsed):
        btnReply = QMessageBox.question(self, 'Attention', "Do you Want to Save this Record?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnUsed == "Save": #save Record
           if btnReply == QMessageBox.Yes:
                tTable = "man_customers"
                tFields = "customerNo,customerCode,fName,mName,lName,address,contact1"
                tString = "(%s,%s,%s,%s,%s,%s,%s)"
                tValues = (self.lblPkeyCus.text(),
                    self.txtCode.text(),
                    self.txtFname.text(),
                    self.txtMname.text(),
                    self.txtLname.text(),
                    self.txtAddress.text(),
                    self.txtContact1.text())
                    
                itr = sqlFunc.execSql("insert",tTable,tFields,tString,tValues,"customerNo")
                if itr == "success":
                    QMessageBox.information(self,"Attention!","Successfully Saved")
                    self.fillTableDataCustomer() 
                    #self.enableTextBox(False)
                    self.btnCancelCusClicked()
                    print("SAVE Function Are Working!!!") #for Debugging purposes
                else:
                    QMessageBox.critical(self,"Attention!","Cancelled!")      
                self.show()
        elif btnUsed == "Update": #update Record
           
            tTable = "man_customers"
            tFields = ["customerCode","fName","mName","lName","address","contact1"]
            tString = "" #("%s,%s,%s,%s,%s,%s,%s,%s,%s")
            tValues = ( self.txtCode.text(),
                    self.txtFname.text(),
                    self.txtMname.text(),
                    self.txtLname.text(),
                    self.txtAddress.text(),
                    self.txtContact1.text(),
                    self.lblPkeyCus.text())
            tUpdateField = "WHERE customerNo=%s"
            itr = sqlFunc.execSql("update",tTable,tFields,tString,tValues,tUpdateField)
            if itr == "success":
                QMessageBox.information(self,"Attention!","Successfully Updated")
                self.btnSave.setText("SAVE")     
                self.fillTableDataCustomer() 
                #self.enableTextBox(False)
                self.btnCancelCusClicked()
                print("UPDATE Function Are Working!!!") #for Debugging purposes
            else:
                QMessageBox.critical(self,"Attention!","Cancelled!")      
            self.show()
        else:
            pass
    #=-----------------------------------------------------------------------------=
   
    #=-----------------------------------------------------------------------------=
    #  OBJECT FUNCTION
    #=-----------------------------------------------------------------------------=
   
    @QtCore.pyqtSlot()
    def btnAddCusClicked(self):
        #pKey = modFunc.getNextPkey("","customerNo","man_customers",6,True,"A1CUS")
        #self.lblPkeyCus.setText(pKey)
        self.lblPkeyCus.setText(modFunc.getNextPkey(self,"customerNo","man_customers",6,True,"A1CUS"))
        
        self.clearTextBoxes()
        self.enableTextBox(True)
        self.btnAdd.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.tblCustList.setEnabled(False)
        self.txtCode.setText((self.lblPkeyCus.text().strip()[-1]))
        self.txtFname.setFocus()

    def btnEditCusClicked(self):
        self.enableTextBox(True)
        self.btnAdd.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.tblCustList.setEnabled(False)
        self.btnSave.setText("UPDATE")        

    def btnDeleteCusClicked(self):
        pass
      
    def btnSaveCusClicked(self):
        #print(isSave)
        if self.btnSave.text() == "SAVE":
            self.saveUpdateRecordCustomer("Save")
            self.tblCustList.setEnabled(True)
            #print(self.btnSave.text())
        else:
            self.saveUpdateRecordCustomer("Update")
            self.tblCustList.setEnabled(True)
   
    def btnCancelCusClicked(self):
        self.enableTextBox(False)
        self.btnSave.setText("SAVE")
        self.tblCustList.setEnabled(True)
        self.btnAdd.setEnabled(True)
        self.btnEdit.setEnabled(True)
        self.btnDelete.setEnabled(True)

    def enableTextBox(self, isEnabled):
        
        self.txtCode.setEnabled(isEnabled)
        self.txtFname.setEnabled(isEnabled)
        self.txtMname.setEnabled(isEnabled)
        self.txtLname.setEnabled(isEnabled)
        self.txtAddress.setEnabled(isEnabled)
        self.txtContact1.setEnabled(isEnabled)
        
        print("Man Customer: enableTextBox working. . .") #for Debugging purposes

    def clearTextBoxes(self):
        self.txtCode.setText("")
        self.txtFname.setText("")
        self.txtMname.setText("")
        self.txtLname.setText("")
        self.txtAddress.setText("")
        self.txtContact1.setText("")
           
        print("Man Customer: clearTextBoxesCus working. . .") #for Debugging purposes
 
    def fetchTblRowDataCustomer(self):
        row = self.tblCustList.currentRow()
        self.txtCode.setText(self.tblCustList.item(row, 0).text() )  #CustomerCode
        self.txtFname.setText(self.tblCustList.item(row, 1).text() ) #First Name
        self.txtMname.setText(self.tblCustList.item(row, 2).text() ) #Middle Name 
        self.txtLname.setText(self.tblCustList.item(row, 3).text() ) #Last Name 
        self.txtAddress.setText(self.tblCustList.item(row, 4).text() ) #Address
        self.txtContact1.setText(self.tblCustList.item(row, 5).text() )#Contact1
        self.lblPkeyCus.setText(self.tblCustList.item(row,6).text() )#CustomerNo
       
        if self.tblCustList.item(row, 7).text() =='Y': #Status
           self.chkActive.setChecked(True)

        print("Man Customer: fetchTblRowDataCustomer working. . .") #for Debugging purposes
    #=-----------------------------------------------------------------------------=
   
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_manCustomer()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())