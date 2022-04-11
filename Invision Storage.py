from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


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
from kivymd.uix.button import MDIconButton

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, ObjectProperty
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
from kivymd.uix.dialog import BaseDialog
import pandas as pd
import numpy as np
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.label import Label
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import MDRectangleFlatButton

class ItemConfirm(OneLineAvatarIconListItem):
	divider = None

	def set_icon(self, instance_check):
		instance_check.active = True
		check_list = instance_check.get_widgets(instance_check.group)
		for check in check_list:
			if check != instance_check:
				check.active = False



# CLASSES IMPORTANTES
class Clientes_():
	def __init__(self):
		read_or_new_pickle(path="clientes.p", default=pd.DataFrame(
			data={"CLASSE": [], "NOME": [], "TELEFONE": [], "EMAIL": [], "CPF/CNPJ": [], "ENDEREÇO": [],
				  "BAIRRO/DISTRITO": [], "CEP": [], "MUNICIPIO": [], "ESTADO": []}))

		self.database = pickle.load((open("clientes.p", "rb")))

	def load(self):
		self.database = pickle.load((open("clientes.p", "rb")))

	def save(self):
		self.database = pickle.dump(self.clientes, open("clientes.p", "wb"))

	def add_data(self, classe="", nome="", telefone="", email="", cpf_cnpj="", endereco="", bairro="", cep="", municipio="", estado=""):
		self.new_id = 1
		try:
			self.new_id = np.array(self.database.index.values).max() + 1
		except ValueError: pass

		new_row = [classe, nome, telefone, email, cpf_cnpj, endereco, bairro, cep, municipio, estado]
		self.database = self.database.append(pd.Series(new_row, index=self.database.columns, name = self.new_id))
		pickle.dump(self.database, open("clientes.p", "wb"))

	def data_info(self, id, classe, nome, telefone):
		#df1_ = self.database.loc[self.database["ID"] == str(id)]
		df2_ = self.database.loc[self.database["NOME"] == str(nome)]
		df3_ = df2_.loc[self.database["CLASSE"] == str(classe)]
		df4_ = df3_.loc[self.database["TELEFONE"] == str(telefone)]
		return df4_

	def change_info(self, id, new_infos):
		self.database.loc[id] = new_infos
		pickle.dump(self.database, open("clientes.p", "wb"))

	def remove_data(self, id):
		self.database.drop(int(id), inplace=True)
		pickle.dump(self.database, open("clientes.p", "wb"))

	def search_item(self, item):
		self.data_found = []
		for coluna in range(len(self.database.columns)):
			coluna_ = self.database.columns[coluna]
			if len(self.database.loc[self.database[coluna_] == item]) > 0 :
				self.data_found = self.database.loc[self.database[coluna_] == item]
				break

		if len(self.data_found) == 0 and item.isdigit() == True:
			self.data_found = self.database.loc[self.database.index == int(item)]

		return self.data_found
class Estoque_():
	def __init__(self):
		read_or_new_pickle(path="estoque.p", default=pd.DataFrame(
			data={"CATEGORIA": [], "PRODUTO": [], "FORNECEDOR": [], "QUANTIDADE": [], "ESTOQUE_CRITICO": [], "FORNECEDOR_ID": [], "FORNECEDOR_TELEFONE": []}))

		self.database = pickle.load((open("estoque.p", "rb")))

	def load(self):
		self.database = pickle.load((open("estoque.p", "rb")))

	def add_data(self, categoria="", produto="", fornecedor="", quantidade="", estoque_critico="", fornecedor_id="", fornecedor_telefone=""):
		self.new_id = 1
		try:
			self.new_id = np.array(self.database.index.values).max() + 1
		except ValueError: pass

		new_row = [categoria, produto, fornecedor, quantidade, estoque_critico, fornecedor_id, fornecedor_telefone]
		self.database = self.database.append(pd.Series(new_row, index=self.database.columns, name = self.new_id))
		pickle.dump(self.database, open("estoque.p", "wb"))

	def data_info(self, id, categoria, produto, fornecedor, quantidade):
		df2_ = self.database.loc[self.database["CATEGORIA"] == str(categoria)]
		df3_ = df2_.loc[self.database["PRODUTO"] == str(produto)]
		df4_ = df3_.loc[self.database["FORNECEDOR"] == str(fornecedor)]
		df5_ = df4_.loc[self.database["QUANTIDADE"] == str(quantidade)]
		return df5_

	def change_info(self, id, new_infos):
		self.database.loc[id].loc[["CATEGORIA", "PRODUTO", "FORNECEDOR", "QUANTIDADE", "ESTOQUE_CRITICO"]] = new_infos
		pickle.dump(self.database, open("estoque.p", "wb"))

	def remove_data(self, id):
		self.database.drop(int(id), inplace=True)
		pickle.dump(self.database, open("estoque.p", "wb"))

	def search_item(self, item):
		self.data_found = []
		for coluna in range(len(self.database.columns)):
			coluna_ = self.database.columns[coluna]
			if len(self.database.loc[self.database[coluna_] == item]) > 0:
				self.data_found = self.database.loc[self.database[coluna_] == item]
				break

		if len(self.data_found) == 0 and item.isdigit() == True:
			self.data_found = self.database.loc[self.database.index == int(item)]

		return self.data_found

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



