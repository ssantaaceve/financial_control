import sqlite3
import os

DB_PATH = os.path.join('data', "finanzas_parejas.db")

def crear_pareja (nombre_pareja, correo_1, correo_2):
    try:
        conexion = sqlite3.connect(DB_PATH) #Nos conectamos a la base de datos
        cursor = conexion.cursor() #linea que crea el cursor que es como la forma en la cual podemos empezar a escribir y leer en la base de datos

        cursor.execute("SELECT id FROM usuarios where correo = ?", (correo_1)) #con
        usuario1 = cursor.fetchone()

        cursor.execute("SELECT id FROM usuarios where correo = ?", (correo_2))
        usuario2 = cursor.fetchone ()

        if not usuario1 or not usuario2:
            print('❌ Uno o ambos correos no están registrados.')
            return
        id1 = usuario1[0]
        id2 = usuario2[0]

        # Insertamos la nueva pareja
        cursor.execute("""
            INSERT INTO parejas (nombre, usuario_1_id, usuario_2_id)
            VALUES (?, ?, ?);
        """, (nombre_pareja, id1, id2))

        conexion.commit()
        conexion.close()
        print("✅ Pareja registrada con éxito.")
        
    except Exception as e:
        print("❌ Error al crear la pareja:", e)
        