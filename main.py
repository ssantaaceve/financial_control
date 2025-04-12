#doc para hacer pruebas
from usuario import registrar_usuario
from pareja import crear_pareja

#En esta funcion se encuentra el menu principal
def menu_principal():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Registrar usuario")
        print("2. Crear pareja")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_registro_usuarios()  # Aquí llamas a la función que hiciste para registrar
        elif opcion == "2":
            pareja_creacion()  # Esta sería tu función ya creada
        elif opcion == "3":
            print("👋 Hasta luego")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")

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

def pareja_creacion():
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

if __name__ == "__main__": 
    menu_principal()

