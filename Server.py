"""

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import socket
import Constantes
import ConstantesConsumidor
import time

class App:
    def __init__(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = "tokenejemplo1"

    def run_app(self):
        while True:
            print('Hola Mundo!')
            time.sleep(10)
        print('*' * 50)
        print("SERVER RUNNING\n")
        socket_consumidor.connect((Constantes.direccion_conexion_consumidor, Constantes.puerto))
        tupla_conexion = socket_consumidor.getsockname()
        print("SERVER CONNECTED: ", tupla_conexion)

        while True:
            if opcion == '':
                print("Opcion invalida, intenta de nuevo\n")
            elif (opcion == ConstantesConsumidor.conectar_consumidor):
                nombre_canal = input("Ingresa el nombre del canal al que te quieres conectar ")
                id_canal = input("Ingresa el id del canal al que te quieres conectar ")
                envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token 
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
            elif (opcion == ConstantesConsumidor.listar_canal):
                envio_MOM = opcion
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
            elif (opcion.split()[0] == ConstantesConsumidor.registrar):
                envio_MOM = opcion
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datosRecibidos.decode(Constantes.formato_decodificacion))

            elif (opcion.split()[0] == ConstantesConsumidor.conectar):
                envio_MOM = opcion
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                respuesta= datosRecibidos.decode(Constantes.formato_decodificacion)
                if(respuesta[0:6] == "token="):
                    token = respuesta[6:]
                    print("Bienvenido "+ opcion.split()[1])
                elif(respuesta == "Contraseña incorrecta"):
                    print("Contraseña incorrecta para el proveedor " + opcion.split()[1])
                else:
                    print("No existe un proveedor que se llame " + opcion.split()[1])
            elif (opcion == ConstantesConsumidor.recibir_mensaje):
                if(token != ""):
                    nombre_canal = input("Ingresa el nombre del canal del cual quieres recibir un mensaje ")
                    id_canal = input("Ingresa el id del canal del cual quieres recibir un mensaje ")
                    envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token
                    socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                    datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                    print(datosRecibidos.decode(Constantes.formato_decodificacion))
            else:
                print("Opción invalida, intenta de nuevo\n")

        socket_consumidor.send(bytes(opcion, Constantes.formato_decodificacion))
        datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
        print(datos_recibidos.decode(Constantes.formato_decodificacion))
        socket_consumidor.close()


socket_consumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
token = ""

def main():
    print('*' * 50)
    print("SERVER RUNNING\n")
    socket_consumidor.connect((Constantes.direccion_conexion_consumidor, Constantes.puerto))
    tupla_conexion = socket_consumidor.getsockname()
    print("SERVER CONNECTED: ", tupla_conexion)

    while True:
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
        elif (opcion == ConstantesConsumidor.conectar_consumidor):
            nombre_canal = input("Ingresa el nombre del canal al que te quieres conectar ")
            id_canal = input("Ingresa el id del canal al que te quieres conectar ")
            envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token 
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
        elif (opcion == ConstantesConsumidor.listar_canal):
            envio_MOM = opcion
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
            datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
        elif (opcion.split()[0] == ConstantesConsumidor.registrar):
            envio_MOM = opcion
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            print(datosRecibidos.decode(Constantes.formato_decodificacion))

        elif (opcion.split()[0] == ConstantesConsumidor.conectar):
            envio_MOM = opcion
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            respuesta= datosRecibidos.decode(Constantes.formato_decodificacion)
            if(respuesta[0:6] == "token="):
                token = respuesta[6:]
                print("Bienvenido "+ opcion.split()[1])
            elif(respuesta == "Contraseña incorrecta"):
                print("Contraseña incorrecta para el proveedor " + opcion.split()[1])
            else:
                print("No existe un proveedor que se llame " + opcion.split()[1])
        elif (opcion == ConstantesConsumidor.recibir_mensaje):
            if(token != ""):
                nombre_canal = input("Ingresa el nombre del canal del cual quieres recibir un mensaje ")
                id_canal = input("Ingresa el id del canal del cual quieres recibir un mensaje ")
                envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datosRecibidos.decode(Constantes.formato_decodificacion))
        else:
            print("Opción invalida, intenta de nuevo\n")

    socket_consumidor.send(bytes(opcion, Constantes.formato_decodificacion))
    datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
    print(datos_recibidos.decode(Constantes.formato_decodificacion))
    socket_consumidor.close()

def server():
	server = Server()
	server.main()

if __name__ == '__main__':
	server()
