# SiriusBot OCR Engine

Microservicio de procesamiento inteligente de imágenes para extracción de información mediante OCR, desarrollado como parte de la plataforma **SiriusBot**.

El servicio recibe imágenes de documentos como facturas, recibos y documentos administrativos, ejecuta validaciones de seguridad, validación de imagen, preprocesamiento, análisis de calidad y extracción de texto mediante OCR.

El resultado se entrega mediante una API REST desarrollada con FastAPI, utilizando respuestas JSON estandarizadas, manejo centralizado de errores, métricas, trazabilidad mediante Request ID y controles de seguridad orientados a producción.

---

## Estado del proyecto

**Estado:** En desarrollo activo 🚧

El proyecto cuenta actualmente con:

- API REST funcional con FastAPI
- Pipeline completo de procesamiento OCR
- Validaciones de seguridad de archivos e imágenes
- Validación de contenido de archivos
- Validación de dimensiones y cantidad de píxeles
- Límite de tamaño de archivos
- Protección durante la lectura de uploads
- Preprocesamiento de imágenes
- Análisis de calidad
- Protección contra tiempos de procesamiento OCR excesivos
- Rate limiting para el endpoint OCR
- Manejo estandarizado de errores
- Logging estructurado en formato JSON
- Request ID para trazabilidad
- Métricas internas
- Métricas compatibles con Prometheus
- Health checks
- Readiness checks
- API Docs controlada por ambiente
- Protección mediante Allowed Hosts
- Security headers
- Configuración orientada a producción
- Contenedor Docker ejecutándose como usuario no root
- GitHub Actions para integración continua
- Validación automática del build Docker
- Smoke test del contenedor de producción
- Tests unitarios e integración

### Calidad actual

```text
Tests:             143 passed
Cobertura:         88%
CI:                GitHub Actions
Containerization:  Docker
Production status: Validated
Branch principal:  main

La rama main contiene actualmente las funcionalidades de seguridad, observabilidad y hardening incorporadas durante las últimas fases de desarrollo.

## Características principales

### API y procesamiento

API REST desarrollada con FastAPI
Python 3.12
Procesamiento de imágenes con Pillow
Motor OCR basado en Tesseract
Pipeline configurable de procesamiento
Respuestas JSON estandarizadas
Serialización consistente mediante aliases camelCase
Manejo centralizado de excepciones
### Seguridad

- Validación del tipo de archivo
Validación del contenido real del archivo
Detección de extensiones inconsistentes
Restricción de tamaño de archivos
Protección durante la lectura de uploads
Validación de imágenes
Protección contra imágenes excesivamente grandes
Validación de dimensiones
Validación de cantidad de píxeles
Rate limiting
Protección contra OCR timeout
Allowed Hosts configurable por ambiente
Rechazo de configuración wildcard en producción
API Docs deshabilitada en producción
Endpoint de métricas deshabilitado en producción
Security headers
Ejecución del contenedor Docker como usuario no root
### Observabilidad

- Request ID
Logging estructurado JSON
Métricas internas
Métricas Prometheus
Health checks
Readiness checks
Telemetría
Registro de duración de peticiones
Registro de duración de procesamiento OCR
### Calidad

- Tests unitarios
Tests de integración
Tests de seguridad
Tests de configuración
Tests de middleware
Tests de rate limiting
Tests de observabilidad
Cobertura mediante pytest-cov
Validación de dependencias mediante pip check
### Infraestructura

- Docker
Docker Compose
GitHub Actions
Linux / WSL
Python virtual environments
## Arquitectura del servicio

                         Cliente
                            |
                            | HTTP Request
                            v
                  +---------------------+
                  |       FastAPI       |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |    Allowed Hosts    |
                  | Environment Policy  |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Observability       |
                  | Middleware          |
                  |                     |
                  | Request ID          |
                  | Structured Logging  |
                  | Request Metrics     |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |   Rate Limiting     |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |  Request Security   |
                  |                     |
                  | Content-Type        |
                  | Request Size        |
                  | Upload Read Limit   |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |   File Security     |
                  |                     |
                  | File Type           |
                  | File Content        |
                  | Extension           |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |  Image Validation   |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |   Image Security    |
                  |                     |
                  | Dimensions          |
                  | Pixel Count         |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |    Preprocessor     |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |   Quality Analysis  |
                  |                     |
                  | Brightness          |
                  | Contrast            |
                  | Dimensions          |
                  | Warnings            |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |     OCR Engine      |
                  |                     |
                  | Tesseract           |
                  | Timeout Protection  |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  |  Response Builder   |
                  +---------------------+
                            |
                            v
                     JSON Response
## Tecnologías utilizadas

### Backend

Python 3.12
FastAPI
Uvicorn
Pydantic
### Procesamiento de imágenes

- Pillow
Tesseract OCR
### Observabilidad

- Python logging
python-json-logger
Prometheus
### Testing

- Pytest
pytest-cov
FastAPI TestClient
AnyIO
### Calidad y desarrollo

- Git
GitHub
GitHub Actions
### Infraestructura

- Docker
Docker Compose
Linux / WSL
## Estructura del proyecto

```text
ocr-engine/
│
├── app.py
├── config.py
├── logger.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements.lock.txt
├── pytest.ini
├── .dockerignore
├── .env.example
│
├── api/
│   └── v1/
│       ├── health.py
│       ├── metrics.py
│       └── ocr.py
│
├── models/
│   ├── request_models.py
│   ├── response_builder.py
│   └── response_models.py
│
├── services/
│   ├── ocr.py
│   ├── ocr_pipeline.py
│   ├── file_security.py
│   ├── image_security.py
│   ├── validator.py
│   ├── preprocessor.py
│   ├── quality.py
│   ├── response_builder.py
│   └── test_response_builder.py
│
├── utils/
│   ├── constants.py
│   ├── exceptions.py
│   ├── error_handlers.py
│   ├── health.py
│   ├── middleware.py
│   ├── telemetry.py
│   ├── metrics.py
│   ├── prometheus_metrics.py
│   ├── logger.py
│   ├── rate_limiter.py
│   ├── request_context.py
│   └── request_security.py
│
├── tests/
│   ├── test_api_docs_config.py
│   ├── test_app.py
│   ├── test_config.py
│   ├── test_error_handlers.py
│   ├── test_exceptions.py
│   ├── test_file_security.py
│   ├── test_file_security_endpoint.py
│   ├── test_health.py
│   ├── test_health_checks.py
│   ├── test_image_security.py
│   ├── test_image_security_endpoint.py
│   ├── test_logger.py
│   ├── test_metrics.py
│   ├── test_metrics_config.py
│   ├── test_metrics_endpoint_security.py
│   ├── test_middleware.py
│   ├── test_ocr.py
│   ├── test_ocr_timeout.py
│   ├── test_preprocessor.py
│   ├── test_prometheus_metrics.py
│   ├── test_quality.py
│   ├── test_rate_limit_middleware.py
│   ├── test_rate_limiter.py
│   ├── test_request_context.py
│   ├── test_request_security.py
│   ├── test_response_builder.py
│   ├── test_telemetry.py
│   └── test_validator.py
│
└── .github/
    └── workflows/
        └── ci.yml
