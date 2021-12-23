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


sm = ScreenManager()

class ScreenOne(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global sc1

        self.switch = Switch()
        h_box = BoxLayout(orientation='horizontal')
        v_box = BoxLayout(orientation='vertical')
        #my_show_list = ["My Way", "Wine Drinker", "Boots"]
        h_box.my_buttons = [] # if you want to keep an "easy" reference to your buttons to do something with them later
                               #kivy doesnt crashes because it creates the property automatically
        #for message in my_show_list:
        switch_box = BoxLayout(orientation='vertical')
        label = Label(text='text')
        #switch = Switch()
        #switch.bind(active=callback)
        switch_box.add_widget(label)
        switch_box.add_widget(self.switch)
        #h_box.my_buttons.append(switch_box)
        h_box.add_widget(switch_box)
        v_box.add_widget(h_box)            
        #self.add_widget(h_box)            
        okbtn = Button(text="OK")
        okbtn.bind(on_press=self.oking)
        v_box.add_widget(okbtn)            
        self.add_widget(v_box)

    def oking(self,*args):
        global sc1

        if self.switch.active :
            print("hello")
        #Clock.unschedule(self.__init__())
        #self.manager.current = 'screen1'        
        
sc1 = ScreenOne(name='screen1')

class TestClass(App):
    def build(self):
        global sc1
        
        
        sm.add_widget(sc1)

        return sm

 
        
if __name__ == "__main__":
    TestClass().run()



    
    