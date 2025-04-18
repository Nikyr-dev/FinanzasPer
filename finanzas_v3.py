
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

# --- Control de gasto diario ---
st.subheader("Control de gasto diario")

# Estimar cuánto queda por gastar en el mes
hoy = pd.Timestamp.today()
fin_de_mes = pd.Timestamp(hoy.year, hoy.month, 28) + pd.offsets.MonthEnd(0)
dias_restantes = (fin_de_mes - hoy).days + 1

ingresos_totales = df[(df["tipo"] == "Ingreso")]["monto"].sum()
gastos_totales = df[(df["tipo"] == "Gasto")]["monto"].sum()
balance_actual = ingresos_totales - gastos_totales

# Estimación de gasto diario posible
if dias_restantes > 0:
    disponible_diario = balance_actual / dias_restantes
else:
    disponible_diario = 0

st.metric("Saldo disponible proyectado", f"${balance_actual:,.2f}")
st.metric("Promedio diario para no entrar en déficit", f"${disponible_diario:,.2f}")

# Alerta de sobre gasto (último gasto registrado)
if not df.empty and df.iloc[-1]["tipo"] == "Gasto":
    gasto_reciente = df.iloc[-1]["monto"]
    if gasto_reciente > disponible_diario:
        st.warning(f"¡Alerta! El último gasto (${gasto_reciente}) supera tu promedio diario disponible.")
    else:
        st.success("El gasto está dentro del rango saludable.")

# Navegación
with st.sidebar:
    seleccion = option_menu("FINANZAS v3 – Panel General", ["Registrar", "Calendario", "Proyección", "Ahorros Auto"],
                            icons=["pencil-fill", "calendar2-week", "graph-up", "piggy-bank"],
                            menu_icon="cash-coin", default_index=0, orientation="horizontal")

# 1. Registro de movimientos
if seleccion == "Registrar":

# --- Distribución automática de ingresos estilo millonario ---
if seleccion == "Registrar" and tipo == "Ingreso":
    st.markdown    ("### Distribución automática del ingreso")

    # Porcentajes ajustables
    ahorro_pct = st.slider("Ahorro (%)", 0, 100, 10)
    inversion_pct = st.slider("Inversión (%)", 0, 100, 10)
    auto_pct = st.slider("Fondo para auto (%)", 0, 100, 10)
    gastos_basicos_pct = st.slider("Gastos básicos (%)", 0, 100, 50)
    gustos_pct = st.slider("Gustos personales (%)", 0, 100, 10)
    emergencia_pct = st.slider("Emergencias / Oportunidad (%)", 0, 100, 10)

    total_pct = ahorro_pct + inversion_pct + auto_pct + gastos_basicos_pct + gustos_pct + emergencia_pct
    if total_pct != 100:
        st.error(f"La suma de los porcentajes debe ser 100%. Actualmente suma {total_pct}%.")
    else:
        if st.button("Registrar ingreso con distribución"):
            partes = {
                "Ahorro": ahorro_pct,
                "Inversión": inversion_pct,
                "Auto": auto_pct,
                "Gastos básicos": gastos_basicos_pct,
                "Gustos": gustos_pct,
                "Emergencia": emergencia_pct
            }

            registros = []
            for categoria, pct in partes.items():
                registros.append({
                    "fecha": fecha,
                    "detalle": f"Ingreso - {categoria}",
                    "monto": monto * pct / 100,
                    "tipo": "Ingreso",
                    "vencimiento": "",
                    "prioridad": "-"
                })

            df = pd.concat([df, pd.DataFrame(registros)], ignore_index=True)
            df.to_csv(archivo, index=False)
            st.success("Ingreso registrado y distribuido correctamente.")

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
