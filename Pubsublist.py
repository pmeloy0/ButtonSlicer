from glob import glob
filelist = glob("*.py")

def findTodo(filename):
	print("Checking",filename)
	ret = []
	savelines = False
	linestring = ""
	with open(filename) as f:
		for num, line in enumerate(f,1):
			if "pub." in line:
				string = "\033[1m" + filename + ":" + line.strip() + "(" + str(num) + ")"+ "\033[0m"
				print(string)


	# ~ theList = []
	# ~ theList.append("FileName")
	# ~ theList.append(3)
	# ~ theList.append(66)
	return ret 
 
for filename in filelist:
	if filename != "TodoList.py":
		_str = findTodo(filename)
		for item in _str:
			print(item)

