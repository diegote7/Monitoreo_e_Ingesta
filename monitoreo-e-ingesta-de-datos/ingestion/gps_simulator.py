import json
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import os

# Configuración desde variables de entorno
BROKER = os.getenv("MQTT_HOST", "mqtt-broker")  # nombre del contenedor MQTT
PORT = 1883
TOPIC = "gps/camiones"

print(f"Conectando a MQTT broker en {BROKER}:{PORT}")
client = mqtt.Client()
client.connect(BROKER, PORT)
print("✅ Conectado a MQTT broker")

# Función para interpolar entre dos coordenadas
def interpolar(lat1, lon1, lat2, lon2, pasos):
    return [
        (lat1 + (lat2 - lat1) * i / pasos, lon1 + (lon2 - lon1) * i / pasos)
        for i in range(1, pasos + 1)
    ]

# Rutas de cada camión (inicio en Córdoba)
rutas_base = {
    # Camión 1 – Norte argentino: Córdoba → La Rioja → Catamarca → Tucumán → Salta
    "camion_01": [
        (-31.4167, -64.1833),  # Córdoba
        (-29.4139, -66.8555),  # La Rioja
        (-28.4697, -65.7795),  # Catamarca
        (-26.8083, -65.2176),  # Tucumán
        (-24.7821, -65.4232)   # Salta
    ],

    # Camión 2 – Sur argentino: Córdoba → La Pampa → Río Negro → Ushuaia
    "camion_02": [
        (-31.4167, -64.1833),  # Córdoba
        (-36.6167, -64.2833),  # La Pampa (aprox)
        (-40.8000, -63.0000),  # Río Negro (aprox)
        (-54.8000, -68.3000)   # Ushuaia
    ],

    # Camión 3 – Buenos Aires: Córdoba → Santa Fe → Buenos Aires
    "camion_03": [
        (-31.4167, -64.1833),  # Córdoba
        (-31.6333, -60.7000),  # Santa Fe (aprox)
        (-34.6037, -58.3816)   # Buenos Aires
    ]
}

# Timestamp inicial
timestamp = datetime.now()

# Generar rutas suavizadas (muchos puntos intermedios)
rutas_suavizadas = {}
pasos_por_tramo = 20  # más pasos = movimiento más suave

for camion, puntos in rutas_base.items():
    ruta_completa = []
    for i in range(len(puntos) - 1):
        ruta_completa += interpolar(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1], pasos_por_tramo)
    rutas_suavizadas[camion] = ruta_completa

print("Iniciando simulación de GPS...")
# Simulación continua
while True:
    for camion, ruta in rutas_suavizadas.items():
        device_id = camion
        for lat, lon in ruta:
            velocidad = random.uniform(40, 90)  # velocidad aleatoria
            data = {
                "device_id": device_id,
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "speed": round(velocidad, 2),       # coincide con la columna gps_data
                "timestamp": timestamp.isoformat()
            }
            client.publish(TOPIC, json.dumps(data))
            print("📤 Enviado a MQTT:", data)
            
            timestamp += timedelta(seconds=10)  # simula el paso del tiempo
            time.sleep(0.5)  # pausa corta para movimiento continuo