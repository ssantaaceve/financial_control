#!/usr/bin/env python3
"""
Script para insertar categorías por defecto en Supabase
"""

import os
import sys
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = "https://your-project.supabase.co"  # Reemplaza con tu URL
SUPABASE_KEY = "your-anon-key"  # Reemplaza con tu anon key

def insert_categories():
    """Insertar categorías por defecto en Supabase"""
    
    # Crear cliente de Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Categorías de gastos
    expense_categories = [
        {"name": "Alimentación", "type": "GASTO", "icon": "🍽️", "color": "#EF4444"},
        {"name": "Transporte", "type": "GASTO", "icon": "🚗", "color": "#F59E0B"},
        {"name": "Vivienda", "type": "GASTO", "icon": "🏠", "color": "#8B5CF6"},
        {"name": "Servicios", "type": "GASTO", "icon": "⚡", "color": "#06B6D4"},
        {"name": "Salud", "type": "GASTO", "icon": "🏥", "color": "#10B981"},
        {"name": "Educación", "type": "GASTO", "icon": "📚", "color": "#3B82F6"},
        {"name": "Entretenimiento", "type": "GASTO", "icon": "🎬", "color": "#EC4899"},
        {"name": "Ropa", "type": "GASTO", "icon": "👕", "color": "#F97316"},
        {"name": "Tecnología", "type": "GASTO", "icon": "💻", "color": "#6366F1"},
        {"name": "Deportes", "type": "GASTO", "icon": "⚽", "color": "#84CC16"},
        {"name": "Viajes", "type": "GASTO", "icon": "✈️", "color": "#14B8A6"},
        {"name": "Mascotas", "type": "GASTO", "icon": "🐕", "color": "#F472B6"},
        {"name": "Regalos", "type": "GASTO", "icon": "🎁", "color": "#A855F7"},
        {"name": "Impuestos", "type": "GASTO", "icon": "📋", "color": "#DC2626"},
        {"name": "Seguros", "type": "GASTO", "icon": "🛡️", "color": "#059669"},
        {"name": "Otros Gastos", "type": "GASTO", "icon": "📦", "color": "#6B7280"}
    ]
    
    # Categorías de ingresos
    income_categories = [
        {"name": "Salario", "type": "INGRESO", "icon": "💰", "color": "#10B981"},
        {"name": "Freelance", "type": "INGRESO", "icon": "💼", "color": "#3B82F6"},
        {"name": "Inversiones", "type": "INGRESO", "icon": "📈", "color": "#F59E0B"},
        {"name": "Negocios", "type": "INGRESO", "icon": "🏢", "color": "#8B5CF6"},
        {"name": "Rentas", "type": "INGRESO", "icon": "🏠", "color": "#06B6D4"},
        {"name": "Bonificaciones", "type": "INGRESO", "icon": "🎉", "color": "#EC4899"},
        {"name": "Reembolsos", "type": "INGRESO", "icon": "↩️", "color": "#84CC16"},
        {"name": "Préstamos", "type": "INGRESO", "icon": "🏦", "color": "#F97316"},
        {"name": "Herencia", "type": "INGRESO", "icon": "💎", "color": "#A855F7"},
        {"name": "Ventas", "type": "INGRESO", "icon": "🛒", "color": "#14B8A6"},
        {"name": "Comisiones", "type": "INGRESO", "icon": "📊", "color": "#6366F1"},
        {"name": "Otros Ingresos", "type": "INGRESO", "icon": "💵", "color": "#6B7280"}
    ]
    
    all_categories = expense_categories + income_categories
    
    try:
        # Insertar categorías
        response = supabase.table("categories").insert(all_categories).execute()
        
        if response.data:
            print(f"✅ Se insertaron {len(response.data)} categorías exitosamente")
            print("\n📊 Categorías insertadas:")
            for category in response.data:
                print(f"  - {category['name']} ({category['type']})")
        else:
            print("❌ No se pudieron insertar las categorías")
            
    except Exception as e:
        print(f"❌ Error al insertar categorías: {e}")

if __name__ == "__main__":
    print("🚀 Insertando categorías por defecto en Supabase...")
    print("\n⚠️  IMPORTANTE: Antes de ejecutar este script, asegúrate de:")
    print("   1. Tener configuradas las credenciales de Supabase")
    print("   2. Haber creado la tabla 'categories' en Supabase")
    print("   3. Tener instalado: pip install supabase")
    print("\n" + "="*50)
    
    # Verificar si las credenciales están configuradas
    if SUPABASE_URL == "https://your-project.supabase.co" or SUPABASE_KEY == "your-anon-key":
        print("❌ Error: Debes configurar las credenciales de Supabase en este script")
        print("   Edita las variables SUPABASE_URL y SUPABASE_KEY con tus credenciales")
        sys.exit(1)
    
    insert_categories() 