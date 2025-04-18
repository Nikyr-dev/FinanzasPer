import streamlit as st
import pandas as pd
import os
from streamlit_calendar import calendar
from datetime import datetime

# Estilo de fondo
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
# Archivo de datos
archivo = "finanzas.csv"

# Cargar o crear DataFrame vacío
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# Nos aseguramos que las fechas estén bien como tipo datetime
if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")
    


#BLOQUE 3 MENU 

# Menú de navegación principal
menu = st.sidebar.radio(
    "Ir a...",
    ("Registrar Movimiento", "Calendario", "Proyección de Finanzas", "Ahorros para Auto")
)

st.title("💸 Finanzas v3 – 2025")



#BLOQUE 4
if menu == "Registrar Movimiento":
    st.header("📝 Registrar Movimiento")

    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"], key="tipo")
    fecha = st.date_input("Fecha del movimiento", value=datetime.today())
    detalle = st.text_input("Detalle del movimiento")
    monto = st.number_input("Monto", min_value=0.0, step=100.0)
    vencimiento = st.date_input("Vencimiento (si corresponde)", value=datetime.today())
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



#BLOQUE 5 CALENDARIO

if menu == "Calendario":
    st.header("📅 Calendario de Vencimientos")

    # Preparar eventos para el calendario
    eventos = []
    if not df.empty:
        for _, row in df.iterrows():
            if pd.isnull(row["vencimiento"]):
                continue
            color = "#FF6961" if (row["vencimiento"] < datetime.now()) else "#FFD93D"
            if row["tipo"] == "Ingreso":
                color = "#77DD77"

            eventos.append({
                "title": f"{row['tipo']}: {row['detalle']} - ${row['monto']}",
                "start": row["vencimiento"].strftime("%Y-%m-%d"),
                "color": color
            })

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": True,
        "locale": "es",
    }

    calendar_component = calendar(events=eventos, options=calendar_options)
    
    # Registrar nuevo movimiento al hacer click en día vacío
    if calendar_component.get("select"):
        fecha_seleccionada = calendar_component["select"]["start"]
        st.success(f"Seleccionaste el {fecha_seleccionada}")

        with st.form("nuevo_movimiento"):
            tipo_nuevo = st.radio("Tipo", ["Ingreso", "Gasto"], key="nuevo_tipo")
            detalle_nuevo = st.text_input("Detalle")
            monto_nuevo = st.number_input("Monto", min_value=0.0, step=100.0, key="monto_nuevo")
            prioridad_nuevo = st.selectbox("Prioridad", ["Alta", "Media", "Baja"], key="prioridad_nuevo")
            submit_nuevo = st.form_submit_button("Registrar nuevo movimiento")

            if submit_nuevo:
                nuevo_evento = {
                    "fecha": fecha_seleccionada,
                    "detalle": detalle_nuevo,
                    "monto": monto_nuevo,
                    "tipo": tipo_nuevo,
                    "vencimiento": fecha_seleccionada,
                    "prioridad": prioridad_nuevo
                }
                df = pd.concat([df, pd.DataFrame([nuevo_evento])], ignore_index=True)
                df.to_csv(archivo, index=False)
                st.success("✅ Nuevo movimiento registrado correctamente.")



#BLOQUE 6
if menu == "Proyección de Finanzas":
    st.header("📈 Proyección de Ingresos y Gastos")

    if not df.empty:
        resumen = df.groupby("tipo")["monto"].sum()
        saldo = resumen.get("Ingreso", 0) - resumen.get("Gasto", 0)

        st.write(f"**Total Ingresos:** ${resumen.get('Ingreso', 0):,.2f}")
        st.write(f"**Total Gastos:** ${resumen.get('Gasto', 0):,.2f}")
        st.write(f"**Saldo Proyectado:** ${saldo:,.2f}")

        st.bar_chart(resumen)
    else:
        st.info("Todavía no hay movimientos cargados para proyectar.")

 
 
 
#BLOQUE 7 AUTO
if menu == "Ahorros para Auto":
    st.header("🚗 Ahorros para el Auto")

    if not df.empty:
        # Aseguramos que 'detalle' sea string
        df["detalle"] = df["detalle"].astype(str)

        # Filtrar movimientos que mencionen "auto"
        ahorros_auto = df[df["detalle"].str.contains("auto", case=False, na=False)]
        total_auto = ahorros_auto["monto"].sum()

        st.metric(label="Total Ahorrado para el Auto", value=f"${total_auto:,.2f}")

        if not ahorros_auto.empty:
            st.subheader("Detalle de aportes:")
            for _, row in ahorros_auto.iterrows():
                st.write(f"🔹 {row['fecha'].date()} - {row['detalle']} - ${row['monto']:,.2f}")
    else:
        st.info("Todavía no hay movimientos relacionados al Auto.")


