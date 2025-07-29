#!/usr/bin/env python3
"""
Script para ejecutar el backend en modo desarrollo
"""
import uvicorn
import os

if __name__ == "__main__":
    # Configurar para desarrollo
    os.environ["DEBUG"] = "True"
    
    print("🚀 Iniciando Financial Control Backend en modo desarrollo...")
    print("📍 URL: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("🔄 Auto-reload activado")
    print("⏹️  Presiona Ctrl+C para detener")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 