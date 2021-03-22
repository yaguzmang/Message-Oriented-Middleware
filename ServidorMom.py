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

class Mom:

	def __init__(self):
		self.MOMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sesiones = {}
		self.contador_tokens = 1

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

		conexion_aplicacion.close()

	def random_char(self,y):
		if (y>15):
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
		self.MOMserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.MOMserver.bind(tupla_conexion)
		self.MOMserver.listen(Constantes.reserva)
		while True:
			conexion_aplicacion, direccion_aplicacion = self.MOMserver.accept()
			print(f'Nueva aplicación conectada desde la dirección IP: {direccion_aplicacion[0]}')
			_thread.start_new_thread(self.hilo, (conexion_aplicacion, direccion_aplicacion))
		self.MOMserver.close()

def mom():
	mom = Mom()
	mom.main()

if __name__ == '__main__':
	mom()
