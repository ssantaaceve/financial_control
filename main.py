#doc para hacer pruebas
from usuario import registrar_usuario, iniciar_sesion_db
from pareja import crear_pareja
from movimientos import registrar_movimiento_DB

#En esta funcion se encuentra la pantalla principal del progra,a
def pantalla_inicio():
    while True:
        print("\n=== Bienvenido a Finanzas en Pareja 💰❤️ ===")
        print("1. Registrarme")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_registro_usuarios()

        elif opcion == "2":
            usuario = iniciar_sesion()  # Llamamos la función de iniciar_sesion() que no necesita parámetros
            if usuario:
                print(f"🌟 ¡Bienvenido {usuario['nombre']}!")
                return usuario  # Lo usas para pasar al menú principal

        elif opcion == "3":
            print("👋 Hasta luego.")
            break

        else:
            print("❌ Opción inválida. Intenta de nuevo.")



#En esta funcion se encuentra el menu de navegacion cuando el usuario ingrese
def menu_principal():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Registrar movimiento")
        print("2. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_movimiento()  # Esta es una funcion creada para registrar un movimiento
        elif opcion == "2":
            print("👋 Hasta luego")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")



def iniciar_sesion():
    correo = input("Correo: ").strip()  # Solicitar correo al usuario
    contraseña = input("Contraseña: ").strip()  # Solicitar contraseña al usuario

    # Aquí llamas la función iniciar_sesion desde usuario.py
    usuario = iniciar_sesion_db(correo, contraseña)  # Pasas los datos del correo y contraseña a la función de usuario.py

    if usuario:
        return usuario  # Si la función retorna un usuario válido, lo regresamos
    else:
        print("❌ Error en inicio de sesión. Intenta de nuevo.")
        return None
def menu_registro_usuarios():  # Esta función muestra un menú para registrar usuarios
    while True:  # Ciclo que se repite hasta que el usuario decida salir
        print("\n=== Registro de Usuario ===")  # Título para identificar el menú

        nombre = input("Nombre: ").strip()  # Pedimos el nombre y eliminamos espacios extras
        correo = input("Correo: ").strip()  # Pedimos el correo y eliminamos espacios extras
        contraseña = input("Contraseña: ").strip()  # Pedimos la contraseña y eliminamos espacios extras

        # Validamos que ningún campo esté vacío
        if not nombre or not correo or not contraseña:
            print("❌ Todos los campos son obligatorios. Intenta de nuevo.")  # Mensaje de error si falta algo
            continue  # Vuelve al inicio del ciclo

        registrar_usuario(nombre, correo, contraseña)  # Llamamos a la función que guarda al usuario en la base de datos

        crear_otro = input("¿Te gustaría crear otro usuario? (sí/no): ").strip().lower()  
        # Preguntamos si quiere crear otro usuario, quitamos espacios y pasamos todo a minúsculas

        if crear_otro == 'no':  # Si escribe "no", salimos del menú
            print("👋 Saliste de la creación de usuarios.")  # Mensaje de despedida
            break  # Finalizamos el ciclo while

def pareja_creacion(): #Funcion para crear pareja

    # Pregunta inicial para saber si el usuario quiere crear una pareja
    validacion_1 = input("¿Te gustaría crear una pareja? (SI/NO): ").strip().lower()

    # Validamos que la respuesta sea afirmativa
    if validacion_1 == 'si':
        # Solicitamos los datos necesarios para crear la pareja
        nombre_pareja = input("Nombre de la pareja: ").strip()
        correo_1 = input("Correo del primer usuario: ").strip()
        correo_2 = input("Correo del segundo usuario: ").strip()

        # Aquí llamamos la función que conecta con la base de datos
        crear_pareja(nombre_pareja, correo_1, correo_2)

    else:
        print("❌ El usuario no quiso crear una pareja.")

def registrar_movimiento():
    print("=== Registro de Movimiento ===")

    pareja_id = input("ID de la pareja: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    categoria = input("Categoría (Ej: Comida, Transporte, etc.): ")
    monto = float(input("Monto: "))
    tipo = input("Tipo (ingreso/gasto): ")
    autor_id = input("ID del autor del movimiento: ")
    descripcion = input("Descripción del movimiento: ")

    registrar_movimiento_DB(pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion)


if __name__ == "__main__": 
    pantalla_inicio()

