import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import logging
import requests
import json
import time

class FrostPreventionSystem:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.frost_threshold = 0  # Température en Celsius
        self.humidity_threshold = 85  # Pourcentage d'humidité
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='frost_prevention.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def process_sensor_data(self, soil_data, air_data, camera_data, weather_forecast):
        try:
            current_data = {
                'soil_temp': soil_data['temperature'],
                'soil_humidity': soil_data['humidity'],
                'air_temp': air_data['temperature'],
                'air_humidity': air_data['humidity'],
                'wind_speed': air_data['wind_speed'],
                'forecast_temp': weather_forecast['temperature'],
                'forecast_humidity': weather_forecast['humidity'],
                'current_frost': camera_data['frost_detected']
            }
            
            print("\n=== DONNÉES DES CAPTEURS ===")
            print(f"Température du sol: {current_data['soil_temp']}°C")
            print(f"Humidité du sol: {current_data['soil_humidity']}%")
            print(f"Température de l'air: {current_data['air_temp']}°C")
            print(f"Humidité de l'air: {current_data['air_humidity']}%")
            print(f"Vitesse du vent: {current_data['wind_speed']} km/h")
            print(f"Température prévue: {current_data['forecast_temp']}°C")
            print(f"Givre détecté par caméra: {'Oui' if current_data['current_frost'] else 'Non'}")
            
            frost_risk = self.analyze_frost_risk(current_data)
            
            print("\n=== RÉSULTAT DE L'ANALYSE ===")
            print(f"Risque de givre détecté: {'OUI' if frost_risk else 'NON'}")
            
            return frost_risk
            
        except Exception as e:
            print(f"ERREUR: {str(e)}")
            logging.error(f"Erreur lors du traitement des données: {str(e)}")
            raise

    def analyze_frost_risk(self, data):
        high_risk_conditions = [
            data['air_temp'] <= self.frost_threshold,
            data['air_humidity'] >= self.humidity_threshold,
            data['wind_speed'] < 5,
            data['forecast_temp'] < 2
        ]
        
        print("\n=== CONDITIONS À RISQUE ===")
        print(f"Température de l'air trop basse: {'Oui' if high_risk_conditions[0] else 'Non'}")
        print(f"Humidité de l'air élevée: {'Oui' if high_risk_conditions[1] else 'Non'}")
        print(f"Vent faible: {'Oui' if high_risk_conditions[2] else 'Non'}")
        print(f"Prévision de température basse: {'Oui' if high_risk_conditions[3] else 'Non'}")
        
        return data['current_frost'] or sum(high_risk_conditions) >= 3

    def trigger_drone_response(self, frost_risk):
        print("\n=== ACTION DES DRONES ===")
        if frost_risk:
            print("🚨 ALERTE: Activation des drones pour pulvérisation anti-givre")
            logging.info("ALERTE: Risque de givre détecté - Activation des drones")
            return True
        else:
            print("✅ Pas d'action nécessaire - Situation normale")
            logging.info("Pas de risque de givre détecté")
            return False

class WeatherAPICollector:
    def __init__(self, api_key):
        self.base_url = "http://api.weatherapi.com/v1"
        self.api_key = api_key

    def get_weather_data(self, latitude, longitude):
        try:
            # Utilisation du point de terminaison forecast pour obtenir les données actuelles et les prévisions
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': f"{latitude},{longitude}",
                'days': 1,
                'aqi': 'no',
                'alerts': 'no'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print("Données météo récupérées avec succès!")
                return self._parse_weather_data(data)
            else:
                print(f"Erreur lors de la récupération des données: {response.status_code}")
                print(f"Message: {response.text}")
                return None
                
        except Exception as e:
            print(f"Erreur lors de la requête API: {str(e)}")
            return None

    def _parse_weather_data(self, raw_data):
        try:
            # Extraction des données actuelles
            current = raw_data['current']
            forecast = raw_data['forecast']['forecastday'][0]['hour']
            
            # Prendre la prévision pour les 3 prochaines heures
            current_hour = datetime.now().hour
            next_hours = current_hour + 3
            if next_hours >= 24:
                next_hours = 23  # Limiter à la dernière heure de la journée
            
            forecast_data = forecast[next_hours]
            
            weather_data = {
                'air_data': {
                    'temperature': current['temp_c'],
                    'humidity': current['humidity'],
                    'wind_speed': current['wind_kph']
                },
                'weather_forecast': {
                    'temperature': forecast_data['temp_c'],
                    'humidity': forecast_data['humidity']
                }
            }
            
            return weather_data
            
        except KeyError as e:
            print(f"Erreur dans le format des données: {str(e)}")
            return None

class EnhancedFrostPreventionSystem:
    def __init__(self, latitude, longitude, api_key):
        self.weather_collector = WeatherAPICollector(api_key)
        self.frost_system = FrostPreventionSystem()
        self.latitude = latitude
        self.longitude = longitude

    def run_with_real_data(self):
        print("\n=== RÉCUPÉRATION DES DONNÉES MÉTÉO ===")
        weather_data = self.weather_collector.get_weather_data(self.latitude, self.longitude)
        
        if weather_data:
            # Estimation des données du sol basée sur les données de l'air
            complete_data = {
                'soil_data': {
                    'temperature': weather_data['air_data']['temperature'] - 1,  # Le sol est généralement plus froid
                    'humidity': min(weather_data['air_data']['humidity'] + 5, 100)  # Légèrement plus humide
                },
                'air_data': weather_data['air_data'],
                'camera_data': {
                    'frost_detected': False  # Par défaut pas de givre détecté par caméra
                },
                'weather_forecast': weather_data['weather_forecast']
            }
            
            frost_risk = self.frost_system.process_sensor_data(**complete_data)
            self.frost_system.trigger_drone_response(frost_risk)
        else:
            print("Impossible de récupérer les données météo. Vérifiez votre API key et votre connexion.")

if __name__ == "__main__":
    # Coordonnées de test (Paris)
    LATITUDE = 48.8566
    LONGITUDE = 2.3522
    # Votre clé API WeatherAPI.com
    API_KEY = "votre-api-weatherapi.com"  # Remplacez par votre clé API réelle
    
    print("=== DÉMARRAGE DU SYSTÈME AVEC WEATHERAPI.COM ===")
    print(f"Position: Latitude {LATITUDE}, Longitude {LONGITUDE}")
    print("Date et heure:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("-" * 50)
    
    enhanced_system = EnhancedFrostPreventionSystem(LATITUDE, LONGITUDE, API_KEY)
    enhanced_system.run_with_real_data()
