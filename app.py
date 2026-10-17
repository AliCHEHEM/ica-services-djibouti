import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="ICA Services - Djibouti",
    page_icon="📊",
    layout="wide",
)

st.title("Tableau de bord statistique ICA Services")
st.subheader("Djibouti — Premier trimestre 2025")
st.caption("Source : bulletin ICA Services T1 2025, INSTAD")

# Données de démonstration à vérifier avec le bulletin officiel
donnees = [
    ("Ensemble des services", -7.7),
    ("Transports et entreposage", 1.6),
    ("Hébergement et restauration", -21.0),
    ("Information et communication", -47.9),
    ("Activités immobilières", 22.9),
    ("Activités spécialisées, scientifiques et techniques", 4.1),
    ("Services de soutien et de bureau", 3.5),
    ("Enseignement", -29.4),
    ("Santé humaine et action sociale", 11.0),
    ("Activités artistiques, sportives et récréatives", 17.6),
    ("Autres activités de services marchands", -20.7),
]

df = pd.DataFrame(
    donnees,
    columns=["Secteur", "Variation trimestrielle (%)"]
)

st.sidebar.header("Filtres")
secteurs = st.sidebar.multiselect(
    "Sélectionner les secteurs",
    options=df["Secteur"].tolist(),
    default=df["Secteur"].tolist(),
)

vue = df[df["Secteur"].isin(secteurs)]

col1, col2, col3 = st.columns(3)
col1.metric("Secteurs affichés", len(vue))
col2.metric(
    "Secteurs en hausse",
    int((vue["Variation trimestrielle (%)"] > 0).sum())
)
col3.metric(
    "Secteurs en baisse",
    int((vue["Variation trimestrielle (%)"] < 0).sum())
)

st.markdown("### Variation trimestrielle par secteur")

fig = px.bar(
    vue.sort_values("Variation trimestrielle (%)"),
    x="Variation trimestrielle (%)",
    y="Secteur",
    orientation="h",
    color="Variation trimestrielle (%)",
    color_continuous_scale="RdYlGn",
    title="T1 2025 par rapport à T4 2024",
)

fig.add_vline(x=0, line_dash="dash")
fig.update_layout(
    height=600,
    coloraxis_showscale=False,
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Données statistiques")
st.dataframe(vue, use_container_width=True, hide_index=True)

st.download_button(
    "Télécharger les données CSV",
    data=vue.to_csv(index=False).encode("utf-8-sig"),
    file_name="ica_services_t1_2025.csv",
    mime="text/csv",
)

st.info(
    "Prototype : vérifiez les valeurs avec le tableau officiel "
    "du bulletin avant diffusion publique."
)
