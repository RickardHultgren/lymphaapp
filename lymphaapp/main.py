
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

#from lympha import *
#import lympha as lympha

sm = ScreenManager()



#pfrom browser import document, bind, html, alert, window
#from javascript import this

#???			
addresses = list()
import subprocess

import sys

#for the graph function:
import os

#regex
import re

def recursive_parse(node,substitutions):
	if hasattr(node.left,"id"):
		if node.left.id in substitutions.keys():
			node.left = substitutions[node.left.id]
	else:
		recursive_parse(node.left,substitutions)

	if hasattr(node.right,"id"):
		if node.right.id in substitutions.keys():
			node.right = substitutions[node.right.id]
	else:
		recursive_parse(node.right,substitutions)

title = str()
prefilenames = list()
prestarts = list()	

# Variables for " 1. Program call through bash-CLI.".
CLI_filename = ""
argv_len = len(sys.argv)
filenames = list()
filename = ""

presteps = int()

# List of statements that should be executed during step 0:
starts = list()

# Steps given from the CLI-command:
steps = 0

local_files = True

# Depending on what the interpreter is supposed to do different modes are used:
mode_graph = False
mode_state = False
mode_exe = False
mode_show = False
mode_map = False

#Graphviz
#d3 = window.d3

# Check if all script files are loaded:
filecheck = False

# Lists of statements:
exe_list = list()
show_list = list()
map_list = list()
series = list()
substates = list()
nextstates = list()
specs = list()

# LYMPHA-langugage grammar:
global_relative_variable1 = None
global_relative_variable2 = None
operator1 = None
statement_value = str()
statement_flow = int()

# Objects to be executed:
exe_objects = list()

CLIcom_segment = 0



#Construction of the section model of the linked list.
class Statement(dict):
	MARKER = object()

	def __init__(self, value=None):
		if value is None:
			pass
		elif isinstance(value, dict):
			for key in value:
				self.__setitem__(key, value[key])
		else:
			raise TypeError('expected dict')

	def __setitem__(self, key, value):
		if isinstance(value, dict) and not isinstance(value, Statement):
			value = Statement(value)
		super(Statement, self).__setitem__(key, value)

	def __getitem__(self, key):
		found = self.get(key, Statement.MARKER)
		if found is Statement.MARKER:
			found = Statement()
		super(Statement, self).__setitem__(key, found)
		return found

	__setattr__, __getattr__ = __setitem__, __getitem__


# A list of all objects:
object_list = dict()
object_list = Statement(object_list)

#class Statement:
#    def __init__(self, flow, name, global_relative_variable1, global_relative_variable2, statement_flow, statement_value, operator1, next_list, binary_list, operation, spec_list):
#        
#        self.flow = int(flow)
#                
#        #list of next nodes:
#        #next_list = next_list
#       self.next_list = list(next_list)
#        
#        #list of specifications:
#        #spec_list = spec_list
#        self.spec_list = list()#
#
#        #list of contents:
#        #binary_list = binary_list
#        self.binary_list = list(binary_list)#
#
#        #should the binary_list be counted as a sum or an equation?
#        #self.summerize = summerize
#        self.operation = operation  #This holds the operation that are found in the string (left to right)
#        
#        #name
#        self.name = name
#        
#        #tipping point
#        self.global_relative_variable1 = global_relative_variable1
#
#        #tipping point
#        self.global_relative_variable2 = global_relative_variable2
#        
#        #relational operator
#        self.operator1 = operator1#
#
#        #statement_flow
#        self.statement_flow = statement_flow
#        #if statement_flow == 0 :self.statement_flow = 0
#        #else: self.statement_flow = 1#
#
#        #statement_value
#        self.statement_value = statement_value


def stripComments(code):
	code = str(code)
	return re.sub(r'(?m)^ *#.*\n?', '', code)

def lexer():

	global CLIcom_segment
	global series
	global filenames
	global local_files
	#Load file content

	global prefilenames 
	global prestarts 
	filenames = prefilenames
	starts = prestarts

	if local_files == True:
		for filename in filenames:
			textfile = open(filename, 'r')
			filetext = textfile.read()
			filetext = stripComments(filetext)
			filetext = filetext.replace('\n', ' ')
			filetext = filetext.replace('  ', ' ')
			series.extend(filetext.split(';'))