## Instalación local
### Clonar repositorio

git clone https://github.com/jhologic12/siriusbot-ocr-engine.git

cd siriusbot-ocr-engine
### Crear entorno virtual

Linux / WSL
python3 -m venv .venv

Activar:

source .venv/bin/activate
Windows
python -m venv .venv

Activar:

.venv\Scripts\activate
Instalar dependencias
python -m pip install -r requirements.txt

Para utilizar las versiones bloqueadas:

python -m pip install -r requirements.lock.txt

Validar dependencias:

python -m pip check
## Configuración

La configuración se controla mediante variables de entorno.

Ejemplo:

cp .env.example .env

Variables principales:

APP_ENV
SERVICE_NAME
LOG_LEVEL
OCR_TIMEOUT_SECONDS
MAX_FILE_SIZE_MB
RATE_LIMIT_REQUESTS
RATE_LIMIT_WINDOW_SECONDS
ALLOWED_HOSTS
### Ambientes

El servicio contempla diferentes comportamientos según APP_ENV:

development
test
production
### Production

En producción:

ALLOWED_HOSTS debe estar explícitamente configurado.
No se permite utilizar * como wildcard.
La documentación interactiva de FastAPI se encuentra deshabilitada.
OpenAPI se encuentra deshabilitado.
Las métricas internas HTTP se encuentran protegidas/deshabilitadas según la política de producción.
Se aplican controles de seguridad adicionales.

Ejemplo:

APP_ENV=production
ALLOWED_HOSTS=localhost

En un despliegue real, ALLOWED_HOSTS debe contener únicamente los hosts válidos utilizados por la infraestructura.

Ejemplo:

ALLOWED_HOSTS=ocr.example.com,api.example.com
## Ejecutar aplicación

Iniciar el servidor:

uvicorn app:app --host 0.0.0.0 --port 8000

Servicio disponible en:

http://localhost:8000
## Docker

