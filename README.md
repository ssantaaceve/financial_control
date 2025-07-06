# financial_control
App para controlar finanzas personales. Proyecto de aprendizaje con Python y Supabase.

# Program to money management
## Description
A tool for personal finance management, helping users gain control of their finances, improve their money management skills, and achieve their financial goals.

## 🧭 Hoja de Ruta General

- [x] Definir la idea y el MVP inicial  
- [x] Crear un prototipo en Python con una interfaz básica  
- [x] Agregar base de datos local usando SQLite
- [x] Crear primera versión funcional  
- [x] Migrar a Supabase (PostgreSQL en la nube)
- [x] Implementar sistema de autenticación
- [x] Agregar funcionalidad de presupuestos
- [ ] Exportar reportes de ingresos y gastos  
- [ ] Construir aplicación móvil con React Native  
- [ ] Conectar a base de datos en la nube (Firebase / PostgreSQL)  
- [ ] Lanzar versión beta para pruebas  

---

## 🔧 Technologies to Use  
- Main language: **Python**  
- Database: **Supabase (PostgreSQL)**
- Authentication: **Supabase Auth**
- Graphical interface: **Streamlit**
- Future frontend: **React Native**  
- Future backend: **Django** or **Firebase**  
- Version control: **Git & GitHub**  
- Project management: **Jira / GitHub Projects**

## 🔧 GITHUB estructura proyecto
    Tipo	¿Cuándo usarlo?
    feat	Cuando creas una nueva funcionalidad
    fix	Cuando arreglas errores o bugs
    refactor	Cuando mejoras código sin cambiar cómo funciona
    chore	Cambios que no son funcionales, como mover archivos o limpiar
    docs	Cambios en los comentarios o documentación interna
    test	Agregar o modificar pruebas (tests)

## 🚀 Nueva Arquitectura con Supabase

### ✅ Migración Completa a Supabase

La aplicación ha sido completamente migrada de SQLite a **Supabase**, proporcionando:

1. **Base de datos PostgreSQL en la nube**
2. **Sistema de autenticación integrado**
3. **API REST automática**
4. **Escalabilidad y confiabilidad**

### ✅ Nuevas Funcionalidades

#### 🔐 Autenticación Mejorada
- Registro e inicio de sesión usando Supabase Auth
- Gestión de perfiles de usuario
- Actualización de datos personales

#### 💰 Gestión de Movimientos
- Registro de ingresos y gastos
- Categorización automática
- Movimientos recurrentes
- Historial con filtros avanzados

#### 📊 Presupuestos
- Creación de presupuestos por categoría
- Seguimiento de gastos vs presupuesto
- Alertas cuando se supera el límite
- Períodos personalizables (semanal, mensual, anual)

#### 📈 Resúmenes Financieros
- Dashboard con métricas del mes
- Balance de ingresos vs gastos
- Visualización de datos

---

## 🛠️ Configuración del Proyecto

### 1. **Instalar dependencias**
```bash
pip install streamlit supabase python-dotenv
```

### 2. **Configurar Supabase**
1. Crear proyecto en [Supabase](https://supabase.com)
2. Ejecutar el SQL de creación de tablas
3. Copiar URL y API Key

### 3. **Configurar variables de entorno**
Crear archivo `.env`:
```
SUPABASE_URL=tu-url-de-supabase
SUPABASE_KEY=tu-anon-key
```

### 4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

---

## 📊 Estructura de la Base de Datos

### Tablas Principales:
- **usuarios**: Perfiles de usuarios (integrados con Supabase Auth)
- **categorias**: Categorías de ingresos y gastos
- **movimientos**: Transacciones financieras
- **presupuestos**: Límites de gasto por categoría

### Características:
- **UUIDs** para todas las claves primarias
- **Relaciones** con integridad referencial
- **Triggers** automáticos para auditoría
- **Índices** optimizados para consultas

---

## 🔧 Funcionalidades Implementadas

### ✅ Gestión de Usuarios
- Registro con email y contraseña
- Inicio de sesión seguro
- Actualización de perfil
- Gestión de contraseñas

### ✅ Movimientos Financieros
- Registro de ingresos y gastos
- Categorización automática
- Descripción detallada
- Fechas personalizables

### ✅ Movimientos Recurrentes
- Configuración de frecuencias
- Aprobación/rechazo manual
- Fechas de inicio y fin
- Gestión de estados

### ✅ Presupuestos
- Límites por categoría
- Períodos personalizables
- Seguimiento en tiempo real
- Alertas de superación

### ✅ Historial y Reportes
- Filtros avanzados
- Exportación de datos
- Visualización en tablas
- Métricas del mes

---

## 🎨 Interfaz de Usuario

### Características:
- **Diseño responsive** con Streamlit
- **Tipografía Montserrat** para mejor legibilidad
- **Tema claro y moderno**
- **Navegación por pestañas**
- **Formularios intuitivos**

### Secciones:
1. **📝 Nuevo Movimiento**: Registro de transacciones
2. **🔄 Recurrentes**: Gestión de movimientos automáticos
3. **📊 Historial**: Consulta y filtrado de datos
4. **⚙️ Configuración**: Gestión de perfil
5. **💸 Presupuestos**: Control de límites de gasto

---

## 🔒 Seguridad

- **Autenticación** mediante Supabase Auth
- **Contraseñas** hasheadas automáticamente
- **Sesiones** seguras con tokens JWT
- **Validación** de datos en frontend y backend
- **Protección** contra inyección SQL

---

## 📈 Próximas Mejoras

- [ ] **Gráficos interactivos** con Plotly
- [ ] **Exportación** a PDF/Excel
- [ ] **Notificaciones** push
- [ ] **Integración** con bancos
- [ ] **Análisis** con IA
- [ ] **App móvil** nativa

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**password database: hocHyf-1dydwa-kotjex supabase**
