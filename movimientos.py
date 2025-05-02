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

        # Validar que tipo sea Ingreso o Gasto
        if tipo not in ['Ingreso', 'Gasto']:
            print("❌ Tipo inválido. Debe ser 'Ingreso' o 'Gasto'.")
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
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        primer_dia_mes = datetime.now().replace(day=1).strftime('%Y-%m-%d')

        # Consulta para obtener ingresos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'Ingreso' 
            AND fecha >= ? 
            AND fecha <= ?
        """, (autor_id, primer_dia_mes, fecha_actual))
        total_ingresos = cursor.fetchone()[0]

        # Consulta para obtener gastos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'Gasto' 
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

def registrar_movimiento_recurrente_DB(autor_id, categoria, monto, tipo, descripcion, frecuencia, fecha_registro, fecha_fin):
    """
    Registra un movimiento recurrente en la base de datos.
    
    Args:
        autor_id: ID del usuario que crea el movimiento
        categoria: Categoría del movimiento
        monto: Monto del movimiento
        tipo: Tipo de movimiento (Ingreso/Gasto)
        descripcion: Descripción del movimiento
        frecuencia: Frecuencia del movimiento (diario/semanal/mensual)
        fecha_registro: Fecha específica para registrar el movimiento
        fecha_fin: Fecha en que termina la recurrencia
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Validar que tipo sea Ingreso o Gasto
        if tipo not in ['Ingreso', 'Gasto']:
            print("❌ Tipo inválido. Debe ser 'Ingreso' o 'Gasto'.")
            conexion.close()
            return False

        # Validar frecuencia
        if frecuencia not in ['diario', 'semanal', 'mensual', 'anual']:
            print("❌ Frecuencia inválida. Debe ser 'diario', 'semanal', 'mensual' o 'anual'.")
            conexion.close()
            return False

        # Insertar el movimiento recurrente
        cursor.execute("""
            INSERT INTO movimientos (
                autor_id, fecha, categoria, monto, tipo, descripcion,
                es_recurrente, frecuencia, fecha_registro, fecha_fin, estado
            )
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, 'pendiente');
        """, (autor_id, datetime.now().strftime('%Y-%m-%d'),
              categoria, monto, tipo, descripcion,
              frecuencia, fecha_registro, fecha_fin))

        conexion.commit()
        conexion.close()
        print("✅ Movimiento recurrente registrado con éxito.")
        return True
    
    except Exception as e:
        print("❌ Error al registrar el movimiento recurrente:", e)
        return False

def obtener_movimientos_recurrentes(autor_id):
    """
    Obtiene todos los movimientos recurrentes pendientes de un usuario.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, categoria, monto, tipo, descripcion, frecuencia, fecha_registro, fecha_fin, estado
            FROM movimientos
            WHERE autor_id = ?
            AND es_recurrente = 1
            AND estado = 'pendiente'
            AND fecha_fin >= CURRENT_DATE
            ORDER BY fecha_registro ASC
        """, (autor_id,))
        
        movimientos = cursor.fetchall()
        conexion.close()
        
        return movimientos
    except Exception as e:
        print("❌ Error al obtener movimientos recurrentes:", e)
        return None

def obtener_movimientos_recurrentes_pendientes(autor_id):
    """
    Obtiene los movimientos recurrentes que están pendientes de aprobación.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, categoria, monto, tipo, descripcion, frecuencia, fecha_registro, fecha_fin
            FROM movimientos
            WHERE autor_id = ?
            AND es_recurrente = 1
            AND estado = 'pendiente'
            AND fecha_registro <= CURRENT_DATE
            AND fecha_fin >= CURRENT_DATE
            ORDER BY fecha_registro ASC
        """, (autor_id,))
        
        movimientos = cursor.fetchall()
        conexion.close()
        
        return movimientos
    except Exception as e:
        print("❌ Error al obtener movimientos recurrentes pendientes:", e)
        return None

