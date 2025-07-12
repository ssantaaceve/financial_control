from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.config import settings
from app.services.supabase_service import supabase_service
from app.models.user import UserCreate, UserResponse, Token, TokenData
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Servicio para manejar autenticación y autorización."""
    
    def __init__(self):
        """Inicializar servicio de autenticación."""
        self.supabase = supabase_service.get_client()
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT de acceso."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verificar y decodificar token JWT."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return TokenData(user_id=user_id)
        except JWTError:
            return None
    
    async def register_user(self, user_data: UserCreate) -> Optional[Dict[str, Any]]:
        """Registrar un nuevo usuario."""
        try:
            # Crear usuario en Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if not auth_response.user:
                return {"success": False, "error": "Error en el registro de autenticación"}
            
            # Crear perfil del usuario en la tabla usuarios
            profile_data = {
                "id": auth_response.user.id,
                "name": user_data.name,
                "email": user_data.email
            }
            
            result = await supabase_service.insert_record("usuarios", profile_data)
            
            if result["success"]:
                logger.info(f"✅ Usuario registrado exitosamente: {user_data.email}")
                return {
                    "success": True,
                    "user": UserResponse(
                        id=auth_response.user.id,
                        email=user_data.email,
                        name=user_data.name
                    )
                }
            else:
                # Si falla la creación del perfil, eliminar el usuario de auth
                try:
                    self.supabase.auth.admin.delete_user(auth_response.user.id)
                except:
                    pass
                return {"success": False, "error": "Error al crear el perfil del usuario"}
                
        except Exception as e:
            logger.error(f"❌ Error al registrar usuario: {e}")
            return {"success": False, "error": str(e)}
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar un usuario."""
        try:
            # Iniciar sesión con Supabase
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                return {"success": False, "error": "Credenciales inválidas"}
            
            # Obtener datos del usuario
            user_result = await supabase_service.get_records("usuarios", {"id": auth_response.user.id})
            
            if not user_result["success"] or not user_result["data"]:
                return {"success": False, "error": "Usuario no encontrado"}
            
            user_data = user_result["data"][0]
            
            # Crear token JWT
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"sub": auth_response.user.id}, 
                expires_delta=access_token_expires
            )
            
            logger.info(f"✅ Usuario autenticado exitosamente: {email}")
            return {
                "success": True,
                "user": UserResponse(
                    id=user_data["id"],
                    email=user_data["email"],
                    name=user_data["name"]
                ),
                "token": Token(access_token=access_token)
            }
            
        except Exception as e:
            logger.error(f"❌ Error al autenticar usuario: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Obtener usuario actual basado en el token."""
        try:
            token_data = self.verify_token(token)
            if token_data is None:
                return None
            
            user_result = await supabase_service.get_records("usuarios", {"id": token_data.user_id})
            
            if not user_result["success"] or not user_result["data"]:
                return None
            
            user_data = user_result["data"][0]
            return UserResponse(
                id=user_data["id"],
                email=user_data["email"],
                name=user_data["name"]
            )
            
        except Exception as e:
            logger.error(f"❌ Error al obtener usuario actual: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar perfil de usuario."""
        try:
            result = await supabase_service.update_record("usuarios", user_id, update_data)
            
            if result["success"]:
                logger.info(f"✅ Perfil de usuario actualizado: {user_id}")
                return {"success": True, "data": result["data"]}
            else:
                return {"success": False, "error": result["error"]}
                
        except Exception as e:
            logger.error(f"❌ Error al actualizar perfil: {e}")
            return {"success": False, "error": str(e)}

# Instancia global del servicio
auth_service = AuthService() 