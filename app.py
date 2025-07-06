import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase_config import get_supabase_client, test_connection
from usuario import (
    registrar_usuario,
    iniciar_sesion_db,
    actualizar_correo_usuario,
    actualizar_contraseña_usuario,
    actualizar_nombre_usuario,
    obtener_datos_usuario
)
from movimientos import (
    registrar_movimiento_DB,
    obtener_resumen_financiero,
    registrar_movimiento_recurrente_DB,
    obtener_movimientos_recurrentes_pendientes,
    aprobar_movimiento_recurrente,
    rechazar_movimiento_recurrente,
    obtener_historial_movimientos,
    obtener_categorias_usuario,
    crear_presupuesto,
    obtener_presupuestos_usuario,
    gasto_acumulado
)

# Configuración de la página
st.set_page_config(
    page_title="Control Financiero",
    page_icon="💰",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: 500;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    .metric-label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        color: #666;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 500;
        font-family: 'Montserrat', sans-serif;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E3F2FD;
        color: #1E88E5;
    }
    .stForm {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
    }
    .stAlert {
        border-radius: 10px;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    /* Estilos para los títulos */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    /* Estilos para los campos de formulario */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

def obtener_movimientos_recientes(usuario_id, limite=5):
    """Obtiene los movimientos más recientes."""
    try:
        movimientos = obtener_historial_movimientos(usuario_id)
        if movimientos:
            return movimientos[:limite]
        return []
    except Exception as e:
        st.error(f"Error al obtener movimientos recientes: {e}")
        return []

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
                usuario = iniciar_sesion_db(correo, contraseña)
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
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Ingresos del Mes</div>
                        <div class="metric-value">${resumen['ingresos']:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Gastos del Mes</div>
                        <div class="metric-value">${resumen['gastos']:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Balance</div>
                        <div class="metric-value">${resumen['balance']:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Nuevo Movimiento", "🔄 Recurrentes", "📊 Historial", "⚙️ Configuración", "💸 Presupuestos"])

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
                    if registrar_movimiento_DB(
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
            
            # Formulario para nuevo movimiento recurrente
            with st.expander("➕ Registrar Nuevo Movimiento Recurrente"):
                with st.form("nuevo_movimiento_recurrente"):
                    col1, col2 = st.columns(2)
                    with col1:
                        tipo_recurrente = st.selectbox("Tipo", ["Ingreso", "Gasto"], key="tipo_recurrente")
                        monto_recurrente = st.number_input("Monto", min_value=0.0, step=0.01, key="monto_recurrente")
                    with col2:
                        categoria_recurrente = st.text_input("Categoría", key="categoria_recurrente")
                        frecuencia = st.selectbox("Frecuencia", ["diario", "semanal", "mensual", "anual"])
                    
                    descripcion_recurrente = st.text_area("Descripción", key="descripcion_recurrente")
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        fecha_inicio = st.date_input("Fecha de inicio")
                    with col4:
                        fecha_fin = st.date_input("Fecha de fin")
                    
                    if st.form_submit_button("Registrar Movimiento Recurrente"):
                        if registrar_movimiento_recurrente_DB(
                            st.session_state.usuario['id'],
                            categoria_recurrente,
                            monto_recurrente,
                            tipo_recurrente,
                            descripcion_recurrente,
                            frecuencia,
                            fecha_inicio.strftime('%Y-%m-%d'),
                            fecha_fin.strftime('%Y-%m-%d')
                        ):
                            st.success("Movimiento recurrente registrado exitosamente")
                        else:
                            st.error("Error al registrar el movimiento recurrente")
            
            # Mostrar movimientos recurrentes pendientes
            st.subheader("Movimientos Recurrentes Pendientes")
            movimientos_recurrentes = obtener_movimientos_recurrentes_pendientes(st.session_state.usuario['id'])
            
            if movimientos_recurrentes:
                for mov in movimientos_recurrentes:
                    categoria_nombre = mov.get('categorias', {}).get('nombre', 'Sin categoría')
                    with st.expander(f"{categoria_nombre} - ${mov['monto']:,.2f} ({mov['frecuencia']})"):
                        st.write(f"Tipo: {mov['tipo']}")
                        st.write(f"Descripción: {mov['descripcion']}")
                        st.write(f"Fecha programada: {mov['fecha']}")
                        st.write(f"Fecha final: {mov['fecha_fin']}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Aprobar", key=f"aprobar_{mov['id']}"):
                                if aprobar_movimiento_recurrente(mov['id']):
                                    st.success("Movimiento aprobado exitosamente")
                                    st.rerun()
                        with col2:
                            if st.button("Rechazar", key=f"rechazar_{mov['id']}"):
                                if rechazar_movimiento_recurrente(mov['id']):
                                    st.success("Movimiento rechazado exitosamente")
                                    st.rerun()
                        with col3:
                            if st.button("Posponer", key=f"posponer_{mov['id']}"):
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
                # Preparar datos para el DataFrame
                datos_movimientos = []
                for mov in movimientos:
                    categoria_nombre = mov.get('categorias', {}).get('nombre', 'Sin categoría')
                    datos_movimientos.append({
                        'Fecha': mov['fecha'],
                        'Categoría': categoria_nombre,
                        'Monto': mov['monto'],
                        'Tipo': mov['tipo'],
                        'Descripción': mov['descripcion']
                    })
                
                df = pd.DataFrame(datos_movimientos)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay movimientos registrados")

        with tab4:
            st.subheader("Configuración de Perfil")
            
            # Obtener datos actuales del usuario
            datos_usuario = obtener_datos_usuario(st.session_state.usuario['id'])
            
            if datos_usuario:
                with st.form("actualizar_perfil"):
                    nuevo_nombre = st.text_input("Nombre", value=datos_usuario.get('nombre', ''))
                    nuevo_correo = st.text_input("Correo electrónico", value=datos_usuario.get('correo', ''))
                    
                    st.subheader("Cambiar Contraseña")
                    contraseña_actual = st.text_input("Contraseña actual", type="password")
                    nueva_contraseña = st.text_input("Nueva contraseña", type="password")
                    confirmar_contraseña = st.text_input("Confirmar nueva contraseña", type="password")
                    
                    if st.form_submit_button("Actualizar Perfil"):
                        # Aquí iría la lógica para actualizar el perfil
                        st.success("Perfil actualizado exitosamente")

        with tab5:
            st.subheader("Presupuestos")
            st.markdown("Define límites de gasto por categoría y periodo. Compara tus gastos reales con tus presupuestos.")
            
            with st.form("nuevo_presupuesto"):
                categoria = st.text_input("Categoría")
                monto = st.number_input("Monto límite", min_value=0.0, step=0.01)
                periodo = st.selectbox("Periodo", ["mensual", "semanal", "anual"])
                fecha_inicio = st.date_input("Fecha de inicio")
                fecha_fin = st.date_input("Fecha de fin")
                
                if st.form_submit_button("Guardar presupuesto"):
                    if crear_presupuesto(st.session_state.usuario['id'], categoria, monto, periodo, fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d')):
                        st.success("¡Presupuesto guardado!")
                    else:
                        st.error("Error al guardar presupuesto")
            
            st.markdown("---")
            st.subheader("Tus presupuestos")
            presupuestos = obtener_presupuestos_usuario(st.session_state.usuario['id'])
            
            if presupuestos:
                for p in presupuestos:
                    categoria_nombre = p.get('categorias', {}).get('nombre', 'Sin categoría')
                    gasto = gasto_acumulado(st.session_state.usuario['id'], categoria_nombre, p['fecha_inicio'], p['fecha_fin'])
                    
                    st.write(f"Categoría: {categoria_nombre}, Límite: ${p['monto_maximo']:,.2f}, Gasto actual: ${gasto:,.2f}")
                    
                    if gasto > p['monto_maximo']:
                        st.error("¡Has superado tu presupuesto!")
                    else:
                        st.info(f"Te quedan ${p['monto_maximo']-gasto:,.2f} en este periodo.")
            else:
                st.info("No tienes presupuestos registrados.")

    else:
        st.title("Bienvenido a Control Financiero")

        st.markdown("""
        Esta app ha sido creada con el objetivo de ayudarte a tener un **control más claro y sencillo de tus finanzas personales y en pareja**.

        🛠️ Actualmente, esta versión fue desarrollada usando:
        - **Python**
        - **Streamlit**
        - **Supabase (PostgreSQL)**

        ### ¿Cómo funciona?
        1. **Regístrate** con tus datos para crear tu cuenta.
        2. Una vez registrado, **inicia sesión** con esos mismos datos.
        3. Podrás registrar tus gastos, ingresos y visualizar resúmenes que te ayudarán a tomar mejores decisiones financieras.

        🚧 Este proyecto está en **construcción activa**. Próximamente se incorporarán mejoras, incluyendo **funcionalidades con Inteligencia Artificial** para análisis y recomendaciones más personalizadas.

        Tu feedback es bienvenido para seguir mejorando. ¡Gracias por ser parte del proceso!
        """)

if __name__ == "__main__":
    main()
