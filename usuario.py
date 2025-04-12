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

