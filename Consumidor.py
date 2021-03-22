"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""

import socket
import Constantes
import ConstantesConsumidor

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
        opcion = menu()
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
        elif (opcion == ConstantesConsumidor.conectar_consumidor):
            nombre_canal = input("Ingresa el nombre del canal al que te quieres conectar ")
            envio_MOM = opcion + ' ' + nombre_canal
            socket_consumidor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            while True:
                datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
                mensaje = datos_recibidos.decode(Constantes.formato_decodificacion)
                print(mensaje)
                if (mensaje[len(mensaje)-10:] == "nuevamente"):
                    break
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
        else:
            print("Opción invalida, intenta de nuevo\n")

    socket_consumidor.send(bytes(opcion, Constantes.formato_decodificacion))
    datos_recibidos = socket_consumidor.recv(Constantes.tamaño_buffer)
    print(datos_recibidos.decode(Constantes.formato_decodificacion))
    socket_consumidor.close()


def menu():
    print("OPCION REGISTRAR_CONSUMIDOR: Para registrar un nuevo proveedor ingresa REGISTRAR_CONSUMIDOR nombre_proveedor contraseña_proveedor")
    print("OPCION CONECTAR_CONSUMIDOR: Para conectarse como proveedor ingresa CONECTAR_CONSUMIDOR nombre_proveedor contraseña_proveedor")
    print("OPCION LISTAR: Listado de Colas en el MOM")
    print("OPCION CONECTAR_CONSUMIDOR_CANAL: Conexión a una Cola del MOM")
    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrese la opcion que quiere realizar ")
    return opcion


if __name__ == '__main__':
    main()
