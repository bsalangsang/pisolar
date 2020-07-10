from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget
from mdlFunction import modFunc

import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()


class UI_manShs(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_manShs, self).__init__()
        uic.loadUi("manShsUIDesign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("MAS SHS: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.onLoadEvent()

        self.cboCustomer.currentTextChanged.connect(lambda : self.passComboItem(self.cboCustomer.currentData()))
         
    def onLoadEvent(self):
        self.fillTableDataShs()
        self.fillComboDataShs()
        print("MAS SHS: onLoadEvent()")
    #=-----------------------------------------------------------------------------=
    #  CORE FUNCTION
    #=-----------------------------------------------------------------------------=
  
    def fillTableDataShs(self):
        fetchValues = sqlFunc.fetchSql("select " + 
                                      "man_shs.shsCode AS 'CODE_', " + 
                                      "man_shs.shsName  AS 'MACHINE_NAME', " + 
                                      "man_shs.serialNo  AS 'SERIAL_', " + 
                                      "man_shs.simNo  AS 'SIM_NO', " +
                                      "man_shs.firmwareVer  AS 'FIRMWARE_', " + 
                                      "man_shs.softwareVer  AS 'SOFTWARE_', " + 
                                      "man_customers.customerCode AS 'CUS_CODE', " + 
                                      "CONCAT(man_customers.fName, ' ',man_customers.mName, ' ',man_customers.lName) AS 'CUSTOMER_', " + 
                                      "man_shs.shsNo AS 'MACHINE_NO', " + 
                                      "man_shs.isActive AS 'STATUS_' " + 
                                      "FROM man_shs " +
                                      "LEFT JOIN man_customers ON man_customers.customerNo = man_shs.customerNo " +
                                      "WHERE man_shs.isActive = 'Y'",
                                      "True")
        
        rowCount = 0
        self.tblMachList.setRowCount(0) #clear table list
        for row_number, row_data in enumerate(fetchValues):
            self.tblMachList.insertRow(row_number)
            rowCount = rowCount + row_number
            for column_number, data in enumerate(row_data):
                self.tblMachList.setItem(row_number,column_number,QTableWidgetItem(str(data)))
       
        self.tblMachList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tblMachList.resizeColumnsToContents()
        self.gbMachList.setTitle("Record(s) Found: " + str(rowCount))  

        x = 0
        for row in fetchValues:
            if x > 0:
                break
            else:
                self.txtMachCode.setText(row[0])
                self.txtMachName.setText(row[1])
                self.txtSerial.setText(row[2])
                self.txtSimNo.setText(row[3])
                self.txtFirmware.setText(row[4])
                self.txtSoftware.setText(row[5])
                self.lblPkeyMach.setText(row[8])

                self.txtCusCode.setText(row[6])
                self.txtCusName.setText(row[7])
                if row[9] == 'Y' :
                    self.txtStatus.setText("ACTIVE")
            x = x + 1

        print("MAS SHS: fillTableDataShs()") #for Debugging purposes
      
    def saveUpdateRecordShs(self, btnUsed):
        btnReply = QMessageBox.question(self, 'Attention', "Do you Want to Save this Record?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnUsed == "Save": #save Record
           if btnReply == QMessageBox.Yes:
                tTable = "man_shs"
                tFields = "shsNo,shsCode,shsName,customerCode,serialNo,simNo,firmwareVer,softwareVer"
                tString = "(%s,%s,%s,%s,%s,%s,%s,%s)"
                tValues = (self.txtMachCode.text(),
                    self.txtMachCode.text(),
                    self.txtMachName.text(),
                    self.txtCusCode.text(),
                    self.txtSerial.text(),
                    self.txtSimNo.text(),
                    self.txtFirmware.text(),
                    self.txtSoftware.text())
                  
                itr = sqlFunc.execSql("insert",tTable,tFields,tString,tValues,"customerNo")
                if itr == "success":
                    QMessageBox.information(self,"Attention!","Successfully Saved")
                    self.fillTableDataShs() 
                    #self.enableTextBox(False)
                    self.btnCancelShsClicked()
                    print("MAS SHS: saveUpdateRecordShs() - SAVE") #for Debugging purposes
                else:
                    QMessageBox.critical(self,"Attention!","Cancelled!")      
                self.cboCustomer.selectedIndex = 0
                self.show()
        elif btnUsed == "Update": #update Record
            tTable = "man_shs"
            tFields = ["shsCode","shsName","customerCode","serialNo","simNo","firmwareVer","softwareVer"]
            tString = "" #("%s,%s,%s,%s,%s,%s,%s,%s,%s")
            tValues = (self.txtMachCode.text(),
                    self.txtMachName.text(),
                    self.txtCusCode.text(),
                    self.txtSerial.text(),
                    self.txtSimNo.text(),
                    self.txtFirmware.text(),
                    self.txtSoftware.text(),
                    self.lblPkeyMach.text())

            tUpdateField = "WHERE shsNo=%s"

            itr = sqlFunc.execSql("update",tTable,tFields,tString,tValues,tUpdateField)
            if itr == "success":
                QMessageBox.information(self,"Attention!","Successfully Updated")
                self.btnSave.setText("SAVE")     
                self.fillTableDataShs() 
                #self.enableTextBox(False)
                self.btnCancelShsClicked()
                print("MAS SHS: saveUpdateRecordShs() - UPDATE") #for Debugging purposes
            else:
                QMessageBox.critical(self,"Attention!","Cancelled!")      
            self.cboCustomer.selectedIndex = 0    
            self.show()
        else:
            pass
   
    def fillComboDataShs(self):
        fetchValues = sqlFunc.fetchSql("select " + 
                                      "customerCode AS 'CODE_', " + 
                                      "CONCAT(fName, ' ',mName,' ',lName) AS 'CUSTOMER_' " + 
                                      "FROM man_customers " +
                                      "WHERE isActive = 'Y'",
                                      "True")
        
        self.cboCustomer.addItem(" ")
        for row in fetchValues:
            self.cboCustomer.addItem(str(row[1]), row[0])

    #=-----------------------------------------------------------------------------=
     
    #=-----------------------------------------------------------------------------=
    #  OBJECT FUNCTION
    #=-----------------------------------------------------------------------------=
   
    @QtCore.pyqtSlot()
    def btnAddShsClicked(self):
        self.lblPkeyMach.setText(modFunc.getNextPkey("","shsNo","man_shs",6,True,"A1SHS"))
        self.clearTextBoxesShs()
        self.enableTextBox(True)
        self.btnAdd.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.tblMachList.setEnabled(False)
        self.txtMachCode.setText((self.lblPkeyMach.text().strip()[-1]))
        self.txtMachName.setFocus()

    def btnEditShsClicked(self):
        self.enableTextBox(True)
        self.btnAdd.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.tblMachList.setEnabled(False)
        self.btnSave.setText("UPDATE")        

    def btnDeleteShsClicked(self):
        pass

    def btnSaveShsClicked(self):
            #print(isSave)
        if self.btnSave.text() == "SAVE":
            self.saveUpdateRecordShs("Save")
            self.tblMachList.setEnabled(True)
        else:
            self.saveUpdateRecordShs("Update")
            self.tblMachList.setEnabled(True)

    def btnCancelShsClicked(self):
        self.enableTextBox(False)
        self.btnSave.setText("SAVE")
        self.tblMachList.setEnabled(True)
        self.btnAdd.setEnabled(True)
        self.btnEdit.setEnabled(True)
        self.btnDelete.setEnabled(True)
   
    def enableTextBox(self, isEnabled):
        self.txtMachCode.setEnabled(isEnabled)
        self.txtMachName.setEnabled(isEnabled)
        self.txtSerial.setEnabled(isEnabled)
        self.txtStatus.setEnabled(isEnabled)
        self.txtSimNo.setEnabled(isEnabled)
        self.txtFirmware.setEnabled(isEnabled)
        self.txtSoftware.setEnabled(isEnabled)
        self.cboCustomer.setEnabled(isEnabled)
        self.txtCusCode.setEnabled(isEnabled)
        self.txtCusName.setEnabled(isEnabled)
        
        print("MAS SHS: enableTextBoxShs()") #for Debugging purposes

    def clearTextBoxesShs(self):
        self.txtMachCode.setText("")
        self.txtMachName.setText("")
        self.txtSerial.setText("")
        self.txtStatus.setText("")
        self.txtSimNo.setText("")
        self.txtFirmware.setText("")
        self.txtSoftware.setText("")
        self.txtCusCode.setText("")
        self.txtCusName.setText("")
       
    
        print("clearTextBoxesShs Function Are Working!!!") #for Debugging purposes
  
    #=-----------------------------------------------------------------------------=
    #  SPECIAL OBJECT FUNCTION
    #===============================================================================

    def fetchTblRowDataShs(self):
        row = self.tblMachList.currentRow()
        self.txtMachCode.setText(self.tblMachList.item(row, 0).text() )  #machineCode
        self.txtMachName.setText(self.tblMachList.item(row, 1).text() ) #machine Name
        self.txtSerial.setText(self.tblMachList.item(row, 2).text() ) #Serial
        self.txtSimNo.setText(self.tblMachList.item(row, 3).text() ) #Sim No
        self.txtFirmware.setText(self.tblMachList.item(row, 4).text() ) #FirmWare
        self.txtSoftware.setText(self.tblMachList.item(row, 5).text() ) #Software
        self.txtCusCode.setText(self.tblMachList.item(row, 6).text() )#Customer Code
        self.txtCusName.setText(self.tblMachList.item(row, 7).text() )#CustomerName
        self.lblPkeyMach.setText(self.tblMachList.item(row, 8).text()) # machine No                                   
      
        if self.tblMachList.item(row, 9).text() =='Y': #Status
           self.txtStatus.setText("ACTIVE")

        print("MAS SHS: fetchTblRowDataShs()") #for Debugging purposes
    
    def passComboItem(self, values):
        
        self.txtCusCode.setText(values)
        self.txtCusName.setText(str(self.cboCustomer.currentText()))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_manShs()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())