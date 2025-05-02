#doc para hacer pruebas
from usuario import registrar_usuario, iniciar_sesion_db, actualizar_correo_usuario, actualizar_contraseña_usuario, actualizar_nombre_usuario, obtener_datos_usuario
from pareja import crear_pareja
from movimientos import (
    registrar_movimiento_DB, 
    obtener_resumen_financiero, 
    registrar_movimiento_recurrente_DB, 
    obtener_movimientos_recurrentes,
    verificar_movimientos_pendientes,
    aprobar_movimiento_recurrente,
    rechazar_movimiento_recurrente,
    obtener_historial_movimientos,
    obtener_categorias_usuario
)
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
            usuario = iniciar_sesion()
            if usuario:
                print(f"🌟 ¡Bienvenido {usuario['nombre']}!")
                return usuario
        elif opcion == "3":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

#En esta funcion se encuentra el menu de navegacion cuando el usuario ingrese
def menu_principal(usuario):
    while True:
        # Verificar movimientos pendientes
        pendientes = verificar_movimientos_pendientes(usuario['id'])
        if pendientes['hay_pendientes']:
            print("\n⚠️ Tienes movimientos recurrentes pendientes de aprobación!")
            print(f"Total pendientes: {pendientes['total']}")
            print("\nMovimientos pendientes:")
            for mov in pendientes['movimientos']:
                print(f"  - {mov}")
            print("\nRevisa la opción 'Ver movimientos recurrentes' para gestionarlos.")
        
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
        print("2. Registrar movimiento recurrente")
        print("3. Ver movimientos recurrentes")
        print("4. Ver historial de movimientos")
        print("5. Configuración de perfil")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_movimiento(usuario)
        elif opcion == "2":
            registrar_movimiento_recurrente(usuario)
        elif opcion == "3":
            ver_movimientos_recurrentes(usuario)
        elif opcion == "4":
            ver_historial_movimientos(usuario)
        elif opcion == "5":
            menu_configuracion(usuario)
        elif opcion == "6":
            print("👋 Hasta luego")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")

#funcion para iniciar sesion de usuario
def iniciar_sesion():
    while True:
        print("\n=== Inicio de Sesión ===")
        correo = input("Correo: ").strip()
        contraseña = input("Contraseña: ").strip()

        usuario = iniciar_sesion_db(correo, contraseña)

        if usuario:
            return usuario
        
        opcion = input("\n¿Deseas intentar de nuevo? (sí/no): ").strip().lower()
        if opcion != 'si':
            print("👋 Volviendo al menú principal.")
            return None

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
            return

        crear_otro = input("¿Te gustaría crear otro usuario? (sí/no): ").strip().lower()  
        # Preguntamos si quiere crear otro usuario, quitamos espacios y pasamos todo a minúsculas

        if crear_otro == 'no':  # Si escribe "no", salimos del menú
            print("👋 Saliste de la creación de usuarios.")  # Mensaje de despedida
            return

#Función para registrar movimientos en el app
def registrar_movimiento(usuario):
    print("\n=== Registro de Movimiento ===")
    
    # Obtener la fecha actual``
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
        if registrar_movimiento_DB(usuario['id'], None, fecha_actual, categoria, monto, tipo, descripcion):
            print("✅ Movimiento registrado exitosamente.")
        else:
            print("❌ Error al registrar el movimiento.")
    else:
        print("❌ Registro cancelado.")

