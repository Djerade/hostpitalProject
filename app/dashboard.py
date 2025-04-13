import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
from db import get_database

# --- Connexion à la base ---
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
                    "avg_duree": {"$avg": "$duree_traitement"}
                }
            }
        ]
        stats = list(collection.aggregate(pipeline))
        if stats:
            data = stats[0]
        else:
            data = {"avg_age": 0, "avg_note": 0, "avg_duree": 0}

        result.append({
            "Service": service,
            "Nombre de patients": count,
            "Âge moyen": round(data["avg_age"], 1),
            "Note moyenne": round(data["avg_note"], 2),
            "Durée moy. traitement": round(data["avg_duree"], 2)
        })
    return pd.DataFrame(result)

# --- Configuration Streamlit ---
st.set_page_config(page_title="Statistiques Hôpital", layout="wide")
st.title("📊 Tableau de bord des statistiques hospitalières")

# --- Sélection année ---
year = st.selectbox("📅 Sélectionnez une année :", ["2025", "2026", "2027", "2028"])
df = get_statistics(year)

# --- Métriques rapides ---
total_patients = df["Nombre de patients"].sum()
moy_age = df["Âge moyen"].mean()
moy_duree = df["Durée moy. traitement"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total patients", total_patients)
col2.metric("🎂 Âge moyen", f"{moy_age:.1f} ans")
col3.metric("⏱️ Durée moy. traitement", f"{moy_duree:.1f} jrs")

# --- Tableau brut ---
st.subheader("📄 Détails des données par service")
st.dataframe(df, use_container_width=True)

# --- Charts ---
st.subheader("📈 Visualisations des données")
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    fig1 = px.pie(df, names="Service", values="Nombre de patients", title="Répartition par service")
    st.plotly_chart(fig1, use_container_width=True)

with fig_col2:
    fig2 = px.bar(df, x="Service", y="Note moyenne", color="Note moyenne", title="Note moyenne par service")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

fig_col3, fig_col4 = st.columns(2)

with fig_col3:
    fig3 = px.line(df, x="Service", y="Âge moyen", markers=True, title="Âge moyen")
    st.plotly_chart(fig3, use_container_width=True)

with fig_col4:
    fig4 = px.histogram(df, x="Durée moy. traitement", nbins=10, title="Histogramme Durée traitement")
    st.plotly_chart(fig4, use_container_width=True)
