# Message-Oriented-Middleware :e-mail:
Implementation of a Message-Oriented Middleware 

## Developers
- Daniel Felipe Gómez Martínez
> dfgomezm@eafit.edu.co
- Yhoan Alejandro Guzmán García
> yaguzmang@eafit.du.co
- Juan Sebastián Pérez Salazar
> jsperezs@eafit.du.co

## Requerimientos
- La conexión y desconexión de los usuarios es autenticada para proveedores y consumidores, los servers no se autentican. 
- Un canal solo puede ser eliminado si no se encuentran consumidores conectados a este.
- Si un usuario se desconecta, las colas que este posea en los diferentes canales en los que estaba conectado serán eliminadas, independientemente de si había mensajes en ella.
- Los canales y las colas dentro de los canales están asociados a un token de proveedor y a un token de consumidor respectivamente.
- La recepción de los mensajes se hace por medio de un mecanismo pull, al igual que la recepción de mensajes por parte de los servers. 
- La única persistencia que se maneja es la de los usuarios proveedor y consumidor, cuyos datos son almacenados en archivos para su posterior uso independientemente de sí el MOM se apaga o no. 
- El servidor es tolerante a fallos, por lo que cualquier error que pueda presentarse este lo maneja de manera adecuada para evitar desconexiones.

## Funcionalidad
### Funcionamiento de los task:
Desde el cliente Proveedor se pueden hacer las siguientes acciones:  

- Crear tarea
- Listar tareas (sin realizar)
- Listar tareas realizadas

El funcionamiento es el siguiente: los proveedores pueden crear tareas, estas tareas son enviadas al Servidor MOM donde se ponen en cola.  

A su vez, hay servidores cuyo objetivo es realizar dichas tareas. Estos servidores se comunican con el MOM y piden que se les asigne una tarea. Si no hay tareas disponibles, el servidor se desconecta y después de cierto tiempo pregunta de nuevo si hay tareas por realizar. Si hay alguna tarea disponible, el Servidor MOM le envía esa tarea al servidor, el servidor la recibe y se desconecta, procesa la tarea y cuando termina, se conecta de nuevo con el MOM e informa que ya acabó la tarea asignada y pide una nueva. Cuando el Servidor MOM recibe que la tarea fue realizada, la agrega a la lista de tareas realizadas. La cola de tareas sirve para múltiples proveedores y múltiples servidores. 

El proveedor puede listar tanto las tareas en cola como las tareas realizadas.

### Funcionamiento de los canales
Desde Proveedor se pueden hacer las siguientes acciones con los canales: 

- Crear canal
- Listar canales
- Borrar canal
- Enviar mensaje a un canal

El funcionamiento consiste básicamente en lo siguiente: Los proveedores pueden crear canales, para crear estos canales se debe asignar un nombre al mismo y el MOM le asignará una identificación única, a su vez, este canal será asociado por medio del token del proveedor por lo que solo este proveedor puede borrar, listar y enviar mensajes a este canal. El proveedor solo puede borrar el canal, si en el momento no se encuentran consumidores conectados al canal.

Cuando el proveedor envía un mensaje al canal, el MOM en un hilo individual, recorre dicho canal y ubica el mensaje en cada una de las colas de los consumidores que estén conectados a este canal para que posteriormente un consumidor pueda recibir un mensaje de este u otro canal al que se encuentre conectado haciendo un pull.

Los consumidores a su vez pueden listar todos los canales que haya disponibles para conectarse y así poder verificar el id del canal al cual quiere conectarse. En el momento en el que un consumidor se desconecta de un canal, la cola que este tenga asignada en dicho canal será eliminada, independientemente de los mensajes que se encuentren dentro de esta. La eliminación y ubicación de estas colas se puede realizar gracias a que, en los canales, los consumidores son almacenados en un diccionario, donde la clave es el token del consumidor y el valor es una lista con los mensajes que este reciba por parte del proveedor.

## Diseño del sistema

