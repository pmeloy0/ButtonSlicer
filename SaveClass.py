from PySide6.QtWidgets import QWidget,QGridLayout,QFontComboBox,QLabel,QLineEdit,QPushButton,QDialog,QComboBox
from PySide6.QtGui import QImageReader

from pathlib import Path
from SingletonPrefsClass import Preferences
from UtilsClass import Utils

Utils = Utils()
Prefs = Preferences()
from pubsub import pub
class SaveClass(QWidget):
	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		
		self._lbName = QLabel("Name")
		self._leName = QLineEdit()
		self._leName.setStyleSheet("background-color: rgb(255, 255, 255)")		
		self._cbFileTypes = QComboBox()
		self._butsaveCaptioned = QPushButton("Save Captioned")
		self._butSavePrefs = QPushButton("Save Preferences")
		self._butDefPrefs = QPushButton("Revert to Defaults")
		self._butShowPrefs = QPushButton("Show Prefs")
		
		self._gridLayout = QGridLayout(self)
		self._gridLayout.addWidget(self._lbName,0,0)
		self._gridLayout.addWidget(self._leName,1,0)
		self._gridLayout.addWidget(self._cbFileTypes,2,0)
		self._gridLayout.addWidget(self._butsaveCaptioned,3,0)
		self._gridLayout.addWidget(self._butSavePrefs,4,0)
		self._gridLayout.addWidget(self._butDefPrefs,5,0)
		self._gridLayout.addWidget(self._butShowPrefs,6,0)
		
		self._butsaveCaptioned.clicked.connect(self.saveCaptioned)
		self._butSavePrefs.clicked.connect(self.savePrefs)
		self._butDefPrefs.clicked.connect(self.defPrefs)
		self._butShowPrefs.clicked.connect(self.showPrefs)
		self.setExtensions()
		
	def showPrefs(self):
		Prefs.showDict()
		
	def setExtensions(self):
		_btypes =  QImageReader.supportedImageFormats()
		_extensions = ""
		_badTypes = ["svg","svgz"]
		self._cbFileTypes.clear()
		for item in _btypes:
			_str = str(item, 'utf-8')
			if _str not in _badTypes:
				self._cbFileTypes.addItem(_str)
		idx = self._cbFileTypes.findText("png")
		if idx >= 0:
			self._cbFileTypes.setCurrentIndex(idx)
		
	def getName(self):
		_filename = self._leName.text()
		if _filename == "":
			print("No name set")
			return False
		return str(_filename)
	
	def getExtention(self):
		_ext = self._cbFileTypes.currentText()
		return _ext
		
	def saveCaptioned(self):
		_text = self._leName.text()
		if  _text == "":
			Utils.flashLineEdit(self._leName)
			print("Name Required")
			return
		pub.sendMessage('save_captioned',_name = self._leName.text(),_ext = self.getExtention())
	
	def savePrefs(self):
		Prefs.savePrefs()
	
	def defPrefs(self):
		Prefs.setDefaults()
			

