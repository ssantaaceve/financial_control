import sqlite3
import os

DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_usuario(nombre, correo, contraseña): # Creamos la funcion para registrar un usuario
    try: #Forma de decir "intenta hacer algo"
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT correo FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone() #busqueda si ya exite el correo

        if resultado:
            print("✅ Correo ya registrado.")
            conexion.close()
            return False  # Ya existe, no se registró
        else:         
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, fecha_creacion)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP);
            """, (nombre, correo, contraseña))

        conexion.commit()
        conexion.close()
        print("✅ Usuario registrado con éxito.")
        return True  # Registro exitoso
    except Exception as e:
        print("❌ Error al registrar el usuario:", e)
        return False  # Hubo un error, no se registró

def iniciar_sesion_db(correo, contraseña):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    # Comprobamos si el correo y la contraseña coinciden
    cursor.execute("SELECT id, nombre FROM usuarios WHERE correo = ? AND contraseña = ?", (correo, contraseña))
    resultado = cursor.fetchone()

    conexion.close()

    # Si existe el usuario, retornamos su id y nombre
    if resultado:
        return {"id": resultado[0], "nombre": resultado[1]}
    else:
        print("❌ Correo o contraseña incorrectos.")
        return None