### Construir imagen

docker build -t siriusbot-ocr:production .
### Ejecutar contenedor

Ejemplo:

docker run -d \
  --name siriusbot-ocr-prod \
  --env APP_ENV=production \
  --env ALLOWED_HOSTS=localhost \
  --publish 8000:8000 \
  siriusbot-ocr:production

El contenedor:

utiliza Python 3.12
incluye Tesseract OCR
incluye soporte para español
ejecuta la aplicación como usuario no root
expone el puerto 8000
incorpora Docker Healthcheck
### Healthcheck del contenedor


Docker verifica:

GET /api/v1/health

El estado puede consultarse mediante:

docker ps
## API

La API utiliza el prefijo:

/api/v1
### Health Check

`GET /api/v1/health`

Ejemplo:

curl http://localhost:8000/api/v1/health

Respuesta:

{
    "status": "healthy",
    "service": "siriusbot-ocr-engine"
}

Este endpoint permite verificar que el servicio está disponible.

### Readiness

`GET /api/v1/ready`

Ejemplo:

curl http://localhost:8000/api/v1/ready

Respuesta:

{
    "status": "ready"
}

El readiness check valida las dependencias necesarias para que el servicio pueda procesar solicitudes.

### Métricas

`GET /api/v1/metrics`

El endpoint permite consultar métricas operativas del servicio cuando se encuentra habilitado para el ambiente actual.

Entre las métricas disponibles se encuentran:

Peticiones recibidas
Peticiones exitosas
Peticiones fallidas
Procesamientos OCR exitosos
Procesamientos OCR fallidos
Tiempo total de peticiones
Tiempo total de procesamiento
Tiempo promedio de procesamiento
Uptime del servicio
Métricas personalizadas de errores

En producción, el endpoint de métricas HTTP se encuentra deshabilitado como parte de la política de hardening.

## Procesamiento OCR

### Endpoint

`POST /api/v1/ocr`

El endpoint recibe una imagen mediante:

multipart/form-data

Ejemplo:

curl -X POST \
  -F "file=@factura.jpg" \
  http://localhost:8000/api/v1/ocr

El procesamiento ejecuta las siguientes etapas:

Upload
  ↓
Request Validation
  ↓
File Security
  ↓
Image Validation
  ↓
Image Security
  ↓
Preprocessing
  ↓
Quality Analysis
  ↓
OCR
  ↓
Response Builder
### Respuesta OCR

Ejemplo de respuesta exitosa:

{
    "success": true,
    "validation": {
        "valid": true,
        "errors": [],
        "warnings": [],
        "metadata": {
            "format": "JPEG",
            "mode": "RGB",
            "width": 1000,
            "height": 1000,
            "pixels": 1000000,
            "sizeBytes": 16503
        }
    },
    "quality": {
        "status": "GOOD",
        "canProcess": true,
        "width": 1200,
        "height": 1200,
        "pixels": 1440000,
        "brightness": 128.5,
        "contrast": 45.2,
        "warnings": []
    },
    "processing": {
        "processed": true,
        "originalSize": 16503,
        "newSize": 8721,
        "width": 1200,
        "height": 1200
    },
    "ocr": {
        "text": "Factura número 12345",
        "confidence": 0.94
    },
    "message": "Proceso completado",
    "error": null
}

Los valores de la respuesta dependen de la imagen procesada.

## Validaciones y seguridad


El Engine incorpora diferentes capas de seguridad antes y durante la ejecución del procesamiento OCR.

### Seguridad del request

Validación del tipo de contenido
Restricción del tamaño máximo del request
Validación durante la lectura del upload
Protección contra uploads excesivamente grandes
### Seguridad del archivo

Validación del tipo de archivo
Validación del contenido real
Detección de extensión inconsistente
Restricción de tamaño
Validación del nombre del archivo
### Seguridad de imagen

Validación de imagen válida
Detección de imágenes corruptas
Validación de dimensiones
Validación de cantidad de píxeles
Protección contra imágenes excesivamente grandes
### Rate limiting

El endpoint OCR cuenta con protección contra exceso de solicitudes.

La configuración se controla mediante:

RATE_LIMIT_REQUESTS
RATE_LIMIT_WINDOW_SECONDS

Cuando un cliente supera el límite configurado, el servicio responde con un error HTTP de rate limiting e incluye información para determinar cuándo puede realizarse una nueva solicitud.

Los endpoints de health no se encuentran sujetos al mismo límite utilizado para OCR.

### Allowed Hosts

El servicio utiliza una política de hosts permitidos.

En producción:

