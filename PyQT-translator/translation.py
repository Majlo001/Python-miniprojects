from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt5.uic import loadUi
import sys
import googletrans
import textblob


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the ui file
        self.ui = loadUi("translate.ui", self)
        self.setWindowTitle("Translation App")

        # Define widgets
        self.t_button = self.findChild(QPushButton, "pushButton")
        self.c_button = self.findChild(QPushButton, "pushButton_2")
        
        self.combo_1 = self.findChild(QComboBox, "comboBox")
        self.combo_2 = self.findChild(QComboBox, "comboBox_2")
        
        self.text_1 = self.findChild(QTextEdit, "textEdit")
        self.text_2 = self.findChild(QTextEdit, "textEdit_2")

        # Click the buttons
        self.t_button.clicked.connect(self.translate)
        self.c_button.clicked.connect(self.clear)

        # Add languages
        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())

        self.combo_1.addItems(self.language_list)
        self.combo_2.addItems(self.language_list)

        self.combo_1.setCurrentText("polish")
        self.combo_2.setCurrentText("english")

        # Show The App
        self.show()
    
    def clear(self):
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        

    def translate(self):
        try:
            for key, value in self.languages.items():
                if (value == self.combo_1.currentText()):
                    from_language_key = key
                if (value == self.combo_2.currentText()):
                    to_language_key = key
            
            translatedWords = textblob.TextBlob(self.text_1.toPlainText())
            translatedWords = translatedWords.translate(from_lang=from_language_key, to=to_language_key)
            self.text_2.setText(str(translatedWords))

        except Exception as e:
            QMessageBox.about(self, "Translator", str(e))




# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
sys.exit(app.exec_()) 
#app.exec_()