class Menu(MDFloatLayout):
	def reset_colors(self):
		pass


from typing import List, NoReturn
from kivy.uix.textinput import TextInput

class ButtonTip_Behavior(BaseDialog):
	def __init__(self, name, posicao, **kwargs):
		super().__init__(**kwargs)
		self.name = name
		self.auto_dismiss = True
		self.posicao = posicao

		if self.name == "view-dashboard":
			self.botao_nome = "Inicio"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		if self.name == "cart-outline":
			self.botao_nome = "Vender"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		if self.name == "package-variant":
			self.botao_nome = "Estoque"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		if self.name == "robot-happy":
			self.botao_nome = "ReVision"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		if self.name == "account-group":
			self.botao_nome = "Clientes"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		if self.name == "cog":
			self.botao_nome = "Configs"
			self.pos_hint = {"center_x": 0.05, "center_y": posicao[1] + 0.007}

		self.label_toast = MDLabel(size_hint=(1, 1), opacity=0, markup=True, color=get_color_from_hex('#FFFFFF'), text=str(self.botao_nome))
		self.label_toast.color = get_color_from_hex('#FFFFFF')
		self.label_toast.font_size = 14
		self.label_toast.halign = "center"
		self.label_toast.pos_hint = {"center_x": 0.5, "center_y": 0.5}

		self.add_widget(self.label_toast)
		self.duration = 1

	def on_open(self) -> NoReturn:
		self.fade_in()
		Clock.schedule_once(self.fade_out, self.duration)

	def fade_in(self) -> NoReturn:
		anim = Animation(opacity=1, duration=0.4)
		anim.start(self.label_toast)
		anim.start(self)

	def fade_out(self, *args) -> NoReturn:
		anim = Animation(opacity=0, duration=0.3)
		anim.bind(on_complete=lambda *x: self.dismiss())
		anim.start(self.label_toast)
		anim.start(self)

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			if self.auto_dismiss:
				self.fade_out()
				return False
		super().on_touch_down(touch)
		return True

class ButtonTip_Clientes (HoverBehavior, MDIconButton):
	cor = StringProperty("eeeeee")
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))
	def animate_enter(self, widget, *args):
		self.cor = 'f6f6f6'
	def animate_leave(self, widget, *args):
		self.cor = 'eeeeee'
	def animate_press(self, widget, *args):
		self.cor = '0b9b53'
	def animate_release(self, widget, *args):
		self.cor = 'eeeeee'
	def on_enter(self):
		self.animate_enter(self)
	def on_leave(self):
		self.animate_leave(self)
	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
			self.animate_release(self.parent)
		Clock.schedule_once(delay, 0.2)


class ButtonTip (HoverBehavior, MDIconButton):
	cor = StringProperty("eeeeee")
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#f6f6f6"), duration=0.25)
		animate.start(widget)

	def animate_leave(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#eeeeee"), duration=0.25)
		animate.start(widget)

	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#0b9b53"), duration=0.1)
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#eeeeee"), duration=0.25)
		animate.start(widget)

	def on_enter(self):
		try:
			nome = str(self.icon)
			pos_percent = (self.pos[0]/Window.width, self.pos[1]/Window.height)
			ButtonTip_Behavior(nome, pos_percent).open()
			self.animate_enter(self)
		except AttributeError: pass

	def on_leave(self):
		try:
			nome = str(self.icon)
			pos_percent = (self.pos[0] / Window.width, self.pos[1] / Window.height)
			ButtonTip_Behavior(nome, pos_percent).dismiss()
			self.animate_leave(self)
		except AttributeError: pass

	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 1)

class Menu_Botao(HoverBehavior, MDBoxLayout):
	cor = StringProperty("eeeeee")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

class InputCapsLock(TextInput):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.always_upper()

	def always_upper(self, *args):
		def caps_lock(dt):
			self.text = self.text.upper()

		Clock.schedule_interval(caps_lock, 0.000002)


from kivymd.uix.button import MDRectangleFlatIconButton


class Header_Clientes_Tabela(MDBoxLayout):
	pass

class Header_Estoque_Tabela(MDBoxLayout):
	pass

class InvButton(MDRectangleFlatIconButton, HoverBehavior):
	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#0b9b53"), duration=0.15, line_color = get_color_from_hex("#31b774"))
		animate.start(widget)

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#6c6d6f"), duration=0.35, line_color = get_color_from_hex("#969799"))
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#323335"), duration=0.18, line_color = get_color_from_hex("#000000"))
		animate.start(widget)

	def on_enter(self):
		self.animate_enter(self)

	def on_leave(self):
		self.animate_release(self)

	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.2)

class FornecedoresButton(MDRectangleFlatIconButton, HoverBehavior):
	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#0b9b53"), duration=0.15, line_color = get_color_from_hex("#31b774"))
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#323335"), duration=0.18, line_color = get_color_from_hex("#000000"))
		animate.start(widget)


	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.2)

# BOTOES PERSONALIZADOS
class Clientes_Deletar(MDRectangleFlatIconButton, HoverBehavior):
	cor = StringProperty("b92034")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#ce3549"), duration=0.25)
		animate.start(widget)

	def animate_leave(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#b92034"), duration=0.25)
		animate.start(widget)

	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#941425"), duration=0.1)
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#b92034"), duration=0.25)
		animate.start(widget)

	def on_enter(self):
		self.animate_enter(self)

	def on_leave(self):
		self.animate_leave(self)

	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.3)