######

######
	global object_list

	nexts = list()
	conts = list()
	#Make new nodes in database
	for serie in series:
#					document <= serie
# Strategy for splitting:
# words a-z A-Z 0-9
# space = - + \s ->
# 
# 
		prearrowobjs = serie.split('->')
		#arrowobjs = re.split('->|=|\+|\-',serie)
		arrowobjs = list()
		for anobj in prearrowobjs:
			almostdone = anobj.split('=')
			arrowobjs.append(almostdone[0])
		count = 0
    
		oops = str() #
		nexts = list()
		conts = list()
		specs = list()
		flow = int()
		global_relative_variable1 = float()
		operator1 = str()
       
		statement_flow = int()
		statement_value = str()
		scale = list()
		# Devide the script's line strings into objects:

		#print(object_list)

		pre_count = int(0)
		count_objs = int()                 
		#alert("60")
		for anobj in arrowobjs:
			anobj = re.sub("\s*", "", anobj) 
			#alert(anobj)
			eqobjs = re.compile(r"((<=)|(>=)|(!=)|(==)(<)|(>))").split(anobj)
			taken = 0
			#Check if the object already exists
			for takenkey in range(0,len(object_list)) :
				if object_list[takenkey].name == anobj :
					taken = 1

				#Avoid number gaps
				else:
				#Spin the list to the end
					pre_count += 1
			count_objs = pre_count
			#Add node at the end of the dicts
			#count_objs -= 1            
			if (anobj) != "" and taken == 0 :

				object_list[((count_objs))].name = str(anobj)

				object_list[((count_objs))].next_list = list()
				object_list[((count_objs))].binary_list = list()
				object_list[((count_objs))].operation = str("")
				object_list[((count_objs))].flow = 1
				object_list[((count_objs))].statement_flow = 1
				object_list[((count_objs))].statement_value = str()
				object_list[((count_objs))].global_relative_variable1 = float()
				object_list[((count_objs))].datatype = ""

	#Connect the database nodes     
	for serie in series:
		arrowobj = serie.split('->')
		count = 0
		nexts = list()
		conts = list()
		# Connect to the next object

		for i in range(0,len(arrowobj)):

			for key in range(0,len(object_list)):

				thename = str(object_list[key].name)
				thename = re.sub("\s*", "", thename) 
				if i != 0 :
					if thename == arrowobj[(0)].replace(" ",""):

						nexting = ""
						nexting = arrowobj[i].replace(" ","")
						if not nexting == "" :
							object_list[key].next_list.append(nexting)
						#print(object_list[key].next_list)
						#print(object_list[key].name)
	#Connect to depending objects:
	#Types of continuations of the side2 string:
	# 1. Operator + Sum of binaries
	# 2. Operator + Equation and value
	# 3. Constant value
	count = 0
	for serie in series:
		if " = " in serie :
			count = 0
			sides = serie.split(' = ')
			side1 = str(sides[0])
			side2 = str(sides[1])
			side1 = side1.replace(" ","")
			side2 = side2.replace(" ","")
			for key in range(0,len(object_list)) :
				#Web version TRY############
				try:
					thename = object_list[key].name
					if ("%s" % thename) == sides[0].replace(" ", "") :
						try:
						
						#For evaluations
						# Check if operator:
							if ("==" in sides[1] or "!=" in sides[1] or "<=" in sides[1] or ">=" in sides[1] or "<" in sides[1] or ">" in sides[1] ) and not "->" in sides[1]:
								if "==" in (sides[1]) :
									object_list[key].operator1="equiv"
	#                            if re.compile(".*>=.*").match(sides[1]) :
								if ">=" in (sides[1]) :
									object_list[key].operator1="geq"
	#                            if re.compile(".*<=.*").match(sides[1]) :
								if "<=" in (sides[1]) :
									object_list[key].operator1="leq"
	#                            if re.compile(".*(!=).*").match(sides[1]) :
								if "!=" in (sides[1]) :
									object_list[key].operator1="no"
								if re.compile(".*>.*").match(sides[1]) and not re.compile(r"(>=)").match(sides[1]) :
									object_list[key].operator1="g"
								if re.compile(".*<.*").match(sides[1]) and not re.compile(r"(<=)").match(sides[1]) :
									object_list[key].operator1="l"
								#print(object_list[key].operator1)
								preop = sides[1].replace(" ","")
								bin_chopped = 0
								if "\|{" in preop or "|{" in preop :
								#if "\|{" in preop and "}|" in preop :
									bin_chopped = 1
								preop = re.sub(r'(\|{)', ' ', preop)
								preop = re.sub(r'(}\|)', ' ', preop)                            
								#preop = preop.replace("}|","")
								#preop = re.sub("\|{","", preop)
								chopcompile = re.compile(r"(<=|>=|!=|==|<|>)")
								operator_chop = re.split(chopcompile, preop)
								#alert("operator_chop:[%s]" % operator_chop)
								#Tipping point
								zerochop = operator_chop[0].replace(" ","")
								object_list[key].global_relative_variable1 = zerochop 
								# chopped into binary list                               
								if bin_chopped == 1 :
										#alert("check1")
										binary_sums = list(operator_chop[2].split(','))
										for binary in binary_sums:
											binary = binary.replace(" ","")
											if binary != "" :
												binary = str(binary.replace(" ",""))
												object_list[key].binary_list.append(str(binary))
											object_list[key].datatype = "bineval"
											#object_list[key].binary_list = list(the_bin_list)<
								elif bin_chopped == 0 :
									object_list[key].statement_value = operator_chop[2]
									object_list[key].datatype = "nonbineval"
	
						#For non-binary values and equations
							elif sides[0] != ""  and sides[1] != "" :
								# # # #print("YYY %s" % object_list[key].name)
								#if 0 == len(operator_chop) :
								object_list[key].statement_value = sides[1] 
								object_list[key].datatype = "valu"                               
						except:
							pass								
	
				except:
					pass
		count += 1          


