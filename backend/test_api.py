#!/usr/bin/env python3
"""
Script para probar todas las rutas de la Financial Control API
"""

import requests
import json
from datetime import date, datetime
import time

# Configuración
BASE_URL = "http://localhost:8001"
API_VERSION = "/api/v1"

# Headers para las peticiones
headers = {
    "Content-Type": "application/json"
}

# Variables para almacenar datos de prueba
test_user = None
auth_token = None
test_movement_id = None
test_budget_id = None

def print_response(response, title):
    """Imprimir respuesta de forma legible."""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*50}")

def test_health_check():
    """Probar endpoint de health check."""
    print("\n🏥 Probando Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def test_root():
    """Probar endpoint raíz."""
    print("\n🏠 Probando Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")

def test_register():
    """Probar registro de usuario."""
    global test_user
    
    print("\n👤 Probando Registro de Usuario...")
    
    user_data = {
        "email": f"test_user_{int(time.time())}@example.com",
        "password": "TestPassword123!",
        "name": "Usuario de Prueba"
    }
    
    response = requests.post(
        f"{BASE_URL}{API_VERSION}/auth/register",
        headers=headers,
        json=user_data
    )
    
    print_response(response, "Registro de Usuario")
    
    if response.status_code == 200:
        test_user = response.json()
        print("✅ Usuario registrado exitosamente")
    else:
        print("❌ Error en el registro")

def test_login():
    """Probar login de usuario."""
    global auth_token
    
    print("\n🔐 Probando Login...")
    
    if not test_user:
        print("❌ No hay usuario registrado para hacer login")
        return
    
    login_data = {
        "email": test_user["user"]["email"],
        "password": "TestPassword123!"
    }
    
    response = requests.post(
        f"{BASE_URL}{API_VERSION}/auth/login",
        headers=headers,
        json=login_data
    )
    
    print_response(response, "Login")
    
    if response.status_code == 200:
        auth_token = response.json()["token"]["access_token"]
        headers["Authorization"] = f"Bearer {auth_token}"
        print("✅ Login exitoso, token obtenido")
    else:
        print("❌ Error en el login")

def test_get_current_user():
    """Probar obtener usuario actual."""
    print("\n👤 Probando Obtener Usuario Actual...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/users/me",
        headers=headers
    )
    
    print_response(response, "Usuario Actual")

def test_update_user_profile():
    """Probar actualización de perfil."""
    print("\n✏️ Probando Actualización de Perfil...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    update_data = {
        "name": "Usuario Actualizado"
    }
    
    response = requests.put(
        f"{BASE_URL}{API_VERSION}/users/me",
        headers=headers,
        json=update_data
    )
    
    print_response(response, "Actualización de Perfil")

def test_create_movement():
    """Probar creación de movimiento."""
    global test_movement_id
    
    print("\n💰 Probando Creación de Movimiento...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    movement_data = {
        "amount": 150.50,
        "category": "Comida",
        "description": "Almuerzo en restaurante",
        "movement_type": "Gasto",
        "movement_date": date.today().isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}{API_VERSION}/movements",
        headers=headers,
        json=movement_data
    )
    
    print_response(response, "Creación de Movimiento")
    
    if response.status_code == 200:
        test_movement_id = response.json()["data"]["id"]
        print(f"✅ Movimiento creado con ID: {test_movement_id}")
    else:
        print("❌ Error al crear movimiento")

def test_get_movements():
    """Probar obtención de movimientos."""
    print("\n📋 Probando Obtener Movimientos...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/movements",
        headers=headers
    )
    
    print_response(response, "Lista de Movimientos")

def test_get_movement_by_id():
    """Probar obtener movimiento por ID."""
    print("\n🔍 Probando Obtener Movimiento por ID...")
    
    if not auth_token or not test_movement_id:
        print("❌ No hay token o ID de movimiento")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/movements/{test_movement_id}",
        headers=headers
    )
    
    print_response(response, "Movimiento por ID")

def test_update_movement():
    """Probar actualización de movimiento."""
    print("\n✏️ Probando Actualización de Movimiento...")
    
    if not auth_token or not test_movement_id:
        print("❌ No hay token o ID de movimiento")
        return
    
    update_data = {
        "amount": 175.00,
        "description": "Almuerzo actualizado"
    }
    
    response = requests.put(
        f"{BASE_URL}{API_VERSION}/movements/{test_movement_id}",
        headers=headers,
        json=update_data
    )
    
    print_response(response, "Actualización de Movimiento")

