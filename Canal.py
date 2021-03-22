# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:29:09 2021

@author: jsperezs
"""

from collections import deque

class Canal:

	def __init__(self, nombre, token_proveedor, id_canal):
		self.id = id_canal
		self.nombre = nombre
		self.token_proveedor = token_proveedor
		self.estado = True
		self.consumidores = {}
		self.canal = deque()

	def get_consumidores(self):
		return self.consumidores

	def set_consumidores(self, arreglo):
		self.consumidores = arreglo

	def agregar_consumidor(self, token_consumidor):
		self.consumidores[token_consumidor] = []

	def get_token_proveedor(self):
		return self.token_proveedor

	def get_id(self):
		return self.id

	def get_nombre(self):
		return self.nombre

	def get_canal(self):
		return self.canal

	def enviar_mensaje(self, mensaje):
		if (len(self.canal) < 3):
			self.canal.append(mensaje)
			return 1
		else:
			return 0

	def conectar(self):
		self.estado = True

	def desconectar(self):
		self.estado = False

	def get_estado(self):
		return self.estado

	def get_tamaño_canal(self):
		return len(self.canal)

