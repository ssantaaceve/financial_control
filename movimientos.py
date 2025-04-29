import sqlite3
import os
from datetime import datetime

# Ruta a la base de datos
DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_movimiento_DB(autor_id, pareja_id, fecha, categoria, monto, tipo, descripcion):
    try:
        # Conectarse a la base de datos
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Validar que tipo sea ingreso o gasto
        if tipo.lower() not in ['ingreso', 'gasto']:
            print("❌ Tipo inválido. Debe ser 'ingreso' o 'gasto'.")
            conexion.close()
            return

        # Si es movimiento de pareja, validar que exista la pareja
        if pareja_id:
            cursor.execute("SELECT id FROM parejas WHERE id = ?", (pareja_id,))
            pareja_existente = cursor.fetchone()
            if not pareja_existente:
                print("❌ Error: La pareja con ese ID no existe.")
                conexion.close()
                return

        # Insertar el movimiento
        cursor.execute("""
            INSERT INTO movimientos (autor_id, pareja_id, fecha, categoria, monto, tipo, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (autor_id, pareja_id, fecha, categoria, monto, tipo, descripcion))

        # Confirmar y cerrar conexión
        conexion.commit()
        conexion.close()

        print("✅ Movimiento registrado con éxito.")
    
    except Exception as e:
        print("❌ Error al registrar el movimiento:", e)

def obtener_resumen_financiero(autor_id):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Obtener la fecha actual y el primer día del mes
        fecha_actual = datetime.now()
        primer_dia_mes = fecha_actual.replace(day=1)

        # Consulta para obtener ingresos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'ingreso' 
            AND fecha >= ? 
            AND fecha <= ?
        """, (autor_id, primer_dia_mes, fecha_actual))
        total_ingresos = cursor.fetchone()[0]

        # Consulta para obtener gastos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'gasto' 
            AND fecha >= ? 
            AND fecha <= ?
        """, (autor_id, primer_dia_mes, fecha_actual))
        total_gastos = cursor.fetchone()[0]

        # Calcular balance
        balance = total_ingresos - total_gastos

        conexion.close()
        return {
            "ingresos": total_ingresos,
            "gastos": total_gastos,
            "balance": balance
        }
    except Exception as e:
        print("❌ Error al obtener el resumen financiero:", e)
        return None
