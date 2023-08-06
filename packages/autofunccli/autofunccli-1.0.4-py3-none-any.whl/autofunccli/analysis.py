"""
Script containing the funciton analysis process
"""
from inspect import getfullargspec,isfunction
import re
import argparse
from typing import Tuple,List
from enum import Enum
"""
Define accepted types
"""

#Accepted types for function argument
acceptedTypes = [
	bool,
	int,
	float,
	str,
	List,
	Tuple
]
#Accepted types for generic type argument
acceptedTypesArg = [
	bool,
	int,
	float,
	str,
]
#Accepted class to inherit
acceptedSubClass = [
	Enum
]

#Util function
def typeRep(t):
	"""
	Return a string representing a type
	"""
	try:
		if(t == None):
			return '?'
		else:
			return t.__name__
	except:
		return '?'
"""
Defining exceptions
"""

class UnsupportedTypeException(Exception):
	"""
	Exception to throw when a function argument doesn't have a supported type.
	"""
	def __init__(self,t,n):
		self.t = t
		self.n = n
	def __str__(self):
		out = '{} argument has type {} which is not accepted.'.format(self.n,self.t)
		out += '\nAccepted types are : {}'.format([str(e) for e in acceptedTypes])
		out += '\nAccepted type arguments are {}'.format([str(e) for e in acceptedTypesArg])
		return out

class WrongInputTypeException(Exception):
	"""
	Exception to throw when the input can't use to build an object from the argument type
	"""
	def __init__(self,n,value):
		self.n = n
		self.value = value
	def __str__(self):
		return 'Argument {} doesn\'t have the right type, input is {}, check the -h.'.format(self.n,self.value)

class NonHomogenousEnumTypeException(Exception):
	"""
	Exception to throw when an Enum type is use and doesn't have values with the same type.
	"""
	def __init__(self,n,types):
		self.n = n
		self.types = types
	def __str__(self):
		return 'Argument Enum {} doesn\'t have homogenous types {}, each values of the enum must be the same.'.format(self.n,self.types)

class EnumHasNoTypeException(Exception):
	"""
	Exception to throw when an Enum type is use and doesn't have any definied value.
	"""
	def __init__(self,n,t):
		self.n = n
		self.t = t
	def __str__(self):
		return 'Enum type {} of argument {} doesn\'t have any value.'.format(self.t,self.n)

class IsNotAFunctionException(Exception):
	"""
	Exception to throw when the input is not a function
	"""
	def __str__(self):
		return 'Argument is not a function.'


class FunctionArgument:
	"""
	Simple class to group informations about a function argument obtained with
	the inspect module
	"""
	def __init__(self,name,t,default,doc,index):
		self.name =name
		self.type = t
		self.default = default
		self.doc = doc
		self.index = index

