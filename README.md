FrostGuard AI 🌡️ 🚀
À propos
FrostGuard AI est un système intelligent de protection contre le givre qui combine :

Capteurs IoT (température du sol, humidité, conditions atmosphériques)
Analyse d'images par caméra pour la détection du givre
Prévisions météorologiques en temps réel
Intelligence artificielle pour l'analyse prédictive
Drones autonomes pour la pulvérisation de solution anti-givre

Fonctionnalités

📊 Collecte en temps réel des données environnementales
🤖 Analyse prédictive du risque de givre par IA
📸 Détection visuelle du givre par caméra
🛩️ Déploiement automatique de drones
📱 Interface de surveillance et alertes
📝 Journalisation complète des interventions

Installation

Cloner le dépôt :

bashCopygit clone https://github.com/votre-username/frostguard-ai.git
cd frostguard-ai

Installer les dépendances :

bashCopypip install -r requirements.txt

Configurer les variables d'environnement :


Créer un fichier .env à la racine du projet
Ajouter votre clé API WeatherAPI.com :

CopyWEATHER_API_KEY=votre_clé_api
Utilisation
pythonCopypython main.py
Structure du Projet
Copyfrostguard-ai/
├── main.py
├── frost_prevention.log
├── requirements.txt
├── .env
└── README.md
Requirements.txt
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.2.2
requests==2.28.2
python-dotenv==1.0.0
logging==0.5.1.2
datetime==5.1
