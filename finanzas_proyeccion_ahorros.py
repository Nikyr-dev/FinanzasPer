
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="FINANZAS - Proyección Anual", page_icon="📊", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #3F51B5;'>📊 Cronograma Anual + Ahorros para el Auto</h1>",
    unsafe_allow_html=True
)

archivo_datos = "movimientos_financieros.csv"
try:
    df = pd.read_csv(archivo_datos, parse_dates=["fecha", "vencimiento"])
except:
    df = pd.DataFrame(columns=["fecha", "tipo", "categoría", "detalle", "monto", "vencimiento", "prioridad", "resuelto"])

df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

df["mes"] = df["vencimiento"].dt.strftime("%b")  # Abreviado: Jan, Feb, etc.
df["año"] = df["vencimiento"].dt.year

año_actual = datetime.datetime.now().year
df_anual = df[df["año"] == año_actual]

# Tabla de resumen mensual
st.subheader("📆 Proyección por mes")
proyeccion = df_anual.groupby(["mes", "tipo"])["monto"].sum().unstack(fill_value=0).reindex(index=[
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])
proyeccion["Balance"] = proyeccion.get("Ingreso", 0) - (
    proyeccion.get("Egreso inmediato", 0) + proyeccion.get("Egreso futuro (tarjeta o deuda)", 0)
)
st.dataframe(proyeccion.style.format("${:,.2f}"), use_container_width=True)

# Sección Ahorros para el Auto
st.subheader("🚗 Ahorros para el Auto")

if "ahorro_auto" not in st.session_state:
    st.session_state.ahorro_auto = 0.0

st.markdown(f"**Saldo actual en el fondo:** ${st.session_state.ahorro_auto:,.2f}")
monto_aporte = st.number_input("¿Cuánto querés aportar hoy al fondo?", min_value=0.0, step=500.0)

if st.button("Agregar al fondo de ahorro"):
    st.session_state.ahorro_auto += monto_aporte
    st.success(f"Se agregaron ${monto_aporte:,.2f} al fondo.")
