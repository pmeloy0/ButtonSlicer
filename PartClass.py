from PySide6.QtWidgets import QWidget,QLabel,QGridLayout,QFileDialog,QSlider,QPushButton
from PySide6.QtCore import QSize,Qt
from pubsub import pub
from SingletonPrefsClass import Preferences

Prefs = Preferences()

class PartImage(QWidget):
	Image = None # Edited version for display and use by slicerbutton
	def __init__(self,which,*args,**kwargs):
		super().__init__(*args,**kwargs)
		pub.subscribe(self.newSrc, 'new_source_image')
		self.setMinimumWidth(Prefs.sourceWidth+50)
		self.setMinimumHeight(Prefs.sourceHeight+80)
		self._baseImage = None #Unedited version from src to create edited version
		self._partNames = ["Left","Mid","Right"]
		self._which = which
		self._minWidthVal = 5
		self._maxWidthVal = 150
		self._start = 0 
		self._partStart = which * 100 #slStart min value for part type
		self._baseWidth = 0 # Width of the _baseImage
		self._partWidth = 0 #Width of the part (1/3 of _baseImage)
		self._width = 0
		self._maxWidthVal = 100


		
		self._gridLayout = QGridLayout(self)

		self._lblTitle = QLabel()
		self._lblTitle.setScaledContents(True)
		self._lblTitle.setAlignment(Qt.AlignCenter)


		self._lblImage = QLabel()
		self._lblImage.setAlignment(Qt.AlignCenter)

		self._gridLayout.addWidget(self._lblImage, 1, 1, 1, 4,Qt.AlignCenter)
#<Todo>
#PartClass Layout
#Figure out how to align title labels properly and get the sizes of the widgets the same
#</Todo>
		if self._which == 0:
			self._lblTitle.setAlignment(Qt.AlignLeft)
			self._lblTitle.setText("Left Part")
			self._gridLayout.addWidget(self._lblTitle, 0, 1,Qt.AlignLeft)		
		elif self._which == 1:
			self._lblTitle.setAlignment(Qt.AlignCenter)
			self._lblTitle.setText("Middle Part")
			self._gridLayout.addWidget(self._lblTitle, 0, 1,Qt.AlignCenter)		
		else:
			self._lblTitle.setAlignment(Qt.AlignRight)
			self._lblTitle.setText("Right Part")
			self._gridLayout.addWidget(self._lblTitle, 0, 1,Qt.AlignRight)		
			
		self._slStart = QSlider()
		self._slStart.setMinimum(0)
		self._slStart.setMaximum(95)
		self._slStart.setValue(0)
		self._slStart.setOrientation(Qt.Horizontal)
		self._gridLayout.addWidget(self._slStart, 3, 2, 1, 2)
		self._slWidth = QSlider()
		self._slWidth.setMinimum(self._minWidthVal)
		self._slWidth.setMaximum(self._maxWidthVal)
		self._slWidth.setValue(self._maxWidthVal)
		self._slWidth.setOrientation(Qt.Horizontal)
		self._gridLayout.addWidget(self._slWidth, 4, 3, 1, 1)
		self._lblStart = QLabel("Start")
		self._gridLayout.addWidget(self._lblStart, 3, 1)

		self._lblWidth = QLabel("Width")
		self._gridLayout.addWidget(self._lblWidth, 4, 1)		


		self._slStart.valueChanged.connect(self.setStart)
		self._slWidth.valueChanged.connect(self.setWidth)
		

	def setStart(self,val):
		if self._baseImage != None:
			self._start =  val
			self.editImage()
				
	def setWidth(self,val):
		if self._baseImage != None:
			self._width = val
			self.editImage()
				
	def newSrc(self,image):
		self._baseImage = image
		self._baseWidth = image.width()
		self._partWidth = self._baseWidth // 3
		self._partStart = self._partWidth * self._which
		self._height = image.height()
		self._slStart.setValue(0)
		self._slStart.setMaximum(self._partWidth)
		self._slWidth.setMinimum(self._minWidthVal)
		self._slWidth.setMaximum(self._partWidth)
		self._slWidth.setValue(self._partWidth)
		self._width = self._partWidth
		self.editImage()

	def editImage(self):
		if self._baseImage != None:
			_start = self._partStart + self._start
			self.Image = self._baseImage.copy(_start,0,self._width,self._height)
			self._lblImage.setPixmap(self.Image.scaledToHeight(Prefs.sourceHeight))
			if self._which == 0:
				pub.sendMessage('new_left_image',image = self.Image)
			elif self._which == 1:
				pub.sendMessage('new_mid_image',image = self.Image)
			elif self._which == 2:
				pub.sendMessage('new_right_image',image = self.Image)
	