def turn2func(ev) :
#The goal is to implement the first step factors
	global object_list
	for an_obj in range(0,len(object_list)): 
		for a_name in document.select(".factorItems"):
			try:	
				if a_name.id == object_list[an_obj].name and a_name.id != "" :
					object_list[an_obj].statement_value  = a_name.value
					if a_name.value == "1B" or  a_name.value == "0B" : 
						object_list[an_obj].datatype = "bina"
						object_list[an_obj].value = a_name.value
					elif nomen.isdigit() == True:
						object_list[an_obj].datatype = "valu"
						object_list[an_obj].value = a_name.value                        
					#else:
						#object_list[an_obj].datatype = "nonbineval"
			except:
				pass
# End results: name, statement_value, datatype:(bina, valu)
	try:
		del starts[:]          
	except:
		pass
	try:
		for start_item in document.select(".theStarts"):
			starts.append(start_item.value)
			temporary_starts.append(start_item.value)
	except:
		pass
	mapfunc()


#document["turn2"].bind("click", turn2func)
#document["addbttn"].bind("click", add_input)
#document["addstart"].bind("click", add_start)
#document["zcriptbttn"].bind("click", zcripts)
#document["menubttn"].bind("click", changeMenu)

#document.getElementById( "index").style.backgroundColor='#EFAB00'
#document.getElementById( "indexsmall").style.backgroundColor='#EFAB00'
#document.getElementById( "index").style.color='#ffffff'
#document.getElementById( "index").className="index2active"

##################
start_turn=0
step_turn=0
#class ScreenOne(FloatLayout):
class ScreenOne(Screen):
    
	inputlabel1 = NumericProperty(0)    
	#def __init__(self, **kwargs):
	def update(self,dt):
				#super().__init__(**kwargs)
        #mainfunc()
				global sm
				global sc1
				global title
				self.switch = Switch()
				#self.clear_widgets()
				h_box = BoxLayout(orientation='horizontal')
				v_box = BoxLayout(orientation='vertical')
        #my_show_list = ["My Way", "Wine Drinker", "Boots"]
				h_box.my_buttons = [] # if you want to keep an "easy" reference to your buttons to do something with them later
                               #kivy doesnt crashes because it creates the property automatically
				#for message in my_show_list:
				switch_box = BoxLayout(orientation='vertical')
				label = Label(text=title)
				#switch = Switch()
				#switch.bind(active=callback)

				#try:
				#	for numbr in range(1, 5):
						#for start in starts:
				#			mapfunc()
				#			label = Label(text=title)
				#			sm.add_widget(sc1)
				#			Clock.unschedule(sc1.__init__())
				#			return sm
				
        #except:		
				#	pass
				switch_box.add_widget(label)
				switch_box.add_widget(self.switch)
				#h_box.my_buttons.append(switch_box)
				h_box.add_widget(switch_box)
				v_box.add_widget(h_box)            
				#self.add_widget(h_box)            
				okbtn = Button(text="OK")
        #okbtn.bind(on_press=self.oking)          
				okbtn.bind(on_press=self.mapfunc)
				v_box.add_widget(okbtn)            
				#self.remove_widget(self.('main'))
				self.add_widget(v_box)               
				#self.manager.current = 'screen1'
				

