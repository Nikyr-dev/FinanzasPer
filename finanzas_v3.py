import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title="FINANZAS v3", page_icon=":moneybag:", layout="wide")

st.markdown("<h1 style='text-align: center; color: green;'>💸 FINANZAS v3 – Panel General</h1>", unsafe_allow_html=True)

# Archivo CSV
archivo = "finanzas.csv"

# Cargar datos
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# Menú de navegación
seleccion = option_menu(
    menu_title=None,
    options=["Registrar", "Calendario", "Proyección", "Ahorros Auto"],
    icons=["pencil-fill", "calendar2-week", "graph-up", "piggy-bank"],
    orientation="horizontal",
)

# 1. Registro de movimientos
if seleccion == "Registrar":
    st.subheader("Registrar nuevo movimiento")

    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"])
    fecha = st.date_input("Fecha del movimiento")
    detalle = st.text_input("Detalle o Descripción")
    monto = st.number_input("Monto", min_value=0.0, step=100.0)
    vencimiento = st.date_input("Fecha de vencimiento (si aplica)")
    
    # Distribución automática de ingresos estilo millonario
    if tipo == "Ingreso":
        st.markdown("### Distribución automática del ingreso")
        
        ahorro_pct = st.slider("Ahorro (%)", 0, 100, 10)
        inversion_pct = st.slider("Inversión (%)", 0, 100, 10)
        auto_pct = st.slider("Fondo para auto (%)", 0, 100, 10)
        gastos_basicos_pct = st.slider("Gastos básicos (%)", 0, 100, 30)
        gustos_pct = st.slider("Gustos personales (%)", 0, 100, 30)
        emergencia_pct = st.slider("Emergencias / Oportunidad (%)", 0, 100, 10)

        total_pct = ahorro_pct + inversion_pct + auto_pct + gastos_basicos_pct + gustos_pct + emergencia_pct

        if total_pct != 100:
            st.error("La suma de los porcentajes debe ser 100%. Actualmente suma: {}%".format(total_pct))
    
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])

    if st.button("Registrar"):
        nuevo = {
            "fecha": fecha,
            "detalle": detalle,
            "monto": monto,
            "tipo": tipo,
            "vencimiento": vencimiento,
            "prioridad": prioridad
        }
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_csv(archivo, index=False)
        st.success("✅ Movimiento registrado correctamente.")

    st.dataframe(df)

# 2. Calendario
if seleccion == "Calendario":
    st.subheader("Calendario de vencimientos")
    hoy = pd.Timestamp("today").normalize()
    df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")
    
    for _, row in df.iterrows():
        fecha_venc = row["vencimiento"]
        if pd.isnull(fecha_venc):
            continue
        dias_restantes = (fecha_venc - hoy).days
        color = "🟥" if dias_restantes < 0 else "🟨" if dias_restantes <= 7 else "🟩"
        st.write(f"{color} {row['detalle']} - {fecha_venc.date()}")

# 3. Proyección
if seleccion == "Proyección":
    st.subheader("Proyección de ingresos y egresos")
    resumen = df.groupby("tipo")["monto"].sum()
    saldo = resumen.get("Ingreso", 0) - resumen.get("Gasto", 0)

    st.write(f"**Total Ingresos:** ${resumen.get('Ingreso', 0):,.2f}")
    st.write(f"**Total Gastos:** ${resumen.get('Gasto', 0):,.2f}")
    st.write(f"**Saldo proyectado:** ${saldo:,.2f}")

    st.bar_chart(resumen)

# 4. Ahorros Auto
if seleccion == "Ahorros Auto":
    st.subheader("Fondo de ahorro para el auto")
    total_auto = df[df["detalle"].str.contains("auto", case=False, na=False)]["monto"].sum()
    st.metric(label="Total Ahorrado para Auto", value=f"${total_auto:,.2f}")
