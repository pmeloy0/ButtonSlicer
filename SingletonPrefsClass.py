#Singleton Preferences

from PySide6.QtGui import QColor,QFont
from PySide6.QtCore import Qt
from os import path
from pubsub import pub
import json

class Preferences:
	_instance = None
	_dict = {}
	def __new__(cls, *args,**kwargs):
			if not Preferences._instance:
				Preferences._instance = super().__new__(cls)
				Preferences._instance.loadPrefs()
			return Preferences._instance

	def __init__(self):
		pass

# Thanks to Gribouillis on the python forum for telling me how to make it load only once!

#Source image sizes
	@property
	def sourceWidth(self):
		return self._dict["sourceWidth"]
	@sourceWidth.setter
	def sourceWidth(self,val):
		self._dict["sourceWidth"] = val
	@property
	def sourceHeight(self):
		return self._dict["sourceHeight"]
	@sourceHeight.setter
	def sourceHeight(self,val):
		self._dict["sourceHeight"] = val

#font properties
	@property
	def font(self):
		return QFont(self._dict["fontFamily"],self._dict["fontSize"])
	@property
	def fontSize(self):
		return self._dict["fontSize"]
	@fontSize.setter
	def fontSize(self,val):
		self._dict["fontSize"] = val
	@property
	def fontFamily(self):
		return self._dict["fontFamily"]
	@fontFamily.setter
	def fontFamily(self,val):
		self._dict["fontFamily"] = val
	@property
	def fontColor(self):
		return QColor.fromString(self._dict["fontColor"])
	@fontColor.setter
	def fontColor(self,val):
		print("fontcolor",val)
		self._dict["fontColor"] = val

#Button properties
	@property
	def buttonWidth(self):
		return self._dict["buttonWidth"]
	@buttonWidth.setter
	def buttonWidth(self,val):
		self._dict["buttonWidth"] = val
	@property
	def buttonHeight(self):
		return self._dict["buttonHeight"]
	@buttonHeight.setter
	def buttonHeight(self,val):
		self._dict["buttonHeight"] = val
	
#utils
	def showDict(self):
		print(self._dict)
		
	def setDefaults(self):
		print("Setting default prefs")
		self._dict = {
		"fontFamily":"None",
		"fontSize":16,
		"fontColor": "white",
		"sourceWidth":300,
		"sourceHeight":100,
		"buttonWidth":120,
		"buttonHeight":40
		}
		self.savePrefs()

	def loadPrefs(self):
		if path.exists("prefs.json"):
			print("Loading prefs")
			with open('prefs.json', 'r') as openfile:
				self._dict = json.load(openfile)
			print(self._dict)
		else:
			self.setDefaults()

	def savePrefs(self):
		self.showDict()
		print("Save singleton Prefs")
		_prefs = json.dumps(self._dict, indent=4)
		with open("prefs.json", "w") as outfile:
			outfile.write(_prefs)
