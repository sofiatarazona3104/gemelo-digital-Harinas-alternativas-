
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Gemelo Digital de Harinas", page_icon="🧪", layout="wide")

st.title("🧪 Gemelo Digital de Harinas")
st.caption("Versión 0.1 enfocada en el comportamiento experimental de trigo, lenteja y arroz.")

humedad = pd.DataFrame({
    "Tiempo (min)": list(range(1,11)),
    "Lenteja":[3.06,4.54,5.62,6.41,7.10,7.69,8.19,8.68,8.88,9.27],
    "Arroz":[3.40,5.00,6.10,6.90,7.40,7.80,8.20,8.40,8.60,8.80],
    "Trigo":[4.16,6.74,8.49,9.70,10.53,11.26,11.73,12.10,12.28,12.47]
})

ph = pd.DataFrame({
    "Harina":["Lenteja"]*3+["Arroz"]*3+["Trigo"]*3,
    "Réplica":[1,2,3]*3,
    "pH inicial":[5.22,5.35,5.23,5.63,5.75,5.71,5.35,5.40,5.42],
    "NaOH (mL)":[1.8,2.0,4.4,0.2,0.4,0.2,0.4,0.4,0.4],
    "pH final":[8.04,8.03,8.00,8.25,8.40,8.00,8.00,8.09,8.07]
})

color = pd.DataFrame({
    "Harina":["Lenteja"]*3+["Arroz"]*3,
    "Réplica":[1,2,3]*2,
    "L*":[42.05,52.08,38.24,51.51,39.68,44.13],
    "a*":[0.00,-0.58,1.54,0.10,0.03,-0.12],
    "b*":[14.31,15.39,13.84,8.29,6.99,7.90]
})

caa = pd.DataFrame({
    "Harina":["Trigo"]*3+["Lenteja"]*3+["Arroz"]*3,
    "Réplica":[1,2,3]*3,
    "Tubo vacío (g)":[6.643]*9,
    "Muestra (g)":[1.0]*9,
    "Tubo + sedimento (g)":[10.0,10.0,9.0,11.0,8.0,8.0,10.0,10.0,9.0]
})

caac = pd.DataFrame({
    "Harina":["Trigo"]*3+["Lenteja"]*3+["Arroz"]*3,
    "Réplica":[1,2,3]*3,
    "Tubo vacío (g)":[6.643]*9,
    "Muestra (g)":[1.0]*9,
    "Tubo + sedimento (g)":[10.0,10.0,10.0,10.0,10.0,9.0,9.0,9.0,10.0]
})

tabs = st.tabs(["Resumen","Humedad","pH y acidez","CIELAB","Tecnofuncionales","Progreso"])

with tabs[0]:
    st.subheader("Resumen")
    prom_ph = ph.groupby("Harina")["pH inicial"].mean()
    c1,c2,c3 = st.columns(3)
    with c1:
        st.metric("Trigo — humedad","12.47 %")
        st.metric("Trigo — pH",f"{prom_ph['Trigo']:.2f}")
    with c2:
        st.metric("Lenteja — humedad","9.27 %")
        st.metric("Lenteja — pH",f"{prom_ph['Lenteja']:.2f}")
    with c3:
        st.metric("Arroz — humedad","8.80 %")
        st.metric("Arroz — pH",f"{prom_ph['Arroz']:.2f}")
    st.warning("CAA, CAAc, IAA, ISA y cenizas aún requieren validación experimental.")

with tabs[1]:
    st.subheader("Comportamiento de humedad")
    hum_long = humedad.melt(id_vars="Tiempo (min)", var_name="Harina", value_name="Humedad (%)")
    fig = px.line(hum_long, x="Tiempo (min)", y="Humedad (%)", color="Harina", markers=True)
    st.plotly_chart(fig, width="stretch")
    st.dataframe(humedad, width="stretch", hide_index=True)
    st.info("Entre los minutos 9 y 10 aún hubo variación: lenteja +0.39, arroz +0.20 y trigo +0.19 puntos porcentuales.")

