#!/usr/bin/env python3

#from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os

#-------------------------------#

# Creating main window class
class MainWindow(QMainWindow):
 
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        # setting window geometry
        self.setGeometry(100, 100, 600, 400)
 
        # creating a layout
        layout = QVBoxLayout()
 
        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()
 
        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
 
        # adding editor to the layout
        layout.addWidget(self.editor)
 
        # creating a QWidget layout
        container = QWidget()
 
        # setting layout to the container
        container.setLayout(layout)
 
        # making container as central widget
        self.setCentralWidget(container)
 
        # calling update title method
        self.update_title()
 
        # showing all the components
        self.show()
 
    # creating dialog critical method
    # to show errors
    def dialog_critical(self, s):
 
        # creating a QMessageBox object
        dlg = QMessageBox(self)
 
        # setting text to the dlg
        dlg.setText(s)
 
        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)
 
        # showing it
        dlg.show()
 
    # update title method
    def update_title(self):
 
        # setting window title with prefix as file name
        # suffix aas PyQt5 Notepad
        self.setWindowTitle("{} - Crypto-Messenger".format('empty chat'))

#-------------------------------#

def main():

	app = QApplication(sys.argv)

	# wikipedia's part
#	root = QWidget()
#	root.resize(320, 240)
#	root.setWindowTitle("Hello, World!")
#	root.show()

	app.setApplicationName("PyQt5-Note")
	#window = ClientGui()
	window = MainWindow()

	sys.exit(app.exec_())
	

# Execute the script
if __name__ == '__main__':
	main()
