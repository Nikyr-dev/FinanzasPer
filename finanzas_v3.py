import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

# Configuración de la página
st.set_page_config(
    page_title="FINANZAS v3",
    page_icon=":moneybag:",
    layout="wide"
)

# Fondo amarillo positano
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

#BLOQUE 2:
# Nombre del archivo CSV
archivo = "finanzas.csv"

# Cargar datos desde el archivo si existe, sino crear DataFrame vacío
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])


#BLOQUE 3 MENU CIRCULAR
menu_html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
.menu-circle {
  position: relative;
  width: 300px;
  height: 300px;
  margin: 30px auto;
}
.menu-circle a {
  display: block;
  width: 60px;
  height: 60px;
  background: white;
  color: black;
  text-align: center;
  line-height: 60px;
  border-radius: 50%;
  position: absolute;
  transition: all 0.3s ease;
  font-size: 28px;
  text-decoration: none;
}
.menu-circle a:hover {
  transform: scale(1.3);
  background: #34a0a4;
  color: white;
}
.menu-circle a:nth-child(1) {
  top: 0;
  left: 120px;
}
.menu-circle a:nth-child(2) {
  top: 120px;
  right: 0;
}
.menu-circle a:nth-child(3) {
  bottom: 0;
  left: 120px;
}
.menu-circle a:nth-child(4) {
  top: 120px;
  left: 0;
}
</style>

<div class="menu-circle">
  <a href="#registrar" title="Registrar"><i class="fas fa-pen"></i></a>
  <a href="#calendario" title="Calendario"><i class="fas fa-calendar-alt"></i></a>
  <a href="#proyeccion" title="Proyección"><i class="fas fa-chart-line"></i></a>
  <a href="#ahorroauto" title="Ahorros Auto"><i class="fas fa-car-side"></i></a>
</div>
"""

components.html(menu_html, height=400)

#BLOQUE 4
# Sección: Registrar Movimiento
st.header("💸 Finanzas v3 - Panel General")
st.subheader("📝 Registrar Movimiento")

# Inputs para registrar
tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"], key="tipo")
fecha = st.date_input("Fecha del movimiento")
detalle = st.text_input("Detalle del movimiento")
monto = st.number_input("Monto", min_value=0.0, step=100.0)
vencimiento = st.date_input("Vencimiento (si corresponde)")
prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])

# Botón para guardar el movimiento
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

#BLOQUE 5
# Sección: Calendario de vencimientos
st.subheader("📅 Calendario de Vencimientos")

# Convertimos la columna vencimiento a tipo fecha
hoy = pd.Timestamp("today").normalize()
df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

# Mostrar movimientos según la fecha de vencimiento
for _, row in df.iterrows():
    fecha_venc = row["vencimiento"]
    if pd.isnull(fecha_venc):
        continue
    dias_restantes = (fecha_venc - hoy).days
    color = "🟥" if dias_restantes < 0 else "🟨" if dias_restantes <= 7 else "🟩"
    st.write(f"{color} {row['detalle']} - Vence: {fecha_venc.date()}")

#BLOQUE 6
# Sección: Proyección de Ingresos y Gastos
st.subheader("📈 Proyección de Ingresos y Gastos")

# Resumen general
resumen = df.groupby("tipo")["monto"].sum()
saldo = resumen.get("Ingreso", 0) - resumen.get("Gasto", 0)

# Mostrar resumen
st.write(f"**Total Ingresos:** ${resumen.get('Ingreso', 0):,.2f}")
st.write(f"**Total Gastos:** ${resumen.get('Gasto', 0):,.2f}")
st.write(f"**Saldo proyectado:** ${saldo:,.2f}")

# Gráfico de barras
st.bar_chart(resumen)
 
#BLOQUE 7
# Sección: Ahorros para el Auto
st.subheader("🚗 Fondo de Ahorros para el Auto")

# Aseguramos que 'detalle' sea string
df["detalle"] = df["detalle"].astype(str)

# Filtrar movimientos que mencionan "auto"
total_auto = df[df["detalle"].str.contains("auto", case=False, na=False)]["monto"].sum()

# Mostrar el total ahorrado
st.metric(label="Total Ahorrado para Auto", value=f"${total_auto:,.2f}")

