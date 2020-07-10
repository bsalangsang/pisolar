from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMessageBox , QTableWidget , QTableWidgetItem,QApplication,QPushButton, QDesktopWidget

import sqlExec

sqlFunc = sqlExec.mysqlExecCmds("db")
sqlFunc.dbConnect()

class UI_manLedger(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI_manLedger, self).__init__()
        uic.loadUi("manShsUIDesign.ui", self)
        #self.setFixedSize(730, 580)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)
        print("MAS SHS: self.__init__()")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UI_manLedger()
    #if os.name == "posix":
    #    window.showFullScreen()
    #else:
    window.show()
        # window.showMaximized()
    sys.exit(app.exec_())