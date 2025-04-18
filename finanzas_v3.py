
#import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu

# --- Estilos de fondo ---
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

# --- Título principal ---
st.markdown("<h1 style='text-align: center;'>🚀 Finanzas v3 - 2025</h1>", unsafe_allow_html=True)




#BLOQUE 2:
menu = option_menu(
    menu_title=None,
    options=["Registrar Movimiento", "Calendario", "Ahorros para Auto"],
    icons=["pencil", "calendar", "car-front-fill"],
    menu_icon="cast",
    orientation="vertical",
    styles={
        "container": {"padding": "0!important", "background-color": "#FFD93D"},
        "icon": {"color": "black", "font-size": "24px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#f0b429"},
        "nav-link-selected": {"background-color": "#FFA500"},
    }
)

    


#BLOQUE 3 MENU 

if menu == "Registrar Movimiento":
    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"])

    if tipo == "Ingreso":
        st.subheader("Distribución automática de Ingresos (Estilo Millonarios)")
        ahorro_pct = st.slider("Ahorro (%)", 0, 100, 10)
        inversion_pct = st.slider("Inversión (%)", 0, 100, 10)
        auto_pct = st.slider("Fondo Auto (%)", 0, 100, 10)
        gastos_basicos_pct = st.slider("Gastos básicos (%)", 0, 100, 50)
        gustos_pct = st.slider("Gustos personales (%)", 0, 100, 20)
        emergencias_pct = st.slider("Emergencias (%)", 0, 100, 10)

        total_pct = ahorro_pct + inversion_pct + auto_pct + gastos_basicos_pct + gustos_pct + emergencias_pct
        if total_pct != 100:
            st.warning(f"⚠️ El total es {total_pct}%. ¡Debe ser 100%!")



#BLOQUE 4
if menu == "Registrar Movimiento":
    tipo = st.radio("Tipo de movimiento", ["Ingreso", "Gasto"])

    fecha = st.date_input("Fecha del movimiento")
    detalle = st.text_input("Detalle del movimiento")
    monto = st.number_input("Monto", min_value=0.0, step=100.0)

    # Solo pedir prioridad si es gasto
    prioridad = ""
    if tipo == "Gasto":
        prioridad = st.selectbox("Prioridad del gasto", ["Alta", "Media", "Baja"])

    if st.button("Registrar"):
        nuevo_registro = {
            "fecha": fecha,
            "detalle": detalle,
            "monto": monto,
            "tipo": tipo,
            "vencimiento": fecha if tipo == "Gasto" else "",
            "prioridad": prioridad if tipo == "Gasto" else ""
        }

        # Guardar en CSV
        if os.path.exists(archivo):
            df = pd.read_csv(archivo)
            df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        else:
            df = pd.DataFrame([nuevo_registro])

        df.to_csv(archivo, index=False)
        st.success("✅ Movimiento registrado correctamente.")




#BLOQUE 5 CALENDARIO

if menu == "Calendario":
    import streamlit_calendar as st_calendar
    from datetime import timedelta

    # Preparar eventos
    eventos = []

    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        for index, row in df.iterrows():
            evento = {
                "title": f"{row['detalle']} (${row['monto']})",
                "start": row['fecha'],
                "end": (pd.to_datetime(row['fecha']) + timedelta(days=1)).strftime('%Y-%m-%d')
            }
            eventos.append(evento)

    st.subheader("📅 Calendario de movimientos")
    st_calendar.calendar(events=eventos)




#BLOQUE 6 AUTO

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
        
        

#BLOQUE 7 MILLONARIOS
if menu == "Distribución Inteligente":
    st.subheader("📈 Distribución de Ingresos (Estilo Millonario)")

    ingreso = st.number_input("💵 Ingresar el monto del nuevo ingreso", min_value=0.0, step=100.0)

    if ingreso > 0:
        ahorro = ingreso * 0.10
        inversion = ingreso * 0.10
        fondo_auto = ingreso * 0.10
        gastos_basicos = ingreso * 0.50
        gustos = ingreso * 0.10
        emergencias = ingreso * 0.10

        st.markdown(f"**Ahorro:** ${ahorro:,.2f}")
        st.markdown(f"**Inversión:** ${inversion:,.2f}")
        st.markdown(f"**Fondo para Auto:** ${fondo_auto:,.2f}")
        st.markdown(f"**Gastos básicos:** ${gastos_basicos:,.2f}")
        st.markdown(f"**Gustos personales:** ${gustos:,.2f}")
        st.markdown(f"**Emergencias / Oportunidades:** ${emergencias:,.2f}")

        st.success("💎 Distribución realizada. ¡Mentalidad millonaria activada!")