class CommandArgument():
	"""
	Class to transform a function argument to an usable argument for the
	argparse.add_argument method.
	"""
	@staticmethod
	def __buildType(t,default,name):
		"""
		Analyse the type of a function argument and add parameters.
		list : nargs='*'
		optional : nargs='?'
		tuple[x,y...] : nargs='len(tuple)'
		add automatic argument parsing using builtin types.
		"""

		#Defines arrays containing the allowed type in order to compare them.
		aType = [str(c) for c in acceptedTypes]
		aArgType = [str(c) for c in acceptedTypesArg]
		subClsType = set([str(c) for c in acceptedSubClass])

		#output information
		parse = t
		representation = ''
		action = None
		nargs = None
		nDefault= default

		class typeManagement():
			"""
			Class to manipulate informations about function argument
			and get command argument.
			"""
			class parameters():
				"""
				Class to group informations about command argument
				"""
				def __init__(self,t,default):
					#function or class to use to parse the raw input
					self.parse = t
					#representation of the type
					self.representation = ''
					#action command argument
					self.action = None
					#nargs command argument
					self.nargs = None
					#default command argument
					self.default = default
					#choice command argument
					self.choices = None
				"""
				Return the informations as an array to make assignation easier.
				"""
				def toArr(self):
					out = [self.parse]
					out += [self.representation]
					out += [self.action]
					out += [self.nargs]
					out += [self.default]
					out += [self.choices]
					return out

			def __init__(self,t,default):
				#default type of the input defined with annotation
			   self.t = t
			   #Default value of the argument
			   self.default = default
			   #Parameters to manipulates
			   self.parameters = typeManagement.parameters(t,default)

			def toTuple(self):
				"""
				Transform the function argument to a tuple command argument :
					- nargs : length of the tuple type list
					- parse : parse each values with the corresponding types
					- represention : show the tuple types
				"""
				self.parameters.nargs = len(self.t.__args__)
				self.parameters.parse = (lambda src:tuple([self.t.__args__[i](x) for i,x in enumerate(src)]))
				self.parameters.representation = ','.join([typeRep(x) for i,x in enumerate(self.t.__args__)])

			def toList(self):
				"""
				Transform the function argument to a list command argument :
					- nargs : '+'
					- parse : parse each values with the list type
					- represention : show the list type
				"""
				self.parameters.nargs = '+'
				self.parameters.parse = (lambda src:[self.t.__args__[0](x) for i,x in enumerate(src)])
				self.parameters.representation = 'List[{}]'.format(typeRep(self.t.__args__[0]))

			def toChoices(self):
				"""
				Transform the function argument to a choices command argument :
					- choices : choices as string
					- parse : parse each values with the enum type (obtained by analyzing values of the enum)
				"""
				enumTypes = set([type(e.value) for e in self.t])
				if(len(enumTypes)>1):
					raise NonHomogenousEnumTypeException(name,set([type(e.value) for e in self.t]))
				if(len(enumTypes)==0 ):
					raise EnumHasNoTypeException(name,self.t)
				enumType = enumTypes.pop()

				if(not(str(enumType) in aType)):
					raise UnsupportedTypeException(enumType,name)

				self.parameters.choices = [str(e.value) for e in self.t]
				self.parameters.parse = (lambda src:self.t(enumType(src)))

			def toBool(self):
				"""
				Transform the function argument to a boolean command argument :
					- represention : show the boolean type
					- if the default value is True use 'store_false' as action else 'store_true'
				"""
				if(self.default):
					self.parameters.action = 'store_false'
				else:
					self.parameters.action = 'store_true'
					self.parameters.default = False
				self.parameters.representation = typeRep(self.t)

			def toType(self):
				"""
				Transform the function argument to a simple command argument :
					- parse : type of the function argument
					- represention : type of the function argument
				"""
				self.parameters.parse = self.t
				self.parameters.representation = typeRep(self.t)

			def toOther(self):
				"""
				If there is no type, convert it to a string
				"""
				self.parameters.parse = str
				self.parameters.representation = typeRep(str)

			def analyse(self):
				"""
				Analyze the function argument type to convert it to a command argument
				"""

				#Define the accepted generic type and the function to use to process
				switchGeneric = {
					str(tuple) : self.toTuple,
					str(list) : self.toList
				}
				#If the type is defined
				if(self.t!=None and type(self.t)!=type(None)):
					#Get the class from which the type derived
					baseTypes = set([str(b) for b in self.t.__bases__]) if hasattr(self.t,'__bases__') else []
					#Test if it's a generic type
					if(hasattr(t,'__args__')):
						if(str(t.__origin__) in switchGeneric):
							#Test if the generic type is accepted
							genBaseTypes = set([str(c) for c in t.__args__ if not(str(c) in aArgType)])
							if(len([c for c in t.__args__ if not(str(c) in aArgType)])>0):
								raise UnsupportedTypeException(self.t,name)
							#Process the generic type
							switchGeneric[str(t.__origin__) ]()
						else:
							raise UnsupportedTypeException(self.t,name)
					else:
						#Test if the type is available
						if(not(str(self.t) in aType)
							and not(baseTypes.intersection(subClsType))):
							raise UnsupportedTypeException(self.t,name)
						#Test if the class derived from an enum
						if(baseTypes.intersection(subClsType) == {str(Enum)}):
							#Process the enum as a choices argument
							self.toChoices()
						#Process a boolean argument
						elif self.t==bool:
							self.toBool()
						#Process other types
						else:
							self.toType()
				else:
					#Process argument with no type
					self.toOther()
				return self.parameters.toArr()

		return typeManagement(t,default).analyse()

	@staticmethod
	def __buildHelp(fArg:FunctionArgument,rep,default):
		"""
		Generate the help command argument
		"""
		return fArg.doc + (' : <'+rep +'>' if rep else '')+ ('('+str(default)+')' if default !=None else '')

	#Initialise the set which track same shortcut names
	previousName = set()
	def __init__(self,fArg:FunctionArgument):

		#Transform the function argument to command argument
		[
			self.parse,
			representation,
			self.action,
			self.nargs,
			self.default,
			self.choices
		] = CommandArgument.__buildType(fArg.type,fArg.default,fArg.name)
		self.name = [fArg.name] if self.default==None else ['-'+fArg.name[0],'--'+fArg.name]
		#Test if there is no shortcut name conflicts
		if(len(self.name)>1):
			if(len(CommandArgument.previousName.intersection({self.name[0]}))>0):
				self.name = [self.name[1]]
			else:
				CommandArgument.previousName.add(self.name[0])
		self.help = CommandArgument.__buildHelp(fArg,representation,self.default)

	def toCommand(self):
		#Return a dict represention of the object to use as a kwarg for the command argument
		out = {
			'help':self.help,
		}
		#Avoid non co-existing argument
		if(self.action):
			out.update({
				'action':self.action
			})
		elif(self.choices):
			out.update({'choices':self.choices})
		else:
			out.update({
				'type' :str
			})
		if(self.default!=None):out.update({'default':self.default})
		if(self.nargs):out.update({'nargs':self.nargs})
		return out


