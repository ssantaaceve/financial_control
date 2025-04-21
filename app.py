import streamlit as st
import pandas as pd
import plotly.express as px

# Simulación de datos
if 'movimientos' not in st.session_state:
    st.session_state.movimientos = []

# Encabezado
st.title("💑 Finanzas en Pareja")
st.subheader("Control de ingresos y gastos compartidos")

# --- Formulario para nuevo movimiento ---
st.markdown("### ➕ Agregar nuevo movimiento")
with st.form("nuevo_movimiento"):
    fecha = st.date_input("Fecha")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    categoria = st.selectbox("Categoría", ["Comida", "Transporte", "Renta", "Ocio", "Salud", "Otro"])
    monto = st.number_input("Monto", min_value=0.0, step=100.0)
    autor = st.selectbox("¿Quién lo hizo?", ["Tatiana", "Sergio"])
    descripcion = st.text_input("Descripción")
    enviado = st.form_submit_button("Guardar")

    if enviado:
        st.session_state.movimientos.append({
            "fecha": fecha,
            "tipo": tipo,
            "categoria": categoria,
            "monto": monto,
            "autor": autor,
            "descripcion": descripcion
        })
        st.success("✅ Movimiento guardado")

# --- Mostrar datos si existen ---
if st.session_state.movimientos:
    df = pd.DataFrame(st.session_state.movimientos)

    # Resumen
    total_ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
    total_gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    saldo = total_ingresos - total_gastos

    st.markdown("### 📊 Resumen")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${total_ingresos:,.0f}")
    col2.metric("Gastos", f"${total_gastos:,.0f}")
    col3.metric("Saldo", f"${saldo:,.0f}")

    # Tabla
    st.markdown("### 📄 Historial de movimientos")
    st.dataframe(df)

    # Gráfico
    st.markdown("### 🧁 Gastos por categoría")
    gastos_df = df[df["tipo"] == "Gasto"]
    if not gastos_df.empty:
        fig = px.pie(gastos_df, names="categoria", values="monto", title="Distribución de gastos")
        st.plotly_chart(fig)
