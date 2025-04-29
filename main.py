#doc para hacer pruebas
from usuario import registrar_usuario, iniciar_sesion_db
from pareja import crear_pareja
from movimientos import registrar_movimiento_DB, obtener_resumen_financiero

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
def menu_principal(usuario):
    while True:
        # Obtener resumen financiero
        resumen = obtener_resumen_financiero(usuario['id'])
        
        if resumen:
            print("\n=== 📊 Resumen Financiero del Mes ===")
            print(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
            print(f"💸 Gastos: ${resumen['gastos']:,.2f}")
            print(f"💵 Balance: ${resumen['balance']:,.2f}")
            print("=" * 40)

        print(f'\n=== Bienvenido {usuario["nombre"]} Menú Principal ===')
        print("1. Registrar movimiento")
        print("2. Crear pareja")
        print("3. Ver historial de movimientos")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_movimiento(usuario)  # Esta es una funcion creada para registrar un movimiento
        elif opcion == "2":
            pareja_creacion()  # Función para crear pareja
        elif opcion == "3":
            print("Historial de movimientos (pendiente de implementar)")
        elif opcion == "4":
            print("👋 Hasta luego")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")
#funcion para iniciar sesion de usuario
def iniciar_sesion():
    while True:  # Ciclo que se repite hasta que el usuario decida no intentar más
        print("\n=== Inicio de Sesión ===")
        correo = input("Correo: ").strip()  # Solicitar correo al usuario
        contraseña = input("Contraseña: ").strip()  # Solicitar contraseña al usuario

        # Aquí llamas la función iniciar_sesion desde usuario.py
        usuario = iniciar_sesion_db(correo, contraseña)  # Pasas los datos del correo y contraseña a la función de usuario.py

        if usuario:
            return usuario  # Si la función retorna un usuario válido, lo regresamos
        
        # Si el inicio de sesión falla, preguntamos si quiere intentar de nuevo
        opcion = input("\n¿Deseas intentar de nuevo? (sí/no): ").strip().lower()
        if opcion == 'si':
            continue
        else:
            print("👋 Volviendo al menú principal.")
            pantalla_inicio()  # Volvemos al menú principal
            return None  # Retornamos None para indicar que no hay usuario logueado
#Funcion para realizar registro de usuarios
def menu_registro_usuarios():  
    while True:  # Ciclo que se repite hasta que el usuario decida salir
        print("\n=== Registro de Usuario ===")  # Título para identificar el menú

        nombre = input("Nombre: ").strip()  # Pedimos el nombre y eliminamos espacios extras
        correo = input("Correo: ").strip()  # Pedimos el correo y eliminamos espacios extras
        
        # Validación del formato del correo
        if '@' not in correo:
            print("❌ El correo debe contener el carácter '@'. Por favor, ingresa un correo válido.")
            continue  # Vuelve al inicio del ciclo para pedir el correo nuevamente
            
        # Validación de la contraseña
        contraseña = input("Contraseña: ").strip()  # Pedimos la contraseña y eliminamos espacios extras
        confirmar_contraseña = input("Confirma tu contraseña: ").strip()  # Pedimos confirmación de la contraseña
        
        if contraseña != confirmar_contraseña:
            print("❌ Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            continue  # Vuelve al inicio del ciclo

        # Validamos que ningún campo esté vacío
        if not nombre or not correo or not contraseña:
            print("❌ Todos los campos son obligatorios. Intenta de nuevo.")  # Mensaje de error si falta algo
            continue  # Vuelve al inicio del ciclo

        # Registramos el usuario en la base de datos
        if registrar_usuario(nombre, correo, contraseña):  # Si el registro fue exitoso
            print("✅ Usuario registrado con éxito.")
            pantalla_inicio()  # Volvemos al menú principal
            break  # Salimos del ciclo de registro de usuarios

        crear_otro = input("¿Te gustaría crear otro usuario? (sí/no): ").strip().lower()  
        # Preguntamos si quiere crear otro usuario, quitamos espacios y pasamos todo a minúsculas

        if crear_otro == 'no':  # Si escribe "no", salimos del menú
            print("👋 Saliste de la creación de usuarios.")  # Mensaje de despedida
            pantalla_inicio()  # Volvemos al menú principal
            break  # Finalizamos el ciclo while
#Función para realizar registro de pareja
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
#Función para registrar movimientos en el app
def registrar_movimiento(usuario):
    print("\n=== Registro de Movimiento ===")
    
    # Preguntar si es movimiento de pareja
    es_pareja = input("¿Es un movimiento de pareja? (sí/no): ").strip().lower()
    
    # Si es movimiento de pareja, pedir el ID de la pareja
    pareja_id = None
    if es_pareja == 'sí':
        pareja_id = input("ID de la pareja: ").strip()
        if not pareja_id:
            print("❌ Debes ingresar un ID de pareja válido.")
            return
    
    # Solicitar información del movimiento
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    categoria = input("Categoría (Ej: Comida, Transporte, etc.): ").strip()
    monto = float(input("Monto: "))
    tipo = input("Tipo (ingreso/gasto): ").strip().lower()
    descripcion = input("Descripción del movimiento: ").strip()

    # Validar que tipo sea ingreso o gasto
    if tipo not in ['ingreso', 'gasto']:
        print("❌ Tipo inválido. Debe ser 'ingreso' o 'gasto'.")
        return

    # Registrar el movimiento
    registrar_movimiento_DB(usuario['id'], pareja_id, fecha, categoria, monto, tipo, descripcion)

#Funcion principal  
if __name__ == "__main__": 
    usuario_logueado = pantalla_inicio()
    
    if usuario_logueado:
        menu_principal(usuario_logueado)


