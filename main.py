# -*- coding: utf-8 -*-
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.label import Label

class ShopVideoApp(App):
    def build(self):
        return Label(text='Hello Shop Video!')

if __name__ == '__main__':
    ShopVideoApp().run()
