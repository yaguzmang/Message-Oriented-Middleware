# -*- coding: utf-8 -*-
"""
@author: yaguzmang
"""

class Tarea:

	def __init__(self, nombre, id_tarea):
		self.id = id_tarea
		self.nombre = nombre

	def get_id(self):
		return self.id

	def get_nombre(self):
		return self.nombre

