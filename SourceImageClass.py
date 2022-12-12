from PySide6.QtWidgets import QWidget,QLabel,QGridLayout,QFileDialog,QSlider,QPushButton
from PySide6.QtCore import QSize,Qt
from PySide6.QtGui import QImageReader,QIcon
from SingletonPrefsClass import Preferences

from pubsub import pub

DEBUG = True
Prefs = Preferences()

class SourceImage(QWidget):
	Icon = None
	PartImage = None
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self._top = 0
		self._bot = 0
		self._width = 0
		self._height = 0
		self._minHeight = 5
		self._lblWidth = Prefs.buttonWidth
		self._lblHeight = Prefs.buttonHeight

		self._gridLayout = QGridLayout(self)


		self._slTop = QSlider()
		self._slTop.setOrientation(Qt.Vertical)
		self._gridLayout.addWidget(self._slTop, 1, 0, Qt.AlignLeft)

		self._pbLoad = QPushButton("Load Image")
		self._gridLayout.addWidget(self._pbLoad, 3, 1,Qt.AlignCenter)

		self._lblImage = QLabel()
		self._lblImage.setFixedSize(300,150)
		# ~ self._lblImage.setScaledContents(True) # Better not scaled when resizing
		self._gridLayout.addWidget(self._lblImage, 1, 1)

		self._lblTop = QLabel()
		self._gridLayout.addWidget(self._lblTop, 0, 0)

		self._lblTitle = QLabel()
		self._lblTitle.setAlignment(Qt.AlignCenter)

		self._gridLayout.addWidget(self._lblTitle, 0, 1)

		self._slHeight = QSlider()
		self._slHeight.setOrientation(Qt.Vertical)

		self._gridLayout.addWidget(self._slHeight, 1, 2)
		
		self._lblBot = QLabel()
		self._gridLayout.addWidget(self._lblBot, 3, 2)
		
		
		self._pbLoad.clicked.connect(self.openSourceImage)
		self._slTop.valueChanged.connect(self.topChanged)
		self._slHeight.valueChanged.connect(self.heightChanged)
	
	def topChanged(self,val):
		self._top = self._height//2 - val
		self.getPartImage()
		
	def heightChanged(self,val):
		_height= self._height-val
		if _height < self._top + self._minHeight:
			_height = self._top + self._minHeight
		self._bot = _height
		self.getPartImage()
					
	def openSourceImage(self):
		_btypes =  QImageReader.supportedImageFormats()
		_filter = ""
		for item in _btypes:
			_str = '*.' + str(item, 'utf-8')+ ' '
			_filter += _str
		_filter = 'Images (' + _filter + _filter.upper() + ')'
		filename, ok = QFileDialog.getOpenFileName(None,"Select a File", "data/sourceimages", _filter)
		if filename:
			self.Icon = QIcon(filename)
			self.PartImage = self.Icon.pixmap(300,100)
			# ~ self._lblImage.setPixmap(self.Icon.pixmap(300,100))
			self._width = self.PartImage.width()
			self._height = self.PartImage.height()
			self._bot = self._height
			#Set values for two sliders
			self._slTop.setMinimum(0)
			self._slTop.setMaximum(self._height // 2)
			self._slTop.setValue(self._height // 2)
			self.getPartImage()

	def getPartImage(self):
		_img = self.Icon.pixmap(Prefs.buttonWidth,Prefs.buttonHeight)
		self.PartImage = _img.copy(0,self._top,self._width,self._bot)
		self._lblImage.setPixmap(self.PartImage.scaled(Prefs.sourceWidth,Prefs.sourceHeight))	
		pub.sendMessage('new_source_image',image=self.PartImage)

			


		