El diseño elegido que se planteó para la realización del aplicativo es el siguiente:
[![Servidor Mom](https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/servidor_mom.png?raw=true "Servidor Mom")](http://https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/servidor_mom.png "Servidor Mom")
**Imagen 1** - Servidor MOM

Acá se puede evidenciar que hay 3 usuarios, los proveedores, los consumidores y los servers, los proveedores y los consumidores poseen una identificación única que se denomina como token, existe una cola para tareas por realizar y una cola para tareas realizadas en el MOM al igual que un espacio para la creación de canales, donde cada canal contiene una cola por consumidor conectado al mismo. En el diagrama se detallan las acciones que puede realizar cada usuario al igual que la forma en que se da la interacción.

## Arquitectura del sistema
[![Arquitectura del sistema](https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/arquitectura.jpeg?raw=true "Arquitectura del sistema")](http://https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/arquitectura.jpeg "Arquitectura del sistema")
**Imagen 2** - Arquitectura general del MOM

## Implementación
EL servidor _MOM_ se aloja en una máquina virtual de AWS la cual fue configurada con una VPC y una subred por default porque en este caso lo que verdaderamente necesita de una configuración específica es agregar los puertos de comunicación con la máquina en el grupo de seguridad:

[![GrupoSeguridad](https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/grupoDeSeguridad.PNG?raw=true "GrupoSeguridad")](http://https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/grupoDeSeguridad.PNG "GrupoSeguridad")
**Imagen 3** - Grupo de seguridad

Lo fundamental en los grupos de seguridad es abrir el puerto **8080** ya que por este los usuarios (proveedores, servers o consumidores) se conectarán mediante sockets al servidor _MOM_ que estará corriendo en la instancia EC2 de aws. Cabe mencionar que se utilizan sockets debido a que es necesario establecer un sistema de envío de mensajes (fiable y ordenado) entre el _MOM_ y los usuarios, otra ventaja de los sockets es que pertenece a familia de los protocolos de internet **TCP/IP**, la cual solo necesita como parámetros la dirección IP origen y la dirección IP remota (destino). Por lo que solo falta conectar el servidor _MOM_ vía sockets con el IP **0.0.0.0** desde el puerto **8080** y a los usuarios (proveedores, servers o consumidores) con el IP de la instancia (que en nuestro caso creamos un IP elástica y se la asignamos a la instancia) desde el puerto **8080**, como se puede ver en la siguiente imagen.

[![Constantes](https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/codigoConstantes.PNG?raw=true "Constantes")](http://https://github.com/yaguzmang/Message-Oriented-Middleware/blob/main/Diagramas/codigoConstantes.PNG "Constantes")
**Imagen 4** - Código de las constantes

## Uso
### Comandos del proveedor

- **Registrarse:** por medio de este comando un proveedor puede registrarse en el MOM para posteriormente poder conectarse.

	**Estructura**
	```sh
	REGISTRAR [nombre usuario] [password] ↵ (Enter)
	```

- **Conectarse:** por medio de este comando un proveedor puede conectarse al MOM para realizar otras acciones como crear un canal.

	**Estructura**
	```sh
	CONECTAR [nombre usuario] [password] ↵ (Enter)
	```

- **Crear canal:** por medio de este comando un proveedor puede crear una tarea para ser puesta en cola en el MOM. 

	**Estructura**
	```sh
	CREAR_CANAL ↵ (Enter)
	[nombre del canal] ↵ (Enter)
	```

- **Listar canales:** Por medio de este comando un proveedor puede listar los canales que se encuentren asociados a su token.

	**Estructura**
	```sh
	LISTAR_CANAL ↵ (Enter)
	```

- **Borrar canal:** Por medio de este comando un proveedor puede borrar un canal que se encuentre asociado a su token siempre y cuando este canal no tenga ningún consumidor conectado.

	**Estructura**
	```sh
	BORRAR_CANAL ↵ (Enter)
	[nombre del canal] ↵ (Enter)
	[id del canal] ↵ (Enter)
	```

- **Enviar mensaje a un canal:** Por medio de este comando un proveedor puede enviar un mensaje a un canal especifico.

	**Estructura**
	```sh
	ENVIAR_MENSAJE_CANAL ↵ (Enter)
	[nombre del canal] ↵ (Enter)
	[id del canal] ↵ (Enter)
	[mensaje] ↵ (Enter)
	```

- **Crear una tarea:** por medio de este comando un proveedor puede crear una tarea para ser puesta en cola en el MOM.

	**Estructura**
	```sh
	CREAR_TAREA ↵ (Enter)
	[nombre de la tarea] ↵ (Enter)
	```

- **Listar tareas:** Por medio de este comando un proveedor puede listar las tareas que se encuentran en cola en el MOM.

	**Estructura**
	```sh
	LISTAR_TAREAS ↵ (Enter)
	```

- **Listar tareas realizadas:** Por medio de este comando un proveedor puede listar las tareas que ya han sido realizadas.

	**Estructura**
	```sh
	LISTAR_TAREAS_R ↵ (Enter)
	```

- **Desconectarse:** Por medio de este comando un proveedor puede desconectarse del MOM.

	**Estructura**
	```sh
	DESCONECTAR ↵ (Enter)
	```

- **Salir:** Por medio de este comando un proveedor puede cerrar la aplicación _Proveedor_.

	**Estructura**
	```sh
	SALIR ↵ (Enter)
	```

### Comandos del consumidor
- **Registrarse:** por medio de este comando un consumidor puede registrarse en el MOM para posteriormente poder conectarse.

	**Estructura**
	```sh
	REGISTRAR_CONSUMIDOR [nombre usuario] [password] ↵ (Enter)
	```

- **Conectarse:** por medio de este comando un consumidor puede conectarse al MOM para realizar otras acciones como crear un canal.

	**Estructura**
	```sh
	CONECTAR_CONSUMIDOR [nombre usuario] [password] ↵ (Enter)
	```

- **Listar canales:** por medio de este comando un consumidor puede listar todos los canales que hayan disponibles en el MOM para conectarse. 

	**Estructura**
	```sh
	LISTAR_CANALES_CONSUMIDOR ↵ (Enter)
	```

- **Conectarse a un canal:** por medio de este comando un consumidor puede conectarse a un canal especifico para recibir mensajes de este.

	**Estructura**
	```sh
	CONECTAR_CONSUMIDOR_CANAL ↵ (Enter)
	[nombre del canal] ↵ (Enter)
	[id del canal] ↵ (Enter)
	```

- **Recibir mensajes de un canal:** por medio de este comando un consumidor puede recibir mensajes de un canal, siempre y cuando haya mensajes en el mismo.

	**Estructura**
	```sh
	RECIBIR_MENSAJE_CANAL ↵ (Enter)
	[nombre del canal] ↵ (Enter)
	[id del canal] ↵ (Enter)
	```

- **Desconectarse:** Por medio de este comando un consumidor puede desconectarse del MOM.

	**Estructura**
	```sh
	DESCONECTAR_CONSUMIDOR ↵ (Enter)
	```

- **Salir:** Por medio de este comando un consumidor puede cerrar la aplicación _Consumidor_.

	**Estructura**
	```sh
	SALIR ↵ (Enter)
	```


