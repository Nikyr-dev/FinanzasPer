import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu

# BLOQUE 1: Configuración inicial
st.set_page_config(page_title="Finanzas v3", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #FFD93D;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# BLOQUE 2: Nombre del archivo CSV
archivo = "finanzas.csv"

# BLOQUE 3: Cargar datos existentes si hay
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# BLOQUE 4: Menú circular
with st.sidebar:
    menu = option_menu(
        "Ir a...", 
        ["Registrar Movimiento", "Calendario", "Ahorros para Auto", "Distribución Inteligente"], 
        icons=["pencil", "calendar", "car-front-fill", "graph-up"],
        menu_icon="cast", 
        default_index=0,
        orientation="vertical"
    )

# BLOQUE 5: Registro de movimientos
if menu == "Registrar Movimiento":
    st.header("📝 Registrar Movimiento")

    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"])
    fecha = st.date_input("Fecha del movimiento")
    detalle = st.text_input("Detalle")
    monto = st.number_input("Monto", min_value=0.0, step=10.0)
    vencimiento = st.date_input("Fecha de vencimiento (si aplica)", value=None)
    
    prioridad = ""
    if tipo == "Gasto":
        prioridad = st.radio("Prioridad", ["Alta", "Media", "Baja"])
    
    if st.button("Registrar"):
        nuevo_registro = {
            "fecha": fecha,
            "detalle": detalle,
            "monto": monto,
            "tipo": tipo,
            "vencimiento": vencimiento if vencimiento else "",
            "prioridad": prioridad
        }
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        df.to_csv(archivo, index=False)
        st.success("✅ Movimiento registrado correctamente.")

# BLOQUE 6: Calendario
if menu == "Calendario":
    import streamlit_calendar as st_calendar
    from datetime import timedelta

    eventos = []
    if os.path.exists(archivo):
        for index, row in df.iterrows():
            evento = {
                "title": f"{row['detalle']} (${row['monto']})",
                "start": row['fecha'],
                "end": (pd.to_datetime(row['fecha']) + timedelta(days=1)).strftime('%Y-%m-%d')
            }
            eventos.append(evento)

    st.header("📅 Calendario de movimientos")
    st_calendar.calendar(events=eventos)

# BLOQUE 7: Ahorros para Auto
if menu == "Ahorros para Auto":
    st.header("🚗 Fondo de Ahorro para el Auto")
    if os.path.exists(archivo):
        df_auto = df[df["detalle"].str.contains("auto", case=False, na=False)]
        total_ahorro_auto = df_auto["monto"].sum()
        st.metric(label="Total Ahorro Acumulado", value=f"${total_ahorro_auto:,.2f}")
    else:
        st.warning("⚠️ No hay datos disponibles todavía.")

# BLOQUE 8: Distribución Inteligente estilo millonario
if menu == "Distribución Inteligente":
    st.header("💎 Distribución Automática de Ingresos (Estilo Millonario)")

    ingreso = st.number_input("Ingresá tu nuevo ingreso 💵", min_value=0.0, step=100.0)

    if ingreso > 0:
        ahorro = ingreso * 0.10
        inversion = ingreso * 0.10
        fondo_auto = ingreso * 0.10
        gastos_basicos = ingreso * 0.50
        gustos = ingreso * 0.10
        emergencias = ingreso * 0.10

        st.success("✅ Ingreso procesado bajo mentalidad millonaria:")
        st.markdown(f"- **Ahorro:** ${ahorro:,.2f}")
        st.markdown(f"- **Inversión:** ${inversion:,.2f}")
        st.markdown(f"- **Fondo Auto:** ${fondo_auto:,.2f}")
        st.markdown(f"- **Gastos Básicos:** ${gastos_basicos:,.2f}")
        st.markdown(f"- **Gustos Personales:** ${gustos:,.2f}")
        st.markdown(f"- **Emergencias/Oportunidades:** ${emergencias:,.2f}")
