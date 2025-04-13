# from generate_data import generate_all_services
# from prometheus_client import start_http_server, Gauge
# import time
# from db import get_database

# # Connexion à la base MongoDB
# db = get_database()

# generate_all_services()

# # Définition d'une métrique Prometheus avec un label "service"
# patients_total = Gauge('patients_total', 'Nombre total de documents par service', ['service'])

# def update_metrics():
#     services = db.list_collection_names()
#     for service in services:
#         count = db[service].count_documents({})
#         patients_total.labels(service=service).set(count)
#         print(f"Service {service} → {count} documents")

# if __name__ == '__main__':
#     print("🎯 Démarrage du serveur de métriques Prometheus sur le port 8000...")
#     start_http_server(8000)  # Expose les métriques sur http://localhost:8000/metrics
#     while True:
#         update_metrics()
#         time.sleep(5)  # Rafraîchit toutes les 10 secondes






import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt
from db import db, get_database

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
st.set_page_config(page_title="Statistiques Hôpital", layout="wide")
st.title("📊 Tableau de bord des services hospitaliers")

year = st.selectbox("Sélectionnez une année :", ["2025", "2026", "2027", "2028"])

df = get_statistics(year)

st.subheader(f"📅 Statistiques pour l'année {year}")
st.dataframe(df, use_container_width=True)

# --- Visualisation ---
st.subheader("📈 Nombre de patients par service")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Service"], df["Nombre de patients"], color="skyblue")
ax.set_ylabel("Nombre de patients")
ax.set_xticklabels(df["Service"], rotation=45, ha="right")
st.pyplot(fig)
