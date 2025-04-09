from generate_data import generate_all_services
from prometheus_client import start_http_server, Gauge
import time
from db import get_database

# Connexion à la base MongoDB
db = get_database()

generate_all_services()

# Définition d'une métrique Prometheus avec un label "service"
patients_total = Gauge('patients_total', 'Nombre total de documents par service', ['service'])

def update_metrics():
    services = db.list_collection_names()
    for service in services:
        count = db[service].count_documents({})
        patients_total.labels(service=service).set(count)
        print(f"Service {service} → {count} documents")

if __name__ == '__main__':
    print("🎯 Démarrage du serveur de métriques Prometheus sur le port 8000...")
    start_http_server(8000)  # Expose les métriques sur http://localhost:8000/metrics
    while True:
        update_metrics()
        time.sleep(5)  # Rafraîchit toutes les 10 secondes
