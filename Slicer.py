import sys
from pubsub import pub
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from SingletonPrefsClass import Preferences
from SourceImageClass import SourceImage
from PartClass import PartImage
from PartCombinerClass import PartCombiner
from CaptionClass import Caption
from SaveClass import SaveClass

DEBUG = False
Prefs =  Preferences()
		#<Todo>
		# All
		# Learn layouts better
		#</Todo>

class ButtonSlicer(QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if DEBUG:
			pub.subscribe(self.newSrc, 'new_source_image')
			pub.subscribe(self.newLeftPart, 'new_left_image')
			pub.subscribe(self.newMidPart, 'new_mid_image')
			pub.subscribe(self.newRightPart, 'new_right_image')
		self._src = SourceImage()
		self._left = PartImage(0)
		self._mid = PartImage(1)
		self._right = PartImage(2)
		self._butCombiner = PartCombiner()
		self._captioner = Caption()
		self._saver = SaveClass()
		
		self._gridLayout=QGridLayout(self)
		self._gridLayout.addWidget(self._src,0,0)
		self._gridLayout.addWidget(self._butCombiner,0,1,Qt.AlignTop)
		self._gridLayout.addWidget(self._captioner,0,2,Qt.AlignTop)
		self._gridLayout.addWidget(self._saver,0,3,Qt.AlignTop)		
		self._gridLayout.addWidget(self._left,1,0)
		self._gridLayout.addWidget(self._mid,1,1)
		self._gridLayout.addWidget(self._right,1,2)
		self.show()
		
	def newSrc(self,image):
		print("<<< Source Image Changed",image.width(),image.height())
	
	def newLeftPart(self,image):
		print("<<< Left Part Image Changed",image.width(),image.height())

	def newMidPart(self,image):
		print("<<< Mid Part Image Changed",image.width(),image.height())

	def newRightPart(self,image):
		print("<<< Right Part Image Changed",image.width(),image.height())
		
	
app = QApplication(sys.argv)
prog = ButtonSlicer()
prog.show()
app.exec()
