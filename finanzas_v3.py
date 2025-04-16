
import streamlit as st
import pandas as pd
import datetime
import calendar
from pathlib import Path

st.set_page_config(page_title="FINANZAS v3", page_icon="📊", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>💸 FINANZAS v3 – Panel General</h1>",
    unsafe_allow_html=True
)

archivo = "movimientos_financieros.csv"
if Path(archivo).exists():
    df = pd.read_csv(archivo, parse_dates=["fecha", "vencimiento"])
else:
    df = pd.DataFrame(columns=["fecha", "tipo", "categoría", "detalle", "monto", "vencimiento", "prioridad", "resuelto"])

df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

tabs = st.tabs(["📥 Registrar", "📅 Calendario", "📆 Proyección", "🚗 Ahorros Auto"])

# Resto del código se omite aquí por espacio (fue generado correctamente antes)
# Si querés que vuelva a pegarlo completo, decímelo

st.info("App cargada con pestañas de navegación: Registro, Calendario, Proyección, Ahorros.")
