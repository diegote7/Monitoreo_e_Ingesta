from pyspark.sql import SparkSession
import psycopg2
import sys

def main():
    """Función principal que se ejecuta una sola vez"""
    try:
        spark = SparkSession.builder \
            .appName("gps_processor") \
            .config("spark.jars", "/opt/airflow/spark/jars/postgresql-42.7.3.jar") \
            .getOrCreate()

        # Conexión a PostgreSQL para insertar resultados
        conn = psycopg2.connect(
            host="postgres-postgis",
            database="monitoreo",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()

        # Leer datos de gps_data
        df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres-postgis:5432/monitoreo") \
            .option("dbtable", "gps_data") \
            .option("user", "admin") \
            .option("password", "admin") \
            .option("driver", "org.postgresql.Driver") \
            .load()

        df.createOrReplaceTempView("gps")

        # Calcular métricas
        result = spark.sql("""
            SELECT
                device_id,
                AVG(speed) as velocidad_promedio,
                MAX(speed) as velocidad_max,
                MIN(speed) as velocidad_min,
                COUNT(*) as registros,
                MIN(timestamp) as periodo_inicio,
                MAX(timestamp) as periodo_fin
            FROM gps
            GROUP BY device_id
        """)

        rows = result.collect()

        # Insertar resultados en gps_metrics
        for row in rows:
            cursor.execute("""
                INSERT INTO gps_metrics 
                (device_id, velocidad_promedio, velocidad_max, velocidad_min, 
                 total_registros, periodo_inicio, periodo_fin)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row.device_id,
                row.velocidad_promedio,
                row.velocidad_max,
                row.velocidad_min,
                row.registros,
                row.periodo_inicio,
                row.periodo_fin
            ))
            conn.commit()

        print(f"✅ Procesados {len(rows)} dispositivos correctamente")
        
        # Cerrar conexiones
        cursor.close()
        conn.close()
        spark.stop()
        
        return 0  # Éxito

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1  # Error

if __name__ == "__main__":
    sys.exit(main())