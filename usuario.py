import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join("data", "finanzas_parejas.db")

def registrar_usuario(nombre, correo, contraseña): # Creamos la funcion para registrar un usuario
    try: #Forma de decir "intenta hacer algo"
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT correo FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone() #busqueda si ya exite el correo

        if resultado:
            print("✅ Correo ya registrado. Intenta con otro correo.")
            conexion.close()
            return False  # Ya existe, no se registró
        else:         
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, fecha_creacion)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP);
            """, (nombre, correo, contraseña))

        conexion.commit()
        conexion.close()
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

def actualizar_correo_usuario(usuario_id, nuevo_correo):
    """
    Actualiza el correo electrónico de un usuario.
    
    Args:
        usuario_id: ID del usuario
        nuevo_correo: Nuevo correo electrónico
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Verificar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = ? AND id != ?", (nuevo_correo, usuario_id))
        if cursor.fetchone():
            print("❌ Este correo electrónico ya está en uso.")
            return False
        
        # Actualizar el correo
        cursor.execute("UPDATE usuarios SET correo = ? WHERE id = ?", (nuevo_correo, usuario_id))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar el correo: {e}")
        return False

def actualizar_contraseña_usuario(usuario_id, contraseña_actual, nueva_contraseña):
    """
    Actualiza la contraseña de un usuario.
    
    Args:
        usuario_id: ID del usuario
        contraseña_actual: Contraseña actual del usuario
        nueva_contraseña: Nueva contraseña
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Verificar la contraseña actual
        cursor.execute("SELECT contraseña FROM usuarios WHERE id = ?", (usuario_id,))
        resultado = cursor.fetchone()
        
        if not resultado or resultado[0] != hashlib.sha256(contraseña_actual.encode()).hexdigest():
            print("❌ Contraseña actual incorrecta.")
            return False
        
        # Actualizar la contraseña
        nueva_contraseña_hash = hashlib.sha256(nueva_contraseña.encode()).hexdigest()
        cursor.execute("UPDATE usuarios SET contraseña = ? WHERE id = ?", (nueva_contraseña_hash, usuario_id))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar la contraseña: {e}")
        return False

def actualizar_nombre_usuario(usuario_id, nuevo_nombre):
    """
    Actualiza el nombre de un usuario.
    
    Args:
        usuario_id: ID del usuario
        nuevo_nombre: Nuevo nombre del usuario
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (nuevo_nombre, usuario_id))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar el nombre: {e}")
        return False

def obtener_datos_usuario(usuario_id):
    """
    Obtiene los datos actuales del usuario.
    
    Args:
        usuario_id: ID del usuario
    
    Returns:
        dict: Diccionario con los datos del usuario o None si hay error
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, nombre, correo FROM usuarios WHERE id = ?", (usuario_id,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            return {
                'id': resultado[0],
                'nombre': resultado[1],
                'correo': resultado[2]
            }
        return None
    except Exception as e:
        print(f"❌ Error al obtener datos del usuario: {e}")
        return None