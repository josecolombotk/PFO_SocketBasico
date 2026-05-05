# PFO_SocketBasico

Chat Cliente-Servidor con Sockets y SQLite

 Descripción
Este proyecto implementa un sistema de comunicación básico cliente-servidor en Python utilizando **sockets TCP/IP**.

El servidor recibe mensajes de clientes, los almacena en una base de datos SQLite y responde con una confirmación que incluye la fecha y hora de recepción.


 Objetivo
* Implementar comunicación cliente-servidor mediante sockets
* Almacenar mensajes en una base de datos SQLite
* Aplicar modularización del código
* Manejar errores comunes en redes y persistencia



 Tecnologías utilizadas

* Python 3
* Módulo `socket`
* Módulo `sqlite3`
* Módulo `datetime`



 Estructura del proyecto


 chat-sockets/
│
├── servidor.py     # Servidor TCP
├── cliente.py      # Cliente de consola
└── mensajes.db     # Base de datos (se genera automáticamente)
```

El sistema utiliza:

```
HOST = 127.0.0.1
PORT = 5000
```

Ambos (cliente y servidor) deben coincidir.

---

Ejecución

1. Ejecutar el servidor

```bash
python servidor.py
```

Salida esperada:

```
[SERVIDOR] Escuchando en 127.0.0.1:5000 ...
```

---

### 2. Ejecutar el cliente

En otra terminal:

```bash
python cliente.py
```

---

### 3. Enviar mensajes

Ejemplo:

```
Vos: Hola
Servidor: Mensaje recibido: 2026-05-04 21:45:10
```

---

### 4. Finalizar

Para salir del cliente:

```
éxito
```

---

 Base de datos

El sistema utiliza SQLite y crea automáticamente la base `mensajes.db` con la tabla:

```sql
CREATE TABLE mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    fecha_envio TEXT NOT NULL,
    ip_cliente TEXT NOT NULL
);
```

Cada mensaje incluye:

* Contenido
* Fecha y hora
* IP del cliente

---

Manejo de errores

El sistema contempla:

* Puerto ocupado
* Error de conexión del cliente
* Fallo en la base de datos
* Desconexión inesperada

Consideraciones

* El servidor maneja conexiones de forma secuencial
* Codificación UTF-8
* No se permiten mensajes vacíos

---

## 🚀 Posibles mejoras

* Soporte para múltiples clientes (threads)
* Interfaz gráfica
* Historial de mensajes
* Comandos personalizados

---

Autor

* Jose Luis Colombo

---
Trabajo práctico

Implementación de un chat cliente-servidor con sockets y base de datos SQLite.


