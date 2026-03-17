from kafka import KafkaConsumer
import json
import psycopg2
import os
from datetime import datetime

# Configuración desde variables de entorno
KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka:9092")
DB_HOST = os.getenv("DB_HOST", "postgres-postgis")
DB_NAME = os.getenv("DB_NAME", "monitoreo")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")

print("=" * 50)
print("🚀 Iniciando Kafka Consumer")
print(f"📡 Conectando a Kafka en: {KAFKA_HOST}")
print(f"🐘 Conectando a PostgreSQL en: {DB_HOST}:5432/{DB_NAME}")
print("=" * 50)

# Conexión a PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("✅ Conectado a PostgreSQL")
except Exception as e:
    print(f"❌ Error conectando a PostgreSQL: {e}")
    exit(1)

# Configuración de Kafka Consumer
try:
    consumer = KafkaConsumer(
        "gps_topic",
        bootstrap_servers=KAFKA_HOST,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    print("✅ Conectado a Kafka")
except Exception as e:
    print(f"❌ Error conectando a Kafka: {e}")
    exit(1)

print("👂 Esperando mensajes de Kafka...")

try:
    for message in consumer:
        data = message.value
        
        print("📥 Recibido de Kafka:", data)

        cursor.execute(
            """
            INSERT INTO gps_data (device_id, lat, lon, speed, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["device_id"],
                data["lat"],
                data["lon"],
                data["speed"],
                data.get("timestamp", datetime.now().isoformat())
            )
        )
        conn.commit()
        print("💾 Guardado en DB")

except KeyboardInterrupt:
    print("\n🛑 Deteniendo consumer...")
finally:
    consumer.close()
    conn.close()