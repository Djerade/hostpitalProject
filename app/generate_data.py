from db import db
from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np

fake = Faker("fr_FR")

services = [
    "medecine_generale", "immunologie", "radiologie", "chirurgie",
    "neurologie", "cardiologie", "ontologie", "pneumologie",
    "odontologie", "pediatrie"
]

diagnostics = [
    "infection virale", "fracture", "diabète", "hypertension",
    "allergie", "asthme", "cancer", "AVC", "migraine", "carie"
]


def generate_base_year(year=2025):
    for service in services:
        collection = db[service]
        for day in range(365):
            date = datetime(year, 1, 1) + timedelta(days=day)
            for _ in range(random.randint(2, 5)):  # patients/jour
                collection.insert_one({
                    "patient_id": fake.uuid4(),
                    "nom": fake.name(),
                    "sexe": random.choice(["Homme", "Femme"]),
                    "age": random.randint(1, 90),
                    "diagnostic": random.choice(diagnostics),
                    "note": round(random.uniform(0.5, 0.9), 2),
                    "duree_traitement": round(random.uniform(1, 10), 2),
                    "date": date.strftime("%Y-%m-%d")
                })


def generate_with_noise(base_year=2025, target_year=2026):
    for service in services:
        base_data = list(db[service].find({"date": {"$regex": f"^{base_year}"}}))
        for entry in base_data:
            old_date = datetime.strptime(entry["date"], "%Y-%m-%d")
            new_date = old_date.replace(year=target_year)

            noisy_age = int(np.clip(entry["age"] + np.random.normal(0, 2), 1, 100))
            noisy_note = float(np.clip(entry["note"] + np.random.normal(0, 0.05), 0, 1))
            noisy_duree = float(np.clip(entry["duree_traitement"] + np.random.normal(0, 1), 0.5, 30))

            db[service].insert_one({
                "patient_id": fake.uuid4(),
                "nom": fake.name(),
                "sexe": entry["sexe"],
                "age": noisy_age,
                "diagnostic": entry["diagnostic"],
                "note": round(noisy_note, 2),
                "duree_traitement": round(noisy_duree, 2),
                "date": new_date.strftime("%Y-%m-%d")
            })


def generate_all_services():
    if all(db[s].count_documents({"date": {"$regex": "^2025"}}) == 0 for s in services):
        print("📅 Génération de l’année 2025...")
        generate_base_year(2025)

    for year in [2026, 2027, 2028]:
        if all(db[s].count_documents({"date": {"$regex": f"^{year}"}}) == 0 for s in services):
            print(f"📅 Génération des données bruitées pour {year}...")
            generate_with_noise(2025, year)
            
    print("✅ Données générées avec succès !")