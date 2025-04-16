
import streamlit as st
import pandas as pd
import datetime
from pathlib import Path

st.set_page_config(page_title="FINANZAS", page_icon="💰", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50; font-size: 50px;'>💰 FINANZAS</h1>",
    unsafe_allow_html=True
)

archivo_datos = "movimientos_financieros.csv"

if Path(archivo_datos).exists():
    df = pd.read_csv(archivo_datos)
else:
    df = pd.DataFrame(columns=["fecha", "tipo", "categoría", "detalle", "monto", "vencimiento", "prioridad"])

st.subheader("Registrar nuevo movimiento")

col1, col2 = st.columns(2)
with col1:
    tipo = st.selectbox("Tipo", ["Ingreso", "Egreso inmediato", "Egreso futuro (tarjeta o deuda)"])
    fecha = st.date_input("Fecha del movimiento", datetime.date.today())
with col2:
    categoria = st.selectbox("Categoría", ["Sueldo", "Servicios", "Comida", "Transporte", "Salidas", "Tarjeta", "Otros"])
    monto = st.number_input("Monto", min_value=0.0, step=100.0)

detalle = st.text_input("Detalle (opcional)")
vencimiento = None
prioridad = None

if tipo == "Egreso futuro (tarjeta o deuda)":
    vencimiento = st.date_input("Fecha de vencimiento", datetime.date.today() + datetime.timedelta(days=30))
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])

if st.button("Agregar"):
    nuevo = pd.DataFrame([{
        "fecha": fecha,
        "tipo": tipo,
        "categoría": categoria,
        "detalle": detalle,
        "monto": monto,
        "vencimiento": vencimiento if vencimiento else "",
        "prioridad": prioridad if prioridad else ""
    }])
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(archivo_datos, index=False)
    st.success("Movimiento registrado.")

st.subheader("Historial de movimientos")
if df.empty:
    st.info("Aún no se registraron movimientos.")
else:
    df["fecha"] = pd.to_datetime(df["fecha"])
    st.dataframe(df.sort_values("fecha", ascending=False), use_container_width=True)

# Cálculo de balances
st.subheader("Resumen general")

ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
egresos_inmediatos = df[df["tipo"] == "Egreso inmediato"]["monto"].sum()
egresos_futuros = df[df["tipo"] == "Egreso futuro (tarjeta o deuda)"]["monto"].sum()
balance = ingresos - egresos_inmediatos

st.markdown(f"**Total ingresado:** ${ingresos:,.2f}")
st.markdown(f"**Gastado hasta hoy:** ${egresos_inmediatos:,.2f}")
st.markdown(f"**Balance disponible:** ${balance:,.2f}")
st.markdown(f"**Comprometido a futuro (tarjeta/deuda):** ${egresos_futuros:,.2f}")

# Alertas por vencimientos cercanos
hoy = datetime.date.today()
df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

proximos = df[
    (df["tipo"] == "Egreso futuro (tarjeta o deuda)") &
    (df["vencimiento"].notna()) &
    (df["vencimiento"].dt.date <= hoy + datetime.timedelta(days=7))
]

if not proximos.empty:
    st.warning("⚠️ Próximos vencimientos en 7 días:")
    for _, row in proximos.iterrows():
        st.markdown(f"- {row['detalle']} (${row['monto']}) vence el {row['vencimiento'].date()} (Prioridad: {row['prioridad']})")
