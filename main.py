from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, uic
from PyQt5.QtWidgets import QMdiSubWindow
from manCustomer import UI_manCustomer
from manShs import UI_manShs
from trnLedger import UI_trnLedger
from trnPayment import UI_trnPayment
from trnSalesReport import UI_trnSalesReport

from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime, timedelta


class UI_MAIN(QtWidgets.QMainWindow):
    def __init__(self, vleNo, vleCode,vleFullName):
        super(UI_MAIN, self).__init__()
        uic.loadUi("mainUIDesign.ui", self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.tblItems.installEventFilter(self)
        QtWidgets.qApp.installEventFilter(self)

        #self.lblTime.setText("{:%Y-%m-%d %I:%M:%S %p}".format(datetime.now()))
        self.lblTime.setText("{:%A, %m-%d-%y %I:%M:%S %p}".format(datetime.now()))

        self.lblVleNo.setText(vleNo)
        self.lblVleCode.setText(vleCode)
        self.lblUser.setText(vleFullName)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        print("Main: self.__init__()")
    
    def updateTime(self):
        #self.lblTime.setText("{:%Y-%m-%d %I:%M:%S %p}".format(datetime.now()))
        self.lblTime.setText("{:%A, %m-%d-%y %I:%M:%S %p}".format(datetime.now()))

    @QtCore.pyqtSlot()
    def manageCustomerSlot(self):
        print("Main: self.manageCustomerSlot()")
        #QtWidgets.qApp.removeEventFilter(self)
        #self.settings_window = UI_manCustomer()
        #self.settings_window.show()
        
        sub = QtWidgets.QMdiSubWindow()
        manCustomerWindow = UI_manCustomer()
        sub.setWidget(manCustomerWindow)
        sub.setObjectName("frmManCustomer")
        sub.setWindowTitle("CUSTOMER MANAGER")
        sub.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        #sub.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        sub.setFixedSize(610,620)
        self.mdiArea.addSubWindow(sub)
        sub.show()

    def manageShsSlot(self):
        print("Main: self.manageShsSlot()")
        sub = QtWidgets.QMdiSubWindow()
        manShsWindow = UI_manShs()
        sub.setWidget(manShsWindow)
        sub.setObjectName("frmManShs")
        sub.setWindowTitle("SHS MANAGER")
        sub.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        sub.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        sub.setFixedSize(610,620)
        self.mdiArea.addSubWindow(sub)
        sub.show()

    def manageLedgerSlot(self):
        print("Main: self.manageLedgerSlot()")
        sub = QtWidgets.QMdiSubWindow()
        trnLedgerWindow = UI_trnLedger()
        sub.setWidget(trnLedgerWindow)
        sub.setObjectName("frmTrnLedger")
        sub.setWindowTitle("LEDGER")
        sub.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        sub.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        sub.setFixedSize(610,620)
        self.mdiArea.addSubWindow(sub)
        sub.show()
    
    def managePaymentSlot(self):
        print("Main: self.managePaymentSlot()")
        sub = QtWidgets.QMdiSubWindow()
        trnPaymentWindow = UI_trnPayment()
        sub.setWidget(trnPaymentWindow)
        sub.setObjectName("frmPayment")
        sub.setWindowTitle("PAYMENT")
        sub.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        sub.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        sub.setFixedSize(600,380)
        self.mdiArea.addSubWindow(sub)
        sub.show()

    def manageReportSlot(self):
        print("Main: self.manageReportSlot()")
        sub = QtWidgets.QMdiSubWindow()
        trnPaymentWindow = UI_trnSalesReport()
        sub.setWidget(trnPaymentWindow)
        sub.setObjectName("frmSalesRpt")
        sub.setWindowTitle("SALES REPORT")
        sub.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        sub.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        sub.setFixedSize(610,620)
        self.mdiArea.addSubWindow(sub)
        sub.show()

    
         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UI_MAIN()
    window.show()
    sys.exit(app.exec_())