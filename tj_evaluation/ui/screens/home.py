from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="欢迎使用本程序!\n\n请先登录账号", font_size=20, halign='center'))