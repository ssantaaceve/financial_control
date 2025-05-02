import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib
from usuario import (
    registrar_usuario,
    iniciar_sesion_db,
    actualizar_correo_usuario,
    actualizar_contraseña_usuario,
    actualizar_nombre_usuario,
    obtener_datos_usuario
)

# Configuración de la página
st.set_page_config(
    page_title="Control Financiero",
    page_icon="💰",
    layout="wide"
)

# Ruta a la base de datos
DB_PATH = os.path.join("data", "finanzas_parejas.db")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def obtener_resumen_financiero(autor_id):
    """Obtiene el resumen financiero del mes actual."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Obtener la fecha actual y el primer día del mes
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        primer_dia_mes = datetime.now().replace(day=1).strftime('%Y-%m-%d')

        # Consulta para obtener ingresos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'Ingreso' 
            AND fecha >= ? 
            AND fecha <= ?
        """, (autor_id, primer_dia_mes, fecha_actual))
        total_ingresos = cursor.fetchone()[0]

        # Consulta para obtener gastos del mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) 
            FROM movimientos 
            WHERE autor_id = ? 
            AND tipo = 'Gasto' 
            AND fecha >= ? 
            AND fecha <= ?
        """, (autor_id, primer_dia_mes, fecha_actual))
        total_gastos = cursor.fetchone()[0]

        # Calcular balance
        balance = total_ingresos - total_gastos

        conexion.close()
        return {
            "ingresos": total_ingresos,
            "gastos": total_gastos,
            "balance": balance
        }
    except Exception as e:
        st.error(f"Error al obtener el resumen financiero: {e}")
        return None

def obtener_movimientos_recientes(autor_id, limite=5):
    """Obtiene los movimientos más recientes."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT fecha, categoria, monto, tipo, descripcion
            FROM movimientos
            WHERE autor_id = ?
            ORDER BY fecha DESC
            LIMIT ?
        """, (autor_id, limite))
        
        movimientos = cursor.fetchall()
        conexion.close()
        
        return movimientos
    except Exception as e:
        st.error(f"Error al obtener movimientos recientes: {e}")
        return None

def obtener_movimientos_recurrentes_pendientes(autor_id):
    """Obtiene los movimientos recurrentes pendientes."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, categoria, monto, tipo, descripcion, frecuencia, fecha_registro, fecha_fin
            FROM movimientos
            WHERE autor_id = ?
            AND es_recurrente = 1
            AND estado = 'pendiente'
            AND fecha_fin >= CURRENT_DATE
            ORDER BY fecha_registro ASC
        """, (autor_id,))
        
        movimientos = cursor.fetchall()
        conexion.close()
        
        return movimientos
    except Exception as e:
        st.error(f"Error al obtener movimientos recurrentes: {e}")
        return None

def registrar_movimiento(autor_id, fecha, categoria, monto, tipo, descripcion):
    """Registra un nuevo movimiento."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO movimientos (autor_id, fecha, categoria, monto, tipo, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (autor_id, fecha, categoria, monto, tipo, descripcion))

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"Error al registrar el movimiento: {e}")
        return False

def iniciar_sesion(correo, contraseña):
    """Inicia sesión y retorna los datos del usuario."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, correo
            FROM usuarios
            WHERE correo = ? AND contraseña = ?
        """, (correo, contraseña))
        
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            return {
                "id": resultado[0],
                "nombre": resultado[1],
                "correo": resultado[2]
            }
        return None
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")
        return None

def registrar_usuario(nombre, correo, contraseña):
    """Registra un nuevo usuario."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Verificar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
        if cursor.fetchone():
            st.error("El correo electrónico ya está registrado")
            return False

        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña)
            VALUES (?, ?, ?)
        """, (nombre, correo, contraseña))

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"Error al registrar usuario: {e}")
        return False

