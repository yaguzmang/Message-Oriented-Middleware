"""
Created on Created on Sun Mar 21 2021

@author: Daniel Felipe Gomez Martinez, Juan Sebastian Perez Salazar and Yhoan Alejandro Guzman Garcia
"""
from colorama import init, Fore, Back, Style

direccion_conexion_servidor = "0.0.0.0" # 0.0.0.0
direccion_conexion_consumidor = "54.83.133.119" # 54.83.133.119
direccion_conexion_proveedor = "54.83.133.119" # 54.83.133.119
puerto = 8080 #8080
reserva = 5
tamaño_buffer = 1024
formato_decodificacion = "utf-8"
comandos = Fore.CYAN + Style.BRIGHT
error = Fore.RED + Style.BRIGHT
exito = Fore.GREEN + Style.BRIGHT
entradas = Fore.YELLOW + Style.BRIGHT
blanco = Fore.WHITE + Style.BRIGHT