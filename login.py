from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMdiSubWindow,QMessageBox
from main import UI_MAIN


import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

class UI_LOGIN(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_LOGIN, self).__init__()
        uic.loadUi("loginUIDesign.ui", self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.tblItems.installEventFilter(self)
        QtWidgets.qApp.installEventFilter(self)
        print("Main: self.__init__()")
    

    def manageMdiMainSlot(self):

        #print("Main: self.manageCustomerSlot()")
  
        fetchValues = sqlFunc.fetchSql("SELECT " + 
                                       "vleNo, " +
                                       "vleCode, " +
                                       "fname, " + 
                                       "mName, " + 
                                       "lName " + 
                                       "FROM " + 
                                       "man_vle " +  
                                       "WHERE Username='"+ str(self.txtUsername.text()) +"' " + 
                                       "AND Password='"+ str(self.txtPassword.text()) +"' ",
                                       "False"
                                       )
        for vle in fetchValues:
            if vle != None:
                print(vle)
                #QtWidgets.qApp.removeEventFilter(self)
                QMessageBox.information(self,"ATTENTION!!!","Access Granted")
                self.vleNo = vle[0]
                self.vleCode = vle[1]
                self.vleFullName = vle[2] + " " + vle[3] + " " + vle[4]
                self.mdiMain = UI_MAIN(self.vleNo, self.vleCode, self.vleFullName)
                self.mdiMain.show()
                self.close()
            else:
                QMessageBox.critical(self,"ATTENTION!!!","Invalid Username/Password")
      
                    
         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UI_LOGIN()
    window.show()
    sys.exit(app.exec_())