class Clientes_Alterar(MDRectangleFlatIconButton, HoverBehavior):
	cor = StringProperty("323335")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#474749"), duration=0.25)
		animate.start(widget)

	def animate_leave(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#323335"), duration=0.25)
		animate.start(widget)

	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#212123"), duration=0.1)
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#323335"), duration=0.25)
		animate.start(widget)

	def on_enter(self):
		self.animate_enter(self)

	def on_leave(self):
		self.animate_leave(self)

	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.3)
class Alterar_Fornecedor(MDRectangleFlatButton, HoverBehavior):
	cor = StringProperty("eeeeee")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.md_bg_color = get_color_from_hex("#{}".format(self.cor))

	def animate_enter(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#c2c2c2"), duration=0.25)
		animate.start(widget)
	def animate_leave(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#eeeeee"), duration=0.25)
		animate.start(widget)

	def animate_press(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#a3a3a3"), duration=0.1)
		animate.start(widget)

	def animate_release(self, widget, *args):
		animate = Animation(md_bg_color=get_color_from_hex("#eeeeee"), duration=0.25)
		animate.start(widget)

	def on_enter(self):
		self.animate_enter(self)

	def on_leave(self):
		self.animate_leave(self)

	def on_press(self):
		self.animate_press(self)

	def on_release(self):
		def delay(dt):
			self.animate_release(self)
		Clock.schedule_once(delay, 0.3)



class Inicio(Screen):
	pass


class Sell(Screen):
	pass


class IA(Screen):
	pass

class SpinnerOptions(SpinnerOption):
	def __init__(self, **kwargs):
		super(SpinnerOptions, self).__init__(**kwargs)
		self.background_normal = ''
		self.background_color = get_color_from_hex('#eeeeee')
		self.height = 40
		self.color = get_color_from_hex('#323335')

class SpinnerDropdown(DropDown):
	def __init__(self, **kwargs):
		super(SpinnerDropdown, self).__init__(**kwargs)
		self.auto_width = True
		self.color = get_color_from_hex('#323335')

class Clientes(Screen):

	class Classes_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = get_color_from_hex('#323335')
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			self.values = ["CLIENTE", "FORNECEDOR"]
			self.text =  "SELECIONAR"

	recycle_view = ObjectProperty(None)
	items_box = ObjectProperty(None)
	height_ = NumericProperty(72.11)
	width_ = Window.width * 0.4947584187408493 * 1.707

	clientes = Clientes_()

	def clientes_info_close(self, widget, *args):
		animate = Animation(size_hint_x = 0.0, duration=0.05)
		animate.start(widget)

	# BARRA DE BUSCA
	def search(self):
		search_for = self.ids.search_bar_clientes.text
		search_for = ' '.join(search_for.split()).upper()
		data_found = self.clientes.search_item(search_for)

		if search_for == "":
			self.ids.recycle_view.data = []
			# ATUALIZAR ITEMS
			for i in range(len(self.clientes.database.index.values)):
				ids = self.clientes.database.index.values
				classes = self.clientes.database["CLASSE"].values
				nomes = self.clientes.database["NOME"].values
				telefones = self.clientes.database["TELEFONE"].values
				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]),'telefone_': str(telefones[i])})

		else:
			if len(data_found) == 0:
				toast(f"Atenção: Nenhum Resultado Encontrado",background=get_color_from_hex('#b92034'))
				self.ids.recycle_view.data = []
				self.clientes_info_close(self.ids.clientes_info)

			else:
				self.ids.recycle_view.data = []
				toast(f"Resultados Encontrados: {len(data_found)}", background=get_color_from_hex('#0b9b53'))
				# ATUALIZAR ITEMS
				for i in range(len(data_found.index.values)):
					ids = data_found.index.values
					classes = data_found["CLASSE"].values
					nomes = data_found["NOME"].values
					telefones = data_found["TELEFONE"].values
					self.ids.recycle_view.data.append({'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]), 'telefone_': str(telefones[i])})

	# DIALOG CRIAR NOVO CLIENTE
	class Conteudo_CriarNovaMateria(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	novo_cliente = None
	def novo_cliente_(self, root, *args):
		if not self.novo_cliente:
			self.novo_cliente = MDDialog(
					title=f'[color=#323335]Adicionar Novo Cliente[/color]',
					md_bg_color=get_color_from_hex('#eeeeee'),

					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_CriarNovaMateria(),
					buttons=[
						MDFlatButton(
							text=f"[color=#323335][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_),
						MDFlatButton(
							text=f"[color=#323335][b]ADICIONAR CLIENTE[/color][/b]",
							theme_text_color="Custom",
							on_release=root.cliente_addFunction)])
		self.novo_cliente.open()
	def close_(self, obj):
		self.novo_cliente.dismiss()
	def cliente_addFunction(self, root, *args):
		classe = ' '.join(self.novo_cliente.content_cls.ids.spinnerClasses.text.split()).upper()
		nome = ' '.join(self.novo_cliente.content_cls.ids.info_add_nome.text.split()).upper()
		telefone = ' '.join(self.novo_cliente.content_cls.ids.info_add_telefone.text.split()).upper()

		verificador = self.clientes.data_info(id=0, nome=nome, classe=classe, telefone=telefone)

		if classe == "" or nome == "" or telefone == "" or classe == "SELECIONAR":
			toast(f"Atenção: Todos os Campos Devem ser Preenchidos",background=get_color_from_hex('#b92034'))

		else:
			if len(verificador) == 0:
				self.novo_cliente.content_cls.ids.info_add_nome.text = ""
				self.novo_cliente.content_cls.ids.info_add_telefone.text = ""

				self.clientes.add_data(nome=nome, classe=classe, telefone=telefone)

				self.ids.recycle_view.data = []
				toast("Cliente Adicionado com Sucesso", background=get_color_from_hex('#0b9b53'))
				# ATUALIZAR ITEMS
				for i in range(len(self.clientes.database.index.values)):
					ids = self.clientes.database.index.values
					classes = self.clientes.database["CLASSE"].values
					nomes = self.clientes.database["NOME"].values
					telefones = self.clientes.database["TELEFONE"].values
					self.ids.recycle_view.data.append({'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]),'telefone_': str(telefones[i])})
			else:
				toast(f"ATENÇÃO: JÁ EXISTE UM {classe} CHAMADO {nome} COM O TELEFONE {telefone}", background=get_color_from_hex('#b92034'))


	# DIALOG DE CONFIRMAR REMOÇÃO CLIENTE
	remover_cliente = None
	def confirmacao_remover_cliente(self, root, *args):
		if not self.remover_cliente:
			self.remover_cliente = MDDialog(
				title=f'[color=#eeeeee][b]Deletar Cliente[/b][/color]',
				text="[color=#eeeeee][b]Você deseja realmente excluir este cliente?\nEsse processo é irreversivel e não poderá ser desfeito.[/b][/color]",
				md_bg_color=get_color_from_hex('#323335'),
				type="custom",
				size_hint=[0.4, 0.4],
				auto_dismiss=True,
				buttons=[
					MDFlatButton(
						text=f"[color=#eeeeee][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_remover),
					MDFlatButton(
						text=f"[color=#eeeeee][b]DELETAR CLIENTE[/color][/b]",
						theme_text_color="Custom",
						on_release=root.remove_client)]
			)
		self.remover_cliente.open()
	def close_remover(self, obj):
		self.remover_cliente.dismiss()


	# FUNÇÕES RELACIONADAS A TABELA DE CLIENTES
	def refresh_infos(self, id, classe, nome, telefone):
		data_find = self.clientes.data_info(id, classe, nome, telefone)

		self.ids.info_id.text = str(data_find.index[0])
		self.ids.info_classe.text = str(data_find["CLASSE"].values[0])
		self.ids.info_nome.text = str(data_find["NOME"].values[0])
		self.ids.info_telefone.text = str(data_find["TELEFONE"].values[0])
		self.ids.info_email.text = str(data_find["EMAIL"].values[0])
		self.ids.info_cpf.text = str(data_find["CPF/CNPJ"].values[0])
		self.ids.info_endereco.text = str(data_find["ENDEREÇO"].values[0])
		self.ids.info_bairro.text = str(data_find["BAIRRO/DISTRITO"].values[0])
		self.ids.info_cep.text = str(data_find["CEP"].values[0])
		self.ids.info_municipio.text = str(data_find["MUNICIPIO"].values[0])
		self.ids.info_estado.text = str(data_find["ESTADO"].values[0])
	def change_infos(self):
		new_row = [self.ids.info_classe.text, self.ids.info_nome.text, self.ids.info_telefone.text, self.ids.info_email.text, self.ids.info_cpf.text, self.ids.info_endereco.text,
				   self.ids.info_bairro.text, self.ids.info_cep.text, self.ids.info_municipio.text, self.ids.info_estado.text]

		if self.ids.info_id.text != "":
			self.clientes.change_info(int(self.ids.info_id.text), new_row)
			toast("Alteração Realizada com Sucesso", background=get_color_from_hex('#0b9b53'))

			# ATUALIZAR ITEMS
			self.ids.recycle_view.data = []
			for i in range(len(self.clientes.database.index.values)):
				ids = self.clientes.database.index.values
				classes = self.clientes.database["CLASSE"].values
				nomes = self.clientes.database["NOME"].values
				telefones = self.clientes.database["TELEFONE"].values
				self.ids.recycle_view.data.append(
					{'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]),
					 'telefone_': str(telefones[i])})
		else:
			toast("Atenção: Nenhum Cliente Selecionado", background=get_color_from_hex('#b92034'))
	def remove_client(self, root):
		if self.ids.info_id.text != "":
			self.clientes.remove_data(int(self.ids.info_id.text))
			self.remover_cliente.dismiss()
			# RESETAR TEXTOS
			self.ids.info_id.text = ""
			self.ids.info_classe.text = ""
			self.ids.info_nome.text = ""
			self.ids.info_telefone.text = ""
			self.ids.info_email.text = ""
			self.ids.info_cpf.text = ""
			self.ids.info_endereco.text = ""
			self.ids.info_bairro.text = ""
			self.ids.info_cep.text = ""
			self.ids.info_municipio.text = ""
			self.ids.info_estado.text = ""
			self.ids.recycle_view.data = []

			toast("Cliente Removido com Sucesso", background=get_color_from_hex('#0b9b53'))

			# ATUALIZAR ITEMS
			for i in range(len(self.clientes.database.index.values)):
				ids = self.clientes.database.index.values
				classes = self.clientes.database["CLASSE"].values
				nomes =  self.clientes.database["NOME"].values
				telefones =  self.clientes.database["TELEFONE"].values
				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]), 'telefone_': str(telefones[i])})
		else:
			toast("Atenção: Nenhum Cliente Selecionado", background=get_color_from_hex('#b92034'))

	def auto_size_id(self, string):
		if len(string) <= 5:
			return string
		else:
			return string[0:5] + "..."
	def auto_size_name(self, string):
		if len(string) <= 24:
			return string
		else:
			return string[0:24] + "..."
	def auto_size_telefone(self, string):
		if len(string) <= 13:
			return string
		else:
			return string[0:13] + "..."

	def on_enter(self):
		def refresh_name(dt):
			self.ids.clientes_header.height = self.ids.menu.children[0].children[0].children[0].children[4].size[1] + 2
			self.ids.clientes_header2.height = self.ids.menu.children[0].children[0].children[0].children[4].size[1] + 2
			self.ids.search_bar_clientes.width = self.ids.search_clientes_box.width * 0.8
		Clock.schedule_interval(refresh_name, 0.05)

		if len(self.ids.recycle_view.data) == 0:
			for i in range(len(self.clientes.database.index.values)):
				ids = self.clientes.database.index.values
				classes = self.clientes.database["CLASSE"].values
				nomes =  self.clientes.database["NOME"].values
				telefones =  self.clientes.database["TELEFONE"].values


				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'classe_': str(classes[i]), 'nome_': str(nomes[i]), 'telefone_': str(telefones[i])})






class Storage(Screen):

	class Classes_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = get_color_from_hex('#323335')
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			self.values = ["CLIENTE", "FORNECEDOR"]
			self.text =  "SELECIONAR"

	recycle_view = ObjectProperty(None)
	items_box = ObjectProperty(None)
	height_ = NumericProperty(72.11)
	width_ = Window.width * 0.4947584187408493 * 1.707

	clientes = Clientes_()
	estoque = Estoque_()

	# FORNECEDORES- FUNÇÕES DE SELECIONAR | FECHAR | ALTERAR
	selecionar_fonecedor = None
	selecionar_fonecedor2 = None
	class Fornecedores(MDFloatLayout, HoverBehavior):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			fornecedores_only = Clientes_()
			fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"]=='FORNECEDOR']
			for i in range(len(fornecedores_only)):
				self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]), 'fornecedor_': str(fornecedores_only["NOME"].values[i])})

		def refresh_data(self):
			self.ids.recycle_view.data = []
			fornecedores_only = Clientes_()
			fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"] == 'FORNECEDOR']
			for i in range(len(fornecedores_only)):
				self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]),'fornecedor_': str(fornecedores_only["NOME"].values[i])})

		def search_fornecedor(self, string):
			fornecedores_search = Clientes_()
			search_for = self.ids.search_bar_fornecedores.text
			search_for = ' '.join(search_for.split()).upper()
			data_found = fornecedores_search.search_item(search_for)
			try:
				data_found = data_found.loc[data_found["CLASSE"] == 'FORNECEDOR']
			except AttributeError: pass

			if search_for == "":
				self.ids.recycle_view.data = []
				# ATUALIZAR ITEMS
				self.ids.recycle_view.data = []
				fornecedores_only = Clientes_()
				fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"] == 'FORNECEDOR']
				for i in range(len(fornecedores_only)):
					self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]),'fornecedor_': str(fornecedores_only["NOME"].values[i])})

			else:
				if len(data_found) == 0:
					toast(f"Atenção: Nenhum Resultado Encontrado", background=get_color_from_hex('#b92034'))
					self.ids.recycle_view.data = []

				else:
					self.ids.recycle_view.data = []
					toast(f"Resultados Encontrados: {len(data_found)}", background=get_color_from_hex('#0b9b53'))
					# ATUALIZAR ITEMS
					for i in range(len(data_found.index.values)):
						self.ids.recycle_view.data.append({'id_': str(data_found.index.values[i]),'fornecedor_': str(data_found["NOME"].values[i])})
	class Fornecedores2(MDFloatLayout, HoverBehavior):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			fornecedores_only = Clientes_()
			fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"]=='FORNECEDOR']
			for i in range(len(fornecedores_only)):
				self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]), 'fornecedor_': str(fornecedores_only["NOME"].values[i])})

		def refresh_data(self):
			self.ids.recycle_view.data = []
			fornecedores_only = Clientes_()
			fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"] == 'FORNECEDOR']
			for i in range(len(fornecedores_only)):
				self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]),'fornecedor_': str(fornecedores_only["NOME"].values[i])})

		def search_fornecedor(self, string):
			fornecedores_search = Clientes_()
			search_for = self.ids.search_bar_fornecedores.text
			search_for = ' '.join(search_for.split()).upper()
			data_found = fornecedores_search.search_item(search_for)
			try:
				data_found = data_found.loc[data_found["CLASSE"] == 'FORNECEDOR']
			except AttributeError: pass

			if search_for == "":
				self.ids.recycle_view.data = []
				# ATUALIZAR ITEMS
				self.ids.recycle_view.data = []
				fornecedores_only = Clientes_()
				fornecedores_only = fornecedores_only.database.loc[fornecedores_only.database["CLASSE"] == 'FORNECEDOR']
				for i in range(len(fornecedores_only)):
					self.ids.recycle_view.data.append({'id_': str(fornecedores_only.index.values[i]),'fornecedor_': str(fornecedores_only["NOME"].values[i])})

			else:
				if len(data_found) == 0:
					toast(f"Atenção: Nenhum Resultado Encontrado", background=get_color_from_hex('#b92034'))
					self.ids.recycle_view.data = []

				else:
					self.ids.recycle_view.data = []
					toast(f"Resultados Encontrados: {len(data_found)}", background=get_color_from_hex('#0b9b53'))
					# ATUALIZAR ITEMS
					for i in range(len(data_found.index.values)):
						self.ids.recycle_view.data.append({'id_': str(data_found.index.values[i]),'fornecedor_': str(data_found["NOME"].values[i])})
	def selecionar_fonecedores2(self, root, *args):
		if not self.selecionar_fonecedor2:
			self.selecionar_fonecedor2 = MDDialog(
				title=f'[color=#323335]Fornecedores[/color]',
				md_bg_color=get_color_from_hex('#eeeeee'),
				type="custom",
				auto_dismiss=False,
				content_cls=self.Fornecedores2(),
				buttons=[
					MDFlatButton(
						text=f"[color=#323335][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_fornecedores2)])
		self.selecionar_fonecedor2.open()
		self.selecionar_fonecedor2.on_open = self.atualizar_fornecedores2
	def atualizar_fornecedores2(self, *args):
		self.selecionar_fonecedor2.content_cls.refresh_data()
	def close_fornecedores2(self, obj):
		self.selecionar_fonecedor2.dismiss()
	def selecionar_fonecedores(self, root, *args):
		if not self.selecionar_fonecedor:
			self.selecionar_fonecedor = MDDialog(
				title=f'[color=#323335]Fornecedores[/color]',
				md_bg_color=get_color_from_hex('#eeeeee'),
				type="custom",
				auto_dismiss=False,
				content_cls=self.Fornecedores(),
				buttons=[
					MDFlatButton(
						text=f"[color=#323335][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_fornecedores)])
		self.selecionar_fonecedor.open()
		self.selecionar_fonecedor.on_open = self.atualizar_fornecedores
	def atualizar_fornecedores(self, *args):
		self.selecionar_fonecedor.content_cls.refresh_data()
	def close_fornecedores(self, obj):
		self.selecionar_fonecedor.dismiss()
	def clientes_info_close(self, widget, *args):
		animate = Animation(size_hint_x = 0.0, duration=0.05)
		animate.start(widget)
	def mudar_fornecedor(self, root, modo, fornecedor=""):
		# USADO DENTRO DO DIALOG - ALTERAR O FORNECEDOR DO MEU ITEM
		if fornecedor != "" and modo == "alterar_fornecedor":
			self.ids.info_fornecedor.text = str(fornecedor)
			toast("Fornecedor Alterado com Sucesso", background=get_color_from_hex('#0b9b53'))
			self.selecionar_fonecedor.dismiss()
			self.change_infos()

		# ABRIR DIALOG - USADO AO CLICAR NO BOTÃO DE FORNECEDOR EM MAIS INFO
		if fornecedor == "" and modo == "open":
			self.selecionar_fonecedores(root)

	def auto_size(self, string):
		if len(string) > 14:
			return string[0:14] + "..."
		else:
			return string

	def NovoProdutoSelecionar_fornecedor(self, root, modo, id, fornecedor=""):
		# USADO DENTRO DO DIALOG - ALTERAR O FORNECEDOR DO MEU ITEM
		if fornecedor != "" and modo == "novo_produto":
			fornecedor_short = self.auto_size(fornecedor)
			self.fornecedor_to_add = fornecedor
			self.fornecedor_id = id

			self.novo_produto.content_cls.ids.fornecedor_novo.text = f"[b]{fornecedor_short}[/b]"
			self.selecionar_fonecedor2.dismiss()

	def AdicionarNovoProduto(self, root, *args):
		try:
			all_fornecedores = Clientes_()
			all_fornecedores = all_fornecedores.database

			id_fornecedor = self.fornecedor_id
			fornecedor = self.fornecedor_to_add
			categoria = self.novo_produto.content_cls.ids.new_product_categoria.text
			produto = self.novo_produto.content_cls.ids.new_product_produto.text
			quantidade = self.novo_produto.content_cls.ids.new_product_quantidade.text
			self.valor_critico = self.novo_produto.content_cls.ids.new_product_critico.text

			categoria = ' '.join(categoria.split()).upper()
			produto = ' '.join(produto.split()).upper()
			quantidade = ' '.join(quantidade.split()).upper()

			if fornecedor == "" or categoria == "" or quantidade == "" or fornecedor == "SELECIONAR":
				toast("Atenção: Todos os Campos Devem ser Preenchidos", background=get_color_from_hex('#b92034'))

			else:
				if self.valor_critico == "":
					self.valor_critico = str(int(0.25*float(quantidade)))

				if self.valor_critico != "":
					self.valor_critico = self.valor_critico

				self.novo_produto.content_cls.ids.fornecedor_novo.text = "SELECIONAR"
				self.novo_produto.content_cls.ids.new_product_categoria.text = ""
				self.novo_produto.content_cls.ids.new_product_produto.text = ""
				self.novo_produto.content_cls.ids.new_product_quantidade.text = ""
				self.novo_produto.content_cls.ids.new_product_critico.text = ""

				self.novo_produto.dismiss()

				estoque_critico = self.valor_critico
				telefone_fornecedor = all_fornecedores.loc[all_fornecedores["CLASSE"] == 'FORNECEDOR']["TELEFONE"][int(id_fornecedor)]
				self.estoque.add_data(categoria, produto, fornecedor, quantidade, estoque_critico, id_fornecedor, telefone_fornecedor)

				toast("Produto Adicionado com Sucesso", background=get_color_from_hex('#0b9b53'))
				self.ids.recycle_view.data = []
				for i in range(len(self.estoque.database.index.values)):
					ids = self.estoque.database.index.values
					categorias = self.estoque.database["CATEGORIA"].values
					produtos = self.estoque.database["PRODUTO"].values
					fornecedores = self.estoque.database["FORNECEDOR"].values
					quantidades = self.estoque.database["QUANTIDADE"].values
					self.ids.recycle_view.data.append(
						{'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]), 'fornecedor_': str(fornecedores[i]), 'quantidade_': str(quantidades[i])})



		except AttributeError:
			toast("Atenção: Todos os Campos Devem ser Preenchidos", background=get_color_from_hex('#b92034'))


	# BARRA DE BUSCA
	def search(self):
		search_for = self.ids.search_bar_clientes.text
		search_for = ' '.join(search_for.split()).upper()
		data_found = self.estoque.search_item(search_for)

		if search_for == "":
			self.ids.recycle_view.data = []
			# ATUALIZAR ITEMS
			for i in range(len(self.estoque.database.index.values)):
				ids = self.estoque.database.index.values
				categorias = self.estoque.database["CATEGORIA"].values
				produtos = self.estoque.database["PRODUTO"].values
				fornecedores = self.estoque.database["FORNECEDOR"].values
				quantidades = self.estoque.database["QUANTIDADE"].values
				self.ids.recycle_view.data.append(
					{'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]),
					 'fornecedor_': str(fornecedores[i]), 'quantidade_': str(quantidades[i])})


		else:
			if len(data_found) == 0:
				toast(f"Atenção: Nenhum Resultado Encontrado",background=get_color_from_hex('#b92034'))
				self.ids.recycle_view.data = []
				self.clientes_info_close(self.ids.clientes_info)

			else:
				self.ids.recycle_view.data = []
				toast(f"Resultados Encontrados: {len(data_found)}", background=get_color_from_hex('#0b9b53'))
				# ATUALIZAR ITEMS
				for i in range(len(data_found.index.values)):
					ids = data_found.index.values
					categorias = data_found["CATEGORIA"].values
					produtos = data_found["PRODUTO"].values
					fornecedores = data_found["FORNECEDOR"].values
					quantidades = data_found["QUANTIDADE"].values
					self.ids.recycle_view.data.append(
						{'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]),  'fornecedor_': str(fornecedores[i]), 'quantidade_': str(quantidades[i])})

	# DIALOG CRIAR NOVO PRODUTO
	class Conteudo_NovoProduto(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	novo_produto = None
	def novo_produto_(self, root, *args):
		if not self.novo_produto:
			self.novo_produto = MDDialog(
					title=f'[color=#323335]Novo Produto[/color]',
					md_bg_color=get_color_from_hex('#eeeeee'),
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_NovoProduto(),
					buttons=[
						MDFlatButton(
							text=f"[color=#323335][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_),
						MDFlatButton(
							text=f"[color=#323335][b]ADICIONAR PRODUTO[/color][/b]",
							theme_text_color="Custom",
							on_release=root.AdicionarNovoProduto)])
		self.novo_produto.open()
	def close_(self, obj):
		self.novo_produto.dismiss()


	# DIALOG DE CONFIRMAR REMOÇÃO CLIENTE
	remover_cliente = None
	def confirmacao_remover_cliente(self, root, *args):
		if not self.remover_cliente:
			self.remover_cliente = MDDialog(
				title=f'[color=#eeeeee][b]Deletar Cliente[/b][/color]',
				text="[color=#eeeeee][b]Você deseja realmente excluir este cliente?\nEsse processo é irreversivel e não poderá ser desfeito.[/b][/color]",
				md_bg_color=get_color_from_hex('#323335'),
				type="custom",
				size_hint=[0.4, 0.4],
				auto_dismiss=True,
				buttons=[
					MDFlatButton(
						text=f"[color=#eeeeee][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_remover),
					MDFlatButton(
						text=f"[color=#eeeeee][b]DELETAR CLIENTE[/color][/b]",
						theme_text_color="Custom",
						on_release=root.remove_client)]
			)
		self.remover_cliente.open()
	def close_remover(self, obj):
		self.remover_cliente.dismiss()


	# FUNÇÕES RELACIONADAS A TABELA DE CLIENTES
	def refresh_infos(self, id, categoria, produto, fornecedor, quantidade):
		data_find = self.estoque.data_info(id, categoria, produto, fornecedor, quantidade)
		self.ids.info_id.text = str(data_find.index[0])
		self.ids.info_categoria.text = str(data_find["CATEGORIA"].values[0])
		self.ids.info_produto.text = str(data_find["PRODUTO"].values[0])
		self.ids.info_fornecedor.text = str(data_find["FORNECEDOR"].values[0])
		self.ids.info_estoque.text = str(data_find["QUANTIDADE"].values[0])
		self.ids.info_critico.text = str(data_find["ESTOQUE_CRITICO"].values[0])
	def change_infos(self):
		new_row = [self.ids.info_categoria.text , self.ids.info_produto.text, self.ids.info_fornecedor.text, self.ids.info_estoque.text, self.ids.info_critico.text]

		if self.ids.info_id.text != "":
			self.estoque.change_info(int(self.ids.info_id.text), new_row)
			toast("Alteração Realizada com Sucesso", background=get_color_from_hex('#0b9b53'))
			self.ids.recycle_view.data = []
			for i in range(len(self.estoque.database.index.values)):
				ids = self.estoque.database.index.values
				categorias = self.estoque.database["CATEGORIA"].values
				produtos = self.estoque.database["PRODUTO"].values
				fornecedores = self.estoque.database["FORNECEDOR"].values
				quantidades = self.estoque.database["QUANTIDADE"].values
				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]), 'fornecedor_': str(fornecedores[i]), 'quantidade_': str(quantidades[i])})
		else:
			toast("Atenção: Nenhum Cliente Selecionado", background=get_color_from_hex('#b92034'))
	def remove_client(self, root):
		if self.ids.info_id.text != "":
			self.estoque.remove_data(int(self.ids.info_id.text))
			self.remover_cliente.dismiss()

			# RESETAR TEXTOS
			self.ids.info_id.text = ""
			self.ids.info_categoria.text = ""
			self.ids.info_produto.text = ""
			self.ids.info_fornecedor.text = ""
			self.ids.info_estoque.text = ""
			self.ids.info_critico.text = ""
			self.ids.recycle_view.data = []
			toast("Cliente Removido com Sucesso", background=get_color_from_hex('#0b9b53'))

			# ATUALIZAR ITEMS
			for i in range(len(self.estoque.database.index.values)):
				ids = self.estoque.database.index.values
				categorias = self.estoque.database["CATEGORIA"].values
				produtos = self.estoque.database["PRODUTO"].values
				fornecedores = self.estoque.database["FORNECEDOR"].values
				quantidades = self.estoque.database["QUANTIDADE"].values
				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]),'fornecedor_': str(fornecedores[i]), 'quantidade_': str(quantidades[i])})

		else:
			toast("Atenção: Nenhum Cliente Selecionado", background=get_color_from_hex('#b92034'))

	def on_enter(self):
		def refresh_name(dt):
			self.ids.clientes_header.height = self.ids.menu.children[0].children[0].children[0].children[4].size[1] + 2
			self.ids.clientes_header2.height = self.ids.menu.children[0].children[0].children[0].children[4].size[1] + 2
			self.ids.search_bar_clientes.width = self.ids.search_clientes_box.width * 0.8
		Clock.schedule_interval(refresh_name, 0.05)

		if len(self.ids.recycle_view.data) == 0:
			for i in range(len(self.estoque.database.index.values)):
				ids = self.estoque.database.index.values
				categorias = self.estoque.database["CATEGORIA"].values
				produtos = self.estoque.database["PRODUTO"].values
				fornecedores = self.estoque.database["FORNECEDOR"].values
				quantidades = self.estoque.database["QUANTIDADE"].values
				self.ids.recycle_view.data.append({'id_': str(ids[i]), 'categoria_': str(categorias[i]), 'nome_': str(produtos[i]), 'fornecedor_':str(fornecedores[i]), 'quantidade_':str(quantidades[i])})

class WindowManager(ScreenManager):
	pass

class InvisionStorage(MDApp):
	cinza_1 = ""

	clientes_info_state = NumericProperty(0)
	def clientes_info_open(self, widget, *args):
		animate = Animation(size_hint_x = 0.4, duration=0.05)
		animate.start(widget)
	def clientes_info_close(self, widget, *args):
		animate = Animation(size_hint_x = 0.0, duration=0.05)
		animate.start(widget)

	def estoque_info_open(self, widget, *args):
		animate = Animation(size_hint_x = 0.3, duration=0.05)
		animate.start(widget)
	def estoque_info_close(self, widget, *args):
		animate = Animation(size_hint_x = 0.0, duration=0.05)
		animate.start(widget)

	def on_start(self):
		def refresh_name(dt):
			if Window.size[0] < 800 :
				Window.size = (800,Window.size[1])
			if Window.size[1] < 600:
				Window.size = (Window.size[0],600)

		Clock.schedule_interval(refresh_name, 0.05)

	def build(self):
		self.title = 'Invision Storage'
		self.icon = 'icon.png'
		#return Builder.load_file('InvisionStorage.kv')



	Window.maximize()

	#Window.custom_titlebar = True



if __name__ == '__main__':
	InvisionStorage().run()


