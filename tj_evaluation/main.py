import os
import sys
sys.dont_write_bytecode = True
from kivy.core.window import Window
from kivy.app import App
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tj_evaluation.ui.screens.main_layout import MainLayout

class NavigationApp(App):
    def build(self):
        Window.maximize()
        return MainLayout()

if __name__ == '__main__':
    NavigationApp().run()