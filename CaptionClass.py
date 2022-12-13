#Font and caption generator
from PySide6.QtWidgets import QWidget,QGridLayout,QFontComboBox,QLabel,QLineEdit,QColorDialog,QPushButton,QSlider
from PySide6.QtCore import QSize,Qt
from PySide6.QtGui import QFont,QFontMetrics,QPixmap,QPainter,QColor
from UtilsClass import Utils
from SingletonPrefsClass import Preferences
from UtilsClass import Utils
from pathlib import Path
from pubsub import pub

Utils = Utils()
Prefs = Preferences()

class Caption(QWidget):
	def __init__(self,*args,**kwargs):
		
		self._blankImage = None
		#<Todo>
		# CaptionClass init
		#Figure out why this line results in "__init__ not called"
		# ~ self.setMinimumWidth(Prefs.getButtonWidth()+ 30)
		#</Todo>
		super().__init__(*args, **kwargs)
		pub.subscribe(self.setButtonImage,"blank_set")
		pub.subscribe(self.saveCaptioned,"save_captioned")
		self._vOffset = 0
		self._hOffset = 0
		
		self._lblCaption = QLabel("Create Caption")
		self._leCaption = QLineEdit()
		self._leCaption.setMaximumSize(180,60)
		self._cbFont = QFontComboBox()
		self._cbFont.setMaximumSize(180,60)
		self._leSize = QLineEdit("16")
		self._leSize.setMaximumWidth(40)
		self._lblButton = QLabel()
		self._lblButton.setFixedSize = QSize(150,50)
		self._lblColor = QLabel()
		self._pbFontColor = QPushButton("Color")
		self._slVertOffset = QSlider(Orientation = Qt.Vertical)
		self._slHorizOffset = QSlider(Orientation = Qt.Horizontal)

		self._gridLayout = QGridLayout(self)
		self._gridLayout.addWidget(self._lblCaption,0,0,1,3)
		self._gridLayout.addWidget(self._leCaption,1,0,1,3)
		self._gridLayout.addWidget(self._cbFont,2,0,1,3)
		self._gridLayout.addWidget(self._leSize,3,0)
		self._gridLayout.addWidget(self._pbFontColor,3,1)
		self._gridLayout.addWidget(self._slVertOffset,4,0)
		self._gridLayout.addWidget(self._lblButton,4,1,Qt.AlignCenter)
		self._gridLayout.addWidget(self._slHorizOffset,5,1)
		
		self._leCaption.textChanged.connect(self.capChanged)
		self._slVertOffset.valueChanged.connect(self.vertOffset)
		self._slHorizOffset.valueChanged.connect(self.horizOffset)
		self._cbFont.currentTextChanged.connect(self.fontChanged)
		self._pbFontColor.clicked.connect(self.chooseColor)
		self._leSize.textChanged.connect(self.sizeChanged)
		
		if Prefs.font == None:
			Prefs.fontFamily(self.getFontName())
			Prefs.fontSize(self.getFontSize())

	def chooseColor(self):
		color = QColorDialog()
		color.setCurrentColor(Prefs.fontColor)
		color.exec()
		_color = color.currentColor()
		_color = str(_color.name())
		Prefs.fontColor = _color
		self.getCaptionImage()
		
	def fontChanged(self):
		Prefs.fontFamily = self._cbFont.currentText()
		self.getCaptionImage()
	
	def sizeChanged(self):
		val = Utils.digitsOnly(self._leSize.text())
		self._leSize.setText(str(val))
		if val > 6:
			Prefs.fontSize = val
			self.getCaptionImage()
		
	def vertOffset(self,val):
		if self._baseImage != None:
			self._vOffset = val
			self.getCaptionImage()
	
	def horizOffset(self,val):
		if self._baseImage != None:		
			self._hOffset = val
			self.getCaptionImage()
					
	def setButtonImage(self,image):
		self._baseImage = image
		self._lblButton.setFixedHeight(self._baseImage.height())
		self._blankImage = image
		self._lblButton.setPixmap(self._baseImage)
		vOff = self._baseImage.height()//2
		self._slVertOffset.setMinimum(0-vOff)
		self._slVertOffset.setMaximum(vOff)
		hOff = self._baseImage.width() //2
		self._slHorizOffset.setMinimum(0-hOff)
		self._slHorizOffset.setMaximum(hOff)
		self.getCaptionImage()
		
	def getFontName(self):
		if self._cbFont.currentText():
			_fontname = self._cbFont.currentText()
			return _fontname

	def getFontSize(self):
		_size = Utils.digitsOnly(self._leSize.text())
		if _size > 0:
			return _size
			
	def getCaptionText(self):
		_text = self._leCaption.text()
		if _text == "":
			return False
		return _text
	
	def getCaptionFontSize(self):
		_size = self._leSize.text()

		if _size == "":
			return False
		_size = Utils.digitsOnly(_size)
		return _size
	
	def capChanged(self):
		_cap = self.getCaptionText()
		_size = self.getCaptionFontSize()
		self.getCaptionImage()
	
	def getCaptionImage(self):
		if self._blankImage == None:
			print("No image still")
			return
		_full = self._blankImage.copy()
		_text = self.getCaptionText()
		if _text:
			print("Caption")
			_fm = QFontMetrics(Prefs.font)
			_rect = _fm.boundingRect(_text)
			_width = _rect.width()
			_height = _rect.height()
			_start = _full.width() //2 - _width //2
			_top = _full.height() //2 - _height //2
			painter = QPainter(_full)
			_font = QFont(Prefs.font)
			painter.setFont(_font)
			_color = Prefs.fontColor
			painter.setPen(_color)
			_rect = _full.rect()
			_rect.moveTo(_start+self._hOffset,_top-self._vOffset)
			painter.drawText(_rect,_text)
			painter.end()
			del(painter)
		self._lblButton.setPixmap(_full)
		return _full
	
	def saveCaptioned(self,_name,_ext):
		if self._blankImage == None:
			print("No image set")
			Utils.errorMessage("Captioner","No Source Image Set")			
			return
		if not _name:
			print("Set a name dummy")
			return
		_img = self.getCaptionImage()
		if _img:
			_path = str(Path("data","fullbuttons",_name +'.' +_ext))
			_img.save(_path)

		
		

