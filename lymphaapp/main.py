#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.7.2') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
#from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
from functools import partial
#from kivy.uix.treeview import TreeView, TreeViewNode
#from kivy.uix.treeview import TreeViewLabel
from kivy.uix.scrollview import ScrollView
try:
	from plyer import sms
except:
	pass
#Declaration of global variables:
settingdata = JsonStore('settingdata.json')

Builder.load_string('''
<MainScreen>:
    allow_screensaver: 0
    name: 'mainscreen'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    GridLayout:
        row_default_height:root.height / 8
		cols:1
        orientation: 'vertical'
        ActionBar:
            width:root.width
            height:root.height / 8
            background_color:125,125,125,1,1
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: 'ont.png'
                    title: ''
                    with_previous: False
                ActionGroup:
                    mode: 'spinner'
                    text: 'Meny'
                    #color: 0,0,0,1
                    ActionButton:
                        text: 'SMS-nr'
                        on_release: root.settings()
        GridLayout:
			cols:1
			id: megabox
        BoxLayout:
            #width:root.width
            #height:root.height / 8
            orientation: 'horizontal'
            size_hint: None,None
            size:root.width, .1*root.height
            id:checkboxes
''')  

class MainScreen(Screen):
	nownr=0
	qlist=(
	u"Hur l\u00E4nge har Du lidit av Ditt nuvarande besv\u00e4r?",
	u"Hur mycket sm\u00E4rta har Du haft den senaste veckan?",
	u"Jag kan utf\u00F6ra l\u00E4ttare arbete under en timme.",
	u"Jag kan sova p\u00E5 natten.",
	u"Hur sp\u00E4nd eller stressad har du k\u00E4nt Dig den senaste veckan?",
	u"I vilken utstr\u00E4ckning har du k\u00E4nt dig nedst\u00E4md den senaste veckan?",
	u"Som Du upplever det sj\u00E4lv, hur stor \u00E4r risken att ditt nuvarande besv\u00E4r skulle bli l\u00E5ngvarigt?",
	u"Hur stor chans tror DU att Du har att kunna arbeta om tre m\u00E5nader?",
	u"Om besv\u00E4ren \u00F6kar, \u00E4r det en signal p\u00E5 att jag b\u00f6r sluta med det jag h\u00E5ller p\u00E5 med, tills besv\u00E4ren minskar.",
	u"Jag b\u00F6r inte utf\u00F6ra mina normala aktiviteter eller arbeten med den sm\u00E4rta jag har f\u00E5r n\u00E4rvarande."
	)
	dscrptn=(
		(
			u"0-1 veckor",
			u"1-2 veckor",
			u"3-4 veckor",
			u"4-5 veckor",
			u"6-8 veckor",
			u"9-11 veckor",
			u"3-6m\xe5nader",
			u"6-9 m\xe5nader",
			u"9-12 m\xe5nader",
			u"\u00D6ver ett \xe5r"
		),
		(
			u"0 Ingen sm\u00E4rta.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 Sv\u00E6rast t\u00E4nkbara sm\u00E4rta"						
		),
		(
			u"10-0 Kan inte g\u00f6ra det p.g.a. sm\u00E4rta.",
			"10-1",
			"10-2",
			"10-3",
			"10-4",
			"10-5",
			"10-6",
			"10-7",
			"10-8",
			"10-9",
			u"10-10 Kan g\u00f6ra det utan sm\u00E4rtproblem."
		),
		(
			u"10-0 Kan inte g\u00f6ra det p.g.a. sm\u0084rta.",
			"10-1",
			"10-2",
			"10-3",
			"10-4",
			"10-5",
			"10-6",
			"10-7",
			"10-8",
			"10-9",
			u"10-10 Kan g\u00f6ra det utan sm\u00E4rtproblem."
		),
		(
			u"0 Helt lugn.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 Mycket sp\u00E4nd."
		),
		(
			u"0 Inte alls.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 V\u00E4ldigt mycket."
		),
		(
			u"0 Ingen risk.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 Mycket stor risk."
		),
		(
			u"10-0 Ingen chans.",
			"10-1",
			"10-2",
			"10-3",
			"10-4",
			"10-5",
			"10-6",
			"10-7",
			"10-8",
			"10-9",
			u"10-10 Mycket stor chans."
		),
		(
			u"0 Inst\u00E4mmer inte alls.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 Inst\u00E4mmer helt."
		),
		(
			u"0 Inst\u00E4mmer inte alls.",
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			u"10 Inst\u00E4mmer helt."
		)		
	)
	valuetuple=(0,0,0,0,0,0,0,0,0,0)
	bttns=(0,0,0,0,0,0,0,0,0,0)
	bigheight=NumericProperty()
	fontheight=15
	linelen=30
	def __init__ (self,**kwargs):
		super (MainScreen, self).__init__(**kwargs)
		self.planupdate()
		
	def planupdate(self):
		self.bigheight=0
		thescroll=ScrollView(size= self.size, bar_pos_x="top")
		bigbox=GridLayout(
                cols=1,
                orientation='vertical',
                #height=self.minimum_height,
                #height=root.bigheight,
                #padding= (thescroll.width * 0.02, thescroll.height * 0.02),
                #spacing= (thescroll.width * 0.02, thescroll.height * 0.02),
                size_hint_y= None,
                size_hint_x= 1,
                do_scroll_x= False,
                do_scroll_y= True,
                )
		#self.linelen=self.ids.bigbox.width/sp(self.fontheight)
		try:
			self.ids.checkboxes.clear_widgets()
			self.ids.megabox.clear_widgets()
		except:
			pass
		for i in range(0,10):
			if self.fontheight*(len(self.qlist[i])/self.linelen) > self.fontheight :
				qheight=0*self.fontheight+self.fontheight*(len(self.qlist[i])/self.linelen)
			else:
				qheight=self.fontheight
			newq=Label(color=(0,0,0,1), size_hint_y=None, size_hint_x=1, size=(bigbox.width, "%ssp"%str(qheight)))#, font_size=self.fontheight)
			newq.bind(width=lambda s, w:
				   s.setter('text_size')(s, (self.width, None)))
			newq.bind(height=newq.setter('texture_size[1]')) 
			newq.bind(height=newq.setter('self.minimum_height'))	
			newbox=Button(id="box%s"%str(i))
			txt=''
			if self.bttns[i]==1:
				txt=str(self.valuetuple[i])
				newbox.color=(1,1,1,1)
			elif self.bttns[i]==0:
				txt="*"
				newbox.color=(0,0,0,1)
			newbox.text=txt
			if i==self.nownr:
				newbox.background_color= (1, .5, 0, 1.0)
				newq.text=(u"%s"%self.qlist[i])
				self.bigheight=self.bigheight+2*newq.height
				bigbox.add_widget(newq)
				for j in range(0,10):
					if self.fontheight*(len(self.dscrptn[i][j])/self.linelen) > 3*self.fontheight :
						bttnheight=2*self.fontheight+self.fontheight*(len(self.dscrptn[i][j])/self.linelen)
					else:
						bttnheight=3*self.fontheight
					smallLabel=Button(text="%s"%self.dscrptn[i][j],size_hint=(1,None), height="%ssp"%str(bttnheight))#, font_size=self.fontheight)
					smallLabel.bind(width=lambda s, w:
						s.setter('text_size')(s, (self.width-100, None)))
					smallLabel.bind(height=smallLabel.setter('texture_size[1]'))
					smallLabel.bind(height=smallLabel.setter('self.minimum_height'))
					smallLabel.bind(on_press=partial(self.radiobox, i, j))
					if self.valuetuple[i] == j and self.bttns[i]==1:
						smallLabel.background_color = (1, .5, 0, 1.0)
					else:
						smallLabel.background_color = (1.0, 1.0, 1.0, 1.0)
					bigbox.add_widget(smallLabel)
					self.bigheight=self.bigheight+smallLabel.height
		
			newbox.bind(on_release=partial(self.chng_bttn, i))
			self.ids.checkboxes.add_widget(newbox)
		
		bigbox.height=self.bigheight
		
		thescroll.bar_pos_x="top"
		thescroll.add_widget(bigbox)
		self.ids.megabox.add_widget(thescroll)
		
		sendbox=Button(id="sendbox", text=">>")
		sendbox.bind(on_release=(lambda store_btn: self.Submit()))
		self.ids.checkboxes.add_widget(sendbox)
		
		
	def	radiobox(self, i,j,*args):
		listV = list(self.valuetuple)
		if i == 2 or i == 3 or i == 7:
			listV[i]=10-(j)
		else:			
			listV[i]=j
		listB = list(self.bttns)
		listB[i]=1
		#self.ids.eval("chckbx%set%s"%(str(i),str(j)))
		#myCheckBox1.value = True
		self.valuetuple = tuple(listV)
		self.bttns = tuple(listB)
		maxloops=2*len(self.bttns)-1
		loops=0
		number=i
		while self.bttns[number] == 1 :
			loops += 1
			if number == len(self.bttns)-1:
				number=0
			if loops==maxloops:
				self.nownr=i
				break
			number += 1
			self.nownr=number
		self.planupdate()
		
	def chng_bttn(self,number, *args):
		self.nownr=number
		self.planupdate()
		
	def settings(self):
		box = BoxLayout(orientation='vertical')
		popup1 = Popup(title='SMS-nr', content=box, size_hint=(.90, .90))
		biggerbox=BoxLayout(orientation='horizontal')
		biggerbox.add_widget(Label(text='SMS-mottagarens nummer:'))
		#inpt=TextInput(multiline=False,input_type='number')
		try:
			inpt=TextInput(multiline=False,input_type='number',text=settingdata.get('email')['address'])
		except:
			inpt=TextInput(multiline=False,input_type='number',text="")
		biggerbox.add_widget(inpt)
		store_btn = Button(text='OK')
		store_btn.bind(on_release=(lambda store_btn: self.change_mail(inpt.text, popup1)))
		#store_btn.bind(on_press = lambda *args: popup1.dismiss())
		
		box.add_widget(biggerbox)
		box.add_widget(store_btn)
		popup1.open()

	def Submit(self):
		filled = 1
		for i in self.bttns :
			if i == 0 :
				filled=0
		if filled==0 :
			box = BoxLayout(orientation='vertical')
			popup1 = Popup(title='', content=box, size_hint=(.75, .75))
			box.add_widget(Label(text='Var god och svara p\x85 alla fr\x85gor.'))
			store_btn = Button(text='OK')
			store_btn.bind(on_press = lambda *args: popup1.dismiss())
			box.add_widget(store_btn)
			popup1.open()
		else:
			summa=sum(self.valuetuple)
			box = BoxLayout(orientation='vertical')
			popup1 = Popup(title='', content=box, size_hint=(.75, .75))
			#freetext=TextInput(multiline=False,input_type='text',text="Plats f\x83r meddelande.")
			root = ScrollView(size_hint=(1, None))
			freetext=TextInput(multiline=True,input_type='text',text=u"Plats f\u00f6r meddelande.")
			root.add_widget(freetext)
			box.add_widget(root)	
			themessage=u'\u00D6MPSQ*-score: %s\n\n*\u00D6rebro Musculoskeletal Pain Screening Questionnaire\ntotala po\x85ng varierar mellan 1-100.'%(summa)
			box.add_widget(Label(text=themessage))	
			store_btn = Button(text='OK')
			themessage="%s\n%s"%(freetext,themessage)
			store_btn.bind(on_press = lambda store_btn: self.send_mail(themessage, popup1))
			box.add_widget(store_btn)
			popup1.open()
	
	def change_mail(self, theaddress, popup1):
		popup1.dismiss()
		settingdata.put('email', address=theaddress)

	def send_mail(self, themessage, popup1):
		popup1.dismiss()
		box = BoxLayout(orientation='vertical')
		tried=0
		try:
			to_nr = str(settingdata.get('email')['address'])
			mess = str(themessage)
			sms.send(recipient=to_nr, message=mess)