def aprobar_movimiento_recurrente(movimiento_id):
    """
    Aprueba y registra un movimiento recurrente.
    Permite registrar el movimiento en la fecha actual, independientemente de la fecha programada.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Obtener los datos completos del movimiento recurrente
        cursor.execute("""
            SELECT autor_id, categoria, monto, tipo, descripcion, fecha_registro, frecuencia
            FROM movimientos
            WHERE id = ?
            AND es_recurrente = 1
            AND estado = 'pendiente'
        """, (movimiento_id,))
        
        movimiento = cursor.fetchone()
        if not movimiento:
            print("❌ Movimiento no encontrado o ya procesado.")
            return False

        autor_id, categoria, monto, tipo, descripcion, fecha_registro, frecuencia = movimiento

        # Registrar el movimiento con la fecha actual
        cursor.execute("""
            INSERT INTO movimientos (
                autor_id, fecha, categoria, monto, tipo, descripcion
            )
            VALUES (?, CURRENT_DATE, ?, ?, ?, ?);
        """, (autor_id, categoria, monto, tipo, descripcion))

        # Actualizar el estado del movimiento recurrente
        cursor.execute("""
            UPDATE movimientos
            SET estado = 'aprobado'
            WHERE id = ?
        """, (movimiento_id,))

        conexion.commit()
        conexion.close()
        print(f"✅ Movimiento de {tipo} por ${monto:,.2f} aprobado y registrado correctamente.")
        return True
    
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos al aprobar el movimiento: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al aprobar el movimiento: {e}")
        return False

def rechazar_movimiento_recurrente(movimiento_id):
    """
    Rechaza un movimiento recurrente.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE movimientos
            SET estado = 'rechazado'
            WHERE id = ?
        """, (movimiento_id,))

        conexion.commit()
        conexion.close()
        print("✅ Movimiento rechazado correctamente.")
        return True
    
    except Exception as e:
        print("❌ Error al rechazar el movimiento:", e)
        return False

def procesar_movimientos_recurrentes():
    """
    Procesa los movimientos recurrentes y crea los movimientos correspondientes
    para el día actual si es necesario.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Obtener movimientos recurrentes activos
        cursor.execute("""
            SELECT id, autor_id, categoria, monto, tipo, descripcion, frecuencia, fecha_fin
            FROM movimientos
            WHERE es_recurrente = 1
            AND fecha_fin >= CURRENT_DATE
        """)
        
        movimientos = cursor.fetchall()
        
        for mov in movimientos:
            mov_id, autor_id, categoria, monto, tipo, descripcion, frecuencia, fecha_fin = mov
            
            # Verificar si ya existe un movimiento para hoy
            cursor.execute("""
                SELECT COUNT(*)
                FROM movimientos
                WHERE autor_id = ?
                AND categoria = ?
                AND monto = ?
                AND tipo = ?
                AND descripcion = ?
                AND fecha = ?
                AND es_recurrente = 0
            """, (autor_id, categoria, monto, tipo, descripcion, fecha_actual))
            
            if cursor.fetchone()[0] == 0:
                # Crear el movimiento para hoy
                cursor.execute("""
                    INSERT INTO movimientos (
                        autor_id, fecha, categoria, monto, tipo, descripcion
                    )
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (autor_id, fecha_actual, categoria, monto, tipo, descripcion))
        
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("❌ Error al procesar movimientos recurrentes:", e)
        return False

def verificar_movimientos_pendientes(autor_id):
    """
    Verifica si hay movimientos recurrentes pendientes de aprobación.
    Muestra todos los movimientos pendientes, independientemente de su fecha de registro.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Obtener movimientos pendientes
        cursor.execute("""
            SELECT COUNT(*), 
                   GROUP_CONCAT(
                       categoria || ' ($' || monto || ') - Fecha programada: ' || fecha_registro
                   ) as movimientos
            FROM movimientos
            WHERE autor_id = ?
            AND es_recurrente = 1
            AND estado = 'pendiente'
            AND fecha_fin >= CURRENT_DATE
        """, (autor_id,))
        
        resultado = cursor.fetchone()
        total_pendientes = resultado[0]
        lista_movimientos = resultado[1] if resultado[1] else ""
        
        conexion.close()
        
        if total_pendientes > 0:
            return {
                "hay_pendientes": True,
                "total": total_pendientes,
                "movimientos": lista_movimientos.split(',')
            }
        return {
            "hay_pendientes": False,
            "total": 0,
            "movimientos": []
        }
        
    except Exception as e:
        print(f"❌ Error al verificar movimientos pendientes: {e}")
        return {
            "hay_pendientes": False,
            "total": 0,
            "movimientos": []
        }

def obtener_historial_movimientos(autor_id, filtros=None):
    """
    Obtiene el historial de movimientos con filtros opcionales.
    
    Args:
        autor_id: ID del usuario
        filtros: Diccionario con filtros opcionales:
            - tipo: 'Ingreso' o 'Gasto'
            - monto_min: monto mínimo
            - monto_max: monto máximo
            - fecha_inicio: fecha inicial (YYYY-MM-DD)
            - fecha_fin: fecha final (YYYY-MM-DD)
            - categoria: categoría específica
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Construir la consulta base
        query = """
            SELECT id, fecha, categoria, monto, tipo, descripcion
            FROM movimientos
            WHERE autor_id = ?
            AND es_recurrente = 0
        """
        params = [autor_id]

        # Agregar filtros si se proporcionan
        if filtros:
            if filtros.get('tipo'):
                query += " AND tipo = ?"
                params.append(filtros['tipo'])
            
            if filtros.get('monto_min') is not None:
                query += " AND monto >= ?"
                params.append(filtros['monto_min'])
            
            if filtros.get('monto_max') is not None:
                query += " AND monto <= ?"
                params.append(filtros['monto_max'])
            
            if filtros.get('fecha_inicio'):
                query += " AND fecha >= ?"
                params.append(filtros['fecha_inicio'])
            
            if filtros.get('fecha_fin'):
                query += " AND fecha <= ?"
                params.append(filtros['fecha_fin'])
            
            if filtros.get('categoria'):
                query += " AND categoria = ?"
                params.append(filtros['categoria'])

        # Ordenar por fecha descendente
        query += " ORDER BY fecha DESC"

        cursor.execute(query, params)
        movimientos = cursor.fetchall()
        conexion.close()

        return movimientos

    except Exception as e:
        print(f"❌ Error al obtener historial de movimientos: {e}")
        return None

def obtener_categorias_usuario(autor_id):
    """
    Obtiene todas las categorías únicas usadas por el usuario.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT DISTINCT categoria
            FROM movimientos
            WHERE autor_id = ?
            ORDER BY categoria
        """, (autor_id,))
        
        categorias = [row[0] for row in cursor.fetchall()]
        conexion.close()
        
        return categorias

    except Exception as e:
        print(f"❌ Error al obtener categorías: {e}")
        return []
