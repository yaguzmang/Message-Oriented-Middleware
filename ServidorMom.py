"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import _thread
import socket
import Constantes
import ConstantesServidor
import ConstantesConsumidor
import ConstantesProveedor
import os.path
import string
import random
from Canal import Canal
from Tarea import Tarea
class Mom:

	def __init__(self):
		self.MOM_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sesiones_proveedor = {} # este es el de proveedores
		self.sesiones_consumidor = {}
		self.contador_tokens = 1

		self.canales = {}
		self.tareas = []
		self.tareas_realizadas = []
		self.contador = 0
		self.contador_tareas = 0
		self.consumidores_conectados = {}
		self.contador_consumidores = 0

	def hilo(self, conexion_aplicacion, direccion_aplicacion):
		while True:
			datos_recibidos = conexion_aplicacion.recv(1024)
			datos_recibidos = str(datos_recibidos.decode("utf-8"))
			arreglo = datos_recibidos.split()
			opcion = arreglo[0]

			if (opcion == ConstantesServidor.salir):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} Vuelva pronto\n'
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'La aplicación {direccion_aplicacion[0]}:{direccion_aplicacion[1]} se desconectó correctamente')
				break
			# loggin y registro para proveedores
			elif(opcion == ConstantesServidor.registrar):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				arreglo_proveedores = self.lista_proveedores()
				proveedor_exixtente,igual_clave = self.proveedor_repetido(arreglo_proveedores,arreglo[1],arreglo[2])
				if(not(proveedor_exixtente)):
					print(f'el nombre del proveedor es: {arreglo[1]} \ncon contraseña: {arreglo[2]}')
					txt = str("\n"+arreglo[1] + "->" +arreglo[2])
					f = open('proveedores.txt', 'a')
					f.write(txt)
					f.close()
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} se creo correctamente el proveedor\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				else:
					print(f'El nombre del proveedor es: {arreglo[1]}')
					print("No se creo el proveedor porque ya hay un proveedor con ese nombre")
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} no se creo el proveedor porque ya hay un proveedor con ese nombre\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.conectar):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				arreglo_proveedores = self.lista_proveedores()
				proveedor_exixtente,igual_clave = self.proveedor_repetido(arreglo_proveedores,arreglo[1],arreglo[2])
				if (proveedor_exixtente):
					if(igual_clave):
						if(not(arreglo[1] in self.sesiones_proveedor)):
							token = self.random_char(self.contador_tokens)
							self.sesiones_proveedor[arreglo[1]]= token
						print(f'Al proveedor: {arreglo[1]} se le asigno el token: {self.sesiones_proveedor[arreglo[1]]}')
						respuesta = f'token={self.sesiones_proveedor[arreglo[1]]}'
						conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
						print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
						self.contador_tokens +=1
					else:
						print(f'Contraseña incorrecta para el proveedor: {arreglo[1]}')
						respuesta = f'Contraseña incorrecta'
						conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
						print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				else:
					print(f'No esxiste un proveedor con nombre: {arreglo[1]}')
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} no hay un proveedor con el nombre de {arreglo[1]}'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
			# loggin y registro para consumidores
			elif (opcion == ConstantesServidor.registrar_consumidor):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				arreglo_consumidores = self.lista_consumidores()
				consumidor_exixtente, igual_clave = self.proveedor_repetido(arreglo_consumidores, arreglo[1], arreglo[2])
				if (not (consumidor_exixtente)):
					print(f'el nombre del proveedor es: {arreglo[1]} \ncon contraseña: {arreglo[2]}')
					txt = str("\n" + arreglo[1] + "->" + arreglo[2])
					f = open('consumidores.txt', 'a')
					f.write(txt)
					f.close()
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} se creo correctamente el consumidor\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				else:
					print(f'El nombre del consumidor es: {arreglo[1]}')
					print("No se creo el consumidor porque ya hay un proveedor con ese nombre")
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} no se creo el consumidor porque ya hay un consumidor con ese nombre\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.conectar_consumidor):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				arreglo_consumidores = self.lista_consumidores()
				consumidor_exixtente, igual_clave = self.proveedor_repetido(arreglo_consumidores, arreglo[1], arreglo[2])
				if (consumidor_exixtente):
					if (igual_clave):
						if (not (arreglo[1] in self.sesiones_consumidor)):
							token = self.random_char(self.contador_tokens)
							self.sesiones_consumidor[arreglo[1]] = token
						print(f'Al consumidor: {arreglo[1]} se le asigno el token: {self.sesiones_consumidor[arreglo[1]]}')
						respuesta = f'token={self.sesiones_consumidor[arreglo[1]]}'
						conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
						print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
						self.contador_tokens += 1
					else:
						print(f'Contraseña incorrecta para el consumidor: {arreglo[1]}')
						respuesta = f'Contraseña incorrecta'
						conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
						print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				else:
					print(f'No esxiste un consumidor con nombre: {arreglo[1]}')
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} no hay un consumidor con el nombre de {arreglo[1]}'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
					print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
			elif (opcion == ConstantesServidor.crear_canal):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				c_canal = Canal(arreglo[1], arreglo[2], self.contador)
				self.canales[self.contador] = c_canal
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} El canal fue creado correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion del canal: {self.contador}\n'
				self.contador = self.contador + 1
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
            
			elif (opcion == ConstantesServidor.listar_canal):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} Listado de canales\n'
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				respuesta = ''
				if (len(self.canales) == 0):
					respuesta = 'No hay canales en el MOM\n'
				else:
					contador_canales = 0
					for canal in self.canales:
						id_canal = canal
						if(self.canales[id_canal].get_token_proveedor() == arreglo[1]):
							contador_canales += 1
							respuesta = respuesta + f'Canal {self.canales[id_canal].get_id()}: {self.canales[id_canal].get_nombre()} estado: {self.canales[id_canal].get_estado()}\n'
					if(contador_canales == 0):
						respuesta = f'Respuesta para: {direccion_aplicacion[0]} Usted no posee canales\n'
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.crear_tarea):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				c_tarea = Tarea(arreglo[1], self.contador_tareas)
				self.tareas.append(c_tarea)
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} La tarea fue creada correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion de la tarea: {self.contador_tareas}\n'
				self.contador_tareas = self.contador_tareas + 1
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.listar_tareas):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} Listado de tareas\n'
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				respuesta = ''
				if (len(self.tareas) == 0):
					respuesta = 'No hay tareas en el MOM\n'
				else:
					for tarea in self.tareas:
						respuesta = respuesta + f'Tarea {tarea.get_id()}: {tarea.get_nombre()}\n'

				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.borrar_canal):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				id_canal = arreglo[2]
				nombre_canal = arreglo[1]
				token_proveedor = arreglo[3]
				try:
					nombre_auxiliar = self.canales[int(id_canal)].get_nombre()
					token_proveedor_aux = self.canales[int(id_canal)].get_token_proveedor()
					id_auxiliar = self.canales[int(id_canal)].get_id()
					if (str(id_canal) == str(id_auxiliar) and str(nombre_canal) == str(nombre_auxiliar) and str(token_proveedor_aux) == str(token_proveedor)):
						if (len(self.canales[int(id_canal)].consumidores) == 0):
							respuesta = f'Respuesta para: {direccion_aplicacion[0]} El canal fue eliminada correctamente\n'
							self.canales.pop(int(id_canal))
						else:
							respuesta = f'Respuesta para: {direccion_aplicacion[0]} El canal no fue eliminado puesto que aún contiene mensajes\n'       
				except:
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
			elif (opcion == ConstantesConsumidor.listar_canal):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				respuesta = f'Respuesta para: {direccion_aplicacion[0]} Listado de canales\n'
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				respuesta = ''
				if (len(self.canales) == 0):
					respuesta = 'No hay canales en el MOM\n'
				else:
					for id_canal in self.canales:
						respuesta = respuesta + f'Canal {self.canales[id_canal].get_id()}: {self.canales[id_canal].get_nombre()} estado: {self.canales[id_canal].get_estado()}\n'

				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
			elif (opcion == ConstantesConsumidor.conectar_consumidor):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				nombre_canal = arreglo[1]
				id_canal = arreglo[2]
				token_consumidor = arreglo[3]
				respuesta = ""
				try:
					nombre_auxiliar = self.canales[int(id_canal)].get_nombre()
					id_auxiliar = self.canales[int(id_canal)].get_id()
					if (str(id_canal) == str(id_auxiliar) and str(nombre_canal) == str(nombre_auxiliar)):
						if token_consumidor not in self.canales[int(id_canal)].get_consumidores():
							self.canales[int(id_canal)].agregar_consumidor(token_consumidor)
							respuesta = f'Respuesta para: {direccion_aplicacion[0]} La conexión se estableció correctamente, ahora puedes recibir mensajes de este canal\n'
						else:
							respuesta = f'Respuesta para: {direccion_aplicacion[0]} Usted YA se encuentra suscrito en este canal\n'
						conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
						
				except:
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} No hay conexión, prueba nuevamente\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
			elif (opcion == ConstantesProveedor.enviar_mensaje):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				nombre_canal = arreglo[1]
				id_canal = arreglo[2]
				mensaje = arreglo[4:]
				token_proveedor = arreglo[3]
				respuesta = ""
				try:
					nombre_auxiliar = self.canales[int(id_canal)].get_nombre()
					id_auxiliar = self.canales[int(id_canal)].get_id()
					token_proveedor_aux = self.canales[int(id_canal)].get_token_proveedor()
					if (str(id_canal) == str(id_auxiliar) and str(nombre_canal) == str(nombre_auxiliar) and str(token_proveedor) == str(token_proveedor_aux)):
						consumidores = self.canales[int(id_canal)].get_consumidores()
						for clave in consumidores.keys():
							consumidores[clave].append(mensaje)
						respuesta = f'Respuesta para: {direccion_aplicacion[0]} El mensaje se transmitió correctamente al canal elegido\n'
					else:
						respuesta = f'Respuesta para: {direccion_aplicacion[0]} Datos errones, intente nuevamente\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				except:
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} No hay conexión, prueba nuevamente\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
			elif (opcion == ConstantesConsumidor.recibir_mensaje):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				nombre_canal = arreglo[1]
				id_canal = arreglo[2]
				token_consumidor = arreglo[3]
				respuesta = ""
				try:
					nombre_auxiliar = self.canales[int(id_canal)].get_nombre()
					id_auxiliar = self.canales[int(id_canal)].get_id()
					if (str(id_canal) == str(id_auxiliar) and str(nombre_canal) == str(nombre_auxiliar)):
						consumidores = self.canales[int(id_canal)].get_consumidores()
						if (token_consumidor in consumidores):
							if (len(consumidores[token_consumidor]) != 0):
								respuesta = f'Respuesta para: {direccion_aplicacion[0]} El mensaje es: {" ".join(consumidores[token_consumidor].pop(0))}\n'
							else:
								respuesta = f'Respuesta para: {direccion_aplicacion[0]} No hay nuevos mensajes\n'
						else:
							respuesta = f'Respuesta para: {direccion_aplicacion[0]} Usted no se encuentra suscrito en este canal\n'
					else:
						respuesta = f'Respuesta para: {direccion_aplicacion[0]} Datos erroneos, intente nuevamente\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				except:
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} No hay conexión, prueba nuevamente\n'
					conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
					
		conexion_aplicacion.close()

	def random_char(self,y):
		if (y>20):
			self.contador_tokens = 2
			y=2
		return ''.join(random.choice(string.ascii_letters) for x in range(y))

	def lista_proveedores(self):
		if (not (os.path.isfile("proveedores.txt"))):
			f = open('proveedores.txt', 'w')
			f.close()
		f = open('proveedores.txt', 'r')
		arreglo_proveedores = f.readlines()
		f.close()
		return arreglo_proveedores

	def lista_consumidores(self):
		if (not (os.path.isfile("consumidores.txt"))):
			f = open('consumidores.txt', 'w')
			f.close()
		f = open('consumidores.txt', 'r')
		arreglo_consumidores = f.readlines()
		f.close()
		return arreglo_consumidores

	def proveedor_repetido(self, arreglo_proveedores,nuevo_proveedor,clave_proveedor):
		proveedor_exixtente = False
		igual_clave = False
		for i in arreglo_proveedores:
			i = str(i).split("->")
			if (nuevo_proveedor == str(i[0])):
				proveedor_exixtente = True
				if (str(clave_proveedor).rstrip('\n') == str(i[1]).rstrip('\n')):
					igual_clave = True
		return proveedor_exixtente,igual_clave

	def main(self):
		print('*' * 50)
		print('El MOM está encendido\n')
		print('La dirección IP del servidor MOM es: ', Constantes.direccion_conexion_servidor)
		print('El puerto por el cual está corriendo el servidor MOM es: ', Constantes.puerto)
		tupla_conexion = (Constantes.direccion_conexion_servidor, Constantes.puerto)
		self.MOM_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.MOM_server.bind(tupla_conexion)
		self.MOM_server.listen(Constantes.reserva)
		while True:
			conexion_aplicacion, direccion_aplicacion = self.MOM_server.accept()
			print(f'Nueva aplicación conectada desde la dirección IP: {direccion_aplicacion[0]}')
			_thread.start_new_thread(self.hilo, (conexion_aplicacion, direccion_aplicacion))
		self.MOM_server.close()

def mom():
	mom = Mom()
	mom.main()

if __name__ == '__main__':
	mom()
