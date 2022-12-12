from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from pathlib import Path
from pubsub import pub
from SingletonPrefsClass import Preferences

DEBUG = False

Prefs = Preferences()

#<Todo>
#PartCombinerClass
#Add repeated center parts as well as stretched center.Width won't be exact but close
#</Todo>
class PartCombiner(QWidget):
	leftImg = None
	midImg = None
	rightImg = None
	fullImage = None
	captionedImg = None
	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		pub.subscribe(self.setLeftImage,'new_left_image')
		pub.subscribe(self.setMidImage,'new_mid_image')
		pub.subscribe(self.setRightImage,'new_right_image')
		
		self.setMinimumWidth(Prefs.buttonWidth+ 30)
		self._iconCount = 0
		self._butImg = QPushButton()
		self._butImg.setFixedSize(QSize(Prefs.buttonWidth + 5,Prefs.buttonHeight))
		self._leWidth = QLineEdit(str(Prefs.buttonWidth))
		self._leHeight = QLineEdit(str(Prefs.buttonHeight))
		self._lbWidth = QLabel("Width")
		self._lbHeight = QLabel("Height")
		self._lbActual = QLabel("Actual Size ")
		self._lbBaseName = QLabel("Base name")
		self._leBaseName = QLineEdit()
		self._cbFileTypes = QComboBox()	
		self._ext = None	
		self._pbSaveParts = QPushButton("Save Parts")
		self._pbSaveBlank = QPushButton("Save Blank")


		self._gridLayout = QGridLayout(self)
		self._gridLayout.addWidget(self._lbWidth,0,0)
		self._gridLayout.addWidget(self._leWidth,1,0)
		self._gridLayout.addWidget(self._lbHeight,2,0)
		self._gridLayout.addWidget(self._leHeight,3,0)
		self._gridLayout.addWidget(self._butImg,4,0)
		self._gridLayout.addWidget(self._lbBaseName,5,0)
		self._gridLayout.addWidget(self._leBaseName,6,0)
		self._gridLayout.addWidget(self._cbFileTypes,7,0)
		self._gridLayout.addWidget(self._pbSaveParts,8,0)
		self._gridLayout.addWidget(self._pbSaveBlank,9,0)

		self.setExtensions()
		
		self._leWidth.returnPressed.connect(self.sizeChanged)
		self._leHeight.returnPressed.connect(self.sizeChanged)
		self._pbSaveParts.clicked.connect(self.saveAllParts)
		self._pbSaveBlank.clicked.connect(self.saveBlank)		
		self._ext = self.getExt()
	
	def sizeChanged(self):
		self._finalSize = self.getFinalSize()
		self.drawIcons()
		
	def setLeftImage(self,image):
		if image == "":
			return
		self.leftImg = image
		if self._iconCount < 3:
			self._iconCount +=1
		if self._iconCount == 3:
			self.drawIcons()

	def setMidImage(self,image):
		if image == "":
			return
		self.midImg = image
		if self._iconCount < 3:
			self._iconCount +=1
		if self._iconCount == 3:
			self.drawIcons()

	def setRightImage(self,image):
		if image == "":
			return
		self.rightImg = image
		if self._iconCount < 3:
			self._iconCount +=1
		if self._iconCount == 3:
			self.drawIcons()
			
	def digitsOnly(self,val):
		_result = ""
		for letter in str(val):
			if letter in ("0123456789"):
				_result += letter
		return _result

	def drawIcons(self):
		if self.leftImg == None or self.rightImg == None:
			return
		_mid = None
		_finalSize = self.getFinalSize()
		_totalWidth = _finalSize.width()
		_height = _finalSize.height()
		_left = self.leftImg.scaledToHeight(_height)
		_right = self.rightImg.scaledToHeight(_height)
		_img = QPixmap(_finalSize.width(),_height)
		_midWidth = _finalSize.width() - _left.width() - _right.width()
		_mid = self.midImg.scaled(_midWidth,_height,Qt.IgnoreAspectRatio)
		_img.fill(QColor(0,0,0,0))

		if _img == None:
			print(">>> Null pixmap")
			return
		_painter = QPainter(_img)
		_painter.drawPixmap(QRect(0, 0, _left.width(), _left.height()),_left)
		_start = _left.width()
		_painter.drawPixmap(QRect(_start, 0, _mid.width(), _mid.height()),_mid)
		_start = _left.width() + _mid.width()
		_painter.drawPixmap(QRect(_start, 0, _right.width(), _right.height()),_right)
		del _painter
		self.fullImage = _img
		# ~ self.fullImage = _img.scaled(_finalSize)
		pub.sendMessage("blank_set",image = self.fullImage)
		
		self._butImg.setFixedSize(self.fullImage.size())
		self._butImg.setIcon(QIcon(self.fullImage))
		self._butImg.setIconSize(self.fullImage.size())
		self._lbActual.setText("Actual size " + str(self.fullImage.width()) + "," + str(self.fullImage.height()))

	def getFinalSize(self):
		_width = self.digitsOnly(self._leWidth.text())
		self._leWidth.setText(_width)
		_width = int(float(_width))
		_height = self.digitsOnly(self._leHeight.text())
		self._leHeight.setText(_height)
		_height = int(float(self._leHeight.text()))
		return QSize(_width,_height)
	
		if res == 3:
			_res=_dialog(res == 3,_imgList)
		else:
			_res=_dialog(res==3,"Images not saved")

		_res.exec()
		del _res

	def saveAllParts(self):
		_filename = self._leBaseName.text()
		if _filename == "":
			print("No file name")
			return
		if self.leftImg == None or self.midImg == None or self.rightImg == None:
			print("Choose an image first")
			return
		_height = Prefs.buttonHeight
		_path = str(Path("data","buttonparts",_filename))
		_savename = _path + "-Left."+self._ext
		_img = self.leftImg.scaledToHeight(_height)
		_img.save(_savename)
		_savename = _path + "-Mid."+self._ext
		_img = self.midImg.scaledToHeight(_height)
		_img.save(_savename)
		_savename = _path + "-Right."+self._ext
		_img = self.rightImg.scaledToHeight(_height)
		_img.save(_savename)
		
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
		
	def getBaseName(self):
		_filename = self._leBaseName.text()
		if _filename == "":
			print("No name set")
			return False
		return str(_filename)
			
	def getExt(self):
		_ext = self._cbFileTypes.currentText()
		if _ext == "":
			print("No extension set")
			return	False
		return _ext
		
	def saveBlank(self):
		_savename = self._leBaseName.text()
		if not _savename:
			print("Provide a name first")
			return
		_ext = self.getExt()
		if not _ext:
			print("No extension set")
			return
		_path = str(Path("data","blankbuttons",_savename+"-Blank." + self.getExt()))
		self.fullImage.save(_path)
		
class _dialog(QDialog):
	def __init__(self,success,imgList):
		super().__init__()

		self.setWindowTitle("Save Parts")
		if success:
			QBtn = QDialogButtonBox.Ok
		else:
			QBtn = QDialogBox.Cancel

		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		self._boxLayout = QVBoxLayout()
		if success:
			lbl = QLabel("Saved parts as:")
			self._boxLayout.addWidget(lbl)
			for item in imgList:
				lbl = QLabel("   " + item)
				self._boxLayout.addWidget(lbl)
		else:
			lbl = QLabel("Failed to save parts")
		self._boxLayout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
	
	def captionImage(self):
		_img = self.fullImage
		
	
