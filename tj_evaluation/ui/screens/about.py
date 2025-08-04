from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="天津市综评自动化检查程序(教师端)\n版本:beta 1.0.0", font_size=20, halign='center'))