def test_create_budget():
    """Probar creación de presupuesto."""
    global test_budget_id
    
    print("\n📊 Probando Creación de Presupuesto...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    # Calcular fechas para el presupuesto (mes actual)
    today = date.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month + 1, 1) if today.month < 12 else date(today.year + 1, 1, 1)
    end_date = end_date.replace(day=1) - date.resolution
    
    budget_data = {
        "category": "Comida",
        "max_amount": 500.00,
        "period": "mensual",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}{API_VERSION}/budgets",
        headers=headers,
        json=budget_data
    )
    
    print_response(response, "Creación de Presupuesto")
    
    if response.status_code == 200:
        test_budget_id = response.json()["data"]["id"]
        print(f"✅ Presupuesto creado con ID: {test_budget_id}")
    else:
        print("❌ Error al crear presupuesto")

def test_get_budgets():
    """Probar obtención de presupuestos."""
    print("\n📋 Probando Obtener Presupuestos...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/budgets",
        headers=headers
    )
    
    print_response(response, "Lista de Presupuestos")

def test_get_budget_by_id():
    """Probar obtener presupuesto por ID."""
    print("\n🔍 Probando Obtener Presupuesto por ID...")
    
    if not auth_token or not test_budget_id:
        print("❌ No hay token o ID de presupuesto")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/budgets/{test_budget_id}",
        headers=headers
    )
    
    print_response(response, "Presupuesto por ID")

def test_update_budget():
    """Probar actualización de presupuesto."""
    print("\n✏️ Probando Actualización de Presupuesto...")
    
    if not auth_token or not test_budget_id:
        print("❌ No hay token o ID de presupuesto")
        return
    
    update_data = {
        "max_amount": 600.00
    }
    
    response = requests.put(
        f"{BASE_URL}{API_VERSION}/budgets/{test_budget_id}",
        headers=headers,
        json=update_data
    )
    
    print_response(response, "Actualización de Presupuesto")

def test_financial_summary():
    """Probar resumen financiero."""
    print("\n📈 Probando Resumen Financiero...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/reports/financial-summary",
        headers=headers
    )
    
    print_response(response, "Resumen Financiero")

def test_budget_summary():
    """Probar resumen de presupuestos."""
    print("\n📊 Probando Resumen de Presupuestos...")
    
    if not auth_token:
        print("❌ No hay token de autenticación")
        return
    
    response = requests.get(
        f"{BASE_URL}{API_VERSION}/reports/budget-summary",
        headers=headers
    )
    
    print_response(response, "Resumen de Presupuestos")

def test_delete_movement():
    """Probar eliminación de movimiento."""
    print("\n🗑️ Probando Eliminación de Movimiento...")
    
    if not auth_token or not test_movement_id:
        print("❌ No hay token o ID de movimiento")
        return
    
    response = requests.delete(
        f"{BASE_URL}{API_VERSION}/movements/{test_movement_id}",
        headers=headers
    )
    
    print_response(response, "Eliminación de Movimiento")

def test_delete_budget():
    """Probar eliminación de presupuesto."""
    print("\n🗑️ Probando Eliminación de Presupuesto...")
    
    if not auth_token or not test_budget_id:
        print("❌ No hay token o ID de presupuesto")
        return
    
    response = requests.delete(
        f"{BASE_URL}{API_VERSION}/budgets/{test_budget_id}",
        headers=headers
    )
    
    print_response(response, "Eliminación de Presupuesto")

def run_all_tests():
    """Ejecutar todas las pruebas en orden."""
    print("🚀 Iniciando pruebas completas de la Financial Control API")
    print(f"📍 URL Base: {BASE_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Pruebas básicas
        test_health_check()
        test_root()
        
        # Pruebas de autenticación
        test_register()
        test_login()
        test_get_current_user()
        test_update_user_profile()
        
        # Pruebas de movimientos
        test_create_movement()
        test_get_movements()
        test_get_movement_by_id()
        test_update_movement()
        
        # Pruebas de presupuestos
        test_create_budget()
        test_get_budgets()
        test_get_budget_by_id()
        test_update_budget()
        
        # Pruebas de reportes
        test_financial_summary()
        test_budget_summary()
        
        # Pruebas de eliminación
        test_delete_movement()
        test_delete_budget()
        
        print("\n🎉 ¡Todas las pruebas completadas!")
        print("✅ La API está funcionando correctamente")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        print("🔍 Revisa que el servidor esté corriendo en el puerto 8001")

if __name__ == "__main__":
    run_all_tests() 