#Function for running the linked list.
	def mapfunc(self,*args):
	#def mapfunc(self,dt):
		#global d3
		#global UI
		#global CLI_filename 
		global start_turn
		global step_turn
		global sm
		global sc1
		global title
		global argv_len 
		global filename 
		global filenames 
		global mode_graph 
		global mode_state 
		global filecheck 
		global mode_exe 
		global mode_show 
		global mode_map 
		global exe_list 
		#global show_list 
		global map_list 
		global series 
		global substates 
		#global nextstates 
		nextstates  = list()
		global specs 
		#global global_relative_variable1 
		global global_relative_variable2 
		#global operator1 
		global statement_flow 
		global statement_value
		global object_list 
		global exe_objects 

		global starts
		global show_list
		global steps
		#if mode_graph == True:
		graphstr = 'digraph lympha {\nnode [shape=record];'
		#ADDED INT IN INT(STEPS)

		global prefilenames 
		global prestarts 
		breaking = False
		filenames = prefilenames
		starts = prestarts
		step_count = 0 
		start_count = 0 
		turned = False
		for step in range(0, int(steps)):
			if step_count > step_turn :
				#step_count += 1
				turned = True
				##breaking = False
			if step_count < step_turn :
				step_count += 1
				turned = False
				#breaking = False
			if step_count == step_turn :
				step_turn += 1
				step_count += 1
				#nextstates = list()
				#print("Steps: %s" % steps)
				checked = 0 
				for start in starts:
					if start_count > start_turn :
						#start_count += 1
						#breaking = True
						turned = False
					if start_count < start_turn :
						start_count += 1
						#breaking = True
						turned = False
					if start_count == start_turn and turned == False:
						#breaking = False
						turned = True
						self.clear_widgets()
						start_turn += 1
						start_count += 1
						for key in range(0,len(object_list)):
							endstring = str()
							strr=str("%s" % object_list[key].name)
							strr = re.sub("\s+", "", strr.strip())

							#sm.add_widget(sc1)
							#Clock.unschedule(sc1.__init__())
							#return sm
							if str(start) == strr :
								# # # #print("mapfunvc")
								#title = object_list[key].name
								if object_list[key].flow == 0 or object_list[key].statement_flow == 0:
									pre_statement_flow = 0
								else:
									if object_list[key].name[-1] != "?":
