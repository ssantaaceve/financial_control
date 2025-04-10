import  sqlite3 #Modlulo estandar de base de datos para trabajar con sql lite, el import nos trae el repositorio
import os #Módulo para interactuar con el sistema operativo (aquí lo usamos para construir la ruta al archivo de la base de datos). con este modulo puedo usar python para interactuar con el sistema operativo en general


DB_PATH = os.path.join("data", "finanzas_parejas.db") #se define ruta para que pueda ser trabajada en diferentes sistemas operativos/ Se guarda la base de datos en mi carpeta ya creada. 

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
        pareja_id INTEGER,
        fecha DATE,
        categoria TEXT,
        monto REAL,
        tipo TEXT,
        autor_id INTEGER,
        descripcion TEXT,
        FOREIGN KEY (pareja_id) REFERENCES parejas(id),
        FOREIGN KEY (autor_id) REFERENCES usuarios(id)
    );
    """)
    conexion.commit() #guarda los cambios en el archivo .db.
    conexion.close() #  cierra la conexión.
    print("✅ Tablas creadas correctamente.")


crear_tablas()
