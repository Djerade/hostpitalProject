from faker import Faker
import random
from db import db
from datetime import datetime


faker = Faker()

def generate_data(service, count=100):
    collection = db[service]
    for _ in range(count):
        data = {
            "patient_id": faker.uuid4(),
            "date": datetime.combine(faker.date_between(start_date="-2y", end_date="today"), datetime.min.time()),
            "diagnostic": faker.sentence(),
            "soin_prescrit": [faker.word() for _ in range(3)],
            "medicament": [faker.word()],
            "intervention": faker.sentence(),
            "doctor_id": faker.name(),
            "service": service,
            "hospitalisation": random.choice(["Oui", "Non"])
        }
        collection.insert_one(data)


# Générer des données pour chaque service
services = ["medecine_generale", "radiologie", "chirurgie", "neurologie"]
for service in services:
    generate_data(service)
