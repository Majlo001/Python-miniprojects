from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QDialog, QPushButton, QMessageBox, QListWidget, QLineEdit, QDialogButtonBox
from PyQt5.uic import loadUi
import sys

from db import TodoDatabase

UI_FILES_PATH = 'ui_files/'


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editItemWindow = None
        self.isEditItemOpen = False
        self.tempItems = []
        
        # Load the ui file
        self.ui = loadUi(UI_FILES_PATH+"todo.ui", self)
        self.setWindowTitle("Todo List App")

        # Define widgets
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")

        self.addItem = self.findChild(QPushButton, "addItem")
        self.editItem = self.findChild(QPushButton, "editItem")
        self.removeItem = self.findChild(QPushButton, "removeItem")
        self.clearList = self.findChild(QPushButton, "clearList")

        self.listWidget = self.findChild(QListWidget, "listWidget")

        # Click the buttons
        self.addItem.clicked.connect(self.add_it)
        self.editItem.clicked.connect(self.edit_it)
        self.removeItem.clicked.connect(self.remove_it)
        self.clearList.clicked.connect(self.clear_list)

        # DB Import
        self.db = TodoDatabase()
        self.db.create_database()
        self.tempItems = self.db.fetch()

        for item in self.tempItems:
            self.add_it_from_db(item[0])
        
        self.tempItems = []

        # Show The App
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close this window?', QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.db.remove_all()
            for i in range(self.listWidget.count()):
                self.db.insert(str(self.listWidget.item(i).text()))
            
            event.accept()
        else:
            event.ignore()

    def add_it_from_db(self, item):
        self.listWidget.addItem(item)

    def add_it(self):
        if self.lineEdit.text() != "":
            item = self.lineEdit.text()
            self.listWidget.addItem(item)
            self.lineEdit.setText("")

    def edit_it(self):
        self.window = QtWidgets.QMainWindow()
        self.editItemWindow = Ui_EditItem()

        if self.isEditItemOpen == False:
            if self.listWidget.currentItem():
                self.isEditItemOpen = True
                thing = self.listWidget.currentItem().text()
                self.editItemWindow.editLineItem.setText(thing)
                self.editItemWindow.submitClickedAccept.connect(self.change_item)
                self.editItemWindow.submitClickedCancel.connect(self.cancle_change)
                self.editItemWindow.show()

    def change_item(self, data):
        self.listWidget.currentItem().setText(data)
        self.isEditItemOpen = False
    
    def cancle_change(self):
        self.isEditItemOpen = False

    def remove_it(self):
        active = self.listWidget.currentRow()
        self.listWidget.takeItem(active)

    def clear_list(self):
        self.listWidget.clear()
        self.db.remove_all()



class Ui_EditItem(QDialog):
    submitClickedAccept = QtCore.pyqtSignal(str)
    submitClickedCancel = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # Load the ui file
        self.ui = loadUi(UI_FILES_PATH+"edit_item.ui", self)
        self.setWindowTitle("Edit Item")

        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")
        self.editLineItem = self.findChild(QLineEdit, "editLineItem")
        
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.exit())


    def exit(self):
        self.submitClickedCancel.emit()
        self.close()

    def accept(self):
        self.submitClickedAccept.emit(self.editLineItem.text())
        self.editLineItem.setText("")
        self.close()


app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())