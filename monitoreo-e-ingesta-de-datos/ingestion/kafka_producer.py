from kafka import KafkaProducer
import json
import time
import random
import os
from datetime import datetime

# Configuración desde variables de entorno
KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka:9092")

print(f"🚀 Iniciando Kafka Producer, conectando a {KAFKA_HOST}")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_HOST,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("✅ Conectado a Kafka")
print("📤 Enviando datos GPS a Kafka...")

while True:
    data = {
        "device_id": "camion_01",
        "lat": round(-31.41 + random.random()/100, 6),
        "lon": round(-64.18 + random.random()/100, 6),
        "speed": round(random.uniform(40, 90), 2),
        "timestamp": datetime.now().isoformat()
    }

    producer.send("gps_topic", data)
    print("📤 Enviado a Kafka:", data)
    time.sleep(2)
