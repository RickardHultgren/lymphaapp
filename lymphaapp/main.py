#import kivy

#from kivy.app import App
#from kivy.uix.button import Button
#from kivy.uix.widget import Widget
#x = 1
#class Example(App):

#    def build(self):
#      buttons = list()
#      for y in range(0,x):
#           button = Button(text="Button")
#           buttons.append(button)
#      return buttons

#Example().run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string('''
<MapScreen>:
 name: 'map'

 GridLayout:
  id: grid
  cols: 1



''')


NUMBER_OF_BUTTONS = 5


class MapScreen(Screen):

    @mainthread
    def on_enter(self):
        for i in range(0,NUMBER_OF_BUTTONS):
            button = Button(text="B_" + str(i))
            self.ids.grid.add_widget(button)


class Test(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MapScreen(name='main'))
        return sm


Test().run()