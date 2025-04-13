import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from db import get_database

# --- Configuration de la page ---
st.set_page_config(
    page_title="Dashboard Hospitalier",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styles CSS personnalisés ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMetric > div {
        color: #2c3e50;
    }
    .stMetric > div > div {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .css-1d391kg {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Connexion à la base de données ---
database = get_database()

services = [
    "medecine_generale", "immunologie", "radiologie", "chirurgie",
    "neurologie", "cardiologie", "ontologie", "pneumologie",
    "odontologie", "pediatrie"
]

def get_statistics(year):
    result = []
    for service in services:
        collection = database[service]
        count = collection.count_documents({"date": {"$regex": f"^{year}"}})
        pipeline = [
            {"$match": {"date": {"$regex": f"^{year}"}}},
            {
                "$group": {
                    "_id": None,
                    "avg_age": {"$avg": "$age"},
                    "avg_note": {"$avg": "$note"},
                    "avg_duree": {"$avg": "$duree_traitement"},
                    "min_age": {"$min": "$age"},
                    "max_age": {"$max": "$age"},
                    "total_patients": {"$sum": 1}
                }
            }
        ]
        stats = list(collection.aggregate(pipeline))
        if stats:
            data = stats[0]
        else:
            data = {"avg_age": 0, "avg_note": 0, "avg_duree": 0, "min_age": 0, "max_age": 0, "total_patients": 0}

        result.append({
            "Service": service.replace("_", " ").title(),
            "Nombre de patients": count,
            "Âge moyen": round(data["avg_age"], 1),
            "Note moyenne": round(data["avg_note"], 2),
            "Durée moy. traitement": round(data["avg_duree"], 2),
            "Âge min": data["min_age"],
            "Âge max": data["max_age"]
        })
    return pd.DataFrame(result)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2967/2967391.png", width=100)
    st.title("🏥 Dashboard Hospitalier")
    st.markdown("---")
    
    # Sélection de l'année
    year = st.selectbox(
        "📅 Sélectionnez une année",
        ["2025", "2026", "2027", "2028"],
        index=0
    )
    
    # Filtres supplémentaires
    st.markdown("### 🔍 Filtres")
    selected_services = st.multiselect(
        "Services",
        [s.replace("_", " ").title() for s in services],
        default=[s.replace("_", " ").title() for s in services]
    )
    
    st.markdown("---")
    st.markdown("### 📊 Métriques")
    df = get_statistics(year)
    filtered_df = df[df["Service"].isin(selected_services)]
    
    total_patients = filtered_df["Nombre de patients"].sum()
    moy_age = filtered_df["Âge moyen"].mean()
    moy_duree = filtered_df["Durée moy. traitement"].mean()
    
    st.metric("Total Patients", f"{total_patients:,}")
    st.metric("Âge Moyen", f"{moy_age:.1f} ans")
    st.metric("Durée Moy. Traitement", f"{moy_duree:.1f} jours")

# --- Main Content ---
st.markdown("# 📊 Tableau de Bord Hospitalier")
st.markdown(f"### Année {year}")

# --- Métriques principales ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Patients",
        f"{total_patients:,}",
        help="Nombre total de patients pour l'année sélectionnée"
    )

with col2:
    st.metric(
        "🎂 Âge Moyen",
        f"{moy_age:.1f} ans",
        help="Âge moyen des patients"
    )

with col3:
    st.metric(
        "⏱️ Durée Moy. Traitement",
        f"{moy_duree:.1f} jours",
        help="Durée moyenne de traitement"
    )

with col4:
    st.metric(
        "⭐ Note Moyenne",
        f"{filtered_df['Note moyenne'].mean():.1f}/10",
        help="Note moyenne de satisfaction"
    )

# --- Graphiques ---
st.markdown("## 📈 Visualisations")

# Premier rang de graphiques
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        filtered_df,
        names="Service",
        values="Nombre de patients",
        title="Répartition des Patients par Service",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        filtered_df,
        x="Service",
        y="Note moyenne",
        title="Satisfaction par Service",
        color="Note moyenne",
        color_continuous_scale="Viridis"
    )
    fig2.update_layout(yaxis_range=[0, 10])
    st.plotly_chart(fig2, use_container_width=True)

# Deuxième rang de graphiques
col3, col4 = st.columns(2)

with col3:
    fig3 = px.box(
        filtered_df,
        x="Service",
        y="Âge moyen",
        title="Distribution des Âges par Service",
        color="Service",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(
        filtered_df,
        x="Durée moy. traitement",
        y="Note moyenne",
        size="Nombre de patients",
        color="Service",
        title="Relation Durée de Traitement vs Satisfaction",
        hover_name="Service",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- Tableau de données ---
st.markdown("## 📋 Données Détailées")
st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "Service": st.column_config.TextColumn("Service"),
        "Nombre de patients": st.column_config.NumberColumn("Patients"),
        "Âge moyen": st.column_config.NumberColumn("Âge Moyen"),
        "Note moyenne": st.column_config.NumberColumn("Note"),
        "Durée moy. traitement": st.column_config.NumberColumn("Durée (jours)")
    }
)

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Dashboard Hospitalier - © 2024</p>
    </div>
    """, unsafe_allow_html=True)
