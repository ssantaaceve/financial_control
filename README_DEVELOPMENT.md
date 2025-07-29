# 🚀 Guía de Desarrollo - Financial Control

## 📋 Desarrollo Local (Tiempo Real)

### 1. **Iniciar Backend (Terminal 1)**
```bash
cd backend
python run_dev.py
```
- Backend en: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Auto-reload activado

### 2. **Iniciar Frontend (Terminal 2)**
```bash
cd frontend
npm run start:dev
```
- Frontend en: http://localhost:3000
- Hot reload activado
- Conectado a backend local

### 3. **Hacer cambios**
- Edita cualquier archivo
- Los cambios se ven **automáticamente** en el navegador
- No necesitas hacer push/deploy

---

## 🌐 Producción

### **Subir cambios a producción:**
```bash
# 1. Agregar cambios
git add .

# 2. Commit
git commit -m "Descripción de cambios"

# 3. Push a main
git push origin main
```

### **Resultado:**
- **Vercel** hará deploy automático del frontend
- **Render** hará deploy automático del backend
- En 2-5 minutos estará en producción

---

## 🔧 Configuración Automática

### **Variables de entorno:**
- **Desarrollo**: Usa `http://localhost:8001` automáticamente
- **Producción**: Usa URL de Render automáticamente
- **No necesitas cambiar nada manualmente**

### **Scripts disponibles:**
- `npm run start:dev` - Desarrollo local
- `npm run build:prod` - Build para producción
- `python run_dev.py` - Backend con auto-reload

---

## 💡 Tips

✅ **Desarrollo local**: Para cambios rápidos y pruebas  
✅ **Producción**: Para ver el resultado final  
✅ **Hot reload**: Los cambios se ven instantáneamente  
✅ **Sin CORS**: Todo funciona en localhost  
✅ **Debugging fácil**: Usa las DevTools del navegador  

---

**¡Desarrollo local = Cambios instantáneos!** 🎉 