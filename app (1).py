
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Gemelo Digital de Harinas",
    page_icon="🧪",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.5rem 1.8rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #f7f8fb 0%, #eef1f6 100%);
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}
.hero h1 {
    margin: 0;
    font-size: 2.2rem;
}
.hero p {
    color: #5f6368;
    margin-top: 0.5rem;
    margin-bottom: 0;
}
.status-ok {
    padding: 0.35rem 0.65rem;
    border-radius: 12px;
    background: #e8f5e9;
    color: #1b5e20;
    font-weight: 600;
}
.status-warn {
    padding: 0.35rem 0.65rem;
    border-radius: 12px;
    background: #fff8e1;
    color: #8d6e00;
    font-weight: 600;
}
.status-pending {
    padding: 0.35rem 0.65rem;
    border-radius: 12px;
    background: #eceff1;
    color: #455a64;
    font-weight: 600;
}
.small-note {
    color: #6b7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧪 Gemelo Digital del comportamiento de harinas</h1>
    <p>
    Representación interactiva del comportamiento fisicoquímico y tecnofuncional
    de harina de trigo, lenteja y arroz para el desarrollo de brownie sin azúcar añadido.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATOS
# ============================================================

humedad = pd.DataFrame({
    "Tiempo (min)": list(range(1,11)),
    "Lenteja":[3.06,4.54,5.62,6.41,7.10,7.69,8.19,8.68,8.88,9.27],
    "Arroz":[3.40,5.00,6.10,6.90,7.40,7.80,8.20,8.40,8.60,8.80],
    "Trigo":[4.16,6.74,8.49,9.70,10.53,11.26,11.73,12.10,12.28,12.47]
})

humedad_final = {
    "Trigo": 12.47,
    "Lenteja": 9.27,
    "Arroz": 8.80
}

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

# ============================================================
# FUNCIONES
# ============================================================

def calc_caa(df):
    x = df.copy()
    x["Sedimento húmedo (g)"] = x["Tubo + sedimento (g)"] - x["Tubo vacío (g)"]
    x["CAA (g/g)"] = (x["Sedimento húmedo (g)"] - x["Muestra (g)"]) / x["Muestra (g)"]
    return x

def calc_caac(df):
    x = df.copy()
    x["Sedimento con aceite (g)"] = x["Tubo + sedimento (g)"] - x["Tubo vacío (g)"]
    x["CAAc (g/g)"] = (x["Sedimento con aceite (g)"] - x["Muestra (g)"]) / x["Muestra (g)"]
    return x

def media_de(df, harina, col):
    vals = df.loc[df["Harina"] == harina, col]
    return vals.mean(), vals.std(ddof=1)

def interpretation(harina):
    ph_mean = ph.loc[ph["Harina"] == harina, "pH inicial"].mean()
    hum = humedad_final[harina]

    txt = []
    if harina == "Trigo":
        txt.append("presentó la mayor humedad final entre las tres harinas evaluadas")
        txt.append("mostró un pH ligeramente ácido y cercano al observado para la harina de lenteja")
    elif harina == "Lenteja":
        txt.append("presentó una humedad menor que la harina de trigo")
        txt.append("mostró el pH promedio más bajo de las tres materias primas")
        txt.append("presentó una mayor componente amarilla b* que la harina de arroz")
    elif harina == "Arroz":
        txt.append("presentó la menor humedad final entre las tres harinas")
        txt.append("mostró el pH promedio más alto del grupo")
        txt.append("presentó menor intensidad amarilla b* que la harina de lenteja")

    return (
        f"La harina de **{harina.lower()}** {txt[0]}. "
        f"Además, {txt[1]}. "
        + (f"También {txt[2]}." if len(txt) > 2 else "")
        + " Las propiedades tecnofuncionales aún deben interpretarse con cautela porque varios datos se encuentran en revisión."
    )

# ============================================================
# NAVEGACIÓN
# ============================================================

menu = st.sidebar.radio(
    "Navegación",
    [
        "Inicio",
        "Perfil de harina",
        "Fisicoquímicas",
        "CIELAB 3D",
        "Tecnofuncionales",
        "Comparación",
        "Progreso Objetivo 1"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Gemelo Digital v0.2")
st.sidebar.caption("Datos experimentales actuales del Objetivo Específico 1")

# ============================================================
# INICIO
# ============================================================

if menu == "Inicio":
    st.subheader("Estado actual del sistema")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Harinas caracterizadas", "3")
    c2.metric("Pruebas con datos", "9")
    c3.metric("Pruebas completas", "2")
    c4.metric("Pruebas en revisión", "6")

    st.markdown("### ¿Qué representa este gemelo digital?")
    st.write(
        "Esta primera versión representa digitalmente el comportamiento observado "
        "en las materias primas antes de formular el brownie. El sistema integra "
        "resultados de humedad, pH, acidez, color y propiedades tecnofuncionales."
    )

    st.markdown("### Resumen de las materias primas")
    resumen = pd.DataFrame({
        "Harina":["Trigo","Lenteja","Arroz"],
        "Humedad (%)":[12.47,9.27,8.80],
        "pH promedio":[
            ph.loc[ph["Harina"]=="Trigo","pH inicial"].mean(),
            ph.loc[ph["Harina"]=="Lenteja","pH inicial"].mean(),
            ph.loc[ph["Harina"]=="Arroz","pH inicial"].mean()
        ],
        "Estado tecnofuncionales":[
            "En revisión",
            "En revisión",
            "En revisión"
        ]
    })
    st.dataframe(resumen.round(2), width="stretch", hide_index=True)

    st.info(
        "El sistema se irá actualizando conforme se validen CAA, CAAc, IAA, ISA, "
        "hinchamiento y cenizas."
    )

# ============================================================
# PERFIL DE HARINA
# ============================================================

elif menu == "Perfil de harina":
    st.subheader("Perfil digital de la harina")

    harina = st.selectbox("Selecciona una harina", ["Trigo","Lenteja","Arroz"])

    ph_mean, ph_sd = media_de(ph, harina, "pH inicial")
    naoh_mean, naoh_sd = media_de(ph, harina, "NaOH (mL)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Humedad final", f"{humedad_final[harina]:.2f} %")
    c2.metric("pH promedio", f"{ph_mean:.2f}")
    c3.metric("NaOH promedio", f"{naoh_mean:.2f} mL")

    if harina in ["Lenteja","Arroz"]:
        col_mean = color[color["Harina"]==harina][["L*","a*","b*"]].mean()
        st.markdown("### Perfil CIELAB")
        c1, c2, c3 = st.columns(3)
        c1.metric("L*", f"{col_mean['L*']:.2f}")
        c2.metric("a*", f"{col_mean['a*']:.2f}")
        c3.metric("b*", f"{col_mean['b*']:.2f}")
    else:
        st.warning("Aún no se han incorporado datos CIELAB de trigo.")

    st.markdown("### Interpretación del comportamiento")
    st.write(interpretation(harina))

    st.markdown("### Estado de pruebas")
    estado = pd.DataFrame({
        "Variable":[
            "Humedad","pH","Acidez titulable","Cenizas",
            "Color CIELAB","CAA","CAAc","IAA","ISA","Hinchamiento"
        ],
        "Estado":[
            "Completada","Completada","En revisión","Repetir / revisar",
            "Disponible" if harina in ["Lenteja","Arroz"] else "Pendiente",
            "En revisión","En revisión","Pendiente","Pendiente","Pendiente"
        ]
    })
    st.dataframe(estado, width="stretch", hide_index=True)

# ============================================================
# FISICOQUÍMICAS
# ============================================================

elif menu == "Fisicoquímicas":
    st.subheader("Caracterización fisicoquímica")

    subtabs = st.tabs(["Humedad","pH","Acidez titulable","Cenizas"])

    with subtabs[0]:
        long = humedad.melt(
            id_vars="Tiempo (min)",
            var_name="Harina",
            value_name="Humedad (%)"
        )
        fig = px.line(
            long,
            x="Tiempo (min)",
            y="Humedad (%)",
            color="Harina",
            markers=True,
            title="Evolución de la humedad durante 10 minutos"
        )
        st.plotly_chart(fig, width="stretch")
        st.dataframe(humedad, width="stretch", hide_index=True)
        st.info(
            "Entre los minutos 9 y 10 todavía hubo incremento: lenteja +0.39, "
            "arroz +0.20 y trigo +0.19 puntos porcentuales."
        )

    with subtabs[1]:
        fig = px.box(
            ph,
            x="Harina",
            y="pH inicial",
            points="all",
            title="Distribución del pH inicial"
        )
        st.plotly_chart(fig, width="stretch")

        resumen = ph.groupby("Harina")["pH inicial"].agg(["mean","std"]).reset_index()
        resumen.columns = ["Harina","Promedio","DE"]
        st.dataframe(resumen.round(3), width="stretch", hide_index=True)

    with subtabs[2]:
        fig = px.bar(
            ph,
            x="Harina",
            y="NaOH (mL)",
            color="Réplica",
            barmode="group",
            title="Gasto de NaOH por réplica"
        )
        st.plotly_chart(fig, width="stretch")
        st.dataframe(ph, width="stretch", hide_index=True)
        st.warning(
            "La réplica 3 de lenteja (4.4 mL) debe revisarse antes de considerar "
            "el resultado como definitivo."
        )

    with subtabs[3]:
        st.warning(
            "La prueba de cenizas se mantiene como 'repetir / revisar' porque "
            "existen registros con pesos finales incompatibles con el peso del crisol vacío."
        )
        st.write(
            "El gemelo conserva este estado para mantener trazabilidad experimental, "
            "pero no genera promedios definitivos de cenizas."
        )

# ============================================================
# CIELAB 3D
# ============================================================

elif menu == "CIELAB 3D":
    st.subheader("Representación tridimensional del color")

    fig = px.scatter_3d(
        color,
        x="L*",
        y="a*",
        z="b*",
        color="Harina",
        symbol="Harina",
        hover_data=["Réplica"],
        title="Distribución de las réplicas en el espacio CIELAB"
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        scene=dict(
            xaxis_title="L* — luminosidad",
            yaxis_title="a* — verde ↔ rojo",
            zaxis_title="b* — azul ↔ amarillo"
        )
    )
    st.plotly_chart(fig, width="stretch")

    resumen_color = color.groupby("Harina")[["L*","a*","b*"]].agg(["mean","std"]).round(2)
    st.dataframe(resumen_color, width="stretch")

    st.info(
        "La harina de lenteja presenta valores b* mayores que la harina de arroz, "
        "lo que refleja una mayor tendencia hacia tonalidades amarillas."
    )

# ============================================================
# TECNOFUNCIONALES
# ============================================================

elif menu == "Tecnofuncionales":
    st.subheader("Propiedades tecnofuncionales")

    st.warning(
        "Los datos de CAA y CAAc son provisionales. Los pesos finales fueron "
        "registrados con poca precisión y la tara de 6.643 g se usa como referencia."
    )

    sub = st.tabs(["CAA","CAAc","IAA / ISA","Hinchamiento"])

    with sub[0]:
        st.markdown("### Capacidad de absorción de agua")
        caa_edit = st.data_editor(
            caa,
            width="stretch",
            hide_index=True,
            key="edit_caa"
        )
        caa_calc = calc_caa(caa_edit)
        st.dataframe(caa_calc.round(3), width="stretch", hide_index=True)

        resumen = caa_calc.groupby("Harina")["CAA (g/g)"].agg(["mean","std"]).reset_index()
        resumen.columns = ["Harina","Promedio","DE"]
        st.dataframe(resumen.round(3), width="stretch", hide_index=True)

    with sub[1]:
        st.markdown("### Capacidad de absorción de aceite")
        caac_edit = st.data_editor(
            caac,
            width="stretch",
            hide_index=True,
            key="edit_caac"
        )
        caac_calc = calc_caac(caac_edit)
        st.dataframe(caac_calc.round(3), width="stretch", hide_index=True)

        resumen = caac_calc.groupby("Harina")["CAAc (g/g)"].agg(["mean","std"]).reset_index()
        resumen.columns = ["Harina","Promedio","DE"]
        st.dataframe(resumen.round(3), width="stretch", hide_index=True)

    with sub[2]:
        st.info(
            "IAA e ISA permanecen pendientes de validación porque deben revisarse "
            "las taras de recipientes, cápsulas y masas de gel/sólidos."
        )

        plantilla = pd.DataFrame({
            "Harina":["Trigo"]*3+["Lenteja"]*3+["Arroz"]*3,
            "Réplica":[1,2,3]*3,
            "Muestra (g)":[2.5]*9,
            "Agua (mL)":[30.0]*9,
            "Recipiente vacío (g)":[np.nan]*9,
            "Recipiente + gel (g)":[np.nan]*9,
            "Cápsula vacía (g)":[np.nan]*9,
            "Cápsula + sólidos secos (g)":[np.nan]*9
        })
        st.data_editor(plantilla, width="stretch", hide_index=True)

    with sub[3]:
        st.info("La capacidad de hinchamiento está pendiente de completar.")
        plantilla = pd.DataFrame({
            "Harina":["Trigo"]*3+["Lenteja"]*3+["Arroz"]*3,
            "Réplica":[1,2,3]*3,
            "Muestra (g)":[1.0]*9,
            "Agua (mL)":[10.0]*9,
            "Volumen inicial (mL)":[np.nan]*9,
            "Volumen final hidratado (mL)":[np.nan]*9
        })
        st.data_editor(plantilla, width="stretch", hide_index=True)

# ============================================================
# COMPARACIÓN
# ============================================================

elif menu == "Comparación":
    st.subheader("Comparación entre harinas")

    ph_means = ph.groupby("Harina")["pH inicial"].mean()

    base = pd.DataFrame({
        "Harina":["Trigo","Lenteja","Arroz"],
        "Humedad (%)":[12.47,9.27,8.80],
        "pH":[ph_means["Trigo"],ph_means["Lenteja"],ph_means["Arroz"]]
    })

    st.markdown("### Humedad")
    fig1 = px.bar(base, x="Harina", y="Humedad (%)", title="Comparación de humedad final")
    st.plotly_chart(fig1, width="stretch")

    st.markdown("### pH")
    fig2 = px.bar(base, x="Harina", y="pH", title="Comparación de pH promedio")
    st.plotly_chart(fig2, width="stretch")

    st.markdown("### Lectura comparativa")
    st.write(
        "- **Trigo:** mayor humedad final.\n"
        "- **Lenteja:** pH promedio más bajo y mayor componente amarilla b* frente al arroz.\n"
        "- **Arroz:** menor humedad final y pH promedio más alto.\n"
        "- **Tecnofuncionales:** todavía en proceso de validación."
    )

# ============================================================
# PROGRESO
# ============================================================

elif menu == "Progreso Objetivo 1":
    st.subheader("Progreso del Objetivo Específico 1")

    progreso = pd.DataFrame({
        "Prueba":[
            "Humedad","Cenizas","pH","Acidez titulable","Color CIELAB",
            "Actividad de agua","CAA","CAAc","IAA","ISA","Hinchamiento"
        ],
        "Tipo":[
            "Fisicoquímica","Fisicoquímica","Fisicoquímica","Fisicoquímica",
            "Fisicoquímica","Fisicoquímica","Tecnofuncional","Tecnofuncional",
            "Tecnofuncional","Tecnofuncional","Tecnofuncional"
        ],
        "Estado":[
            "Completada","Repetir / revisar","Completada","En revisión",
            "Parcialmente completada","No realizada","En revisión","En revisión",
            "Pendiente","Pendiente","Pendiente"
        ],
        "Avance (%)":[100,50,100,75,75,0,75,75,50,50,0]
    })

    avance_general = progreso["Avance (%)"].mean() / 100

    st.metric("Avance general estimado", f"{avance_general*100:.0f} %")
    st.progress(float(avance_general))

    st.dataframe(progreso, width="stretch", hide_index=True)

    completadas = (progreso["Avance (%)"] == 100).sum()
    revision = progreso["Estado"].str.contains("revisión|Repetir", case=False, regex=True).sum()
    pendientes = (progreso["Avance (%)"] == 0).sum()

    c1,c2,c3 = st.columns(3)
    c1.metric("Completadas", completadas)
    c2.metric("En revisión", revision)
    c3.metric("Pendientes", pendientes)

    st.info(
        "Este porcentaje es un indicador de seguimiento interno. "
        "No representa un resultado estadístico ni experimental."
    )

st.markdown("---")
st.caption(
    "Gemelo Digital de Harinas v0.2 — representación académica del comportamiento "
    "fisicoquímico y tecnofuncional de materias primas."
)
