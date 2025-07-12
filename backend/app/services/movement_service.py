from typing import Optional, Dict, Any, List
from datetime import date, datetime
from app.services.supabase_service import supabase_service
from app.models.movement import MovementCreate, MovementResponse, MovementUpdate, MovementFilter, MovementType
import logging

logger = logging.getLogger(__name__)

class MovementService:
    """Servicio para gestionar movimientos financieros."""
    
    def __init__(self):
        """Inicializar servicio de movimientos."""
        self.supabase = supabase_service.get_client()
    
    async def create_movement(self, user_id: str, movement_data: MovementCreate) -> Optional[Dict[str, Any]]:
        """Crear un nuevo movimiento."""
        try:
            # Obtener o crear la categoría
            category_id = await self._get_or_create_category(user_id, movement_data.category, movement_data.movement_type)
            
            if not category_id:
                return {"success": False, "error": "Error al obtener/crear categoría"}
            
            # Preparar datos del movimiento
            movement_record = {
                "usuario_id": user_id,
                "fecha": movement_data.movement_date.strftime('%Y-%m-%d'),
                "categoria_id": category_id,
                "monto": movement_data.amount,
                "tipo": movement_data.movement_type.value,
                "descripcion": movement_data.description,
                "es_recurrente": False
            }
            
            result = await supabase_service.insert_record("movimientos", movement_record)
            
            if result["success"]:
                logger.info(f"✅ Movimiento creado exitosamente para usuario {user_id}")
                return {
                    "success": True,
                    "data": result["data"][0] if result["data"] else None
                }
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al crear movimiento: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_movements(self, user_id: str, filters: Optional[MovementFilter] = None) -> Optional[Dict[str, Any]]:
        """Obtener movimientos del usuario con filtros opcionales."""
        try:
            # Construir consulta base
            query = self.supabase.table('movimientos').select('*, categorias(nombre)').eq('usuario_id', user_id).eq('es_recurrente', False)
            
            # Aplicar filtros si se proporcionan
            if filters:
                if filters.movement_type:
                    query = query.eq('tipo', filters.movement_type.value)
                
                if filters.category:
                    # Filtrar por nombre de categoría
                    query = query.eq('categorias.nombre', filters.category)
                
                if filters.date_from:
                    query = query.gte('fecha', filters.date_from.strftime('%Y-%m-%d'))
                
                if filters.date_to:
                    query = query.lte('fecha', filters.date_to.strftime('%Y-%m-%d'))
                
                if filters.amount_min:
                    query = query.gte('monto', filters.amount_min)
                
                if filters.amount_max:
                    query = query.lte('monto', filters.amount_max)
            
            # Ordenar por fecha descendente
            response = query.order('fecha', desc=True).execute()
            
            if response.data:
                # Transformar datos al formato de respuesta
                movements = []
                for mov in response.data:
                    movements.append({
                        "id": mov["id"],
                        "user_id": mov["usuario_id"],
                        "amount": mov["monto"],
                        "category": mov.get("categorias", {}).get("nombre", "Sin categoría"),
                        "description": mov["descripcion"],
                        "movement_type": MovementType(mov["tipo"]),
                        "movement_date": mov["fecha"],
                        "created_at": mov.get("created_at"),
                        "updated_at": mov.get("updated_at")
                    })
                
                return {"success": True, "data": movements}
            else:
                return {"success": True, "data": []}
                
        except Exception as e:
            logger.error(f"❌ Error al obtener movimientos: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_movement_by_id(self, user_id: str, movement_id: str) -> Optional[Dict[str, Any]]:
        """Obtener un movimiento específico por ID."""
        try:
            response = self.supabase.table('movimientos').select('*, categorias(nombre)').eq('id', movement_id).eq('usuario_id', user_id).execute()
            
            if response.data:
                mov = response.data[0]
                return {
                    "success": True,
                    "data": {
                        "id": mov["id"],
                        "user_id": mov["usuario_id"],
                        "amount": mov["monto"],
                        "category": mov.get("categorias", {}).get("nombre", "Sin categoría"),
                        "description": mov["descripcion"],
                        "movement_type": MovementType(mov["tipo"]),
                        "movement_date": mov["fecha"],
                        "created_at": mov.get("created_at"),
                        "updated_at": mov.get("updated_at")
                    }
                }
            else:
                return {"success": False, "error": "Movimiento no encontrado"}
                
        except Exception as e:
            logger.error(f"❌ Error al obtener movimiento: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_movement(self, user_id: str, movement_id: str, update_data: MovementUpdate) -> Optional[Dict[str, Any]]:
        """Actualizar un movimiento."""
        try:
            # Verificar que el movimiento existe y pertenece al usuario
            movement_check = await self.get_movement_by_id(user_id, movement_id)
            if not movement_check["success"]:
                return {"success": False, "error": "Movimiento no encontrado"}
            
            # Preparar datos de actualización
            update_record = {}
            
            if update_data.amount is not None:
                update_record["monto"] = update_data.amount
            
            if update_data.category is not None:
                # Obtener o crear nueva categoría
                category_id = await self._get_or_create_category(user_id, update_data.category, update_data.movement_type or MovementType.GASTO)
                if category_id:
                    update_record["categoria_id"] = category_id
            
            if update_data.description is not None:
                update_record["descripcion"] = update_data.description
            
            if update_data.movement_type is not None:
                update_record["tipo"] = update_data.movement_type.value
            
            if update_data.movement_date is not None:
                update_record["fecha"] = update_data.movement_date.strftime('%Y-%m-%d')
            
            if not update_record:
                return {"success": False, "error": "No hay datos para actualizar"}
            
            result = await supabase_service.update_record("movimientos", movement_id, update_record)
            
            if result["success"]:
                logger.info(f"✅ Movimiento actualizado exitosamente: {movement_id}")
                return {"success": True, "data": result["data"]}
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al actualizar movimiento: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_movement(self, user_id: str, movement_id: str) -> Optional[Dict[str, Any]]:
        """Eliminar un movimiento."""
        try:
            # Verificar que el movimiento existe y pertenece al usuario
            movement_check = await self.get_movement_by_id(user_id, movement_id)
            if not movement_check["success"]:
                return {"success": False, "error": "Movimiento no encontrado"}
            
            result = await supabase_service.delete_record("movimientos", movement_id)
            
            if result["success"]:
                logger.info(f"✅ Movimiento eliminado exitosamente: {movement_id}")
                return {"success": True, "message": "Movimiento eliminado exitosamente"}
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al eliminar movimiento: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_financial_summary(self, user_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Optional[Dict[str, Any]]:
        """Obtener resumen financiero del usuario."""
        try:
            # Construir consulta base
            query = self.supabase.table('movimientos').select('monto, tipo').eq('usuario_id', user_id).eq('es_recurrente', False)
            
            # Aplicar filtros de fecha si se proporcionan
            if start_date:
                query = query.gte('fecha', start_date.strftime('%Y-%m-%d'))
            if end_date:
                query = query.lte('fecha', end_date.strftime('%Y-%m-%d'))
            
            response = query.execute()
            
            if response.data:
                total_income = sum(mov["monto"] for mov in response.data if mov["tipo"] == "Ingreso")
                total_expenses = sum(mov["monto"] for mov in response.data if mov["tipo"] == "Gasto")
                balance = total_income - total_expenses
                
                return {
                    "success": True,
                    "data": {
                        "total_income": total_income,
                        "total_expenses": total_expenses,
                        "balance": balance,
                        "movement_count": len(response.data)
                    }
                }
            else:
                return {
                    "success": True,
                    "data": {
                        "total_income": 0,
                        "total_expenses": 0,
                        "balance": 0,
                        "movement_count": 0
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Error al obtener resumen financiero: {e}")
            return {"success": False, "error": str(e)}
    
    async def _get_or_create_category(self, user_id: str, category_name: str, movement_type: MovementType) -> Optional[str]:
        """Obtener una categoría existente o crear una nueva."""
        try:
            # Buscar categoría existente
            response = self.supabase.table('categorias').select('id').eq('usuario_id', user_id).eq('nombre', category_name).eq('tipo', movement_type.value).execute()
            
            if response.data:
                return response.data[0]['id']
            
            # Crear nueva categoría
            category_data = {
                "nombre": category_name,
                "tipo": movement_type.value,
                "usuario_id": user_id
            }
            
            result = await supabase_service.insert_record("categorias", category_data)
            
            if result["success"] and result["data"]:
                return result["data"][0]['id']
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error al obtener/crear categoría: {e}")
            return None

# Instancia global del servicio
movement_service = MovementService() 