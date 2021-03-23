"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import socket
import Constantes
import ConstantesConsumidor
from colorama import init

socket_consumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
token = ""

def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación consumidora al MOM\n")
    socket_consumidor.connect((Constantes.direccion_conexion_consumidor, Constantes.puerto))
    tupla_conexion = socket_consumidor.getsockname()
    print("Tu dirección de conexión es: ", tupla_conexion)
    opcion = menu()

    while opcion != ConstantesConsumidor.salir:
        
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
        elif (opcion == ConstantesConsumidor.conectar_consumidor):
            if (token != ""):
                print(Constantes.entradas)
                nombre_canal = input("Ingresa el nombre del canal al que te quieres conectar ")
                id_canal = input("Ingresa el id del canal al que te quieres conectar ")
                envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token
                print(Constantes.exito)
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
            else:
                print(Constantes.error)
                print("Debe logearse primero\n")

        elif (opcion == ConstantesConsumidor.listar_canal):
            if (token != ""):
                print(Constantes.exito)
                envio_MOM = opcion
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datos_recibidos.decode(Constantes.formato_decodificacion))
            else:
                print(Constantes.error)
                print("Debe logearse primero\n")

        elif (opcion.split()[0] == ConstantesConsumidor.registrar):
            envio_MOM = opcion
            print(Constantes.exito)
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
            print(datosRecibidos.decode(Constantes.formato_decodificacion))

        elif (opcion.split()[0] == ConstantesConsumidor.conectar):
            if (token == ""):
                try:
                    arreglo0 = opcion[0]
                    arreglo1 = opcion[1]
                    arreglo2 = opcion[2]
                    if (arreglo0 != "" and arreglo1 != "" and arreglo2 != ""):
                        envio_MOM = opcion
                        socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                        datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                        respuesta= datosRecibidos.decode(Constantes.formato_decodificacion)
                        if(respuesta[0:6] == "token="):
                            print(Constantes.exito)
                            token = respuesta[6:]
                            print("Bienvenido "+ opcion.split()[1])
                        elif(respuesta == "Contraseña incorrecta"):
                            print(Constantes.error)
                            print("Contraseña incorrecta para el consumidor " + opcion.split()[1])
                        else:
                            print(Constantes.error)
                            print("No existe un consumidor que se llame " + opcion.split()[1])
                    else:
                        print(Constantes.error)
                        print("Llene correctamente los campos nombre_consumidor y contraseña_consumidor\n")
                except:
                    print(Constantes.error)
                    print("Recuerde que la sintaxis es CONECTAR_CONSUMIDOR nombre_consumidor contraseña_consumidor\n")
            else:
                print(Constantes.error)
                print("Debe desconectarse primero\n")

        elif (opcion == ConstantesConsumidor.recibir_mensaje):
            if(token != ""):
                print(Constantes.exito)
                nombre_canal = input("Ingresa el nombre del canal del cual quieres recibir un mensaje ")
                id_canal = input("Ingresa el id del canal del cual quieres recibir un mensaje ")
                envio_MOM = opcion + ' ' + nombre_canal + ' ' + id_canal + ' ' + token
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datosRecibidos.decode(Constantes.formato_decodificacion))
            else:
                print(Constantes.error)
                print("Debe logearse primero\n")

        elif (opcion.split()[0] == ConstantesConsumidor.desconectar):
            if (token != ""):
                print(Constantes.exito)
                envio_MOM = opcion + " " + token
                socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
                datosRecibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                print(datosRecibidos.decode(Constantes.formato_decodificacion))
            else:
                print(Constantes.error)
                print("Debe logearse primero\n")

        else:
            print(Constantes.error)
            print("Opción invalida, intenta de nuevo\n")
        opcion = menu()
    print(Constantes.exito)
    socket_consumidor.send(bytes(opcion, Constantes.formato_decodificacion))
    datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
    print(datos_recibidos.decode(Constantes.formato_decodificacion))
    socket_consumidor.close()


def menu():
    print(Constantes.comandos)
    print("*"*50)
    print("OPCION REGISTRAR_CONSUMIDOR: Para registrar un nuevo proveedor ingresa REGISTRAR_CONSUMIDOR nombre_consumidor contraseña_consumidor")
    print("OPCION CONECTAR_CONSUMIDOR: Para conectarse como proveedor ingresa CONECTAR_CONSUMIDOR nombre_consumidor contraseña_consumidor")
    print("OPCION SALIR: Desconectar aplicación")
    if (token != ""):
        print("OPCION LISTAR: Listado de Colas en el MOM")
        print("OPCION CONECTAR_CONSUMIDOR_CANAL: Conexión a una Cola del MOM")
        print("OPCION DESCONECTAR_CONSUMIDOR: Desconectar consumidor")
        print("OPCION SALIR: Desconectar aplicación")
    print("*"*50)
    print(Constantes.entradas)
    opcion = input("Ingrese la opcion que quiere realizar ")
    return opcion


if __name__ == '__main__':
    init()
    main()
