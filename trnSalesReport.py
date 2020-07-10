from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget
from datetime import datetime

import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

class UI_trnSalesReport(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_trnSalesReport, self).__init__()
        uic.loadUi("salesRptUIDEsign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("LEDGER: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.dtSortFrom.setDate(QtCore.QDate.currentDate())
        self.dtSortTo.setDate(QtCore.QDate.currentDate())
               
    @QtCore.pyqtSlot()
    def displayReport(self):

        dtSortFrm = str(datetime.strptime(self.dtSortFrom.text(), '%m/%d/%Y').date())
        dtSortTo = str(datetime.strptime(self.dtSortTo.text(), '%m/%d/%Y').date())

        fetchValues = sqlFunc.fetchSql("SELECT " + 
                                      "ldgr_shs.ldgrdate AS 'DATE_', " + 
                                      "ldgr_shs.ldgrNo AS 'ctrlNo', " + 
                                      "IF(ldgr_shs.ldgrTypeNo='2', FORMAT(amount,2),'') AS 'credit', " + 
                                      "IF(ldgr_shs.ldgrTypeNo='1', FORMAT(amount,2),'') AS 'debit', " +
                                      "FORMAT(ldgr_shs.balance,2) AS 'balance', " +
                                      "IF(ldgr_shs.isActive='Y', 'ACTIVE', 'INACTIVE') AS 'status' " +
                                      "FROM ldgr_shs " +
                                      "LEFT JOIN man_shs ON man_shs.shsNo = ldgr_shs.shsNo " +
                                      "WHERE (" +
                                      "ldgr_shs.ldgrDate >= '" + dtSortFrm + "' AND " +
                                      "ldgr_shs.ldgrDate <= '" + dtSortTo + "') " +
                                      "AND ldgr_shs.isActive = 'Y' ",
                                      "True")
        
        rowCount = 0
        totalDebit = 0
        totalCredit = 0
        self.tblLedger.setRowCount(0) #clear table list
        for row_number, row_data in enumerate(fetchValues):
            self.tblLedger.insertRow(row_number)
            if row_data[2] !="":
                totalCredit = totalCredit +  float(row_data[2].replace(",",""))
            if row_data[3] !="":
                totalDebit = totalDebit + float(row_data[3].replace(",",""))
            rowCount = rowCount + row_number
            
            for column_number, data in enumerate(row_data):
                self.tblLedger.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.tblLedger.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tblLedger.resizeColumnsToContents()
     
        self.lblTotDebit.setText("{:,.2f}".format(float(totalDebit)))
        self.lblTotCredit.setText("{:,.2f}".format(float(totalCredit)))
       


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_trnSalesReport()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())