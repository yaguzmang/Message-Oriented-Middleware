"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import socket
import Constantes
import ConstantesProveedor
socket_proveedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
token = ""

def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación consumidora al MOM\n")
    socket_proveedor.connect((Constantes.direccion_conexion_proveedor, Constantes.puerto))
    tupla_conexion = socket_proveedor.getsockname()
    print("Tu dirección de conexión es: ", tupla_conexion)

    while True:
        opcion = menu()
        if(opcion.split()[0] == ConstantesProveedor.salir):
            socket_proveedor.send(bytes(opcion, Constantes.formato_decodificacion))
            datosRecibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datosRecibidos.decode(Constantes.formato_decodificacion))
            socket_proveedor.close()
            break

        elif (opcion.split()[0] == ConstantesProveedor.registrar):
            envioMOM = opcion
            socket_proveedor.send(bytes(envioMOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datosRecibidos.decode(Constantes.formato_decodificacion))

        elif (opcion.split()[0] == ConstantesProveedor.conectar):
            envioMOM = opcion
            socket_proveedor.send(bytes(envioMOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            respuesta= datosRecibidos.decode(Constantes.formato_decodificacion)
            if(respuesta[0:6] == "token="):
                token = respuesta[6:]
                print("Bienvenido "+ opcion.split()[1])
            elif(respuesta == "Contraseña incorrecta"):
                print("Contraseña incorrecta para el proveedor " + opcion.split()[1])
            else:
                print("No existe un proveedor que se llame " + opcion.split()[1])
        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

def menu():
    print("OPCION REGISTRAR: Para registrar un nuevo proveedor ingresa REGISTRAR nombre_proveedor contraseña_proveedor")
    print("OPCION CONECTAR: Para conectarse como proveedor ingresa CONECTAR nombre_proveedor contraseña_proveedor")
    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    while(not(str(opcion).split()[0] in ConstantesProveedor.constantes_proveedor)):
        opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion


if __name__ == '__main__':
    main()