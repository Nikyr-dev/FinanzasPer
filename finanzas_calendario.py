
import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(page_title="FINANZAS - Calendario", page_icon="📅", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #2196F3;'>📅 Calendario de Finanzas</h1>",
    unsafe_allow_html=True
)

archivo_datos = "movimientos_financieros.csv"
try:
    df = pd.read_csv(archivo_datos, parse_dates=["fecha", "vencimiento"])
except:
    df = pd.DataFrame(columns=["fecha", "tipo", "categoría", "detalle", "monto", "vencimiento", "prioridad", "resuelto"])

df["vencimiento"] = pd.to_datetime(df["vencimiento"], errors="coerce")

# Seleccionar mes y año
hoy = datetime.date.today()
año = st.selectbox("Año", list(range(hoy.year - 1, hoy.year + 2)), index=1)
mes = st.selectbox("Mes", list(calendar.month_name)[1:], index=hoy.month - 1)
mes_num = list(calendar.month_name).index(mes)

# Filtrar movimientos del mes seleccionado
inicio_mes = datetime.date(año, mes_num, 1)
fin_mes = datetime.date(año, mes_num, calendar.monthrange(año, mes_num)[1])
df_mes = df[(df["vencimiento"].dt.date >= inicio_mes) & (df["vencimiento"].dt.date <= fin_mes)]

# Renderizar calendario
st.markdown(f"### {mes} {año}")

dias_mes = calendar.monthrange(año, mes_num)[1]
calendario_html = "<table style='width: 100%; border-collapse: collapse;'>"
calendario_html += "<tr>" + "".join(f"<th>{d}</th>" for d in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]) + "</tr>"

primero_dia_semana = (datetime.date(año, mes_num, 1).weekday() + 1) % 7
semana = [""] * primero_dia_semana

for dia in range(1, dias_mes + 1):
    fecha_actual = datetime.date(año, mes_num, dia)
    movimientos_dia = df_mes[df_mes["vencimiento"].dt.date == fecha_actual]

    color = "#FFFFFF"
    if not movimientos_dia.empty:
        if (movimientos_dia["resuelto"] == "Sí").all():
            color = "#C8E6C9"  # verde
        elif fecha_actual < hoy:
            color = "#FFCDD2"  # rojo
        elif (fecha_actual - hoy).days <= 7:
            color = "#FFF9C4"  # amarillo

    semana.append(f"<td style='background-color:{color}; padding: 10px; border: 1px solid #CCC; text-align: center;'>{dia}</td>")

    if len(semana) == 7:
        calendario_html += "<tr>" + "".join(semana) + "</tr>"
        semana = []

if semana:
    semana += [""] * (7 - len(semana))
    calendario_html += "<tr>" + "".join(semana) + "</tr>"

calendario_html += "</table>"
st.markdown(calendario_html, unsafe_allow_html=True)
