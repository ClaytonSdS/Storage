from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False


from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.list import MDList
import os

from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

from kivy.uix.dropdown import DropDown
from kivymd.uix.datatables import MDDataTable
import re
import datetime
from datetime import date
from kivymd.uix.pickers import MDTimePicker, MDDatePicker

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.toast import toast
import webbrowser
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine, MDExpansionPanelOneLine
from kivymd import images_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivy.animation import Animation

class Tema():
	def __init__(self, cor_aplicativo, cor_aplicativo_tuple, cor_fundo_trabalho, cor_fundo_trabalho_tuple, cor_widget, cor_widget_hover, cor_fundo_menu_deg1, cor_fundo_menu_deg2, cor_letra_menu, cor_licenca, cor_licenca_texto):
		self.cor_aplicativo = cor_aplicativo
		self.cor_aplicativo_tuple = cor_aplicativo_tuple
		self.cor_fundo_trabalho = cor_fundo_trabalho
		self.cor_fundo_trabalho_tuple = cor_fundo_trabalho_tuple
		self.cor_widget = cor_widget
		self.cor_widget_hover = cor_widget_hover
		self.cor_fundo_menu_deg1 = cor_fundo_menu_deg1
		self.cor_fundo_menu_deg2 = cor_fundo_menu_deg2
		self.cor_letra_menu = cor_letra_menu
		self.cor_licenca = cor_licenca
		self.cor_licenca_texto = cor_licenca_texto

def read_or_new_pickle(path, default):
	if os.path.isfile(path):
		with open(path, "rb") as f:
			try:
				return pickle.load(f)
			except Exception:  # so many things could go wrong, can't be more specific.
				pass
	with open(path, "wb") as f:
		pickle.dump(default, f)
	return default

class ButtonGrid(ButtonBehavior, MDBoxLayout, HoverBehavior):
	pass

class Content(BoxLayout):
    '''Custom content.'''


class Menu_Botao(ButtonBehavior, HoverBehavior, MDBoxLayout):
	cor = StringProperty("323335")
	def __init__(self,**kwargs):
		super().__init__( **kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color= get_color_from_hex("#656667"), duration=0.25)
		animate.start(widget)

	def animate_leave(self, widget, *args):
		animate = Animation(md_bg_color= get_color_from_hex("#323335"), duration=0.25)
		animate.start(widget)

	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color= get_color_from_hex("#b92034"), duration=0.2)
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color= get_color_from_hex("#323335"), duration=0.4)
		animate.start(widget)


	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.2)

	def on_enter(self):
		self.animate_enter(self)

	def on_leave(self):
		self.animate_leave(self)

class Inicio(Screen):
	def animate_rotate(self, widget, *args):
		animate = Animation(rotation=360)
		animate.start(widget)



class Inicio(Screen):
	pass

class Sell(Screen):
	pass

class Storage(Screen):
	pass

class IA(Screen):
	pass

class WindowManager(ScreenManager):
	pass

class InvisionStorage(MDApp):
	cinza_1 = ""


	def build(self):
		self.title = 'Invision Storage'
		self.icon = 'icons\icon.png'
		return Builder.load_file('InvisionStorage.kv')

	#Window.borderless = True
	Window.maximize()

	#Window.custom_titlebar = True



if __name__ == '__main__':
	InvisionStorage().run()


