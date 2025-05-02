import  sqlite3 #Modlulo estandar de base de datos para trabajar con sql lite, el import nos trae el repositorio
import os #Módulo para interactuar con el sistema operativo (aquí lo usamos para construir la ruta al archivo de la base de datos). con este modulo puedo usar python para interactuar con el sistema operativo en general
from datetime import datetime


DB_PATH = os.path.join("data", "finanzas_parejas.db") #se define ruta para que pueda ser trabajada en diferentes sistemas operativos/ Se guarda la base de datos en mi carpeta ya creada. 
#Funcion para crear tablas base de datos.
def crear_tablas():
    conexion = sqlite3.connect(DB_PATH) #Abrimos la base de datos que creamos en la variable anterior
    cursor = conexion.cursor() # con este objeto podemos enviar los comando que vamos a escribir a SQL/. en este caso usamos un herramienta de conexion, con cursos podemos mandar comando SQL. 


    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        contraseña TEXT NOT NULL
    );
    """) #con .execute podemos empezar a crear coido sql para crear la tabla y definir las variables, esto debe ir entre comillas, usamos tres comillas para podemos escribir varias lineas. 



    # Tabla de parejas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parejas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        usuario_1_id INTEGER,
        usuario_2_id INTEGER,
        FOREIGN KEY (usuario_1_id) REFERENCES usuarios(id),
        FOREIGN KEY (usuario_2_id) REFERENCES usuarios(id)
    );
    """)
    # Tabla de movimientos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        autor_id INTEGER,
        pareja_id INTEGER,
        fecha DATE,
        categoria TEXT,
        monto REAL,
        tipo TEXT,
        descripcion TEXT,
        es_recurrente BOOLEAN DEFAULT 0,
        frecuencia TEXT,
        fecha_fin DATE,
        FOREIGN KEY (autor_id) REFERENCES usuarios(id),
        FOREIGN KEY (pareja_id) REFERENCES parejas(id)
    );
    """)
    conexion.commit() #guarda los cambios en el archivo .db.
    conexion.close() #  cierra la conexión.
    print("✅ Tablas creadas correctamente.")

#Comando para agregar o modificar campos en tabla base de datos
def agregar_campos():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    nuevos_campos = {
        "recurrente": "BOOLEAN DEFAULT 0",
        "medio_de_pago": "TEXT",
    }

    for campo, tipo in nuevos_campos.items():
        try:
            cursor.execute(f"ALTER TABLE movimientos ADD COLUMN {campo} {tipo};")
            print(f"✅ Campo '{campo}' agregado correctamente.")
        except sqlite3.OperationalError as e:
            print(f"⚠️ No se pudo agregar '{campo}': {e}")

    conexion.commit()
    conexion.close()
#Funcion para crear tablas especificas para el programa.
def crear_tablas_especifico():
    conexion = sqlite3.connect(DB_PATH)  # Abrimos la base de datos
    cursor = conexion.cursor()  # Creamos el cursor para ejecutar comandos SQL

    # Tabla de categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('Ingreso', 'Gasto')) NOT NULL
    );
    """)

    # Confirmar cambios y cerrar conexión
    conexion.commit()
    conexion.close()


#Funcion para estandarizar los tipos de movimientos en la base de datos.
def estandarizar_tipos_movimientos():
    """
    Estandariza los tipos de movimientos en la base de datos.
    Convierte todos los 'ingreso' a 'Ingreso' y 'gasto' a 'Gasto'.
    Esta función solo debe ejecutarse una vez.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Actualizar todos los registros que tengan 'ingreso' a 'Ingreso'
        cursor.execute("""
            UPDATE movimientos 
            SET tipo = 'Ingreso' 
            WHERE LOWER(tipo) = 'ingreso'
        """)

        # Actualizar todos los registros que tengan 'gasto' a 'Gasto'
        cursor.execute("""
            UPDATE movimientos 
            SET tipo = 'Gasto' 
            WHERE LOWER(tipo) = 'gasto'
        """)

        # Confirmar los cambios
        conexion.commit()
        
        # Obtener estadísticas de la actualización
        cursor.execute("SELECT COUNT(*) FROM movimientos WHERE tipo = 'Ingreso'")
        ingresos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM movimientos WHERE tipo = 'Gasto'")
        gastos = cursor.fetchone()[0]
        
        conexion.close()
        
        return {
            "success": True,
            "message": "✅ Tipos de movimientos estandarizados correctamente.",
            "estadisticas": {
                "total_ingresos": ingresos,
                "total_gastos": gastos
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al estandarizar los tipos de movimientos: {e}",
            "estadisticas": None
        }
    
def actualizar_tabla_movimientos():
    """
    Actualiza la tabla movimientos para agregar los campos necesarios para movimientos recurrentes.
    Esta función es segura para ejecutar en bases de datos existentes.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Verificar si los campos ya existen
        cursor.execute("PRAGMA table_info(movimientos)")
        campos_existentes = [campo[1] for campo in cursor.fetchall()]

        # Agregar campos si no existen
        nuevos_campos = {
            "es_recurrente": "BOOLEAN DEFAULT 0",
            "frecuencia": "TEXT",
            "fecha_registro": "DATE",  # Fecha específica para registrar el movimiento
            "fecha_fin": "DATE",
            "estado": "TEXT DEFAULT 'pendiente'"  # pendiente, aprobado, rechazado
        }

        for campo, tipo in nuevos_campos.items():
            if campo not in campos_existentes:
                cursor.execute(f"ALTER TABLE movimientos ADD COLUMN {campo} {tipo}")
                print(f"✅ Campo '{campo}' agregado correctamente.")
            else:
                print(f"ℹ️ El campo '{campo}' ya existe.")

        conexion.commit()
        conexion.close()
        print("✅ Tabla movimientos actualizada correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error al actualizar la tabla movimientos: {e}")
        return False
    
