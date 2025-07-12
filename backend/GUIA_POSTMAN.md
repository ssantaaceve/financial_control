# 🚀 Guía para Probar la API con Postman

## 📋 Requisitos Previos

1. **Postman instalado** - Descarga desde [postman.com](https://www.postman.com/downloads/)
2. **Servidor corriendo** - Asegúrate de que el backend esté ejecutándose en `http://localhost:8001`
3. **Colección importada** - Importa el archivo `Financial_Control_API.postman_collection.json`

## 🔧 Configuración Inicial

### 1. Importar la Colección
1. Abre Postman
2. Haz clic en "Import" (botón azul)
3. Selecciona el archivo `Financial_Control_API.postman_collection.json`
4. La colección aparecerá en tu workspace

### 2. Configurar Variables de Entorno
1. En la colección, ve a la pestaña "Variables"
2. Verifica que `base_url` esté configurado como `http://localhost:8001`
3. Las variables `auth_token`, `movement_id`, y `budget_id` se llenarán automáticamente

## 🧪 Flujo de Pruebas Recomendado

### Paso 1: Verificar el Sistema
1. **Health Check** - Verifica que el servidor esté funcionando
2. **Root Endpoint** - Confirma que la API responde

### Paso 2: Autenticación
1. **Registrar Usuario** - Crea un nuevo usuario
   - Cambia el email en el body si es necesario
   - Guarda el `user.id` de la respuesta
2. **Login Usuario** - Inicia sesión
   - Copia el `access_token` de la respuesta
   - Pégalo en la variable `auth_token` de la colección

### Paso 3: Gestión de Usuario
1. **Obtener Usuario Actual** - Verifica que el token funciona
2. **Actualizar Perfil** - Prueba la actualización de datos

### Paso 4: Movimientos Financieros
1. **Crear Movimiento** - Crea un gasto o ingreso
   - Guarda el `id` del movimiento creado
   - Pégalo en la variable `movement_id`
2. **Obtener Movimientos** - Lista todos los movimientos
3. **Obtener Movimientos con Filtros** - Prueba los filtros
4. **Obtener Movimiento por ID** - Obtiene un movimiento específico
5. **Actualizar Movimiento** - Modifica el movimiento
6. **Eliminar Movimiento** - Elimina el movimiento

### Paso 5: Presupuestos
1. **Crear Presupuesto** - Crea un presupuesto mensual
   - Guarda el `id` del presupuesto creado
   - Pégalo en la variable `budget_id`
2. **Obtener Presupuestos** - Lista todos los presupuestos
3. **Obtener Presupuesto por ID** - Obtiene un presupuesto específico
4. **Actualizar Presupuesto** - Modifica el presupuesto
5. **Eliminar Presupuesto** - Elimina el presupuesto

### Paso 6: Reportes
1. **Resumen Financiero** - Obtiene estadísticas generales
2. **Resumen Financiero con Fechas** - Filtra por período
3. **Resumen de Presupuestos** - Estadísticas de presupuestos

## 📝 Ejemplos de Datos de Prueba

### Usuario de Prueba
```json
{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Usuario de Prueba"
}
```

### Movimiento de Gasto
```json
{
    "amount": 150.50,
    "category": "Comida",
    "description": "Almuerzo en restaurante",
    "movement_type": "Gasto",
    "movement_date": "2025-07-11"
}
```

### Movimiento de Ingreso
```json
{
    "amount": 2500.00,
    "category": "Salario",
    "description": "Pago mensual",
    "movement_type": "Ingreso",
    "movement_date": "2025-07-01"
}
```

### Presupuesto Mensual
```json
{
    "category": "Comida",
    "max_amount": 500.00,
    "period": "mensual",
    "start_date": "2025-07-01",
    "end_date": "2025-07-31"
}
```

## 🔍 Verificación de Respuestas

### Respuesta Exitosa (200)
```json
{
    "success": true,
    "message": "Operación exitosa",
    "data": { ... }
}
```

### Error de Autenticación (401)
```json
{
    "detail": "Token inválido o expirado"
}
```

### Error de Validación (422)
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "field"],
            "msg": "Field required"
        }
    ]
}
```

## 🎯 Consejos de Uso

### Variables Automáticas
- **auth_token**: Se llena automáticamente al hacer login
- **movement_id**: Se llena al crear un movimiento
- **budget_id**: Se llena al crear un presupuesto

### Headers Importantes
- `Content-Type: application/json` - Para requests con body
- `Authorization: Bearer {{auth_token}}` - Para rutas protegidas

### Filtros Disponibles
- **Movimientos**: `movement_type`, `category`, `date_from`, `date_to`, `amount_min`, `amount_max`
- **Reportes**: `start_date`, `end_date`

## 🚨 Solución de Problemas

### Error: "Address already in use"
- El puerto 8001 está ocupado
- Detén otros procesos o cambia el puerto

### Error: "Token inválido o expirado"
- El token ha expirado (30 minutos)
- Haz login nuevamente para obtener un nuevo token

### Error: "Could not find column"
- Verifica que la estructura de la base de datos coincida
- Revisa los logs del servidor para más detalles

### Error: "Connection refused"
- El servidor no está corriendo
- Ejecuta `python run.py` en el directorio backend

## 📊 Monitoreo

### Logs del Servidor
Los logs muestran todas las operaciones:
- ✅ Operaciones exitosas
- ❌ Errores y excepciones
- 🔍 Consultas a la base de datos

### Respuestas de la API
- Status codes: 200 (éxito), 400 (error cliente), 401 (no autorizado), 500 (error servidor)
- Mensajes descriptivos en caso de error
- Datos estructurados en formato JSON

## 🎉 ¡Listo para Probar!

Con esta guía puedes probar todas las funcionalidades de la API de manera sistemática. Cada endpoint está documentado y configurado para funcionar correctamente con la autenticación JWT. 