with tabs[2]:
    st.subheader("pH y acidez titulable")
    fig = px.box(ph, x="Harina", y="pH inicial", points="all", title="pH inicial por harina")
    st.plotly_chart(fig, width="stretch")
    st.dataframe(ph, width="stretch", hide_index=True)
    fig2 = px.bar(ph, x="Harina", y="NaOH (mL)", color="Réplica", barmode="group", title="Consumo de NaOH")
    st.plotly_chart(fig2, width="stretch")
    st.warning("La réplica 3 de lenteja (4.4 mL) debe revisarse antes de cerrar el análisis.")

with tabs[3]:
    st.subheader("Color CIELAB")
    fig = px.scatter_3d(color, x="L*", y="a*", z="b*", color="Harina", symbol="Harina",
                        hover_data=["Réplica"], title="Distribución CIELAB 3D")
    fig.update_traces(marker=dict(size=7))
    st.plotly_chart(fig, width="stretch")
    resumen = color.groupby("Harina")[["L*","a*","b*"]].agg(["mean","std"]).round(2)
    st.dataframe(resumen, width="stretch")
    st.caption("Falta incorporar trigo cuando se obtengan sus tres lecturas CIELAB.")

with tabs[4]:
    st.subheader("Tecnofuncionales")
    st.warning("Los cálculos de CAA y CAAc son provisionales porque algunos pesos fueron registrados sin decimales.")
    st.markdown("### CAA")
    caa_edit = st.data_editor(caa, width="stretch", hide_index=True, key="caa")
    caa_edit["Sedimento húmedo (g)"] = caa_edit["Tubo + sedimento (g)"] - caa_edit["Tubo vacío (g)"]
    caa_edit["CAA (g/g)"] = (caa_edit["Sedimento húmedo (g)"] - caa_edit["Muestra (g)"]) / caa_edit["Muestra (g)"]
    st.dataframe(caa_edit.round(3), width="stretch", hide_index=True)

    st.markdown("### CAAc")
    caac_edit = st.data_editor(caac, width="stretch", hide_index=True, key="caac")
    caac_edit["Sedimento con aceite (g)"] = caac_edit["Tubo + sedimento (g)"] - caac_edit["Tubo vacío (g)"]
    caac_edit["CAAc (g/g)"] = (caac_edit["Sedimento con aceite (g)"] - caac_edit["Muestra (g)"]) / caac_edit["Muestra (g)"]
    st.dataframe(caac_edit.round(3), width="stretch", hide_index=True)

    st.markdown("### IAA / ISA")
    st.info("Déjalos como pendientes hasta verificar taras de recipientes y cápsulas.")

    st.markdown("### Capacidad de hinchamiento")
    plantilla = pd.DataFrame({
        "Harina":["Trigo"]*3+["Lenteja"]*3+["Arroz"]*3,
        "Réplica":[1,2,3]*3,
        "Muestra (g)":[1.0]*9,
        "Agua (mL)":[10.0]*9,
        "Volumen inicial (mL)":[np.nan]*9,
        "Volumen final (mL)":[np.nan]*9
    })
    st.data_editor(plantilla, width="stretch", hide_index=True)

with tabs[5]:
    st.subheader("Progreso del Objetivo 1")
    progreso = pd.DataFrame({
        "Prueba":["Humedad","Cenizas","pH","Acidez titulable","Color CIELAB","Actividad de agua",
                  "CAA","CAAc","IAA","ISA","Hinchamiento"],
        "Estado":["Completada","Repetir/revisar","Completada","En revisión","Parcialmente completada",
                  "No realizada","En revisión","En revisión","Pendiente","Pendiente","Pendiente"]
    })
    st.dataframe(progreso, width="stretch", hide_index=True)
    st.progress(0.60)
    st.caption("60 % es solo un indicador inicial; puedes cambiarlo cuando definas tu criterio de avance.")
