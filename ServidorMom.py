"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import _thread
import socket
import Constantes
import ConstantesServidor
import os.path
import string
import random
from Canal import Canal

class Mom:

	def __init__(self):
		self.MOM_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sesiones = {} # este es el de proveedores
		self.sesiones_consumidor = {}
		self.contador_tokens = 1

		self.canales = {}
		self.contador = 0
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
						if(not(arreglo[1] in self.sesiones)):
							token = self.random_char(self.contador_tokens)
							self.sesiones[arreglo[1]]= token
						print(f'Al proveedor: {arreglo[1]} se le asigno el token: {self.sesiones[arreglo[1]]}')
						respuesta = f'token={self.sesiones[arreglo[1]]}'
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
					for canal in self.canales:
						id_canal = canal
						if(self.canales[id_canal].get_token_proveedor() == arreglo[1]):
							respuesta = respuesta + f'Canal {self.canales[id_canal].get_id()}: {self.canales[id_canal].get_nombre()} estado: {self.canales[id_canal].get_estado()}\n'

				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')

			elif (opcion == ConstantesServidor.borrar_canal):
				print(f'{direccion_aplicacion[0]} solicita: {opcion}')
				id_canal = arreglo[3]
				nombre_canal = arreglo[1]
				clave_acceso = arreglo[2]
				try:
					nombre_auxiliar = self.canales[int(id_canal)].get_nombre()
					clave_auxiliar = self.canales[int(id_canal)].get_token_proveedor()
					id_auxiliar = self.canales[int(id_canal)].get_id()
					if (str(id_canal) == str(id_auxiliar) and str(nombre_canal) == str(nombre_auxiliar) and str(
							clave_auxiliar) == str(clave_acceso)):
						respuesta = f'Respuesta para: {direccion_aplicacion[0]} El canal fue eliminada correctamente\n'
						self.canales.pop(int(id_canal))
				except:
					respuesta = f'Respuesta para: {direccion_aplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
				print(f'Se envio respuesta a: {direccion_aplicacion[0]} por la solicitud: {opcion}')
				conexion_aplicacion.sendall(respuesta.encode(Constantes.formato_decodificacion))


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
