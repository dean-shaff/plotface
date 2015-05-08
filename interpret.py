from numpy import *
import matplotlib.pyplot as plt

def interpreter(string):
	"""
	This function attempts to interpret user input 
	in order to create a meaningful graph
	This does all the processing -- it returns x and y arrays.

	Returns:

		- val_range: independent variable range 
		- fn: a string that contains the numpy functions to be evaluated 
		- mod_list: a list of the modifiers in fn 
		- method: plotting or solving and plotting diffeq? 
			if solve: method is a dictionary containing the initial values
			elif plot: method is a string
	"""
	method = str()
	string = string.lower()
	if 'plot' in string:
		method = 'plot'
	elif 'solve' in string:
		y_index = string.index('y')
		if string[y_index+1] == '"':
			type = 'second'
		elif string[y_index+1] == '\'' and string[y_index+2] == '\'':
			type = 'second'
		elif string[y_index+1] == '\'':
			type = 'first'

		method = {'solve':asarray([0,1.0])}

	else:
		method = 'plot' #assume default mode is plot

	try:
		relevant = string[string.index("=")+1::]
	except ValueError:
		relevant = string[string.index(' ')+1::]
	except ValueError:
		relevant = string

	rel_list = [phrase for phrase in relevant.split(',')]

	if len(rel_list) == 1:
		mod_list = []
		relevant = rel_list[0]

	if len(rel_list) > 1:
		mod_list = rel_list[1::]
		mod_list = [mod.strip() for mod in mod_list]
		num_mod = len(mod_list)
		relevant = rel_list[0]

	try:
		from_place = relevant.index('from')
		val_str = relevant[from_place+1::]
		val_str = val_str.split()
		val_range = []
		for val in val_str:
			try:
				val_range.append(float(val))
			except ValueError:
				continue
		x = arange(val_range[0],val_range[1],0.1)
	except (ValueError, IndexError):
		from_place = len(relevant)-1
		x = arange(-1,1,0.1)
		val_range = [-1,1]

	fn = relevant[:from_place]
	fn = relevant[:from_place].replace('x','{0}')
	if 'e{0}p' in fn:
		fn = fn.replace('e{0}p','exp')

	# print(fn)
	return val_range, fn, mod_list, method

def evaluater(x_val_range, fn, mod_list=None, mod_val=None, increment=0.1):
	"""
	This function returns a numpy array with the function evaluated
	properly.
	mod_list is the name of the modifier, eg "a" or "b"
	mod_val is the actual value of the modifier
	"""
	x = arange(x_val_range[0],x_val_range[1],increment)
	if mod_list != None and mod_val != None: 
		for index,mod in enumerate(mod_list):
			fn = fn.replace(mod,str(mod_val[index]))
	try:
		y = asarray([eval(fn.format(xi)) for xi in x])
	except (NameError,AttributeError):
		y = "Error"

	return x, y

def diffeqsolver(x_val_range, fn, mod_list=None, mod_val=None, increment = 0.1):
	pass

def gen_code(x_val_range, fn, mod_list=None, mod_val=None, increment=0.1):

	code = "\n\nfrom numpy import *\n"
	code += "import matplotlib.pyplot as plt\n\n"
	code += "def f(x,*args):\n\t"

	if mod_list != None:
		for mod in mod_list:
			code += "{} ".format(mod)
		code += "= args\n\t"
	code += "return "
	code += fn.replace("{0}","x")
	code += "\n\n"
	code += "x = arange({},{},{})\n".format(x_val_range[0],x_val_range[1],increment)
	code += "y = f(x,"

	if mod_list != None:
		for index in mod_list:
			code += "{},".format(mod_val[index])
	code += ")\n\n"
	code += "fig = plt.figure(figsize=(16,9))\nax = fig.add_subplot(111)"
	code += "ax.plot(x,y)"
	code += "plt.show()"

	return code






# print(evaluater([-10,10],"sin(a*{0})",['a'],[3]))
# print(interpreter("plot f(x)=cos(x)*sin(x) from -10 to 10"))
# print(interpreter("x**2"))
# print(interpreter("2.*x"))