######28
										pre_statement_flow = 0
										title = object_list[key].name
										if step == 0 :
											object_list[key].flow = 1
											object_list[key].statement_flow = 1
										#if mode_exe == True :	
											#ScreenOne.procedure(object_list[key].name)
											#title = object_list[key].name
									else:
										#ScreenOne.procedure(object_list[key].name)
										title = object_list[key].name							        
										if object_list[key].flow == 1 or object_list[key].statement_flow == 1:
											pre_statement_flow = 1
										else:
											pre_statement_flow = 0

										#document <= ("NAME: %s" % object_list[key].name)
				
										#For binaries
										if object_list[key].datatype == "bina":	
											if object_list[key].statement_value == "1B" :
												pre_statement_flow = 1
												object_list[key].statement_flow = 1
											if object_list[key].statement_value == "0B" :
												pre_statement_flow = 0
												object_list[key].statement_flow = 0
											checked = 1

										#For binary evaluation
										#if object_list[key].datatype == "bineval" :# and len(object_list[key].binary_list) >= 1:
										if len(object_list[key].binary_list) >= 1:
											pre_statement_flow = 0
											subfactors = list()
											#Convecrting variables into values
											for binobj in object_list[key].binary_list :
												for item in range(0,len(object_list)) :
													thename = object_list[item].name
													thename = str(thename)
													#thename = thename[1:]
													#thename = thename[:1]
													#thename = re.sub("\s+", "", thename.strip())
													#if object_list[item].name == binobj.replace(" ","") :
													if thename == ("%s" % binobj.replace(" ","")) :
														pass
														#subfactors.append(int(int(object_list[item].value[:-1])))
											sum1 = subfactors.count(1)
											sum0 = subfactors.count(0)
											if object_list[key].operator1 != None: # and object_list[key].statement_flow == None :
												if object_list[key].operator1 == "equiv" and int(object_list[key].global_relative_variable1) == int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "geq" and int(object_list[key].global_relative_variable1) >= int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "leq" and int(object_list[key].global_relative_variable1) <= int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "no" and int(object_list[key].global_relative_variable1) != int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "g" and int(object_list[key].global_relative_variable1) > int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "l" and int(object_list[key].global_relative_variable1) < int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												else:
													pre_statement_flow = 0
												#print(object_list[key].statement_value)
											object_list[key].statement_flow = int(pre_statement_flow)       
											checked = 1

							#For binary equations:
							#if object_list[key].datatype == "bineval" and len(object_list[key].binary_list) >= 1:
							#	#alert("begin B2")
								#pre_statement_flow = 0
								#subfactors = list()
								#Convecrting variables into values
								#for binobj in object_list[key].binary_list :
								#		for item in range(0,len(object_list)) :
								#			thename = object_list[item].name
								#			thename = str(thename)
								#		 #thename = thename[1:]
								#		 #thename = thename[:1]
								#		 #thename = re.sub("\s+", "", thename.strip())
								#		 #if object_list[item].name == binobj.replace(" ","") :
								#			if thename == ("%s" % binobj.replace(" ","")) :
								#				subfactors.append(int(object_list[item].statement_flow))
								#sum1 = subfactors.count(1)
								#sum0 = subfactors.count(0)
								#pre_statement_flow = 1

								#alert("begin B3")
											if object_list[key].operator1 != None: # and object_list[key].statement_flow == None :

												if object_list[key].operator1 == "equiv" and int(object_list[key].global_relative_variable1) == int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "geq" and int(object_list[key].global_relative_variable1) >= int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "leq" and int(object_list[key].global_relative_variable1) <= int(sum1):
													pre_statement_flow = 1
													object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
												elif object_list[key].operator1 == "no" and int(object_list[key].global_relative_variable1) != int(sum1):
													pre_statement_flow = 1
												object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
											elif object_list[key].operator1 == "g" and int(object_list[key].global_relative_variable1) > int(sum1):
												pre_statement_flow = 1
												object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
											elif object_list[key].operator1 == "l" and int(object_list[key].global_relative_variable1) < int(sum1):
												pre_statement_flow = 1
												object_list[key].statement_value = ("score: %s\nthreshold: %s" % (sum1, object_list[key].global_relative_variable1))
											else:
												pre_statement_flow = 0
								#alert("begin B4")
								object_list[key].statement_flow = int(pre_statement_flow)   
								object_list[key].flow = int(pre_statement_flow)        
								checked = 1

							#alert("begin C1")
							#For equations
							if object_list[key].datatype == "valu":
							#if object_list[key].statement_value != "" and object_list[key].operator1 == "" :

										#comp = re.compile(r'(\d*)', re.IGNORECASE)
										endstring = str()
										string = (object_list[key].statement_value.replace(" ",""))
										pattern = re.compile(r'([\=\+\-\/\*\(\)])')      
										iteratorUntouched = re.split(pattern, string)
							
										eqlist = list()
										for varWord in iteratorUntouched:
											#print(varWord)
											checked = 0
											for objWord in range(len(object_list)):
												thename = object_list[objWord].name
												if thename == varWord:
													eqlist.append(object_list[objWord].statement_value)
													checked = 1
											if checked == 0:
												eqlist.append(varWord) 
										endstring = (("").join(eqlist))                             
										endstring = str(endstring)
										object_list[key].statement_value = endstring


							#For float equations
							if object_list[key].datatype == "valu" :                
							#else:
										#comp = re.compile(r'(\d*)', re.IGNORECASE)
										endstring = str()
										string = (object_list[key].statement_value.replace(" ",""))
  
										#pattern = re.compile(r'([\=\+\-\/\*\(\)])')
										#iteratorFresh = re.split(pattern, string)
										iteratorFresh = re.split("(?:(?:[^a-zA-Z])|(?:[^a-zA-Z]+))|(?:[^a-zA-Z]+)", string)

										eqlist = list()
										for varWord in iteratorFresh:
											checked = 0
											for objWord in range(len(object_list)):
												thename = object_list[objWord].name
												if thename == varWord:
													eqlist.append(object_list[objWord].statement_value)
													checked = 1
											if checked == 0:
												eqlist.append(varWord) 
										endstring = (("").join(eqlist))
										#Bugprone euation line:  
										#endstring = str(eval(str(endstring)))
										
										object_list[key].statement_value = endstring
										#endnum = float()
										#endnum = float(eval(str(endstring)))
										endnum = endstring
										pre_statement_flow = 0
										try:
											op = "failed"
											if object_list[key].operator1 == "equiv" and int(object_list[key].global_relative_variable1) == int(str(endnum)):
													op = "=="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "leq" and int(object_list[key].global_relative_variable1) >= int((endnum)):
													op = ">="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "geq" and (int(object_list[key].global_relative_variable1) <= int(str(endnum))):
													op = "<="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "no" and int(object_list[key].global_relative_variable1) != int(str(endnum)):
													op = "!="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "g" and int(object_list[key].global_relative_variable1) < int(str(endnum)):

													op = "<"
													pre_statement_flow = 1
											elif object_list[key].operator1 == "l" and int(object_list[key].global_relative_variable1) > int(str(endnum)):
													op = ">"
													pre_statement_flow = 1
											else:
													pre_statement_flow = 0
											document <= html.BR()
											document <= str("%s = "%object_list[key].name)

											document <= html.BR()
										except:
											#endnum = float(eval(str(endstring)))
											endnum = endstring
											op = "failed"
											if object_list[key].operator1 == "equiv" and float(object_list[key].global_relative_variable1) == float(str(endnum)):
													op = "=="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "leq" and float(object_list[key].global_relative_variable1) >= float((endnum)):
													op = ">="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "geq" and (float(object_list[key].global_relative_variable1) <= float(str(endnum))):
													op = "<="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "no" and float(object_list[key].global_relative_variable1) != float(str(endnum)):
													op = "!="
													pre_statement_flow = 1
											elif object_list[key].operator1 == "g" and float(object_list[key].global_relative_variable1) < float(str(endnum)):
													op = "<"
													pre_statement_flow = 1
											elif object_list[key].operator1 == "l" and float(object_list[key].global_relative_variable1) > float(str(endnum)):
													op = ">"
													pre_statement_flow = 1
											else:
													pre_statement_flow = 0

											#document <= html.BR()
											#document <= str("%s = "%object_list[key].name)
											
											#document <= html.BR()

										object_list[key].statement_flow = int(pre_statement_flow)
   
							#alert("begin D1")
							#For nonbinar-evaluations
							if object_list[key].datatype == "nonbineval" :
							
										#comp = re.compile(r'(\d*)', re.IGNORECASE)
										endstring = str()
										string = (object_list[key].statement_value.replace(" ",""))
										pattern = re.compile(r'([\=\+\-\/\*\(\)])')
										iteratorUntouched = re.split(pattern, string)
							
										eqlist = list()
										for varWord in iteratorUntouched:
											#print(varWord)
											checked = 0
											for objWord in range(len(object_list)):
												thename = object_list[objWord].name
												if thename == varWord:
													eqlist.append(object_list[objWord].statement_value)
													checked = 1
											if checked == 0:
												eqlist.append(varWord) 
										endstring = (("").join(eqlist))                             
										endstring = str(eval(str(endstring)))
										object_list[key].statement_value = endstring
										endnum = float()
										endnum = float(eval(str(endstring)))

										pre_statement_flow = 0
										try:
											if object_list[key].operator1 == "equiv" and int(object_list[key].global_relative_variable1) == int(str(endnum)):
													#print ("%s == %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "leq" and int(object_list[key].global_relative_variable1) >= int((endnum)):
													#print ("%s >= %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "geq" and (int(object_list[key].global_relative_variable1) <= int(str(endnum))):
													#print ("%s <= %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "no" and int(object_list[key].global_relative_variable1) != int(str(endnum)):
													#print ("%s != %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "g" and int(object_list[key].global_relative_variable1) < int(str(endnum)):
													#print ("%s < %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "l" and int(object_list[key].global_relative_variable1) > int(str(endnum)):
													#print ("%s > %s ; exe" % (int(object_list[key].global_relative_variable1), int(str(endnum))))
													pre_statement_flow = 1
											else:
													pre_statement_flow = 0

										except:
											endnum = float(eval(str(endstring)))

											if object_list[key].operator1 == "equiv" and float(object_list[key].global_relative_variable1) == float(str(endnum)):
													#print ("%s == %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "leq" and float(object_list[key].global_relative_variable1) <= float((endnum)):
													#print ("%s <= %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "geq" and (float(object_list[key].global_relative_variable1) >= float(str(endnum))):
													#print ("%s >= %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "no" and float(object_list[key].global_relative_variable1) != float(str(endnum)):
													#print ("%s != %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "g" and float(object_list[key].global_relative_variable1) < float(str(endnum)):
													#print ("%s < %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											elif object_list[key].operator1 == "l" and float(object_list[key].global_relative_variable1) > float(str(endnum)):
													#print ("%s > %s ; exe" % (float(object_list[key].global_relative_variable1), float(str(endnum))))
													pre_statement_flow = 1
											else:
													pre_statement_flow = 0

					#object_list[key].statement_flow = int(pre_statement_flow)

					#alert("begin E1")
					#if object_list[key].statement_flow == 0 or object_list[key].flow == 0 :    
							if object_list[key].flow != 1 :    
						#alert("A8 IF 0 name:%s  ; datatype:%s  ; flow:%s  ; #statement_flow:%s" % (object_list[key].name, object_list[key].datatype, object_list[key].flow, object_list[key].statement_flow ))									

						#object_list[key].flow = 0 
						#object_list[key].statement_flow = 0 
						#pre_statement_flow = 0

								object_list[key].statement_flow = int(pre_statement_flow)        
								object_list[key].flow = int(pre_statement_flow)        
					#if object_list[key].flow == 0 :
					#	object_list[key].statement_flow = 0 

							if step == 0 :
								object_list[key].flow = 1
								object_list[key].statement_flow = 1


						#DELTETED GRAPHMODE-IF
							if object_list[key].statement_flow == 0:

									graph_string=""
									if object_list[key].datatype == "bina" :
										graph_string="0B"
									if object_list[key].datatype == "bineval" :
										graph_string=object_list[key].statement_value
									if object_list[key].datatype == "nonbineval" :
										graph_string=("score: %s" % (object_list[key].statement_value))
									if object_list[key].datatype == "valu" :                                
										graph_string=object_list[key].statement_value
									#graphstr += ('"%s" [label="step %s: %s\\n%s", fillcolor=white, style=filled] ; \n' % (start,step+1,start,str(graph_string)))
									title += ('"%s" [label="step %s: %s\\n%s", fillcolor=white, style=filled] ; \n' % (start,step+1,start,str(graph_string)))
									print("1")

							#graphstr += ('"%s" [label="step %s: %s\\n%s"] \n' % (start,step+1,start,graph_string)) 
					#alert("before draw")
							if object_list[key].statement_flow == 1:

								graph_string=""
								if object_list[key].datatype == "bina" :
									graph_string="1B"
								if object_list[key].datatype == "bineval" :
									graph_string=object_list[key].statement_value
								if object_list[key].datatype == "nonbineval" :
									graph_string=("score: %s" % (object_list[key].statement_value))
								if object_list[key].datatype == "valu" :                                
									graph_string=object_list[key].statement_value

								#graphstr += ('"%s" [label="step %s: %s\\n%s", fillcolor=yellow, style=filled] ; \n' % (start,step+1,start,str(graph_string)))
								title = ('"%s" [label="step %s: %s\\n%s", fillcolor=yellow, style=filled] ; \n' % (start,step+1,start,str(graph_string)))
								print("2")
							#self.clear_widgets()
							#self.reload()
							#Clock.unschedule(self.__init__())
								#return
								#sm.add_widget(sc1)
								#sm.current
								#return sm
							try:	
								for next_object in object_list[key].next_list :

									if object_list[key].name != next_object :
										graphstr += ('"%s" -> "%s" ; \n' % (start,next_object))
										nextstates.append(next_object)
							except:
								pass


					for start in starts :
						for k in range(0,len(object_list)):
							if object_list[k].name==start:
								for nexting in object_list[k].next_list :
									for l in range(0,len(object_list)):  
										if object_list[l].name == nexting :          
											nextstates.append(nexting)									
						if checked == 0:
							for k in range(0,len(object_list)):
								if object_list[k].name==start:
									for nexting in object_list[k].next_list :
										for l in range(0,len(object_list)):  
											if object_list[l].name == nexting :          
												if object_list[k].flow  == 0 or object_list[k].statement_flow == 0 :
													object_list[l].flow = 0
													object_list[l].statement_flow = 0
							for k in range(0,len(object_list)):
								if object_list[k].name==start:
									for nexting in object_list[k].next_list :
										for l in range(0,len(object_list)):  
											if object_list[l].name == nexting :         
								
												if object_list[k].flow  == 1 or object_list[k].statement_flow == 1 and object_list[l].flow != 0:
													object_list[l].flow = 1
													object_list[l].statement_flow = 1
					checked = 0
					del starts[:]
							#starts = list()                           
					for nexting in nextstates: 
						if nexting not in starts: 
									starts.append(nexting) 
					print(starts)
					del nextstates[:]
