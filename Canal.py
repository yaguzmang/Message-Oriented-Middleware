# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:29:09 2021

@author: jsperezs
"""

from collections import deque

class Canal:

	def __init__(self, nombre, clave_acceso, id_canal):
		self.id = id_canal
		self.nombre = nombre
		self.clave_acceso = clave_acceso
		self.estado = True
		self.consumidores = []
		self.estado_consumidores = []
		self.canal = deque()

	def get_consumidores(self):
		return self.consumidores

	def set_consumidores(self, arreglo):
		self.consumidores = arreglo

	def actualizar_todos_consumidores(self):
		for i in range(0,len(self.estado_consumidores)):
			self.estado_consumidores[i] = False

	def agregar_consumidor(self, cliente):
		self.consumidores.append(cliente)
		self.estado_consumidores.append(False)

	def cambiar_estado_consumidor(self,i):
		self.estado_consumidores[i] = True

	def get_estados_consumidores(self):
		return self.estado_consumidores

	def set_estados_consumidores(self, arreglo):
		self.estado_consumidores = arreglo


	def cambiar_indice_envio(self):
		mensaje = self.canal.popleft()
		return mensaje

	def get_clave_acceso(self):
		return self.clave_acceso

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

