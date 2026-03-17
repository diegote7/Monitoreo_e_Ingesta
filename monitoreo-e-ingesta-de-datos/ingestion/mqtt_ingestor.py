import paho.mqtt.client as mqtt
import psycopg2
import json
import os
from datetime import datetime

# Configuración desde variables de entorno
DB_HOST = os.getenv("DB_HOST", "postgres-postgis")
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt-broker")
DB_NAME = os.getenv("DB_NAME", "monitoreo")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")

print("=" * 50)
print("🚀 Iniciando MQTT Ingestor")
print(f"📡 Conectando a MQTT broker en: {MQTT_HOST}:1883")
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

# Función que se ejecuta cuando llega un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        device_id = data["device_id"]
        lat = data["lat"]
        lon = data["lon"]
        speed = data["speed"]
        timestamp = data.get("timestamp", datetime.now().isoformat())

        query = """
        INSERT INTO gps_data (device_id, lat, lon, speed, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (device_id, lat, lon, speed, timestamp))
        conn.commit()
        
        print(f"💾 Guardado en DB - {device_id}: lat={lat}, lon={lon}, speed={speed}")

    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
        conn.rollback()

# Configuración MQTT
client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(MQTT_HOST, 1883)
    print("✅ Conectado a MQTT broker")
except Exception as e:
    print(f"❌ Error conectando a MQTT: {e}")
    exit(1)

client.subscribe("gps/camiones")
print("👂 Escuchando datos MQTT en topic 'gps/camiones'...")
print("=" * 50)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Deteniendo ingestor...")
    client.disconnect()
    conn.close()