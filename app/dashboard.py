import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
# from pymongo import MongoClient
from db import get_database

# Connexion MongoDB
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

# --- Interface Streamlit ---
st.set_page_config(
    page_title="📊 Dashboard Statistiques Hôpital",
    layout="wide"
)

st.title("📈 Statistiques des Services Hospitaliers")

year = st.selectbox("Sélectionnez une année :", ["2025", "2026", "2027", "2028"])
df = get_statistics(year)

st.subheader(f"📅 Données pour l'année {year}")
st.dataframe(df, use_container_width=True)

# --- Courbe : Note moyenne par service ---
st.subheader("📉 Note moyenne par service")
fig1 = px.line(df, x="Service", y="Note moyenne", markers=True, title="Note moyenne")
st.plotly_chart(fig1, use_container_width=True)

# --- Histogramme : Âge moyen ---
st.subheader("📊 Histogramme des âges moyens")
fig2 = px.histogram(df, x="Âge moyen", nbins=10, title="Distribution des âges moyens")
st.plotly_chart(fig2, use_container_width=True)

# --- Bar chart : Nombre de patients ---
st.subheader("🧍 Nombre de patients par service")
fig3 = px.bar(df, x="Service", y="Nombre de patients", color="Service", title="Nombre de patients")
st.plotly_chart(fig3, use_container_width=True)

# --- Camembert : Répartition des patients ---
st.subheader("🥧 Répartition des patients par service")
fig4 = px.pie(df, names="Service", values="Nombre de patients", title="Répartition")
st.plotly_chart(fig4, use_container_width=True)

# --- Heatmap : Patients vs. Durée traitement ---
st.subheader("🌡️ Heatmap : Nombre de patients / Durée traitement")
fig5 = px.density_heatmap(
    data_frame=df,
    x="Durée moy. traitement",
    y="Nombre de patients",
    nbinsx=20,
    nbinsy=20,
    color_continuous_scale="Viridis",
    title="Heatmap Patients / Durée"
)
st.plotly_chart(fig5, use_container_width=True)