ALLOWED_HOSTS es obligatorio.
No se permite utilizar *.
Las solicitudes con un host no autorizado son rechazadas.

Ejemplo:

curl \
  -H "Host: malicious.example.com" \
  http://localhost:8000/api/v1/health

Resultado esperado:

HTTP 400 Bad Request
Invalid host header
### Security Headers

Las respuestas incluyen headers de seguridad como:

X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
### Protección contra OCR Timeout

El procesamiento OCR incorpora protección contra tiempos de ejecución excesivos.

La configuración se controla mediante:

OCR_TIMEOUT_SECONDS

Cuando el procesamiento supera el tiempo permitido, el servicio evita mantener indefinidamente la operación y genera un error controlado.

Código asociado:

OCR_TIMEOUT
### Calidad de imagen

Antes de ejecutar OCR, el servicio analiza características de la imagen como:

Brillo
Contraste
Dimensiones
Cantidad de píxeles
Calidad general
Advertencias

Cuando la imagen no cumple las condiciones necesarias, el pipeline puede rechazar el procesamiento.

## Manejo de errores

El servicio utiliza excepciones y respuestas estandarizadas.

Ejemplo:

{
    "success": false,
    "error": {
        "code": "INVALID_IMAGE",
        "message": "Imagen inválida"
    }
}

Algunos códigos utilizados:

INVALID_IMAGE
FILE_SECURITY_ERROR
IMAGE_SECURITY_ERROR
LOW_IMAGE_QUALITY
OCR_PROCESSING_ERROR
OCR_TIMEOUT
OCR_EXCEPTION

Los errores controlados son transformados por handlers globales en respuestas HTTP consistentes.

## Observabilidad

El Engine incorpora una capa de observabilidad orientada a trazabilidad, métricas operativas y monitoreo de salud.

### Request ID

Cada petición recibe un identificador único:

X-Request-ID

Ejemplo:

X-Request-ID: 05d4f0b2-cc53-4b10-b0cb-7379c4f29826

Esto permite relacionar una petición HTTP con los logs generados durante su procesamiento.

### Logging estructurado

Los eventos de aplicación se registran utilizando formato JSON.

Eventos principales:

request_started
request_completed
request_failed

Incluyendo información como:

Request ID
Método HTTP
Ruta
Código de respuesta
Duración de la petición

Ejemplo conceptual:

{
    "levelname": "INFO",
    "name": "utils.middleware",
    "message": "request_completed",
    "request_id": "05d4f0b2-cc53-4b10-b0cb-7379c4f29826",
    "method": "GET",
    "path": "/api/v1/health",
    "status_code": 200,
    "duration_ms": 0.72
}
### Métricas

El Engine mantiene métricas internas para observar el comportamiento del servicio.

Métricas principales:

requests_total
requests_success
requests_failed

ocr_success
ocr_failed

total_request_time
total_processing_time

uptime_seconds
average_processing_time

También permite registrar métricas personalizadas relacionadas con errores y procesamiento.

### Prometheus

El servicio incorpora métricas compatibles con Prometheus.

Las métricas permiten observar información como:

Total de requests
Requests por método
Requests por endpoint
Código HTTP
Duración de requests
Procesamiento OCR
Métricas operativas de la aplicación

El endpoint de métricas se encuentra sujeto a la política de seguridad del ambiente.

En desarrollo y test puede utilizarse:

GET /api/v1/metrics

En producción se encuentra deshabilitado como parte del hardening de la superficie API.

### Health y Readiness

El servicio diferencia entre:

Health

Indica si la aplicación está disponible:

GET /api/v1/health
Readiness

Indica si el servicio está preparado para procesar solicitudes:

GET /api/v1/ready

El readiness check puede validar dependencias relacionadas con el motor OCR y su configuración.

Esto permite diferenciar entre:

Application is running

y:

Application is ready to process OCR
API Documentation

FastAPI proporciona documentación interactiva mediante:

/docs
/redoc
/openapi.json

Estas funcionalidades están disponibles durante los ambientes de desarrollo y test.

En producción se encuentran deshabilitadas para reducir la superficie de exposición de la API.

La configuración está controlada por APP_ENV.

Testing

El proyecto utiliza Pytest para validar el comportamiento del servicio.

Actualmente se cuenta con:

143 tests passed
96% coverage

Los tests cubren diferentes áreas del sistema.

