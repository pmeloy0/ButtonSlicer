#String searcher

from glob import glob

def searchFiles(_filelist,_string):
	ret = []
	for _filename in _filelist:
		with open(_filename) as f:
			for num, line in enumerate(f,1):
	
				if _string in line:
					ret.append(_filename + "(" + str(num)  +": " + line)
		return ret
	
running = True
while running:
	print("")
	_string=input("String to search for ")
	filelist = glob("*.py")	
	_found = searchFiles(filelist,_string)
	print(*_found)

