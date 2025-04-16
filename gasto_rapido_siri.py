
import streamlit as st
import pandas as pd
import datetime
from pathlib import Path

st.set_page_config(page_title="Registrar Gasto Rápido", page_icon="⚡", layout="centered")

st.markdown(
    "<h2 style='text-align: center; color: #FF5722;'>⚡ Registro Rápido de Gasto</h2>",
    unsafe_allow_html=True
)

archivo = "registro_rapido.csv"

if Path(archivo).exists():
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto"])

detalle = st.text_input("¿Qué compraste?")
monto = st.number_input("¿Cuánto gastaste?", min_value=0.0, step=100.0)

if st.button("Registrar"):
    nuevo = pd.DataFrame([{
        "fecha": datetime.date.today(),
        "detalle": detalle,
        "monto": monto
    }])
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(archivo, index=False)
    st.success(f"Se registró: {detalle} por ${monto:,.2f}")

st.divider()
st.markdown("### Últimos gastos registrados")
if df.empty:
    st.info("Todavía no hay registros.")
else:
    st.dataframe(df.tail(5), use_container_width=True)
