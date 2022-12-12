from glob import glob
filelist = glob("*.py")

def findTodo(filename):
	ret = []
	savelines = False
	linestring = ""
	with open(filename) as f:
		for num, line in enumerate(f,1):
			if savelines:
				if not "#</Todo>" in line:
					line = line.replace("#","")
					line = line.strip()
					if linenumber:
						string = "\033[1m" + filename + ":" + line.strip() + "(" + str(linenumber) + ")"+ "\033[0m"
						ret.append(string)
						linenumber = None
					else:
						linestring = "	" + line
						ret.append(linestring)
					linestring = ""
				else:
					savelines = False
					ret.append("")

			if "#<Todo>" in line:
				linenumber = num
				savelines = True
	return ret 

for filename in filelist:
	if filename != "TodoList.py":
		_str = findTodo(filename)
		for item in _str:
			print(item)

