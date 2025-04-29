from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random

# red = [1,0,0,1]
# green = [0,1,0,1]
# blue =  [0,0,1,1]
# purple = [1,0,1,1]

# class MainApp(App):
#     def build(self):
#         label = Label(text="Hello World",
#         size_hint = (0.1, 0.5),
#         pos_hint = {"center_x": 0.5,  "center_y": 0.5})

#         img = Image(source=rf"C:\Users\nickc\Desktop\Wallpapers\20180903_144149.jpg",
#         size_hint=(1, .5),
#         pos_hint={'center_x':.5, 'center_y':.5})

#         layout = BoxLayout(padding=10)
#         colors = [red, green, blue, purple]
#         for i in range(5):
#             btn = Button(text="Button #%s" % (i+1),
#                          background_color=random.choice(colors)
#                          )
#             layout.add_widget(btn)

#         button = Button(text='Hello from Kivy',
#                         size_hint=(.5, .5),
#                         pos_hint={'center_x': .5, 'center_y': .5})
#         button.bind(on_press=self.on_press_button)

#         return button
    
#     def on_press_button(self, instance):
#         print('You pressed the button!')
        
            
class ButtonApp(App):
    def build(self):
        Button(text='Hello from Kivy',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        return Button()

    def on_press_button(self):
        print('You pressed the button!')

    
if __name__ == "__main__":
    app = ButtonApp()
    app.run()