#				if mode_graph == True:
#				graphstr += '}'

							#try:
							#	graphstr += "}"

							#except:	
							#	pass        
#					open('lympha.dot', 'w').close()
#					outputfile = open("lympha.dot", "w")
#					outputfile.write(graphstr)
#					outputfile.close()
#					cmd = 'dot lympha.dot -Tps -o lympha.pdf'
#					os.system(cmd)
		
		CLI_filename = None
		argv_len = None
		filename = None
		filenames = None
		#filenames = list()
		#starts = None
		#steps = None
		mode_graph = None
		mode_state = None
		filecheck = None
		mode_exe = None
		mode_show = None
		mode_map = None
		exe_list = None
		show_list = None
		map_list = None
		#series = None
		substates = None
		nextstates = None
		specs = None
		global_relative_variable1 = None
		global_relative_variable2 = None
		operator1 = None
		statement_flow = None
		statement_value = None
		#object_list = None
		exe_objects = None
		
		del CLI_filename, argv_len, filename, filenames, mode_graph, mode_state, filecheck, mode_exe, mode_show, mode_map, exe_list, show_list, map_list, substates, nextstates, specs, global_relative_variable1, global_relative_variable2, operator1, statement_flow, statement_value, exe_objects,# object_list, steps, starts,


sc1 = ScreenOne(name='screen1')

class TestClass(App):
		def build(self):
			#mainfunc()
			global sc1
			global sm
			global filenames
			global filecheck
			global mode_exe  
			global starts
			global steps
			global prefilenames 
			#global prestarts 
			sys.argv = list()
			sys.argv = ["-f", "CRB65.lympha","-steps", "2", "-exe", "-start", "crepitation."]
			argv_len=len(sys.argv)

			for x in range(0, argv_len):
				if sys.argv[x] == "-f":
					filename = sys.argv[x+1]
					prefilenames.append(filename)
					filecheck = True
				if sys.argv[x] == "-steps":
					steps = int(sys.argv[x+1])
				if sys.argv[x] == "-start":
					prestarts.append(sys.argv[x+1])
					starts.append(sys.argv[x+1])
			global sc1
			#steps = 1
			lexer()
			#Clock.schedule_interval(sc1.oking, 0.2)
			nextstates = list()

			#mapfunc()
###???
			#sm.add_widget(sc1)
			Clock.schedule_interval(sc1.update , 0.2)
			return sc1

 
        
if __name__ == "__main__":
    TestClass().run()



    
    