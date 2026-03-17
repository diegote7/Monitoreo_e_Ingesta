# 🚛 Monitoreo e Ingesta de Datos GPS

Sistema completo de procesamiento de datos GPS en tiempo real utilizando una arquitectura de microservicios con Docker, Apache Airflow, Apache Spark, MQTT, Kafka, PostgreSQL, Prometheus y Grafana.

## 📋 **Descripción del Proyecto**

Este proyecto implementa un pipeline de datos para simular, ingerir, procesar y visualizar datos GPS de flotas de camiones. Los datos son generados por un simulador, transmitidos vía MQTT, consumidos y almacenados en PostgreSQL, procesados con Apache Spark para calcular métricas agregadas, y finalmente orquestados con Apache Airflow. Todo el sistema es monitoreado con Prometheus y visualizado con Grafana.

## 🏗️ **Arquitectura**


## 🚀 **Tecnologías Utilizadas**

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 24.0+ | Contenerización de servicios |
| **Apache Airflow** | 2.8.1 | Orquestación de pipelines |
| **Apache Spark** | 3.5.8 | Procesamiento de datos |
| **PostgreSQL + PostGIS** | 15-3.4 | Base de datos espacial |
| **MQTT (Mosquitto)** | Latest | Broker de mensajería ligera |
| **Apache Kafka** | 3.7.0 | Streaming de datos |
| **Prometheus** | 2.48.0 | Monitoreo y métricas |
| **Grafana** | 10.2.2 | Visualización de datos |
| **cAdvisor** | 0.47.0 | Monitoreo de contenedores |

## 📁 **Estructura del Proyecto**
/home/nsx/monitoreo-e-ingesta-de-datos
├── airflow
│   ├── airflow-webserver.pid
│   ├── airflow.cfg
│   ├── airflow.db
│   ├── dags
│   ├── logs
│   ├── plugins
│   └── webserver_config.py
├── airflow-webserver.pid
├── airflow.cfg
├── airflow.db
├── dags
│   ├── __pycache__
│   └── pipeline_gps.py
├── dashboard
├── dashboards
├── data
│   ├── processed
│   └── raw
├── database
├── docker
│   ├── Dockerfile.airflow
│   ├── docker-compose.yml
│   └── init-db.sql
├── ingestion
│   ├── gps_simulator.py
│   ├── kafka_consumer.py
│   ├── kafka_producer.py
│   └── mqtt_ingestor.py
├── logs
│   ├── dag_id=pipeline_gps
│   ├── dag_processor_manager
│   └── scheduler
├── monitoring
│   └── prometheus.yml
├── plugins
├── process
├── requirements.txt
├── simulator
├── spark
│   ├── jars
│   ├── spark_processor.py
│   └── spark_processor.py.bak
├── store
├── venv
│   ├── bin
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   ├── pyvenv.cfg
│   └── share
└── webserver_config.py

30 directories, 23 files


## ⚙️ **Configuración e Instalación**

### Prerrequisitos

- Docker Engine 24.0+
- Docker Compose 2.20+
- Python 3.8+ (para desarrollo local)
- 8GB+ RAM recomendado

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/monitoreo-e-ingesta-de-datos.git
cd monitoreo-e-ingesta-de-datos


## ⚙️ **Configuración e Instalación**

### Prerrequisitos

- Docker Engine 24.0+
- Docker Compose 2.20+
- Python 3.8+ (para desarrollo local)
- 8GB+ RAM recomendado

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/monitoreo-e-ingesta-de-datos.git
cd monitoreo-e-ingesta-de-datos

🌐 Acceso a Servicios
Servicio	URL	Credenciales
Airflow	http://localhost:8080	admin / admin
Grafana	http://localhost:3001	admin / admin
Prometheus	http://localhost:9090	-
cAdvisor	http://localhost:8081	-
PostgreSQL	localhost:5432	admin / admin

📚 Documentación Adicional
Apache Airflow Documentation

Apache Spark Documentation

PostgreSQL Documentation

Prometheus Documentation

Grafana Documentation

🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto

Crear rama feature (git checkout -b feature/AmazingFeature)

Commit cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abrir Pull Request


🙏 Agradecimientos
Comunidad de Apache Airflow

Comunidad de Apache Spark

Docker por su excelente plataforma

📧 Contacto
Para preguntas o sugerencias: tu-email@ejemplo.com

