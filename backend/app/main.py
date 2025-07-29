from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.services.supabase_service import supabase_service
from app.services.auth_service import auth_service
from app.services.movement_service import movement_service
from app.services.budget_service import budget_service
from app.services.category_service import category_service
from app.models.user import UserCreate, UserResponse, UserLogin, Token
from app.models.movement import MovementCreate, MovementUpdate, MovementFilter
from app.models.budget import BudgetCreate, BudgetUpdate
from app.models.category import MovementType as CategoryMovementType

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicio y cierre de la aplicación."""
    # Startup
    logger.info("🚀 Iniciando Financial Control API...")
    
    # Probar conexión a Supabase
    connection_test = await supabase_service.test_connection()
    if connection_test:
        logger.info("✅ Conexión a Supabase establecida")
    else:
        logger.error("❌ Error al conectar con Supabase")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando Financial Control API...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API para control de finanzas personales",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener usuario actual
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Obtener usuario actual basado en el token JWT."""
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# Rutas de autenticación
@app.post(f"{settings.API_V1_STR}/auth/register", response_model=dict)
async def register(user_data: UserCreate):
    """Registrar un nuevo usuario."""
    try:
        result = await auth_service.register_user(user_data)
        
        if result["success"]:
            # Crear token para el usuario registrado
            from datetime import timedelta
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = auth_service.create_access_token(
                data={"sub": result["user"].id}, 
                expires_delta=access_token_expires
            )
            
            return {
                "success": True,
                "message": "Usuario registrado exitosamente",
                "user": result["user"],
                "token": {
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.post(f"{settings.API_V1_STR}/auth/login", response_model=dict)
async def login(credentials: UserLogin):
    """Iniciar sesión de usuario."""
    try:
        result = await auth_service.authenticate_user(credentials.email, credentials.password)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Login exitoso",
                "user": result["user"],
                "token": result["token"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Rutas protegidas de usuario
@app.get(f"{settings.API_V1_STR}/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Obtener información del usuario actual."""
    return current_user

@app.put(f"{settings.API_V1_STR}/users/me", response_model=dict)
async def update_user_profile(
    update_data: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar perfil del usuario actual."""
    try:
        result = await auth_service.update_user_profile(current_user.id, update_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Perfil actualizado exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al actualizar perfil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Rutas de movimientos
@app.post(f"{settings.API_V1_STR}/movements", response_model=dict)
async def create_movement(
    movement_data: MovementCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear un nuevo movimiento."""
    try:
        result = await movement_service.create_movement(current_user.id, movement_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Movimiento creado exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al crear movimiento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get(f"{settings.API_V1_STR}/movements", response_model=dict)
async def get_movements(
    movement_type: str = None,
    category: str = None,
    date_from: str = None,
    date_to: str = None,
    amount_min: float = None,
    amount_max: float = None,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener movimientos del usuario con filtros opcionales."""
    try:
        # Construir filtros
        filters = None
        if any([movement_type, category, date_from, date_to, amount_min, amount_max]):
            from datetime import date
            from app.models.movement import MovementType
            
            filters = MovementFilter(
                movement_type=MovementType(movement_type) if movement_type else None,
                category=category,
                date_from=date.fromisoformat(date_from) if date_from else None,
                date_to=date.fromisoformat(date_to) if date_to else None,
                amount_min=amount_min,
                amount_max=amount_max
            )
        
        result = await movement_service.get_movements(current_user.id, filters)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al obtener movimientos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get(f"{settings.API_V1_STR}/movements/{{movement_id}}", response_model=dict)
async def get_movement(
    movement_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener un movimiento específico."""
    try:
        result = await movement_service.get_movement_by_id(current_user.id, movement_id)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al obtener movimiento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.put(f"{settings.API_V1_STR}/movements/{{movement_id}}", response_model=dict)
async def update_movement(
    movement_id: str,
    update_data: MovementUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar un movimiento."""
    try:
        result = await movement_service.update_movement(current_user.id, movement_id, update_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Movimiento actualizado exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al actualizar movimiento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.delete(f"{settings.API_V1_STR}/movements/{{movement_id}}", response_model=dict)
async def delete_movement(
    movement_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar un movimiento."""
    try:
        result = await movement_service.delete_movement(current_user.id, movement_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al eliminar movimiento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Rutas de presupuestos
@app.post(f"{settings.API_V1_STR}/budgets", response_model=dict)
async def create_budget(
    budget_data: BudgetCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear un nuevo presupuesto."""
    try:
        result = await budget_service.create_budget(current_user.id, budget_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Presupuesto creado exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al crear presupuesto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get(f"{settings.API_V1_STR}/budgets", response_model=dict)
async def get_budgets(current_user: UserResponse = Depends(get_current_user)):
    """Obtener todos los presupuestos del usuario."""
    try:
        result = await budget_service.get_budgets(current_user.id)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al obtener presupuestos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get(f"{settings.API_V1_STR}/budgets/{{budget_id}}", response_model=dict)
async def get_budget(
    budget_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener un presupuesto específico."""
    try:
        result = await budget_service.get_budget_by_id(current_user.id, budget_id)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al obtener presupuesto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.put(f"{settings.API_V1_STR}/budgets/{{budget_id}}", response_model=dict)
async def update_budget(
    budget_id: str,
    update_data: BudgetUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar un presupuesto."""
    try:
        result = await budget_service.update_budget(current_user.id, budget_id, update_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Presupuesto actualizado exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al actualizar presupuesto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.delete(f"{settings.API_V1_STR}/budgets/{{budget_id}}", response_model=dict)
async def delete_budget(
    budget_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar un presupuesto."""
    try:
        result = await budget_service.delete_budget(current_user.id, budget_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al eliminar presupuesto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Rutas de reportes
@app.get(f"{settings.API_V1_STR}/reports/financial-summary", response_model=dict)
async def get_financial_summary(
    start_date: str = None,
    end_date: str = None,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener resumen financiero del usuario."""
    try:
        from datetime import date
        
        start = date.fromisoformat(start_date) if start_date else None
        end = date.fromisoformat(end_date) if end_date else None
        
        result = await movement_service.get_financial_summary(current_user.id, start, end)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error al obtener resumen financiero: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get(f"{settings.API_V1_STR}/reports/budget-summary", response_model=dict)
async def get_budget_summary(current_user: UserResponse = Depends(get_current_user)):
    """Obtener resumen de presupuestos del usuario."""
    try:
        result = await budget_service.get_budget_summary(current_user.id)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error getting budget summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Rutas de categorías
@app.get(f"{settings.API_V1_STR}/categories", response_model=dict)
async def get_categories(
    type: CategoryMovementType = None,
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener categorías, opcionalmente filtradas por tipo."""
    try:
        categories = await category_service.get_categories(type)
        
        return {
            "success": True,
            "data": [category.dict() for category in categories]
        }
            
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.post(f"{settings.API_V1_STR}/categories", response_model=dict)
async def create_category(
    category_data: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear una nueva categoría."""
    try:
        from app.models.category import CategoryCreate, MovementType
        
        # Validar que el tipo sea válido
        if category_data.get("type") not in ["INGRESO", "GASTO"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo debe ser 'INGRESO' o 'GASTO'"
            )
        
        # Crear objeto CategoryCreate
        category_create = CategoryCreate(
            name=category_data["name"],
            type=MovementType.INGRESO if category_data["type"] == "INGRESO" else MovementType.GASTO,
            icon=category_data.get("icon"),
            color=category_data.get("color", "#6B7280")
        )
        
        result = await category_service.create_category(category_create)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Categoría creada exitosamente",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Ruta de prueba
@app.get("/")
async def root():
    """Ruta raíz de la API."""
    return {
        "message": "Financial Control API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Verificar estado de la API."""
    return {
        "status": "healthy",
        "database": "connected" if await supabase_service.test_connection() else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 