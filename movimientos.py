import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_movimiento_DB(pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion):
    try:
        # Conectarse a la base de datos
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Insertar el movimiento
        cursor.execute("""
            INSERT INTO movimientos (pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion))

        # Confirmar y cerrar conexión
        conexion.commit()
        conexion.close()

        print("✅ Movimiento registrado con éxito.")
    
    except Exception as e:
        print("❌ Error al registrar el movimiento:", e)
