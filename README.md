## Monitoreo e Ingesta de Datos GPS ##
[![logo.png](https://i.postimg.cc/C1DCGdjj/logo.png)](https://postimg.cc/yg1SB1pd)

Sistema completo de procesamiento de datos GPS en tiempo real utilizando una arquitectura de microservicios con Docker, Apache Airflow, Apache Spark, MQTT, Kafka, PostgreSQL, Prometheus y Grafana.

## 📋 **Descripción del Proyecto**

Este proyecto implementa un pipeline de datos para simular, ingerir, procesar y visualizar datos GPS de flotas de camiones. Los datos son generados por un simulador, transmitidos vía MQTT, consumidos y almacenados en PostgreSQL, procesados con Apache Spark para calcular métricas agregadas, y finalmente orquestados con Apache Airflow. Todo el sistema es monitoreado con Prometheus y visualizado con Grafana.

## 🏗️ **Arquitectura**

┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ GPS Simulator │────▶│ MQTT Broker │────▶│ MQTT Ingestor │────▶│ PostgreSQL │
│ (Python/MQTT) │ │ (Mosquitto) │ │ (Python/DB) │ │ (PostGIS) │
└─────────────────┘ └──────────────┘ └─────────────────┘ └────────┬────────┘
│
▼
┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Grafana │◀────│ Traefik │◀────│ Airflow │◀────│ Spark │
│ Dashboards │ │ Proxy Inverso│ │ Orquestador │ │ Procesador │
└─────────────────┘ └──────────────┘ └─────────────────┘ └─────────────────┘
│
▼
┌─────────────────┐
│ Prometheus │
│ & cAdvisor │
│ (Monitoreo) │
└─────────────────┘

**Flujo de datos:**
1. **Simulador GPS** genera datos de camiones en movimiento
2. **MQTT Broker** recibe y distribuye los mensajes
3. **MQTT Ingestor** consume y persiste datos crudos en PostgreSQL
4. **Spark** procesa los datos calculando métricas (velocidad promedio, máxima, mínima)
5. **Airflow** orquesta todo el pipeline con reintentos automáticos
6. **Traefik** unifica el acceso a todos los servicios web
7. **Prometheus + Grafana** monitorean el estado del sistema

## 🚀 **Tecnologías Utilizadas**

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 24.0+ | Contenerización de servicios |
| **Apache Airflow** | 2.8.1 | Orquestación de pipelines |
| **Apache Spark** | 3.5.8 | Procesamiento de datos |
| **PostgreSQL + PostGIS** | 15-3.4 | Base de datos espacial |
| **MQTT (Mosquitto)** | Latest | Broker de mensajería ligera |
| **Apache Kafka** | 3.7.0 | Streaming de datos |
| **Traefik** | 3.6+ | Proxy inverso y balanceador de carga |
| **Prometheus** | 2.48.0 | Monitoreo y métricas |
| **Grafana** | 10.2.2 | Visualización de datos |
| **cAdvisor** | 0.47.0 | Monitoreo de contenedores |
| **Jaeger** | Latest | Tracing distribuido |

## 🌐 **Proxy Inverso con Traefik**

El sistema utiliza **Traefik** como puerta de entrada única para todos los servicios web, ofreciendo:

- **Dashboard** para monitoreo visual de rutas y servicios
- **Access Logs** con registro detallado de todas las peticiones
- **Métricas Prometheus** para exportación automática
- **Tracing** integrado con Jaeger
- **Descubrimiento automático** de nuevos servicios

### Servicios expuestos vía Traefik

| Servicio | URL de acceso (configurable) |
|----------|------------------------------|
| **Traefik Dashboard** | `traefik.localhost` |
| **Apache Airflow** | `airflow.localhost` |
| **Grafana** | `grafana.localhost` |
| **Prometheus** | `prometheus.localhost` |
| **cAdvisor** | `cadvisor.localhost` |

> **Nota:** Las URLs y credenciales se configuran mediante archivo `.env` local.


## 📁 **Estructura del Proyecto**
[![estructura.png](https://i.postimg.cc/cHjjHKdy/estructura.png)](https://postimg.cc/62rzbp7Y)

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

📊 Modelo de Datos
Tabla	Propósito
gps_data	Datos GPS crudos (latitud, longitud, velocidad, timestamp)
gps_metrics	Métricas procesadas por Spark (velocidad promedio, máxima, mínima)
gps_alerts	Alertas y eventos del sistema
gps_positions	Posiciones detalladas con heading y altitud

📈 Monitoreo y Observabilidad
El stack de monitoreo completo incluye:

Herramienta	Función
Prometheus	Recolección de métricas
Grafana	Visualización de dashboards
cAdvisor	Métricas de contenedores
Jaeger	Tracing distribuido
Traefik	Logs de acceso y métricas del proxy
Métricas recolectadas
Contenedores: CPU, memoria, red, disco

Servicios: Tiempo de respuesta, peticiones por segundo, errores

Base de datos: Conexiones activas, tiempo de consultas

Pipeline: Datos procesados, tiempo de ejecución, fallos

📚 Documentación Adicional
Apache Airflow Documentation

Apache Spark Documentation

PostgreSQL Documentation

Prometheus Documentation

Grafana Documentation

# PostgreSQL
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=monitoreo

# Airflow
AIRFLOW_SECRET_KEY=tu_clave_secreta

# Grafana
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=tu_password

🐛 Solución de Problemas Comunes
Problema	Posible solución
Traefik no sirve métricas	Verificar entryPoints en traefik/config/traefik.yml
Error de conexión a PostgreSQL	Verificar red Docker: docker network inspect monitoreo-red
Airflow no inicia	Ejecutar airflow db init y crear usuario admin
Grafana no conecta a PostgreSQL	Usar nombre del contenedor como host y SSL mode disable

📚 Documentación Adicional
Apache Airflow Documentation
Apache Spark Documentation
PostgreSQL Documentation
Prometheus Documentation
Grafana Documentation
Traefik Documentation

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
Para preguntas o sugerencias: diegofender777@hotmail.com

