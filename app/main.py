from flask import Flask, render_template_string
from generate_data import generate_all_services
from db import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Génération de données simulées au démarrage
generate_all_services()

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Dashboard Hôpital</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800 p-6">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Statistiques de l'hôpital</h1>
    <div id="stats" class="grid grid-cols-1 gap-4">
      <div class='bg-white p-4 rounded shadow'>
        <h3 class='text-lg font-semibold'>Total des patients</h3>
        <p class='text-2xl'>{{ total }}</p>
      </div>
    </div>
    <h2 class="text-2xl font-semibold mt-8 mb-2">Tendance mensuelle</h2>
    <div id="trend" class="bg-white p-4 rounded shadow">
      {% for item in trend %}
        <div class='border-b py-1 flex justify-between'>
          <span>{{ item.date }}</span>
          <span>{{ item.patients }} patients</span>
        </div>
      {% endfor %}
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    services = db.list_collection_names()
    trend = []
    total = 1
    
    print("---",service)
    # Calcul des tendances mensuelles
    for month in range(1, 13):
        mois = f"2025-{str(month).zfill(2)}"
        count = 0
        for service in services:
            count += db[service].count_documents({"date": {"$regex": f"^{mois}"}})
        trend.append({"date": mois, "patients": count})
        total += count

    # Injecter les données dans le template
    return render_template_string(TEMPLATE, total=total, trend=trend)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
# Route d'accueil
# @app.route("/")
# def home():
#     return jsonify({"message": "Bienvenue dans le système de gestion des données de l'hôpital Donanam"}), 200

# Récupérer toutes les données d'un service
# @app.route("/<service>", methods=["GET"])
# def get_service_data(service):
#     if service not in db.list_collection_names():
#         return jsonify({"error": "Service non trouvé"}), 404

#     documents = list(db[service].find())
#     return jsonify([serialize_doc(doc) for doc in documents]), 200

# Ajouter un patient à un service
# @app.route("/<service>/add", methods=["POST"])
# def add_patient(service):
#     if service not in db.list_collection_names():
#         return jsonify({"error": "Service non trouvé"}), 404

#     data = request.json
#     if not data:
#         return jsonify({"error": "Données invalides"}), 400

#     inserted_id = db[service].insert_one(data).inserted_id
#     return jsonify({"message": "Patient ajouté", "id": str(inserted_id)}), 201

# Modifier un patient
# @app.route("/<service>/update/<id>", methods=["PUT"])
# def update_patient(service, id):
#     if service not in db.list_collection_names():
#         return jsonify({"error": "Service non trouvé"}), 404

#     data = request.json
#     if not data:
#         return jsonify({"error": "Données invalides"}), 400

#     result = db[service].update_one({"_id": ObjectId(id)}, {"$set": data})
#     if result.matched_count == 0:
#         return jsonify({"error": "Patient non trouvé"}), 404

#     return jsonify({"message": "Patient mis à jour"}), 200

# Supprimer un patient
# @app.route("/<service>/delete/<id>", methods=["DELETE"])
# def delete_patient(service, id):
#     if service not in db.list_collection_names():
#         return jsonify({"error": "Service non trouvé"}), 404

#     result = db[service].delete_one({"_id": ObjectId(id)})
#     if result.deleted_count == 0:
#         return jsonify({"error": "Patient non trouvé"}), 404

#     return jsonify({"message": "Patient supprimé"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
