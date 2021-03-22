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
    global token
    print('*' * 50)
    print("Estás conectando una nueva aplicación proveedora al MOM\n")
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
            envio_MOM = opcion
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datosRecibidos.decode(Constantes.formato_decodificacion))

        elif (opcion.split()[0] == ConstantesProveedor.conectar):
            envio_MOM = opcion
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datosRecibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            respuesta= datosRecibidos.decode(Constantes.formato_decodificacion)
            if(respuesta[0:6] == "token="):
                token = respuesta[6:]
                print("Bienvenido "+ opcion.split()[1])
            elif(respuesta == "Contraseña incorrecta"):
                print("Contraseña incorrecta para el proveedor " + opcion.split()[1])
            else:
                print("No existe un proveedor que se llame " + opcion.split()[1])

        elif (opcion == ConstantesProveedor.crear_canal):
            nombre_canal = input("Ingresa el nombre del canal ")
            envio_MOM = opcion + ' ' + nombre_canal + ' ' + token
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))

        elif (opcion == ConstantesProveedor.crear_tarea):
            nombre_canal = input("Ingresa el nombre de la tarea")
            envio_MOM = opcion + ' ' + nombre_canal + ' ' + token
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))

        elif (opcion == ConstantesProveedor.listar_canal):
            envio_MOM = opcion +' '+ token
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))

        elif (opcion == ConstantesProveedor.listar_tareas_cola):
            envio_MOM = opcion +' '+ token
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))

        elif (opcion == ConstantesProveedor.borrar_canal):
            nombre_canal = input("Ingresa el nombre del canal a eliminar ")
            id_canal = input("Ingresa el token de identificacion del canal a eliminar ")
            envio_MOM = opcion + ' ' + nombre_canal + ' ' + token + ' ' + id_canal
            socket_proveedor.send(bytes(envio_MOM, Constantes.formato_decodificacion))
            datos_recibidos = socket_proveedor.recv(Constantes.tamaño_buffer)
            print(datos_recibidos.decode(Constantes.formato_decodificacion))

        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

def menu():
    print("OPCION REGISTRAR: Para registrar un nuevo proveedor ingresa REGISTRAR nombre_proveedor contraseña_proveedor")
    print("OPCION CONECTAR: Para conectarse como proveedor ingresa CONECTAR nombre_proveedor contraseña_proveedor")
    print("OPCION CREAR_CANAL: Crear un nuevo canal")
    print("OPCION LISTAR_CANAL: Listado de canales en el MOM")
    print("OPCION BORRAR_CANAL: Eliminar un canal del MOM")
    print("OPCION CREAR_TAREA: Crear una nueva tarea")
    print("OPCION LISTAR_TAREAS_COLA: Listado de las tareas en cola en el MOM")
    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    while(not(str(opcion).split()[0] in ConstantesProveedor.constantes_proveedor)):
        opcion = input("Ingrese la opcion que quiere realizar ")
    return opcion


if __name__ == '__main__':
    main()