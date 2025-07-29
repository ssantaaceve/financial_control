from typing import List, Optional
from app.services.supabase_service import supabase_service
from app.models.category import CategoryCreate, CategoryUpdate, CategoryResponse, MovementType
import logging

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self):
        self.table_name = "categories"

    async def get_categories(self, type: Optional[MovementType] = None) -> List[CategoryResponse]:
        """Obtener todas las categorías o filtrar por tipo."""
        try:
            query = supabase_service.supabase.table(self.table_name).select("*")
            
            if type:
                # Convertir el enum a string para la consulta
                type_str = "INGRESO" if type == MovementType.INGRESO else "GASTO"
                query = query.eq("type", type_str)
            
            response = query.execute()
            
            if response.data:
                categories = []
                for item in response.data:
                    # Convertir el tipo de string a enum
                    movement_type = MovementType.INGRESO if item["type"] == "INGRESO" else MovementType.GASTO
                    category = CategoryResponse(
                        id=item["id"],
                        name=item["name"],
                        type=movement_type,
                        icon=item.get("icon"),
                        color=item.get("color"),
                        created_at=item.get("created_at"),
                        updated_at=item.get("updated_at")
                    )
                    categories.append(category)
                return categories
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            raise e

    async def get_category_by_id(self, category_id: str) -> Optional[CategoryResponse]:
        """Obtener una categoría por ID."""
        try:
            response = supabase_service.supabase.table(self.table_name).select("*").eq("id", category_id).execute()
            
            if response.data:
                item = response.data[0]
                movement_type = MovementType.INGRESO if item["type"] == "INGRESO" else MovementType.GASTO
                return CategoryResponse(
                    id=item["id"],
                    name=item["name"],
                    type=movement_type,
                    icon=item.get("icon"),
                    color=item.get("color"),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting category by ID: {e}")
            raise e

    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        """Crear una nueva categoría."""
        try:
            # Convertir el enum a string para Supabase
            type_str = "INGRESO" if category_data.type == MovementType.INGRESO else "GASTO"
            
            data = {
                "name": category_data.name,
                "type": type_str,
                "icon": category_data.icon,
                "color": category_data.color
            }
            
            response = supabase_service.supabase.table(self.table_name).insert(data).execute()
            
            if response.data:
                item = response.data[0]
                movement_type = MovementType.INGRESO if item["type"] == "INGRESO" else MovementType.GASTO
                return CategoryResponse(
                    id=item["id"],
                    name=item["name"],
                    type=movement_type,
                    icon=item.get("icon"),
                    color=item.get("color"),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
            else:
                raise Exception("Failed to create category")
                
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            raise e

    async def update_category(self, category_id: str, category_data: CategoryUpdate) -> Optional[CategoryResponse]:
        """Actualizar una categoría existente."""
        try:
            data = {}
            if category_data.name is not None:
                data["name"] = category_data.name
            if category_data.type is not None:
                data["type"] = "INGRESO" if category_data.type == MovementType.INGRESO else "GASTO"
            if category_data.icon is not None:
                data["icon"] = category_data.icon
            if category_data.color is not None:
                data["color"] = category_data.color
            
            if not data:
                return await self.get_category_by_id(category_id)
            
            response = supabase_service.supabase.table(self.table_name).update(data).eq("id", category_id).execute()
            
            if response.data:
                item = response.data[0]
                movement_type = MovementType.INGRESO if item["type"] == "INGRESO" else MovementType.GASTO
                return CategoryResponse(
                    id=item["id"],
                    name=item["name"],
                    type=movement_type,
                    icon=item.get("icon"),
                    color=item.get("color"),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
            return None
            
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            raise e

    async def delete_category(self, category_id: str) -> bool:
        """Eliminar una categoría."""
        try:
            response = supabase_service.supabase.table(self.table_name).delete().eq("id", category_id).execute()
            return len(response.data) > 0 if response.data else False
            
        except Exception as e:
            logger.error(f"Error deleting category: {e}")
            raise e

# Instancia global del servicio
category_service = CategoryService() 