
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: green;'>💸 FINANZAS v3 – Panel General</h1>",
    unsafe_allow_html=True
)

# Inicializar dataset
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["fecha", "detalle", "monto", "tipo", "vencimiento", "prioridad"])

# Menú de navegación
selected = option_menu(
    menu_title=None,
    options=["Registrar", "Calendario", "Proyección", "Ahorros Auto"],
    icons=["pencil-fill", "calendar2-week", "graph-up", "piggy-bank-fill"],
    menu_icon="cast",
    orientation="horizontal",
)

st.write(f"Tab actual seleccionado: {selected}")

# --- Registrar nuevo movimiento ---
if selected == "Registrar":
    st.subheader("Registrar nuevo movimiento")

    with st.form("registro_form"):
        fecha = st.date_input("Fecha", value=datetime.today())
        detalle = st.text_input("Detalle")
        monto = st.number_input("Monto", step=100.0)
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        vencimiento = st.date_input("Fecha de vencimiento (si aplica)", value=datetime.today())
        prioridad = st.select_slider("Prioridad", options=["Baja", "Media", "Alta"])
        submitted = st.form_submit_button("Registrar")

        if submitted:
            nuevo = {
                "fecha": fecha,
                "detalle": detalle,
                "monto": monto,
                "tipo": tipo,
                "vencimiento": vencimiento,
                "prioridad": prioridad
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Movimiento registrado correctamente.")

    st.dataframe(st.session_state.df)

# --- Calendario ---
elif selected == "Calendario":
    st.subheader("Vista de calendario (modo visual en desarrollo)")
    df = st.session_state.df.copy()
    if not df.empty:
        df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")
        df["estado"] = df["vencimiento"].apply(lambda x: "Resuelto" if x < pd.Timestamp.today() else "Pendiente")
        st.dataframe(df[["detalle", "vencimiento", "prioridad", "estado"]])
    else:
        st.info("No hay datos registrados aún.")

# --- Proyección Anual ---
elif selected == "Proyección":
    st.subheader("Proyección de ingresos y egresos")
    df = st.session_state.df.copy()
    if not df.empty:
        df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M")
        resumen = df.groupby(["mes", "tipo"])["monto"].sum().unstack(fill_value=0)
        resumen["Balance"] = resumen.get("Ingreso", 0) - resumen.get("Gasto", 0)
        st.line_chart(resumen["Balance"])
        st.dataframe(resumen)
    else:
        st.info("Aún no hay proyecciones para mostrar.")

# --- Ahorros Auto ---
elif selected == "Ahorros Auto":
    st.subheader("Ahorros para el auto")
    df = st.session_state.df.copy()
    if not df.empty:
        auto_ahorros = df[(df["tipo"] == "Ingreso") & (df["detalle"].str.lower().str.contains("auto"))]
        total_auto = auto_ahorros["monto"].sum()
        st.metric("Total ahorrado para el auto", f"${total_auto:,.2f}")
        st.dataframe(auto_ahorros)
    else:
        st.info("No hay movimientos relacionados con el auto.")
