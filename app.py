import streamlit as st
import sqlite3
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Control Financiero",
    page_icon="💰",
    layout="wide"
)

# Conexión a la base de datos
DB_PATH = os.path.join("data", "finanzas_parejas.db")

def obtener_resumen_financiero(autor_id):
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

def obtener_movimientos(autor_id):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT fecha, tipo, categoria, monto, descripcion
            FROM movimientos
            WHERE autor_id = ?
            ORDER BY fecha DESC
        """, (autor_id,))
        
        movimientos = cursor.fetchall()
        conexion.close()
        
        if movimientos:
            df = pd.DataFrame(movimientos, columns=['Fecha', 'Tipo', 'Categoría', 'Monto', 'Descripción'])
            return df
        return None
    except Exception as e:
        st.error(f"Error al obtener movimientos: {e}")
        return None

# --- Inicio de la aplicación ---
st.title("💰 Control Financiero Personal")

# Sidebar para autenticación
with st.sidebar:
    st.header("Iniciar Sesión")
    correo = st.text_input("Correo electrónico")
    contraseña = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        try:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM usuarios WHERE correo = ? AND contraseña = ?", 
                         (correo, contraseña))
            usuario = cursor.fetchone()
            conexion.close()
            
            if usuario:
                st.session_state['usuario_id'] = usuario[0]
                st.session_state['nombre'] = usuario[1]
                st.success(f"¡Bienvenido, {usuario[1]}!")
            else:
                st.error("Credenciales incorrectas")
        except Exception as e:
            st.error(f"Error al iniciar sesión: {e}")

# Si el usuario está logueado, mostrar el contenido principal
if 'usuario_id' in st.session_state:
    # Resumen financiero
    resumen = obtener_resumen_financiero(st.session_state['usuario_id'])
    if resumen:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ingresos", f"${resumen['ingresos']:,.2f}")
        with col2:
            st.metric("Gastos", f"${resumen['gastos']:,.2f}")
        with col3:
            st.metric("Balance", f"${resumen['balance']:,.2f}")

    # Formulario para nuevo movimiento
    with st.expander("➕ Agregar Nuevo Movimiento", expanded=False):
        with st.form("nuevo_movimiento"):
            col1, col2 = st.columns(2)
            with col1:
                tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
                categoria = st.text_input("Categoría")
            with col2:
                monto = st.number_input("Monto", min_value=0.0, step=100.0)
                descripcion = st.text_input("Descripción")
            
            if st.form_submit_button("Guardar Movimiento"):
                try:
                    conexion = sqlite3.connect(DB_PATH)
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO movimientos (autor_id, fecha, categoria, monto, tipo, descripcion)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (st.session_state['usuario_id'], 
                          datetime.now().strftime('%Y-%m-%d'),
                          categoria, monto, tipo, descripcion))
                    conexion.commit()
                    conexion.close()
                    st.success("✅ Movimiento registrado con éxito")
                except Exception as e:
                    st.error(f"Error al registrar el movimiento: {e}")

    # Historial de movimientos
    st.subheader("📄 Historial de Movimientos")
    movimientos = obtener_movimientos(st.session_state['usuario_id'])
    if movimientos is not None:
        st.dataframe(movimientos, use_container_width=True)
        
        # Gráfico de gastos por categoría
        if not movimientos[movimientos['Tipo'] == 'Gasto'].empty:
            st.subheader("📊 Distribución de Gastos")
            fig = px.pie(movimientos[movimientos['Tipo'] == 'Gasto'], 
                        values='Monto', 
                        names='Categoría',
                        title='Gastos por Categoría')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay movimientos registrados")
else:
    st.info("👋 Por favor, inicia sesión para ver tu control financiero")
