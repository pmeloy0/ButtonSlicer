#Utils class
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox

class Utils:
	def __new__(self):
		""" creates a singleton object, if it is not created,
		or else returns the previous singleton object"""
		if not hasattr(self, 'instance'):
			self.instance = super(Utils, self).__new__(self)
		return self.instance	
	
	def __init__(self):
		pass
	
	# Takes a string, extracts only digits and returns int
	def digitsOnly(self,_string):
		_str = ""
		for letter in _string:
			if letter in ("0123456789"):
				_str += letter
		return int(float(_str))
	
	#Takes a string and returns a float
	def floatOnly(self,_string):
		_str = ""
		for letter in _string:
			if letter in (".0123456789"):
				_str += letter
		return float(_str)
	
	def flashLineEdit(self,_control):
		_oldSheet = _control.styleSheet()
		_control.setStyleSheet("background-color: rgb(255,0,0)")
		QTimer.singleShot(250, lambda :_control.setStyleSheet(_oldSheet))		

	def errorMessage(self,_title,_message):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Critical)
		msgBox.setText(_message)
		msgBox.setWindowTitle(_title)
		msgBox.setStandardButtons(QMessageBox.Ok)
		returnValue = msgBox.exec()
		
		
	
