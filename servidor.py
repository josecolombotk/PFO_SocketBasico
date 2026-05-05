import socket
import sqlite3
import datetime

# CONFIGURACIÓN GENERAL
# El servidor escucha en localhost puerto 5000.

HOST = "127.0.0.1"
PORT = 5000
DB_NAME = "mensajes.db"


# FUNCIÓN: inicializar_db
# Crea la base de datos SQLite y la tabla 'mensajes' si no existe.
def inicializar_db():
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido   TEXT    NOT NULL,
                fecha_envio TEXT    NOT NULL,
                ip_cliente  TEXT    NOT NULL
            )
        """)
        conexion.commit()
        print(f"[DB] Base de datos '{DB_NAME}' lista.")
        return conexion
    except sqlite3.Error as e:
        raise RuntimeError(f"[ERROR] No se pudo inicializar la base de datos: {e}")


# FUNCIÓN: guardar_mensaje
# Guarda el mensaje con timestamp e IP del cliente.
def guardar_mensaje(conexion_db, contenido, ip_cliente):
    try:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conexion_db.cursor()
        cursor.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, fecha, ip_cliente)
        )
        conexion_db.commit()
        print(f"[DB] Guardado → ip: {ip_cliente} | fecha: {fecha} | msg: '{contenido}'")
        return fecha  # Devolvemos el timestamp para usarlo en la respuesta
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo guardar el mensaje: {e}")
        return None


# FUNCIÓN: inicializar_socket
# Configura el socket TCP/IP del servidor.
def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar el puerto
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST, PORT))
        servidor.listen(5)
        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT} ...")
        return servidor
    except OSError as e:
        raise RuntimeError(f"[ERROR] No se pudo iniciar el socket en {PORT}: {e}")


# FUNCIÓN: aceptar_conexiones
# Maneja conexiones de clientes de forma secuencial.
def aceptar_conexiones(servidor, conexion_db):
    while True:
        try:
            cliente_socket, direccion_cliente = servidor.accept()
            ip_cliente = direccion_cliente[0]
            print(f"\n[SERVIDOR] Cliente conectado desde {ip_cliente}:{direccion_cliente[1]}")

            with cliente_socket:
                while True:
                    try:
                        datos = cliente_socket.recv(1024)

                        if not datos:
                            print(f"[SERVIDOR] Cliente {ip_cliente} desconectado.")
                            break

                        mensaje = datos.decode("utf-8").strip()
                        print(f"[SERVIDOR] Mensaje recibido de {ip_cliente}: '{mensaje}'")

                        # Si el cliente envía "éxito" o "exito", se corta la conexión
                        if mensaje.lower() in ["exito", "éxito"]:
                            print(f"[SERVIDOR] Cliente {ip_cliente} finalizó la conexión.")
                            break

                        # Guardar mensaje y obtener timestamp
                        fecha = guardar_mensaje(conexion_db, mensaje, ip_cliente)

                        # RESPUESTA CORRECTA SEGÚN CONSIGNA
                        if fecha:
                            respuesta = f"Mensaje recibido: {fecha}"
                        else:
                            respuesta = "Error al guardar el mensaje"

                        cliente_socket.sendall(respuesta.encode("utf-8"))

                    except ConnectionResetError:
                        print(f"[SERVIDOR] Conexión con {ip_cliente} interrumpida.")
                        break

        except KeyboardInterrupt:
            print("\n[SERVIDOR] Cerrando servidor...")
            break


# PUNTO DE ENTRADA
if __name__ == "__main__":
    try:
        conexion_db = inicializar_db()
        servidor = inicializar_socket()
        aceptar_conexiones(servidor, conexion_db)
    except RuntimeError as e:
        print(e)
    finally:
        try:
            servidor.close()
            print("[SERVIDOR] Socket cerrado.")
        except Exception:
            pass
        try:
            conexion_db.close()
            print("[DB] Conexión cerrada.")
        except Exception:
            pass