def main():
    # Inicializar estado de sesión
    if 'usuario' not in st.session_state:
        st.session_state.usuario = None

    # Sidebar para login/registro
    with st.sidebar:
        st.title("💰 Control Financiero")
        
        if st.session_state.usuario is None:
            st.subheader("Iniciar Sesión")
            correo = st.text_input("Correo electrónico")
            contraseña = st.text_input("Contraseña", type="password")
            
            if st.button("Iniciar Sesión"):
                usuario = iniciar_sesion(correo, contraseña)
                if usuario:
                    st.session_state.usuario = usuario
                    st.success(f"¡Bienvenido, {usuario['nombre']}!")
                    st.rerun()
                else:
                    st.error("Correo o contraseña incorrectos")
            
            st.markdown("---")
            st.subheader("Registrarse")
            nuevo_nombre = st.text_input("Nombre")
            nuevo_correo = st.text_input("Nuevo correo electrónico")
            nueva_contraseña = st.text_input("Nueva contraseña", type="password")
            
            if st.button("Registrarse"):
                if registrar_usuario(nuevo_nombre, nuevo_correo, nueva_contraseña):
                    st.success("Usuario registrado exitosamente")
                else:
                    st.error("Error al registrar usuario")
        else:
            st.subheader(f"👤 {st.session_state.usuario['nombre']}")
            if st.button("Cerrar Sesión"):
                st.session_state.usuario = None
                st.rerun()

    # Contenido principal
    if st.session_state.usuario:
        # Resumen financiero
        resumen = obtener_resumen_financiero(st.session_state.usuario['id'])
        if resumen:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Ingresos", f"${resumen['ingresos']:,.2f}")
            with col2:
                st.metric("💸 Gastos", f"${resumen['gastos']:,.2f}")
            with col3:
                st.metric("💵 Balance", f"${resumen['balance']:,.2f}")

        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Nuevo Movimiento", "🔄 Recurrentes", "📊 Historial", "⚙️ Configuración"])

        with tab1:
            st.subheader("Registrar Nuevo Movimiento")
            with st.form("nuevo_movimiento"):
                col1, col2 = st.columns(2)
                with col1:
                    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
                    monto = st.number_input("Monto", min_value=0.0, step=0.01)
                with col2:
                    categoria = st.text_input("Categoría")
                    fecha = st.date_input("Fecha")
                
                descripcion = st.text_area("Descripción")
                
                if st.form_submit_button("Registrar"):
                    if registrar_movimiento(
                        st.session_state.usuario['id'],
                        fecha.strftime('%Y-%m-%d'),
                        categoria,
                        monto,
                        tipo,
                        descripcion
                    ):
                        st.success("Movimiento registrado exitosamente")
                    else:
                        st.error("Error al registrar el movimiento")

        with tab2:
            st.subheader("Movimientos Recurrentes")
            movimientos_recurrentes = obtener_movimientos_recurrentes_pendientes(st.session_state.usuario['id'])
            
            if movimientos_recurrentes:
                for mov in movimientos_recurrentes:
                    with st.expander(f"{mov[1]} - ${mov[2]:,.2f} ({mov[5]})"):
                        st.write(f"Tipo: {mov[3]}")
                        st.write(f"Descripción: {mov[4]}")
                        st.write(f"Fecha programada: {mov[6]}")
                        st.write(f"Fecha final: {mov[7]}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Aprobar", key=f"aprobar_{mov[0]}"):
                                st.success("Movimiento aprobado")
                        with col2:
                            if st.button("Rechazar", key=f"rechazar_{mov[0]}"):
                                st.error("Movimiento rechazado")
                        with col3:
                            if st.button("Posponer", key=f"posponer_{mov[0]}"):
                                st.info("Movimiento pospuesto")
            else:
                st.info("No hay movimientos recurrentes pendientes")

        with tab3:
            st.subheader("Historial de Movimientos")
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                tipo_filtro = st.selectbox("Tipo", ["Todos", "Ingreso", "Gasto"])
            with col2:
                fecha_inicio = st.date_input("Fecha inicio")
            with col3:
                fecha_fin = st.date_input("Fecha fin")
            
            # Mostrar movimientos recientes
            movimientos = obtener_movimientos_recientes(st.session_state.usuario['id'])
            if movimientos:
                df = pd.DataFrame(movimientos, columns=['Fecha', 'Categoría', 'Monto', 'Tipo', 'Descripción'])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay movimientos registrados")

        with tab4:
            st.subheader("Configuración de Perfil")
            
            # Obtener datos actuales del usuario
            datos_usuario = obtener_datos_usuario(st.session_state.usuario['id'])
            
            if datos_usuario:
                with st.form("actualizar_perfil"):
                    nuevo_nombre = st.text_input("Nombre", value=datos_usuario['nombre'])
                    nuevo_correo = st.text_input("Correo electrónico", value=datos_usuario['correo'])
                    
                    st.subheader("Cambiar Contraseña")
                    contraseña_actual = st.text_input("Contraseña actual", type="password")
                    nueva_contraseña = st.text_input("Nueva contraseña", type="password")
                    confirmar_contraseña = st.text_input("Confirmar nueva contraseña", type="password")
                    
                    if st.form_submit_button("Actualizar Perfil"):
                        # Aquí iría la lógica para actualizar el perfil
                        st.success("Perfil actualizado exitosamente")

    else:
        st.title("Bienvenido a Control Financiero")
        st.write("Por favor, inicia sesión para acceder a tus finanzas.")

if __name__ == "__main__":
    main()