def registrar_movimiento_recurrente(usuario):
    print("\n=== Registro de Movimiento Recurrente ===")
    
    # Validación de categoría
    while True:
        categoria = input("Categoría (Ej: Comida, Transporte, Salario, etc.): ").strip()
        if categoria and len(categoria) <= 50:
            break
        print("❌ La categoría no puede estar vacía y debe tener máximo 50 caracteres.")
    
    # Validación de monto
    while True:
        try:
            monto = float(input("Monto: "))
            if monto > 0:
                break
            print("❌ El monto debe ser un número positivo.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
    
    # Menú para seleccionar tipo de movimiento
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
        if descripcion and len(descripcion) <= 200:
            break
        print("❌ La descripción no puede estar vacía y debe tener máximo 200 caracteres.")

    # Validación de frecuencia
    while True:
        print("\nSelecciona la frecuencia:")
        print("1. Diario")
        print("2. Semanal")
        print("3. Mensual")
        
        try:
            opcion = int(input("Opción (1-3): "))
            if opcion in [1, 2, 3]:
                frecuencias = {1: "diario", 2: "semanal", 3: "mensual"}
                frecuencia = frecuencias[opcion]
                break
            print("❌ Opción inválida. Debe ser 1, 2 o 3.")
        except ValueError:
            print("❌ Debes ingresar un número (1, 2 o 3).")

    # Validación de fecha de registro
    while True:
        try:
            fecha_registro = input("Fecha de registro (YYYY-MM-DD): ").strip()
            fecha_registro_dt = datetime.strptime(fecha_registro, '%Y-%m-%d')
            fecha_actual = datetime.now()
            
            if fecha_registro_dt < fecha_actual:
                print("❌ La fecha de registro no puede ser en el pasado.")
                continue
                
            break
        except ValueError:
            print("❌ Formato de fecha inválido. Usa YYYY-MM-DD")

    # Validación de fecha fin
    while True:
        try:
            fecha_fin = input("Fecha de finalización (YYYY-MM-DD): ").strip()
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            
            if fecha_fin_dt <= fecha_registro_dt:
                print("❌ La fecha de finalización debe ser posterior a la fecha de registro.")
                continue
                
            break
        except ValueError:
            print("❌ Formato de fecha inválido. Usa YYYY-MM-DD")

    # Confirmación del movimiento
    print("\n=== Resumen del Movimiento Recurrente ===")
    print(f"Categoría: {categoria}")
    print(f"Monto: ${monto:,.2f}")
    print(f"Tipo: {tipo}")
    print(f"Descripción: {descripcion}")
    print(f"Frecuencia: {frecuencia}")
    print(f"Fecha de registro: {fecha_registro}")
    print(f"Fecha de finalización: {fecha_fin}")
    
    while True:
        confirmar = input("\n¿Confirmar el registro de este movimiento recurrente? (si/no): ").strip().lower()
        if confirmar in ['si', 'no']:
            break
        print("❌ Por favor, responde con 'si' o 'no'.")
    
    if confirmar == 'si':
        if registrar_movimiento_recurrente_DB(usuario['id'], categoria, monto, tipo, descripcion, frecuencia, fecha_registro, fecha_fin):
            print("✅ Movimiento recurrente registrado con éxito.")
        else:
            print("❌ No se pudo registrar el movimiento recurrente.")
    else:
        print("❌ Registro cancelado.")

def ver_movimientos_recurrentes(usuario):
    print("\n=== Movimientos Recurrentes Pendientes ===")
    movimientos = obtener_movimientos_recurrentes(usuario['id'])
    
    if movimientos:
        for mov in movimientos:
            print(f"\nID: {mov[0]}")
            print(f"Categoría: {mov[1]}")
            print(f"Monto: ${mov[2]:,.2f}")
            print(f"Tipo: {mov[3]}")
            print(f"Descripción: {mov[4]}")
            print(f"Frecuencia: {mov[5]}")
            print(f"Fecha programada: {mov[6]}")
            print(f"Fecha de finalización: {mov[7]}")
            print(f"Estado: {mov[8]}")
            print("-" * 40)
            
            # Si el movimiento está pendiente, ofrecer opciones
            if mov[8] == 'pendiente':
                while True:
                    print("\n¿Qué deseas hacer con este movimiento?")
                    print("1. Aprobar y registrar (se registrará con la fecha actual)")
                    print("2. Rechazar")
                    print("3. Posponer")
                    
                    try:
                        opcion = int(input("Opción (1-3): "))
                        if opcion == 1:
                            if aprobar_movimiento_recurrente(mov[0]):
                                break
                        elif opcion == 2:
                            if rechazar_movimiento_recurrente(mov[0]):
                                break
                        elif opcion == 3:
                            print("Movimiento pospuesto para revisión posterior.")
                            break
                        else:
                            print("❌ Opción inválida. Debe ser 1, 2 o 3.")
                    except ValueError:
                        print("❌ Por favor, ingresa un número válido (1, 2 o 3).")
    else:
        print("No hay movimientos recurrentes pendientes.")

def ver_historial_movimientos(usuario):
    print("\n=== Historial de Movimientos ===")
    
    # Obtener categorías disponibles
    categorias = obtener_categorias_usuario(usuario['id'])
    
    # Inicializar filtros
    filtros = {}
    
    # Menú de filtros
    while True:
        print("\nOpciones de filtro:")
        print("1. Filtrar por tipo de movimiento")
        print("2. Filtrar por rango de montos")
        print("3. Filtrar por rango de fechas")
        print("4. Filtrar por categoría")
        print("5. Aplicar filtros y ver resultados")
        print("6. Limpiar filtros")
        print("7. Volver al menú principal")
        
        try:
            opcion = int(input("\nSelecciona una opción (1-7): "))
            
            if opcion == 1:
                print("\nSelecciona el tipo de movimiento:")
                print("1. Ingresos")
                print("2. Gastos")
                print("3. Ambos")
                tipo_opcion = int(input("Opción (1-3): "))
                if tipo_opcion == 1:
                    filtros['tipo'] = 'Ingreso'
                elif tipo_opcion == 2:
                    filtros['tipo'] = 'Gasto'
                elif tipo_opcion == 3:
                    filtros.pop('tipo', None)
            
            elif opcion == 2:
                print("\nFiltrar por rango de montos:")
                try:
                    monto_min = float(input("Monto mínimo (dejar vacío para no filtrar): ") or 0)
                    monto_max = float(input("Monto máximo (dejar vacío para no filtrar): ") or float('inf'))
                    filtros['monto_min'] = monto_min
                    filtros['monto_max'] = monto_max
                except ValueError:
                    print("❌ Por favor, ingresa montos válidos.")
            
            elif opcion == 3:
                print("\nFiltrar por rango de fechas (YYYY-MM-DD):")
                fecha_inicio = input("Fecha inicial (dejar vacío para no filtrar): ").strip()
                fecha_fin = input("Fecha final (dejar vacío para no filtrar): ").strip()
                
                if fecha_inicio:
                    try:
                        datetime.strptime(fecha_inicio, '%Y-%m-%d')
                        filtros['fecha_inicio'] = fecha_inicio
                    except ValueError:
                        print("❌ Formato de fecha inicial inválido.")
                
                if fecha_fin:
                    try:
                        datetime.strptime(fecha_fin, '%Y-%m-%d')
                        filtros['fecha_fin'] = fecha_fin
                    except ValueError:
                        print("❌ Formato de fecha final inválido.")
            
            elif opcion == 4:
                if categorias:
                    print("\nCategorías disponibles:")
                    for i, cat in enumerate(categorias, 1):
                        print(f"{i}. {cat}")
                    try:
                        cat_opcion = int(input("\nSelecciona una categoría (0 para no filtrar): "))
                        if 0 < cat_opcion <= len(categorias):
                            filtros['categoria'] = categorias[cat_opcion - 1]
                        elif cat_opcion == 0:
                            filtros.pop('categoria', None)
                    except ValueError:
                        print("❌ Por favor, ingresa un número válido.")
                else:
                    print("No hay categorías disponibles.")
            
            elif opcion == 5:
                # Mostrar movimientos con filtros actuales
                movimientos = obtener_historial_movimientos(usuario['id'], filtros)
                if movimientos:
                    print("\n=== Resultados ===")
                    print(f"Total de movimientos: {len(movimientos)}")
                    print("\nDetalles:")
                    for mov in movimientos:
                        print(f"\nID: {mov[0]}")
                        print(f"Fecha: {mov[1]}")
                        print(f"Categoría: {mov[2]}")
                        print(f"Monto: ${mov[3]:,.2f}")
                        print(f"Tipo: {mov[4]}")
                        print(f"Descripción: {mov[5]}")
                        print("-" * 40)
                else:
                    print("\nNo se encontraron movimientos con los filtros actuales.")
            
            elif opcion == 6:
                filtros = {}
                print("\n✅ Filtros limpiados.")
            
            elif opcion == 7:
                return
            
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
        
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")

def menu_configuracion(usuario):
    """
    Menú de configuración del perfil del usuario.
    """
    while True:
        print("\n=== ⚙️ Configuración de Perfil ===")
        print("1. Ver información del perfil")
        print("2. Actualizar nombre")
        print("3. Actualizar correo electrónico")
        print("4. Cambiar contraseña")
        print("5. Volver al menú principal")
        
        opcion = input("\nSelecciona una opción (1-5): ")
        
        if opcion == "1":
            datos = obtener_datos_usuario(usuario['id'])
            if datos:
                print("\n=== Información del Perfil ===")
                print(f"Nombre: {datos['nombre']}")
                print(f"Correo electrónico: {datos['correo']}")
            else:
                print("❌ No se pudieron obtener los datos del perfil.")
        
        elif opcion == "2":
            nuevo_nombre = input("\nNuevo nombre: ").strip()
            if nuevo_nombre:
                if actualizar_nombre_usuario(usuario['id'], nuevo_nombre):
                    print("✅ Nombre actualizado correctamente.")
                    usuario['nombre'] = nuevo_nombre  # Actualizar en memoria
                else:
                    print("❌ No se pudo actualizar el nombre.")
            else:
                print("❌ El nombre no puede estar vacío.")
        
        elif opcion == "3":
            nuevo_correo = input("\nNuevo correo electrónico: ").strip()
            if nuevo_correo and '@' in nuevo_correo:
                if actualizar_correo_usuario(usuario['id'], nuevo_correo):
                    print("✅ Correo electrónico actualizado correctamente.")
                else:
                    print("❌ No se pudo actualizar el correo electrónico.")
            else:
                print("❌ Por favor, ingresa un correo electrónico válido.")
        
        elif opcion == "4":
            contraseña_actual = input("\nContraseña actual: ").strip()
            nueva_contraseña = input("Nueva contraseña: ").strip()
            confirmar_contraseña = input("Confirmar nueva contraseña: ").strip()
            
            if nueva_contraseña and nueva_contraseña == confirmar_contraseña:
                if actualizar_contraseña_usuario(usuario['id'], contraseña_actual, nueva_contraseña):
                    print("✅ Contraseña actualizada correctamente.")
                else:
                    print("❌ No se pudo actualizar la contraseña.")
            else:
                print("❌ Las contraseñas no coinciden o están vacías.")
        
        elif opcion == "5":
            return
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

#Funcion principal  
if __name__ == "__main__": 
    usuario_logueado = pantalla_inicio()
    
    if usuario_logueado:
        menu_principal(usuario_logueado)


