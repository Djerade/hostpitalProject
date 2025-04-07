from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from app.db import db

app = Flask(__name__)

# Définition des métriques
total_patients = Gauge('total_patients', 'Nombre total de patients', ['service'])
consultations_counter = Counter('consultations_total', 'Nombre total de consultations', ['service'])

def collect_metrics():
    for service in db.list_collection_names():
        collection = db[service]
        count = collection.count_documents({})
        total_patients.labels(service=service).set(count)
        consultations_counter.labels(service=service).inc(count)

@app.route('/metrics')
def metrics():
    collect_metrics()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
