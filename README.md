Parfait ! Voici une version du **README.md** que tu peux directement utiliser pour ton projet GitHub ou GitLab. Je l’ai adapté à partir de ta documentation, avec un focus sur la présentation rapide et l’exécution du projet.

---

```markdown
# 🏥 Hopital Data Management

Projet de visualisation et d’analyse des données médicales de l’hôpital **Donanam**. Ce dashboard permet de visualiser les statistiques médicales par service et par année, à l’aide de MongoDB, Streamlit et Grafana.

## 🚀 Fonctionnalités

- Analyse de la fréquentation hospitalière par service
- Visualisation interactive avec Streamlit (graphes, tableaux, heatmaps)
- Monitoring des données avec Prometheus et Grafana
- Simulation de données pour 10 services hospitaliers

## 🧰 Technologies utilisées

- **MongoDB** : base de données NoSQL
- **Python** : scripts de génération et traitement de données
- **Streamlit** : interface web interactive
- **Prometheus** + **Grafana** : monitoring
- **Docker & Docker Compose** : conteneurisation

## 🗂️ Architecture du projet

```
/hopital-data-management
│── docker-compose.yml
│── Dockerfile
│── Dockerfile.streamlit
│── app/
│   ├── main.py
│   ├── db.py
│   ├── dashboard.py
│   ├── generate_data.py
│── requirements.txt
```

## ⚙️ Installation & Exécution

### 🔁 Méthode Docker (recommandée)

1. Clone le dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/hopital-data-management.git
   cd hopital-data-management
   ```

2. Lancer les services :
   ```bash
   docker-compose build
   docker-compose up
   ```

3. Accéder aux interfaces :
   - Streamlit : [http://localhost:8501](http://localhost:8501)
   - Grafana : [http://localhost:3000](http://localhost:3000) (identifiants : `admin/admin`)
   - Prometheus : [http://localhost:9090](http://localhost:9090)

### ⚙️ Méthode manuelle (développement)

1. Crée un environnement Python :
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate sur Windows
   pip install -r requirements.txt
   ```

2. Lance MongoDB (local ou distant).

3. Génère les données :
   ```bash
   python app/generate_data.py
   ```

4. Lance l'interface :
   ```bash
   streamlit run app/dashboard.py
   ```

---

## 📊 Exemple de données

```json
{
  "nom": "Jean Dupont",
  "age": 52,
  "date": "2025-03-15",
  "note": 8.5,
  "duree_traitement": 5.2
}
```

---

## 👨‍💼 Auteur

**Djeradé Golbé Parfait**  
Consultant Data Analyst — Projet réalisé pour l'hôpital Donanam

---

```

Souhaites-tu aussi que je te génère un fichier `README.md` prêt à télécharger ou à coller dans ton projet ?