#			email.send(recipient=StringProperty(str(settingdata.get('email')['address'])),
#				subject=StringProperty('MADRS-S'),
#				text=StringProperty('%s'%themessage)
				#,create_chooser=BooleanProperty()
#				)
			box.add_widget(Label(text='SMS skickat till: %s'%settingdata.get('email')['address']))
			#box.add_widget(Label(text='Email sent to:%s'%settingdata.get('email')['address']))
			tried=1
		except:
			#box.add_widget(Label(text='Couldn\'t send e-mail'))
			box.add_widget(Label(text='Kunde inte skicka SMS'))
		
		popup2 = Popup(title='Settings', content=box, size_hint=(.75, .75))
		store_btn = Button(text='OK')
		store_btn.bind(on_press = lambda *args: popup2.dismiss())
		box.add_widget(store_btn)
		popup2.open()


class ontApp(App):
	def build(self):
			the_screenmanager = ScreenManager()
			#the_screenmanager.transition = FadeTransition()
			mainscreen = MainScreen(name='mainscreen')
			the_screenmanager.add_widget(mainscreen)
			return the_screenmanager
					
	def on_pause(self):
			# Here you can save data if needed
			return True

	def on_resume(self):
			#the_screenmanager = ScreenManager()
			#mainscreen = MainScreen(name='mainscreen')
			#the_screenmanager.add_widget(mainscreen)
			#return the_screenmanager
			
			#return True
			
			pass
		
	#def on_start(self):
			#the_screenmanager = ScreenManager()
			#mainscreen = MainScreen(name='mainscreen')
			#the_screenmanager.add_widget(mainscreen)
			#return the_screenmanager
			
			#return True
			
			#pass

			

	def on_stop(self):
		pass


if __name__ == '__main__':
	ontApp().run()
