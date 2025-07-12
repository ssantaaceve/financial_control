import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración de la aplicación."""
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # React dev server (alternative port)
        "http://localhost:8501",  # Streamlit (temporal)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8501",
        "https://financial-control-frontend.vercel.app",  # Vercel frontend
        "https://*.vercel.app",  # Any Vercel subdomain
    ]
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Financial Control API"

# Instancia global de configuración
settings = Settings() 