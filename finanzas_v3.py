import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# ---- CONFIGURACIÓN GENERAL ----
st.set_page_config(page_title="Finanzas v3 - 2025", page_icon="💸", layout="wide")

# Fondo amarillo positano
st.markdown(
    '''
    <style>
    body {
        background-color: #FFD93D;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# ---- BLOQUE 2: Gestión del archivo CSV ----
archivo = "finanzas.csv"

if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# ---- BLOQUE 3.1: Registro de movimientos ----
st.title("💸 Finanzas v3 - Panel General")

secciones = ["Registrar Movimiento", "Calendario", "Ahorros Auto"]
seleccion = st.sidebar.radio("Ir a...", secciones)

if seleccion == "Registrar Movimiento":
    st.header("Registrar Nuevo Movimiento")

    tipo = st.radio("Tipo de movimiento", ("Ingreso", "Gasto"))

    fecha = st.date_input("Fecha del movimiento")
    detalle = st.text_input("Detalle")
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")

    vencimiento = st.date_input("Fecha de vencimiento (si aplica)")
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])

    if tipo == "Ingreso":
        st.subheader("📈 Distribución automática del ingreso")

        ahorro_pct = st.slider("Ahorro (%)", 0, 100, 10)
        inversion_pct = st.slider("Inversión (%)", 0, 100, 10)
        auto_pct = st.slider("Fondo para Auto (%)", 0, 100, 10)
        gastos_basicos_pct = st.slider("Gastos básicos (%)", 0, 100, 50)
        gustos_pct = st.slider("Gustos personales (%)", 0, 100, 20)
        emergencia_pct = st.slider("Emergencias / Oportunidad (%)", 0, 100, 10)

        total_pct = ahorro_pct + inversion_pct + auto_pct + gastos_basicos_pct + gustos_pct + emergencia_pct

        if total_pct != 100:
            st.error(f"La suma de porcentajes es {total_pct}%. ¡Debe ser exactamente 100%!")
        else:
            st.success("✅ ¡Distribución lista para aplicar!")

    if st.button("Registrar"):
        nuevo_mov = pd.DataFrame({
            "fecha": [fecha],
            "detalle": [detalle],
            "monto": [monto],
            "tipo": [tipo],
            "vencimiento": [vencimiento],
            "prioridad": [prioridad]
        })

        df = pd.concat([df, nuevo_mov], ignore_index=True)
        
        # ---- BLOQUE 5.1: Guardado automático ----
        df.to_csv(archivo, index=False)
        st.success("✅ Movimiento guardado exitosamente.")

elif seleccion == "Calendario":
    st.header("📅 Calendario (en desarrollo)")

elif seleccion == "Ahorros Auto":
    st.header("🚗 Fondo de Ahorro para el Auto")

    if "auto" in df["detalle"].astype(str).str.lower().values:
        total_auto = df[df["detalle"].str.contains("auto", case=False, na=False)]["monto"].sum()
        st.metric(label="💰 Total Fondo Auto", value=f"${total_auto:,.2f}")
    else:
        st.info("Todavía no hay registros destinados al ahorro para auto.")