Categorías de pruebas
API
Health
Readiness
OCR
Metrics
Request ID
Security headers
Configuración
Ambientes
Logging
OCR timeout
Upload size
Rate limiting
Allowed Hosts
Políticas de producción
Seguridad
File security
Image security
Request security
Upload size
Rate limiting
Allowed Hosts
OCR
Extracción de texto
Validación
Timeout
Pipeline
Calidad
Observabilidad
Middleware
Logging
Request ID
Métricas
Prometheus
Telemetría
Ejecutar tests

Ejecutar toda la suite:

python -m pytest -v

Ejecutar con cobertura:

python -m pytest -v --cov=. --cov-report=term-missing

Ejecutar un archivo específico:

python -m pytest tests/test_config.py -v
Integración continua

El proyecto utiliza GitHub Actions para validar automáticamente los cambios.

El workflow se encuentra en:

.github/workflows/ci.yml

El pipeline ejecuta dos etapas principales.

Tests

El job de testing:

Configura Python 3.12
Instala dependencias del sistema
Instala dependencias bloqueadas
Ejecuta pip check
Ejecuta Pytest
Genera reporte de cobertura
Docker Build

Después de superar los tests:

Construye la imagen Docker
Inicia un contenedor configurado como producción
Configura APP_ENV=production
Configura ALLOWED_HOSTS
Ejecuta un smoke test
Valida /api/v1/health
Valida /api/v1/ready
Valida la superficie de API de producción
Verifica que /docs, /redoc, /openapi.json y /api/v1/metrics no estén expuestos en producción
Limpia el contenedor utilizado para la validación

Flujo:

Push / Pull Request
        |
        v
   Run Tests
        |
        v
   Coverage
        |
        v
    pip check
        |
        v
   Docker Build
        |
        v
Production Smoke Test
        |
        v
Health / Readiness
        |
        v
Production API Surface
        |
        v
      Success
Docker Security

La imagen Docker incorpora diferentes medidas de hardening.

Usuario no root

El servicio no se ejecuta como root.

El Dockerfile crea:

ocruser

y ejecuta la aplicación utilizando dicho usuario.

Dependencias

La imagen instala únicamente las dependencias necesarias para ejecutar:

Python
Tesseract OCR
Tesseract Spanish
Pillow y dependencias relacionadas
librerías necesarias para el servicio
curl para healthcheck
Healthcheck

El contenedor incorpora un healthcheck:

GET /api/v1/health
Versionamiento y flujo de trabajo

El desarrollo utiliza Git y ramas orientadas a funcionalidades, seguridad, documentación y mantenimiento.

Ejemplos:

feature/*
security/*
chore/*
docs/*

El flujo recomendado es:

Create branch
      |
      v
Implement change
      |
      v
Run tests
      |
      v
Validate Docker
      |
      v
Commit
      |
      v
Push branch
      |
      v
Pull Request
      |
      v
CI validation
      |
      v
Merge to main
      |
      v
Delete branch

La rama principal es:

main
Estado de seguridad actual

El proyecto ha incorporado progresivamente controles de hardening orientados a un escenario de producción.

Actualmente incluye:

✓ File validation
✓ Image validation
✓ Image size / pixel protection
✓ Request size protection
✓ Upload read limit
✓ OCR timeout protection
✓ Rate limiting
✓ Security headers
✓ Allowed Hosts
✓ Production configuration validation
✓ API documentation disabled in production
✓ Metrics endpoint disabled in production
✓ Docker non-root execution
✓ Health checks
✓ Readiness checks
✓ Structured logging
✓ Request ID
✓ Prometheus metrics
✓ Automated CI validation
✓ Docker smoke test

Estos controles buscan reducir la superficie de ataque, mejorar la resiliencia del servicio y facilitar su operación.

Roadmap

El proyecto continúa evolucionando como parte de la plataforma SiriusBot.

Áreas de evolución:

Mejoras adicionales de seguridad
Observabilidad avanzada
Integración con infraestructura de monitoreo
Optimización del pipeline OCR
Mejoras en extracción y estructuración de información
Integración con SiriusBot
Automatización de despliegues
Pruebas adicionales de integración
Mejoras de rendimiento
Evolución hacia un entorno de producción completo
Relación con SiriusBot

El OCR Engine forma parte de la arquitectura de SiriusBot.

Responsabilidad principal:

SiriusBot
    |
    v
Conversational / Automation Layer
    |
    v
OCR Engine
    |
    v
Image Validation
    |
    v
OCR Processing
    |
    v
Structured JSON Response

El objetivo es desacoplar el procesamiento OCR del resto de la plataforma, permitiendo que SiriusBot consuma el servicio mediante una API REST.

Licencia

Proyecto en desarrollo.

La información relacionada con la licencia será definida antes de una distribución pública formal del servicio.
