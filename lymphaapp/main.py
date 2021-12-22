import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

x = 0
sm = ScreenManager()

class ScreenOne(Screen):
    global x
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global sc1
        global x
        x += 1
        print("hello")
        my_box = BoxLayout()
        #my_show_list = ["My Way", "Wine Drinker", "Boots"]
        my_box.my_buttons = [] # if you want to keep an "easy" reference to your buttons to do something with them later
                               #kivy doesnt crashes because it creates the property automatically
        #for message in my_show_list:
        for x in range(0,x):
            button = Button(text="press")
            button.bind(on_press=self.changer)
            my_box.my_buttons.append(button)
            my_box.add_widget(button)
            print(x)
        self.add_widget(my_box)            
        #return my_box

    def changer(self,*args):
        global sc1
        global x
        x += 1
        print(x)
        Clock.unschedule(self.__init__())
        #self.manager.current = 'screen1'        
        


sc1 = ScreenOne(name='screen1')

class TestClass(App):
    def build(self):
        global x
        global sc1
        
        
        sm.add_widget(sc1)

        return sm

 
        
if __name__ == "__main__":
    TestClass().run()



    
    