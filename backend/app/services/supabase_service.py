from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    """Servicio base para interactuar con Supabase."""
    
    def __init__(self):
        """Inicializar cliente de Supabase."""
        try:
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("✅ Cliente de Supabase inicializado correctamente")
        except Exception as e:
            logger.error(f"❌ Error al inicializar Supabase: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Probar conexión a Supabase."""
        try:
            # Intentar hacer una consulta simple
            response = self.client.table('usuarios').select('id').limit(1).execute()
            logger.info("✅ Conexión a Supabase exitosa")
            return True
        except Exception as e:
            logger.error(f"❌ Error de conexión a Supabase: {e}")
            return False
    
    def get_client(self) -> Client:
        """Obtener cliente de Supabase."""
        return self.client
    
    async def execute_query(self, query_func) -> Optional[Dict[str, Any]]:
        """Ejecutar una consulta con manejo de errores."""
        try:
            result = query_func()
            return {"success": True, "data": result.data, "error": None}
        except Exception as e:
            logger.error(f"❌ Error en consulta Supabase: {e}")
            return {"success": False, "data": None, "error": str(e)}
    
    async def insert_record(self, table: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insertar un registro en una tabla."""
        try:
            response = self.client.table(table).insert(data).execute()
            return {"success": True, "data": response.data, "error": None}
        except Exception as e:
            logger.error(f"❌ Error al insertar en {table}: {e}")
            return {"success": False, "data": None, "error": str(e)}
    
    async def get_records(self, table: str, filters: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Obtener registros de una tabla con filtros opcionales."""
        try:
            query = self.client.table(table).select('*')
            
            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query = query.eq(key, value)
            
            response = query.execute()
            return {"success": True, "data": response.data, "error": None}
        except Exception as e:
            logger.error(f"❌ Error al obtener registros de {table}: {e}")
            return {"success": False, "data": None, "error": str(e)}
    
    async def update_record(self, table: str, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar un registro en una tabla."""
        try:
            response = self.client.table(table).update(data).eq('id', record_id).execute()
            return {"success": True, "data": response.data, "error": None}
        except Exception as e:
            logger.error(f"❌ Error al actualizar en {table}: {e}")
            return {"success": False, "data": None, "error": str(e)}
    
    async def delete_record(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Eliminar un registro de una tabla."""
        try:
            response = self.client.table(table).delete().eq('id', record_id).execute()
            return {"success": True, "data": response.data, "error": None}
        except Exception as e:
            logger.error(f"❌ Error al eliminar de {table}: {e}")
            return {"success": False, "data": None, "error": str(e)}

# Instancia global del servicio
supabase_service = SupabaseService() 