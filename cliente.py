import socket


HOST = "127.0.0.1"
PORT = 5000


# FUNCIÓN: conectar_servidor
# Crea el socket del cliente y establece la conexión.
def conectar_servidor():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        print(f"[CLIENTE] Conectado al servidor {HOST}:{PORT}")
        print("[CLIENTE] Escribí tus mensajes. Escribí 'éxito' para salir.\n")
        return cliente
    except ConnectionRefusedError:
        raise RuntimeError(
            f"[ERROR] No se pudo conectar a {HOST}:{PORT}. "
            "Asegurate de que el servidor esté corriendo."
        )



# FUNCIÓN: enviar_mensajes
# Permite enviar múltiples mensajes y recibir respuestas.
def enviar_mensajes(cliente):
    with cliente:
        while True:
            try:
                mensaje = input("Vos: ").strip()

                # Condición de salida: acepta "éxito" o "exito"
                if mensaje.lower() in ["exito", "éxito"]:
                    print("[CLIENTE] Saliendo... ¡Hasta luego!")
                    break

                if not mensaje:
                    print("[CLIENTE] No se puede enviar un mensaje vacío.")
                    continue

                cliente.sendall(mensaje.encode("utf-8"))

                respuesta = cliente.recv(1024).decode("utf-8")
                print(f"Servidor: {respuesta}\n")

            except KeyboardInterrupt:
                print("\n[CLIENTE] Conexión interrumpida por el usuario.")
                break
            except ConnectionResetError:
                print("[ERROR] El servidor cerró la conexión inesperadamente.")
                break


# PUNTO DE ENTRADA
if __name__ == "__main__":
    try:
        cliente = conectar_servidor()
        enviar_mensajes(cliente)
    except RuntimeError as e:
        print(e)