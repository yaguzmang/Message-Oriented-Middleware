# -*- coding: utf-8 -*-
"""
@author: yaguzmang
"""

from collections import deque

class Tarea:

	def __init__(self, nombre, clave_acceso, id_tarea):
		self.id = id_tarea
		self.nombre = nombre
		self.clave_acceso = clave_acceso
		self.estado = True
		self.servers = []
		self.estado_servers = []
		self.tareas = deque()

	def get_servers(self):
		return self.servers

	def set_servers(self, arreglo):
		self.servers = arreglo

	def actualizar_todos_servers(self):
		for i in range(0,len(self.estado_servers)):
			self.estado_servers[i] = False

	def agregar_servers(self, cliente):
		self.servers.append(cliente)
		self.estado_servers.append(False)

	def cambiar_estado_server(self,i):
		self.estado_servers[i] = True

	def get_estados_servers(self):
		return self.estado_servers

	def set_estados_servers(self, arreglo):
		self.estado_servers = arreglo


	def cambiar_indice_envio(self):
		mensaje = self.tareas.popleft()
		return mensaje

	def get_clave_acceso(self):
		return self.clave_acceso

	def get_id(self):
		return self.id

	def get_nombre(self):
		return self.nombre

	def get_tareas(self):
		return self.tareas

	def enviar_mensaje(self, mensaje):
		if (len(self.tareas) < 3):
			self.tareas.append(mensaje)
			return 1
		else:
			return 0

	def conectar(self):
		self.estado = True

	def desconectar(self):
		self.estado = False

	def get_estado(self):
		return self.estado

	def get_cantidad_tareas(self):
		return len(self.tareas)

