"""

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import socket
import Constantes
import ConstantesConsumidor
import time
import random

class Server:
    def __init__(self):
        self.token = "tokenejemplo1"

    def run_app(self):
        print('*' * 50)
        print("SERVER RUNNING\n")
        tarea_fue_realizada = False
        while True:
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.connect((Constantes.direccion_conexion_consumidor, Constantes.puerto))
            tupla_conexion = self.socket_server.getsockname()
            print("SERVER CONNECTED: ", tupla_conexion)
            envio_MOM = ConstantesConsumidor.asignar_tarea
            self.socket_server.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = self.socket_server.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
            datos_recibidos = self.socket_server.recv(Constantes.tamaño_buffer)
            print('Mensaje recibido')
            respuesta = datos_recibidos.decode(Constantes.formato_decodificacion)
            if respuesta.lower().strip() == "No hay tareas en el MOM".lower().strip():
               tarea_fue_realizada = False
               print(respuesta)
               self.socket_server.close()
               time.sleep(5)
            else:
                print("Tarea a realizar: " + respuesta)
                info_tarea = respuesta.split(':')
                self.socket_server.close()
                tiempo_ex = random.randint(5, 10)
                time.sleep(tiempo_ex)
                tarea_fue_realizada = True
                self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_server.connect((Constantes.direccion_conexion_consumidor, Constantes.puerto))
                tupla_conexion = self.socket_server.getsockname()
                envio_MOM = ConstantesConsumidor.tarea_realizada + ' ' +  info_tarea[0] + ' ' + info_tarea[1] + ' ' + str(tiempo_ex)
                self.socket_server.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datos_recibidos = self.socket_server.recv(Constantes.tamaño_buffer)
                respuesta = datos_recibidos.decode(Constantes.formato_decodificacion)
                self.socket_server.close()
                print(respuesta)
def main():
    server()
    
def server():
	server = Server()
	server.run_app()

if __name__ == '__main__':
	server()
