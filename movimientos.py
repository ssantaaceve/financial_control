import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_movimiento_DB(pareja_id, fecha, categoria, monto, tipo, autor_id, descripcion):
    try:
        # Conectarse a la base de datos
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        # ✅ Validar si existe la pareja
        cursor.execute("SELECT id FROM parejas WHERE id = ?", (pareja_id,))
        pareja_existente = cursor.fetchone()
        if not pareja_existente:
            print("❌ Error: La pareja con ese ID no existe.")
            conexion.close()
            return

        # ✅ Validar si existe el autor
        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (autor_id,))
        autor_existente = cursor.fetchone()
        if not autor_existente:
            print("❌ Error: El autor con ese ID no existe.")
            conexion.close()
            return

        # ✅ Validar que tipo sea ingreso o gasto
        if tipo.lower() not in ['ingreso', 'gasto']:
            print("❌ Tipo inválido. Debe ser 'ingreso' o 'gasto'.")
            conexion.close()
            return

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
