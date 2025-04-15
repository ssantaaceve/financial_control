import sqlite3
import os

DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_usuario(nombre, correo, contraseña): # Creamos la funcion para registrar un usuario
    try: #Forma de decir "intenta hacer algo"
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña)
            VALUES (?, ?, ?);
        """, (nombre, correo, contraseña))

        conexion.commit()
        conexion.close()
        print("✅ Usuario registrado con éxito.")
    except Exception as e:
        print("❌ Error al registrar el usuario:", e)

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