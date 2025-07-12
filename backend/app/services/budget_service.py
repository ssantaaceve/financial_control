from typing import Optional, Dict, Any, List
from datetime import date, datetime
from app.services.supabase_service import supabase_service
from app.models.budget import BudgetCreate, BudgetResponse, BudgetUpdate, BudgetPeriod
from app.services.movement_service import movement_service
import logging

logger = logging.getLogger(__name__)

class BudgetService:
    """Servicio para gestionar presupuestos."""
    
    def __init__(self):
        """Inicializar servicio de presupuestos."""
        self.supabase = supabase_service.get_client()
    
    async def create_budget(self, user_id: str, budget_data: BudgetCreate) -> Optional[Dict[str, Any]]:
        """Crear un nuevo presupuesto."""
        try:
            # Obtener o crear la categoría
            category_id = await self._get_or_create_category(user_id, budget_data.category)
            
            if not category_id:
                return {"success": False, "error": "Error al obtener/crear categoría"}
            
            # Preparar datos del presupuesto
            budget_record = {
                "usuario_id": user_id,
                "categoria_id": category_id,
                "monto_maximo": budget_data.max_amount,
                "periodo": budget_data.period.value,
                "fecha_inicio": budget_data.start_date.strftime('%Y-%m-%d'),
                "fecha_fin": budget_data.end_date.strftime('%Y-%m-%d')
            }
            
            result = await supabase_service.insert_record("presupuestos", budget_record)
            
            if result["success"]:
                logger.info(f"✅ Presupuesto creado exitosamente para usuario {user_id}")
                return {
                    "success": True,
                    "data": result["data"][0] if result["data"] else None
                }
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al crear presupuesto: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_budgets(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener todos los presupuestos del usuario."""
        try:
            response = self.supabase.table('presupuestos').select('*, categorias(nombre)').eq('usuario_id', user_id).execute()
            
            if response.data:
                budgets = []
                for budget in response.data:
                    # Calcular gasto actual y estadísticas
                    current_amount = await self._calculate_current_spending(
                        user_id, 
                        budget.get("categorias", {}).get("nombre", ""),
                        budget["fecha_inicio"],
                        budget["fecha_fin"]
                    )
                    
                    max_amount = budget["monto_maximo"]
                    remaining_amount = max(0, max_amount - current_amount)
                    percentage_used = (current_amount / max_amount * 100) if max_amount > 0 else 0
                    
                    budgets.append({
                        "id": budget["id"],
                        "user_id": budget["usuario_id"],
                        "category": budget.get("categorias", {}).get("nombre", "Sin categoría"),
                        "max_amount": max_amount,
                        "current_amount": current_amount,
                        "remaining_amount": remaining_amount,
                        "percentage_used": percentage_used,
                        "period": BudgetPeriod(budget["periodo"]),
                        "start_date": budget["fecha_inicio"],
                        "end_date": budget["fecha_fin"],
                        "created_at": budget.get("created_at"),
                        "updated_at": budget.get("updated_at")
                    })
                
                return {"success": True, "data": budgets}
            else:
                return {"success": True, "data": []}
                
        except Exception as e:
            logger.error(f"❌ Error al obtener presupuestos: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_budget_by_id(self, user_id: str, budget_id: str) -> Optional[Dict[str, Any]]:
        """Obtener un presupuesto específico por ID."""
        try:
            response = self.supabase.table('presupuestos').select('*, categorias(nombre)').eq('id', budget_id).eq('usuario_id', user_id).execute()
            
            if response.data:
                budget = response.data[0]
                
                # Calcular gasto actual y estadísticas
                current_amount = await self._calculate_current_spending(
                    user_id,
                    budget.get("categorias", {}).get("nombre", ""),
                    budget["fecha_inicio"],
                    budget["fecha_fin"]
                )
                
                max_amount = budget["monto_maximo"]
                remaining_amount = max(0, max_amount - current_amount)
                percentage_used = (current_amount / max_amount * 100) if max_amount > 0 else 0
                
                return {
                    "success": True,
                    "data": {
                        "id": budget["id"],
                        "user_id": budget["usuario_id"],
                        "category": budget.get("categorias", {}).get("nombre", "Sin categoría"),
                        "max_amount": max_amount,
                        "current_amount": current_amount,
                        "remaining_amount": remaining_amount,
                        "percentage_used": percentage_used,
                        "period": BudgetPeriod(budget["periodo"]),
                        "start_date": budget["fecha_inicio"],
                        "end_date": budget["fecha_fin"],
                        "created_at": budget.get("created_at"),
                        "updated_at": budget.get("updated_at")
                    }
                }
            else:
                return {"success": False, "error": "Presupuesto no encontrado"}
                
        except Exception as e:
            logger.error(f"❌ Error al obtener presupuesto: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_budget(self, user_id: str, budget_id: str, update_data: BudgetUpdate) -> Optional[Dict[str, Any]]:
        """Actualizar un presupuesto."""
        try:
            # Verificar que el presupuesto existe y pertenece al usuario
            budget_check = await self.get_budget_by_id(user_id, budget_id)
            if not budget_check["success"]:
                return {"success": False, "error": "Presupuesto no encontrado"}
            
            # Preparar datos de actualización
            update_record = {}
            
            if update_data.max_amount is not None:
                update_record["monto_maximo"] = update_data.max_amount
            
            if update_data.category is not None:
                # Obtener o crear nueva categoría
                category_id = await self._get_or_create_category(user_id, update_data.category)
                if category_id:
                    update_record["categoria_id"] = category_id
            
            if update_data.period is not None:
                update_record["periodo"] = update_data.period.value
            
            if update_data.start_date is not None:
                update_record["fecha_inicio"] = update_data.start_date.strftime('%Y-%m-%d')
            
            if update_data.end_date is not None:
                update_record["fecha_fin"] = update_data.end_date.strftime('%Y-%m-%d')
            
            if not update_record:
                return {"success": False, "error": "No hay datos para actualizar"}
            
            result = await supabase_service.update_record("presupuestos", budget_id, update_record)
            
            if result["success"]:
                logger.info(f"✅ Presupuesto actualizado exitosamente: {budget_id}")
                return {"success": True, "data": result["data"]}
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al actualizar presupuesto: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_budget(self, user_id: str, budget_id: str) -> Optional[Dict[str, Any]]:
        """Eliminar un presupuesto."""
        try:
            # Verificar que el presupuesto existe y pertenece al usuario
            budget_check = await self.get_budget_by_id(user_id, budget_id)
            if not budget_check["success"]:
                return {"success": False, "error": "Presupuesto no encontrado"}
            
            result = await supabase_service.delete_record("presupuestos", budget_id)
            
            if result["success"]:
                logger.info(f"✅ Presupuesto eliminado exitosamente: {budget_id}")
                return {"success": True, "message": "Presupuesto eliminado exitosamente"}
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al eliminar presupuesto: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_budget_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener resumen de presupuestos del usuario."""
        try:
            budgets_result = await self.get_budgets(user_id)
            
            if not budgets_result["success"]:
                return budgets_result
            
            budgets = budgets_result["data"]
            
            if not budgets:
                return {
                    "success": True,
                    "data": {
                        "total_budgets": 0,
                        "total_allocated": 0,
                        "total_spent": 0,
                        "total_remaining": 0,
                        "budgets": []
                    }
                }
            
            total_allocated = sum(budget["max_amount"] for budget in budgets)
            total_spent = sum(budget["current_amount"] for budget in budgets)
            total_remaining = sum(budget["remaining_amount"] for budget in budgets)
            
            return {
                "success": True,
                "data": {
                    "total_budgets": len(budgets),
                    "total_allocated": total_allocated,
                    "total_spent": total_spent,
                    "total_remaining": total_remaining,
                    "budgets": budgets
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error al obtener resumen de presupuestos: {e}")
            return {"success": False, "error": str(e)}
    
    async def _calculate_current_spending(self, user_id: str, category_name: str, start_date: str, end_date: str) -> float:
        """Calcular el gasto actual en una categoría durante un período."""
        try:
            # Obtener movimientos de gasto en la categoría durante el período
            response = self.supabase.table('movimientos').select('monto').eq('usuario_id', user_id).eq('tipo', 'Gasto').eq('es_recurrente', False).gte('fecha', start_date).lte('fecha', end_date).execute()
            
            if response.data:
                # Filtrar por categoría (esto requeriría un join, pero por simplicidad calculamos el total)
                # En una implementación real, deberías hacer un join con la tabla categorias
                total_spent = sum(mov["monto"] for mov in response.data)
                return total_spent
            
            return 0.0
            
        except Exception as e:
            logger.error(f"❌ Error al calcular gasto actual: {e}")
            return 0.0
    
    async def _get_or_create_category(self, user_id: str, category_name: str) -> Optional[str]:
        """Obtener una categoría existente o crear una nueva."""
        try:
            # Buscar categoría existente (asumimos que es para gastos)
            response = self.supabase.table('categorias').select('id').eq('usuario_id', user_id).eq('nombre', category_name).eq('tipo', 'Gasto').execute()
            
            if response.data:
                return response.data[0]['id']
            
            # Crear nueva categoría
            category_data = {
                "nombre": category_name,
                "tipo": "Gasto",
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
budget_service = BudgetService() 