// Script para configurar automáticamente las variables de Postman
// Este script se ejecuta después de cada request

// Función para extraer y configurar el token de autenticación
function setupAuthToken() {
    if (pm.response.code === 200) {
        const response = pm.response.json();
        
        // Para login exitoso
        if (response.token && response.token.access_token) {
            pm.collectionVariables.set("auth_token", response.token.access_token);
            console.log("✅ Token configurado automáticamente");
        }
        
        // Para registro exitoso
        if (response.user && response.user.id) {
            pm.collectionVariables.set("user_id", response.user.id);
            console.log("✅ User ID configurado automáticamente");
        }
    }
}

// Función para extraer IDs de movimientos y presupuestos
function setupEntityIds() {
    if (pm.response.code === 200) {
        const response = pm.response.json();
        
        // Para creación de movimientos
        if (response.data && response.data.id && pm.request.url.path.includes("movements")) {
            pm.collectionVariables.set("movement_id", response.data.id);
            console.log("✅ Movement ID configurado automáticamente:", response.data.id);
        }
        
        // Para creación de presupuestos
        if (response.data && response.data.id && pm.request.url.path.includes("budgets")) {
            pm.collectionVariables.set("budget_id", response.data.id);
            console.log("✅ Budget ID configurado automáticamente:", response.data.id);
        }
    }
}

// Función para validar respuestas
function validateResponse() {
    if (pm.response.code === 200) {
        console.log("✅ Request exitoso");
        
        // Validar estructura de respuesta
        const response = pm.response.json();
        if (response.success !== undefined) {
            console.log("📋 Respuesta estructurada correctamente");
        }
    } else {
        console.log("❌ Error en request:", pm.response.code);
        console.log("📄 Respuesta:", pm.response.text());
    }
}

// Ejecutar funciones según el tipo de request
const requestName = pm.request.name;

if (requestName.includes("Login") || requestName.includes("Registrar")) {
    setupAuthToken();
} else if (requestName.includes("Crear")) {
    setupEntityIds();
}

// Validar todas las respuestas
validateResponse();

// Mostrar variables actuales
console.log("🔧 Variables actuales:");
console.log("- auth_token:", pm.collectionVariables.get("auth_token") ? "Configurado" : "No configurado");
console.log("- movement_id:", pm.collectionVariables.get("movement_id") ? "Configurado" : "No configurado");
console.log("- budget_id:", pm.collectionVariables.get("budget_id") ? "Configurado" : "No configurado"); 