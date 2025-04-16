
import streamlit as st
import pandas as pd
from datetime import date
from streamlit_option_menu import option_menu
import os

# Inicialización
st.set_page_config(page_title="FINANZAS v3", layout="wide")
archivo = "finanzas.csv"

# Carga de datos
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# Navegación
with st.sidebar:
    seleccion = option_menu("FINANZAS v3 – Panel General", ["Registrar", "Calendario", "Proyección", "Ahorros Auto"],
                            icons=["pencil-fill", "calendar2-week", "graph-up", "piggy-bank"],
                            menu_icon="cash-coin", default_index=0, orientation="horizontal")

# 1. Registro de movimientos
if seleccion == "Registrar":
    st.subheader("Registrar Movimiento")
    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"], horizontal=True)
    fecha = st.date_input("Fecha", value=date.today())
    detalle = st.text_input("Detalle del movimiento")
    monto = st.number_input("Monto", min_value=0.0, step=100.0)

    vencimiento = st.date_input("Fecha de vencimiento (si aplica)", value=None)
    if tipo == "Gasto" and vencimiento:
        prioridad = st.radio("Prioridad", ["Alta", "Media", "Baja"], horizontal=True)
    else:
        prioridad = "-"

    if st.button("Registrar"):
        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "detalle": detalle,
            "monto": monto,
            "tipo": tipo,
            "vencimiento": vencimiento if vencimiento else "",
            "prioridad": prioridad
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv(archivo, index=False)
        st.success("Movimiento registrado correctamente.")

    st.dataframe(df)

# 2. Calendario
elif seleccion == "Calendario":
    st.subheader("Calendario de movimientos")

    hoy = pd.Timestamp("today").normalize()
    df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

    def color_fila(row):
        if pd.isna(row["vencimiento"]):
            return ""
        elif row["vencimiento"] < hoy:
            return "color: red"
        elif row["vencimiento"] == hoy:
            return "color: orange"
        elif row["vencimiento"] > hoy:
            return "color: green"
        return ""

    st.dataframe(df.style.applymap(color_fila, subset=["vencimiento"]))

# 3. Proyección mensual
elif seleccion == "Proyección":
    st.subheader("Proyección de ingresos y egresos")
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    proyeccion = df.groupby(["mes", "tipo"])["monto"].sum().unstack(fill_value=0)
    proyeccion["Balance"] = proyeccion.get("Ingreso", 0) - proyeccion.get("Gasto", 0)

    st.bar_chart(proyeccion)

# 4. Ahorros para el auto
elif seleccion == "Ahorros Auto":
    st.subheader("Fondo de Ahorro para el Auto")
    ahorros = df[(df["tipo"] == "Ingreso") & (df["detalle"].str.contains("auto", case=False))]
    total = ahorros["monto"].sum()
    st.metric("Total Ahorrado", f"${total:,.2f}")
    st.dataframe(ahorros)
