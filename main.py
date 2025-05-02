#doc para hacer pruebas
from usuario import registrar_usuario, iniciar_sesion_db
from pareja import crear_pareja
from movimientos import registrar_movimiento_DB, obtener_resumen_financiero
from datetime import datetime

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
        print("2. Ver historial de movimientos")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_movimiento(usuario)
            # Limpiar la pantalla y volver al menú principal
            print("\n" * 2)  # Agregar espacio para separar
        elif opcion == "2":
            print("Historial de movimientos (pendiente de implementar)")
        elif opcion == "3":
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
#Función para registrar movimientos en el app
def registrar_movimiento(usuario):
    print("\n=== Registro de Movimiento ===")
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    print(f"\nFecha del movimiento: {fecha_actual}")
    
    # Validación de categoría
    while True:
        categoria = input("Categoría (Ej: Comida, Transporte, Salario, etc.): ").strip()
        if categoria and len(categoria) <= 50:  # Validar que no esté vacío y tenga longitud razonable
            break
        print("❌ La categoría no puede estar vacía y debe tener máximo 50 caracteres.")
    
    # Validación de monto
    while True:
        try:
            monto = float(input("Monto: "))
            if monto > 0:  # Validar que el monto sea positivo
                break
            print("❌ El monto debe ser un número positivo.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
    
    # Menú para seleccionar tipo de movimiento con validación
    while True:
        print("\nSelecciona el tipo de movimiento:")
        print("1. Ingreso")
        print("2. Gasto")
        
        try:
            opcion = int(input("Opción (1-2): "))
            if opcion in [1, 2]:
                tipo = "Ingreso" if opcion == 1 else "Gasto"
                break
            print("❌ Opción inválida. Debe ser 1 o 2.")
        except ValueError:
            print("❌ Debes ingresar un número (1 o 2).")
    
    # Validación de descripción
    while True:
        descripcion = input("Descripción del movimiento: ").strip()
        if descripcion and len(descripcion) <= 200:  # Validar que no esté vacío y tenga longitud razonable
            break
        print("❌ La descripción no puede estar vacía y debe tener máximo 200 caracteres.")

    # Confirmación del movimiento
    print("\n=== Resumen del Movimiento ===")
    print(f"Fecha: {fecha_actual}")
    print(f"Categoría: {categoria}")
    print(f"Monto: ${monto:,.2f}")
    print(f"Tipo: {tipo}")
    print(f"Descripción: {descripcion}")
    
    confirmar = input("\n¿Confirmar el registro de este movimiento? (si/no): ").strip().lower()
    
    if confirmar == 'si':
        # Registrar el movimiento
        registrar_movimiento_DB(usuario['id'], None, fecha_actual, categoria, monto, tipo, descripcion)

#Funcion principal  
if __name__ == "__main__": 
    usuario_logueado = pantalla_inicio()
    
    if usuario_logueado:
        menu_principal(usuario_logueado)


