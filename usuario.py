from supabase_config import get_supabase_client
from datetime import datetime
import hashlib

def registrar_usuario(nombre, correo, contraseña):
    """
    Registra un nuevo usuario en Supabase.
    Nota: En Supabase, los usuarios se crean a través del sistema de autenticación.
    Esta función crea el perfil del usuario después del registro.
    """
    try:
        supabase = get_supabase_client()
        
        # Crear usuario en el sistema de autenticación de Supabase
        auth_response = supabase.auth.sign_up({
            "email": correo,
            "password": contraseña
        })
        
        if auth_response.user:
            # Crear perfil del usuario en la tabla usuarios
            user_data = {
                "id": auth_response.user.id,
                "nombre": nombre,
                "correo": correo
            }
            
            response = supabase.table('usuarios').insert(user_data).execute()
            
            if response.data:
                print("✅ Usuario registrado exitosamente.")
                return True
            else:
                print("❌ Error al crear el perfil del usuario.")
                return False
        else:
            print("❌ Error en el registro de autenticación.")
            return False
            
    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        return False

def iniciar_sesion_db(correo, contraseña):
    """
    Inicia sesión usando el sistema de autenticación de Supabase.
    """
    try:
        supabase = get_supabase_client()
        
        # Iniciar sesión
        auth_response = supabase.auth.sign_in_with_password({
            "email": correo,
            "password": contraseña
        })
        
        if auth_response.user:
            # Obtener datos del usuario
            user_data = obtener_datos_usuario(auth_response.user.id)
            if user_data:
                return {
                    "id": auth_response.user.id,
                    "nombre": user_data.get('nombre'),
                    "correo": user_data.get('correo')
                }
        
        return None
        
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        return None

def obtener_datos_usuario(usuario_id):
    """
    Obtiene los datos de un usuario por su ID.
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('usuarios').select('*').eq('id', usuario_id).execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        print(f"❌ Error al obtener datos del usuario: {e}")
        return None

def actualizar_correo_usuario(usuario_id, nuevo_correo):
    """
    Actualiza el correo electrónico de un usuario.
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar si el correo ya existe
        response = supabase.table('usuarios').select('id').eq('correo', nuevo_correo).execute()
        if response.data:
            print("❌ El correo electrónico ya está en uso.")
            return False
        
        # Actualizar correo
        response = supabase.table('usuarios').update({'correo': nuevo_correo}).eq('id', usuario_id).execute()
        
        if response.data:
            print("✅ Correo electrónico actualizado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al actualizar correo: {e}")
        return False

def actualizar_contraseña_usuario(usuario_id, contraseña_actual, nueva_contraseña):
    """
    Actualiza la contraseña de un usuario.
    Nota: En Supabase, esto se maneja a través del sistema de autenticación.
    """
    try:
        supabase = get_supabase_client()
        
        # Actualizar contraseña en el sistema de autenticación
        auth_response = supabase.auth.update_user({
            "password": nueva_contraseña
        })
        
        if auth_response.user:
            print("✅ Contraseña actualizada exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al actualizar contraseña: {e}")
        return False

def actualizar_nombre_usuario(usuario_id, nuevo_nombre):
    """
    Actualiza el nombre de un usuario.
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('usuarios').update({'nombre': nuevo_nombre}).eq('id', usuario_id).execute()
        
        if response.data:
            print("✅ Nombre actualizado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al actualizar nombre: {e}")
        return False