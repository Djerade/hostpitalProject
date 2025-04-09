from flask import Flask, jsonify, request
from generate_data import generate_all_services
from db import db
from bson import ObjectId

app = Flask(__name__)

generate_all_services()
# Convertisseur pour les objets BSON ObjectId
def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

# Route d'accueil
@app.route("/")
def home():
    return jsonify({"message": "Bienvenue dans le système de gestion des données de l'hôpital Donanam"}), 200

# Récupérer toutes les données d'un service
@app.route("/<service>", methods=["GET"])
def get_service_data(service):
    if service not in db.list_collection_names():
        return jsonify({"error": "Service non trouvé"}), 404

    documents = list(db[service].find())
    return jsonify([serialize_doc(doc) for doc in documents]), 200

# Ajouter un patient à un service
@app.route("/<service>/add", methods=["POST"])
def add_patient(service):
    if service not in db.list_collection_names():
        return jsonify({"error": "Service non trouvé"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Données invalides"}), 400

    inserted_id = db[service].insert_one(data).inserted_id
    return jsonify({"message": "Patient ajouté", "id": str(inserted_id)}), 201

# Modifier un patient
@app.route("/<service>/update/<id>", methods=["PUT"])
def update_patient(service, id):
    if service not in db.list_collection_names():
        return jsonify({"error": "Service non trouvé"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Données invalides"}), 400

    result = db[service].update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Patient non trouvé"}), 404

    return jsonify({"message": "Patient mis à jour"}), 200

# Supprimer un patient
@app.route("/<service>/delete/<id>", methods=["DELETE"])
def delete_patient(service, id):
    if service not in db.list_collection_names():
        return jsonify({"error": "Service non trouvé"}), 404

    result = db[service].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Patient non trouvé"}), 404

    return jsonify({"message": "Patient supprimé"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
