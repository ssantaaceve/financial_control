import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hzkpfmguqfoleedqfatt.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "tu-anon-key-aqui")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    """Retorna el cliente de Supabase configurado."""
    return supabase

def test_connection():
    """Prueba la conexión a Supabase."""
    try:
        # Intentar hacer una consulta simple
        response = supabase.table('usuarios').select('id').limit(1).execute()
        print("✅ Conexión a Supabase exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a Supabase: {e}")
        return False 