class FunctionReturn:
	"""
	class for representing the return type and documentation of a function
	"""
	def __init__(self,t,doc):
		self.type = t
		self.doc = doc



class FunctionArgParser():
	"""
	Parse a function to extract arguments,annotations and documentation
	to build an argparser from it.
	"""
	__paramReg = re.compile(":\s*(\w+)\s*(\w*)\s*:(.*)\\n?")
	@staticmethod
	def __extractDoc(func):
		"""
		Return the description of the function and its parameters using
		the doc.
		"""
		if(not(isfunction(func))):
			raise IsNotAFunctionException()
		doc = func.__doc__
		#Extract param docstring
		params = FunctionArgParser.__paramReg.findall(doc) if doc else ''
		desc = doc[0:FunctionArgParser.__paramReg.search(doc).span()[0]] if doc and FunctionArgParser.__paramReg.search(doc) else doc
		desc = '\n'.join([s.strip() for s in desc.split('\n')]) if doc else ''
		retDesc = ''
		paramsDesc = {}

		for i in params:
			if(i[0]=="param"):
				paramsDesc[i[1]] = i[2].strip()
			if(i[0]=="return"):
				retDesc = i[2].strip()


		return desc,paramsDesc,retDesc

	@staticmethod
	def __extractArgs(func,argDoc,retDoc):
		"""
		return informations of the function and transform them to command arguments
		"""
		args = []
		spec =  getfullargspec(func)
		defautls_set = spec.defaults if spec.defaults else []
		annotations = spec.annotations if spec.annotations else []
		varNames = spec.args
		#Getting types
		types = {d:None for d in varNames}
		types.update({'return':None})
		for k in types:
			if(k in annotations):
				types[k] = annotations[k]
		#Getting default values
		defaults = {d:None for d in varNames}
		for i in range(len(varNames)-len(defautls_set),len(varNames)):
			defaults[varNames[i]] = defautls_set[i-len(defautls_set)]
		#Getting index
		index = {}
		for i in range(0,len(varNames)):
			index[varNames[i]]=i
		#Transform each arguments
		for n in varNames:
			if(not(n in argDoc)):argDoc[n]=''
			if(not(n in types)):types[n]=str
			if(not(n in defaults)):defaults[n]=None
			args.append(FunctionArgument(n,types[n],defaults[n],argDoc[n],index[n]))
		returned = FunctionReturn(types['return'],retDoc)
		return args,returned

	def __init__(self,func):
		#Initialise the set which track same shortcut names
		CommandArgument.previousName = set()
		self.argList = []
		self.ref = func
		self.name = func.__name__
		self.doc,argDoc,retDoc = FunctionArgParser.__extractDoc(func)
		self.argList,self.ret = FunctionArgParser.__extractArgs(func,argDoc,retDoc)
		self.commandList = [CommandArgument(a) for a in self.argList]
		#Define how to parse each raw values from the command parser results
		self.postParse = {self.argList[i].name:x.parse for i,x in enumerate(self.commandList)}
		if(self.ret):
			self.epilog = '\n\t[RETURN] '
			self.epilog+=((self.ret.doc) if self.ret.doc else '')
			self.epilog+=((': <'+typeRep(self.ret.type)+'>') if self.ret.type else '')
	def toArgParse(self):
		"""
		Convert the analyzed function to an argparser.
		"""
		parser = argparse.ArgumentParser(description=self.doc,epilog=self.epilog)
		for arg in self.commandList:
			parser.add_argument(*arg.name,**(arg.toCommand()))
		return parser

	def parse(self,*arg,**kwargs):
		"""
		Parse an input using the function parser and return the result
		If there is no input, try to parse sys.argv.
		"""
		parser = self.toArgParse()
		if(parser):
			parsed = parser.parse_args(*arg,**kwargs)
			out = {}
			if(parsed):
				for k,value in parsed._get_kwargs():
					try:
						out.update({k:self.postParse[k](value)})
					except:
						raise WrongInputTypeException(k,value)
			return self.ref(**out)

	def __call__(self,*arg,**kwargs):
		self.ref(*arg,**kwargs)

	def main(self,__name__):
		if(__name__=='__main__'):
			return self.parse()
		else:
			return None